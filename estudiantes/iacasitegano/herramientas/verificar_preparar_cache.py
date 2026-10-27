"""Prueba el margen de `preparar()` con arranques Docker concurrentes en frío.

Desde la raíz del repo:
    nice -n 19 python3 -B estudiantes/iacasitegano/herramientas/verificar_preparar_cache.py

Cada contenedor usa torneo-bot-base:local, 1024 MiB, una cuota CPU configurable y la
ruta de equipo `/bot` con que se generó el caché Numba. El directorio compartido del
motor se enmascara para que la medición pruebe el caché del equipo y nada más.
"""

from __future__ import annotations

import argparse
import json
import math
import shlex
import statistics
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EQUIPO = ROOT / "estudiantes" / "iacasitegano"
IMAGEN = "torneo-bot-base:local"
PROBE_CODE = """\
import json, sys, time
from pathlib import Path
sys.path.insert(0, "/workspace/sistema")
from arbitro import runner
runner.calentar_motor()
inicio = time.perf_counter()
equipo = Path("/bot")
estrategia = runner.cargar_estrategia(equipo)
fin_import = time.perf_counter()
estrategia.preparar(runner.Config("blancas", 8675309, equipo / "data", 30.0))
fin = time.perf_counter()
print(json.dumps({"ok": True, "import_s": fin_import-inicio,
                  "preparar_s": fin-fin_import, "total_s": fin-inicio}))
"""


def percentil95(valores: list[float]) -> float:
    ordenados = sorted(valores)
    return ordenados[max(0, math.ceil(0.95 * len(ordenados)) - 1)]


def medir(cpu: float, indice: int, cache_motor_vacia: Path) -> dict:
    comando = [
        "docker", "run", "--rm", f"--cpus={cpu:g}", "--memory=1024m",
        "--memory-swap=1024m", "--network=none",
        "--tmpfs", "/tmp/numba:size=64m,noexec,mode=1777",
        "-v", f"{ROOT}:/workspace:ro",
        "-v", f"{EQUIPO}:/bot:ro",
        "-v", f"{cache_motor_vacia}:/opt/numba_listo:ro",
        "-w", "/workspace",
        "-e", "NUMBA_CACHE_DIR=/tmp/numba",
        "-e", "PYTHONPATH=/workspace/sistema",
        "--entrypoint", "/bin/bash", IMAGEN, "-lc",
        "nice -n 19 python3 -B -c " + shlex.quote(PROBE_CODE),
    ]
    proc = subprocess.run(comando, capture_output=True, text=True, check=False)
    registro = {"cpu": cpu, "repeticion": indice, "exit": proc.returncode}
    try:
        medicion = json.loads(proc.stdout.strip().splitlines()[-1])
        registro["medicion"] = medicion
    except (IndexError, json.JSONDecodeError):
        registro["medicion"] = {"ok": False, "error": proc.stderr[-2000:] or proc.stdout[-2000:]}
    return registro


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeticiones", type=int, default=20)
    parser.add_argument("--workers", type=int, default=7)
    parser.add_argument("--cpu", type=float, default=0.5)
    parser.add_argument("--limite", type=float, default=10.0)
    args = parser.parse_args()
    if args.repeticiones < 1 or args.workers < 1 or args.cpu <= 0:
        parser.error("repeticiones, workers y cpu deben ser positivos")

    with tempfile.TemporaryDirectory(prefix="iacasitegano-cache-test-") as temporal:
        cache_vacia = Path(temporal) / "cache-motor-vacia"
        cache_vacia.mkdir()
        registros = []
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            tareas = [pool.submit(medir, args.cpu, i, cache_vacia)
                      for i in range(1, args.repeticiones + 1)]
            for tarea in as_completed(tareas):
                registro = tarea.result()
                registros.append(registro)
                print(json.dumps(registro, ensure_ascii=False), flush=True)

    correctas = [r["medicion"] for r in registros
                 if r["exit"] == 0 and r["medicion"].get("ok")]
    totales = [m["total_s"] for m in correctas]
    resumen = {
        "cpu": args.cpu,
        "workers": args.workers,
        "repeticiones": args.repeticiones,
        "ok": len(correctas),
        "fallos": args.repeticiones - len(correctas),
        "total_p50_s": statistics.median(totales) if totales else None,
        "total_p95_s": percentil95(totales) if totales else None,
        "total_max_s": max(totales) if totales else None,
        "limite_s": args.limite,
    }
    print(json.dumps(resumen, ensure_ascii=False), flush=True)
    return 0 if len(correctas) == args.repeticiones and max(totales) < args.limite else 1


if __name__ == "__main__":
    raise SystemExit(main())
