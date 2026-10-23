"""Lanza Fase 2 solo después de regenerar el libro del campeón restaurado."""

from __future__ import annotations

import re
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

import numpy as np


BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
LIBRO_LOG = BASE / "libro_regenerado_campeon_antes.log"
SUPERVISOR_LOG = BASE / "fase2_limpia_supervisor.log"
LIGA_LOG = BASE / "fase2_liga_limpia_campeon.log"
INFORME = BASE / "INFORME.md"
PESOS = BASE / "data/pesos.npy"
CAMPEON = BASE / "data/pesos_antes_selfplay_300.npy"
RTK = shutil.which("rtk") or "rtk"


def registrar(mensaje: str) -> None:
    with SUPERVISOR_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {mensaje}\n")


def esperar_libro() -> None:
    while True:
        texto = LIBRO_LOG.read_text(encoding="utf-8") if LIBRO_LOG.exists() else ""
        if "  300/300 partidas" in texto and "Guardado en" in texto:
            registrar("libro confirmado en 300/300 y Guardado en libro.json")
            return
        registrar("libro aún no termina; no se lanza Fase 2")
        time.sleep(300)


def main() -> None:
    esperar_libro()
    if not np.array_equal(np.load(PESOS), np.load(CAMPEON)):
        raise RuntimeError("pesos.npy ya no coincide con pesos_antes_selfplay_300.npy")
    registrar("campeón restaurado verificado; lanzando Fase 2 limpia")
    comando = [
        RTK,
        "./torneo",
        "jugar",
        "iacasitegano",
        "montecarlo",
        "--partidas",
        "40",
        "--semilla",
        "2030",
        "--sin-docker",
        "-v",
    ]
    with LIGA_LOG.open("w", encoding="utf-8") as salida:
        proceso = subprocess.Popen(comando, cwd=ROOT, stdout=salida, stderr=subprocess.STDOUT)
        while True:
            codigo = proceso.poll()
            if codigo is not None:
                registrar(f"Fase 2 limpia terminó con código {codigo}")
                break
            registrar("Fase 2 limpia sigue viva; aún sin resultado final")
            time.sleep(300)

    texto = LIGA_LOG.read_text(encoding="utf-8")
    resultado = re.search(r"Resultado: montecarlo (\d+) [–-] (\d+) iacasitegano", texto)
    if not resultado:
        registrar("Fase 2 terminó sin línea Resultado; no se actualiza INFORME")
        return
    derrotas, victorias = map(int, resultado.groups())
    total = derrotas + victorias
    with INFORME.open("a", encoding="utf-8") as f:
        f.write(
            "\n\n## Fase 2 limpia: orden de jugadas con el campeón correcto\n\n"
            "La prueba anterior `36-4` queda descartada para juzgar el ordenamiento: "
            "se ejecutó con los pesos self-play 300, posteriormente rechazados.\n\n"
            "Esta prueba usa el campeón restaurado `pesos_antes_selfplay_300`, "
            "ordenamiento de jugadas activado, `strategy.jugar()`, reparto de reloj "
            "`0.5/2.0/16`, 40 partidas reales, semilla 2030 y `--sin-docker`.\n\n"
            f"Resultado: Monte Carlo {derrotas} - {victorias} iacasitegano "
            f"({victorias}/{total} = {victorias / total:.1%}), contra la referencia "
            "histórica de iacasitegano 6-14 (30%).\n"
        )
    registrar(f"Resultado documentado: MC {derrotas}-{victorias}")


if __name__ == "__main__":
    main()
