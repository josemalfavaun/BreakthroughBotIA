"""Corre varias tandas de torneo en paralelo y agrega un reporte Markdown.

Cada trabajo lanza `./torneo jugar <equipo> <rival> --sin-docker` en la
imagen local de la CLI, con cuota de 1 CPU. Los bots se ejecutan como
procesos locales dentro de esa invocación. Cada semilla escribe resultados
en una carpeta propia.
"""

from __future__ import annotations

import argparse
import json
import math
import shlex
import subprocess
import sys
import time
from statistics import fmean
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
IMAGE = "torneo-base:local"
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS")
Z95 = 1.959963984540054


def docker_cpus() -> int:
    p = subprocess.run(
        ["docker", "info", "--format", "{{.NCPU}}"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return int(p.stdout.strip())


def wilson(wins: int, total: int) -> tuple[float, float]:
    if total == 0:
        return 0.0, 0.0
    z2 = Z95 * Z95
    p = wins / total
    den = 1 + z2 / total
    center = (p + z2 / (2 * total)) / den
    radius = Z95 * math.sqrt(p * (1 - p) / total + z2 / (4 * total**2)) / den
    return max(0.0, center - radius), min(1.0, center + radius)


def construir_trabajos(total: int, por_trabajo: int, seed0: int, output: Path) -> list[dict]:
    jobs = []
    left = total
    seed = seed0
    while left:
        n = min(left, por_trabajo)
        dest = output / "resultados" / f"semilla_{seed}"
        dest.mkdir(parents=True, exist_ok=False)
        jobs.append({"seed": seed, "games": n, "dest": dest})
        seed += 1
        left -= n
    return jobs


def ejecutar(job: dict, bot: str, rival: str, output: Path) -> dict:
    dest_rel = job["dest"].relative_to(output).as_posix()
    command = [
        "./torneo", "jugar", bot, rival, "--sin-docker",
        "--partidas", str(job["games"]), "--semilla", str(job["seed"]),
    ]
    docker = [
        "docker", "run", "--rm", "--cpus=1", "--memory=1024m", "--network=none",
        "--tmpfs", "/tmp/numba:size=256m",
        "-v", f"{ROOT}:/workspace", "-w", "/workspace",
        "-v", f"{output}:/medicion",
        "-e", f"TORNEO_RESULTADOS=/medicion/{dest_rel}",
        "-e", "NUMBA_CACHE_DIR=/tmp/numba",
    ]
    for name in THREAD_VARS:
        docker += ["-e", f"{name}=1"]
    docker += ["--entrypoint", "/bin/bash", IMAGE, "-lc", shlex.join(command)]
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(docker, cwd=ROOT, capture_output=True, text=True, check=False)
        elapsed = time.perf_counter() - t0
        (job["dest"] / "salida.log").write_text(proc.stdout + proc.stderr)
        records = [
            json.loads(p.read_text())
            for p in sorted(job["dest"].rglob("*.json"))
            if p.name != "manifest.json"
        ]
        err = None if proc.returncode == 0 else proc.stderr[-3000:]
        return {"seed": job["seed"], "expected": job["games"], "records": records,
                "seconds": elapsed, "exit": proc.returncode, "error": err}
    except Exception as exc:
        return {"seed": job["seed"], "expected": job["games"], "records": [],
                "seconds": time.perf_counter() - t0, "exit": -1,
                "error": f"{type(exc).__name__}: {exc}"}


def agregar(jobs: list[dict], bot: str) -> dict:
    colors = {
        c: {"wins": 0, "losses": 0, "points": 0, "clock_max": 0.0}
        for c in ("blancas", "negras")
    }
    out = {"games": 0, "wins": 0, "losses": 0, "points": 0, "clock_max": 0.0,
           "clocks": [], "depths": [],
           "colors": colors, "timeouts": 0, "bot_timeouts": 0,
           "finish_reasons": {}, "incident_reasons": {}, "illegal_moves": 0,
           "exceptions": 0, "events": [], "bot_output_count": 0,
           "execution_errors": []}
    for job in jobs:
        if job["error"]:
            out["execution_errors"].append({"seed": job["seed"], "error": job["error"]})
        if len(job["records"]) != job["expected"]:
            out["execution_errors"].append({
                "seed": job["seed"],
                "error": f"faltan/sobran JSON: {len(job['records'])}/{job['expected']}",
            })
        for rec in job["records"]:
            out["games"] += 1
            bot_color = next(c for c in ("blancas", "negras") if rec["meta"][c] == bot)
            color = "blancas" if bot_color == "blancas" else "negras"
            win = rec["meta"][rec["ganador"]] == bot
            outcome = "wins" if win else "losses"
            out[outcome] += 1
            colors[color][outcome] += 1
            score = int(rec["puntos"][color])
            out["points"] += score
            colors[color]["points"] += score
            used = float(rec.get("reloj_usado", {}).get(bot_color, 0.0))
            out["clocks"].append(used)
            out["clock_max"] = max(out["clock_max"], used)
            colors[color]["clock_max"] = max(colors[color]["clock_max"], used)
            reason = rec.get("motivo", "desconocido")
            out["finish_reasons"][reason] = out["finish_reasons"].get(reason, 0) + 1
            if reason not in ("puntos", "sin_jugadas"):
                out["incident_reasons"][reason] = out["incident_reasons"].get(reason, 0) + 1
            if reason == "reloj":
                out["timeouts"] += 1
                if not win:
                    out["bot_timeouts"] += 1
            if "ilegal" in reason.lower():
                out["illegal_moves"] += 1
            if "excep" in reason.lower():
                out["exceptions"] += 1
            if reason == "reloj" or "ilegal" in reason.lower() or "excep" in reason.lower():
                out["events"].append({
                    "seed": rec.get("meta", {}).get("semilla_maestra"),
                    "game": rec.get("meta", {}).get("juego"),
                    "reason": reason,
                    "bot_color": bot_color,
                    "bot_won": win,
                })
            if rec.get("salidas", {}).get(bot):
                out["bot_output_count"] += 1
            out["depths"].extend(
                float(j["info"]["prof"])
                for j in rec.get("jugadas", [])
                if j.get("color") == bot_color and isinstance(j.get("info"), dict)
                and j["info"].get("prof") is not None
            )
    out["win_rate"] = out["wins"] / out["games"] if out["games"] else 0.0
    out["wilson95"] = wilson(out["wins"], out["games"])
    for c in colors.values():
        c["games"] = c["wins"] + c["losses"]
        c["win_rate"] = c["wins"] / c["games"] if c["games"] else 0.0
        c["wilson95"] = wilson(c["wins"], c["games"])
    sorted_clocks = sorted(out["clocks"])
    out["clock_mean"] = fmean(sorted_clocks) if sorted_clocks else 0.0
    out["clock_p95"] = sorted_clocks[math.ceil(0.95 * len(sorted_clocks)) - 1] if sorted_clocks else 0.0
    out["depth_mean"] = fmean(out["depths"]) if out["depths"] else 0.0
    return out


def markdown(name: str, bot: str, rival: str, workers: int, cpus: int, started: str,
             elapsed: float, jobs: list[dict], stats: dict) -> str:
    lines = [
        f"# {name}", "", f"- Inicio: {started}",
        f"- Entorno: `{IMAGE}` ejecutando `./torneo jugar {bot} {rival} --sin-docker`.",
        f"- Workers: {workers}; CPU Docker: {cpus}; cuota: 1 CPU por worker; memoria limitada a 1024 MiB por contenedor.",
        f"- Semillas: {', '.join(str(j['seed']) for j in jobs)}",
        f"- Partidas: {stats['games']}; duración total: {elapsed:.1f} s.", "",
        "## Resultado agregado", "",
        f"- Victorias–derrotas: **{stats['wins']}–{stats['losses']}**.",
        f"- Tasa de victorias: **{100*stats['win_rate']:.1f}%**; Wilson 95%: **{100*stats['wilson95'][0]:.1f}%–{100*stats['wilson95'][1]:.1f}%**.",
        f"- Puntos anotados: **{stats['points']}**.",
        f"- Reloj máximo: **{stats['clock_max']:.3f} s**.",
        f"- Reloj usado por partida ({bot}): media **{stats['clock_mean']:.3f} s**, p95 **{stats['clock_p95']:.3f} s**, máximo **{stats['clock_max']:.3f} s**.",
        f"- Profundidad media ({bot}, sobre jugadas con `info.prof`): **{stats['depth_mean']:.3f}**; mediciones: {len(stats['depths'])}.",
        f"- Finales por motivo: `{json.dumps(stats['finish_reasons'], ensure_ascii=False, sort_keys=True)}`.",
        f"- Timeouts totales: **{stats['timeouts']}**; del bot: **{stats['bot_timeouts']}**; jugadas ilegales: **{stats['illegal_moves']}**; excepciones: **{stats['exceptions']}**.",
        f"- Salidas no vacías del bot: {stats['bot_output_count']}; errores de ejecución/lectura: {len(stats['execution_errors'])}.",
        "- Memoria máxima observada: no instrumentada; el límite cgroup de 1024 MiB evita excederlo y un OOM produce fallo/exit no cero.", "",
        f"| Color de {bot} | Victorias–derrotas | Tasa | Wilson 95% | Puntos | Reloj máximo |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for color in ("blancas", "negras"):
        c = stats["colors"][color]
        lines.append(f"| {color} | {c['wins']}–{c['losses']} | {100*c['win_rate']:.1f}% | {100*c['wilson95'][0]:.1f}%–{100*c['wilson95'][1]:.1f}% | {c['points']} | {c['clock_max']:.3f} s |")
    if stats["events"]:
        lines += ["", "## Timeouts, ilegales y excepciones", "", "| Semilla | Juego | Motivo | Color del bot | Ganó el bot |", "|---:|---:|---|---|---:|"]
        lines += [f"| {e['seed']} | {e['game']} | {e['reason']} | {e['bot_color']} | {e['bot_won']} |" for e in stats["events"]]
    lines += ["", "## Invocaciones", "", "| Semilla | Partidas | Duración | Exit |", "|---:|---:|---:|---:|"]
    for j in jobs:
        lines.append(f"| {j['seed']} | {len(j['records'])}/{j['expected']} | {j['seconds']:.1f} s | {j['exit']} |")
    if stats["execution_errors"]:
        lines += ["", "## Errores de ejecución", ""]
        lines += [f"- Semilla {e['seed']}: {e['error']}" for e in stats["execution_errors"]]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--partidas", type=int, required=True, help="total par de partidas")
    ap.add_argument("--por-trabajo", type=int, default=20, help="partidas pares por proceso")
    ap.add_argument("--semilla-inicio", type=int, required=True)
    ap.add_argument("--workers", type=int, default=None, help="máximo CPU Docker menos un núcleo")
    ap.add_argument("--nombre", default="tanda")
    ap.add_argument("--equipo", default="iacasitegano", help="equipo en estudiantes/ (default: iacasitegano)")
    ap.add_argument("--rival", default="montecarlo", help="rival en estudiantes/ (default: montecarlo)")
    ap.add_argument("--salida", type=Path, default=None, help="directorio único bajo el repo")
    args = ap.parse_args()
    if args.partidas <= 0 or args.partidas % 2:
        ap.error("--partidas debe ser positivo y par")
    if args.por_trabajo <= 0 or args.por_trabajo % 2:
        ap.error("--por-trabajo debe ser positivo y par")

    cpus = docker_cpus()
    max_workers = max(1, cpus - 1)
    workers = args.workers if args.workers is not None else max_workers
    if not 1 <= workers <= max_workers:
        ap.error(f"--workers debe estar entre 1 y {max_workers}; Docker informa {cpus} CPU")
    started_dt = datetime.now().astimezone()
    started = started_dt.isoformat(timespec="seconds")
    suffix = started_dt.strftime("%Y%m%d_%H%M%S")
    output = args.salida or ROOT / "resultados" / "medicion" / f"{args.nombre}_{suffix}"
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    jobs = construir_trabajos(args.partidas, args.por_trabajo, args.semilla_inicio, output)

    t0 = time.perf_counter()
    done = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(ejecutar, job, args.equipo, args.rival, output): job for job in jobs}
        for future in as_completed(futures):
            item = future.result()
            done.append(item)
            print(f"semilla {item['seed']}: {len(item['records'])}/{item['expected']}, "
                  f"{item['seconds']:.1f}s, exit {item['exit']}", flush=True)
    elapsed = time.perf_counter() - t0
    done.sort(key=lambda x: x["seed"])
    stats = agregar(done, args.equipo)
    (output / "reporte.md").write_text(markdown(
        args.nombre, args.equipo, args.rival, workers, cpus, started, elapsed, done, stats
    ))
    print(f"\nReporte: {output / 'reporte.md'}")
    print(f"Total: {stats['wins']}–{stats['losses']}; Wilson95 "
          f"{stats['wilson95'][0]:.3f}–{stats['wilson95'][1]:.3f}; "
          f"reloj máximo {stats['clock_max']:.3f}s; {elapsed:.1f}s", flush=True)
    return 1 if stats["execution_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
