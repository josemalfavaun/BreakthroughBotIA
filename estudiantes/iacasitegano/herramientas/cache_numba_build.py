"""Compila las funciones Numba activas del equipo dentro de torneo-bot-base:local.

Se invoca en el contenedor con el equipo montado en /bot y NUMBA_CACHE_DIR=/tmp/numba.
El cache locator conserva /bot como ruta fuente, igual que en una partida oficial.
"""

from __future__ import annotations

import json
import hashlib
import os
import platform
from pathlib import Path
import sys


def main() -> None:
    equipo = Path("/bot")
    datos = equipo / "data"
    sys.path.insert(0, str(equipo))
    from motor import Estado, simular_al_azar

    # Mismo calentamiento común que runner.calentar_motor(), fuera del tiempo de preparar.
    estado = Estado.inicial()
    estado.siguiente(estado.jugadas()[0])
    simular_al_azar(estado, 1, 0, "blancas")
    import strategy as estrategia

    # Reproduce la carga de pesos y la compilación que strategy.preparar() ejecuta,
    # pero no lee la caché anterior: esta salida debe poder regenerarse desde cero.
    import numpy as np
    import numba

    with np.load(datos / estrategia.PESOS_EVAL3) as archivo:
        estrategia._busqueda.cargar_pesos(archivo["pesos"])
    estrategia._busqueda.calentar()

    cache = Path(os.environ["NUMBA_CACHE_DIR"])
    prefijos_equipo = ("eval3.", "busqueda_eval3.")
    conservar = []
    for archivo in cache.rglob("*"):
        if not archivo.is_file():
            continue
        if archivo.name.startswith(prefijos_equipo) and archivo.suffix in {".nbi", ".nbc"}:
            conservar.append(archivo)
        else:
            archivo.unlink()
    for carpeta in sorted((p for p in cache.rglob("*") if p.is_dir()), reverse=True):
        try:
            carpeta.rmdir()
        except OSError:
            pass
    if not conservar:
        raise RuntimeError("Numba no generó archivos .nbi/.nbc de eval3 ni busqueda_eval3")

    fuentes = {
        nombre: hashlib.sha256(ruta.read_bytes()).hexdigest()
        for nombre, ruta in {
            "strategy.py": equipo / "strategy.py",
            "eval3.py": equipo / "eval3.py",
            "busqueda_eval3.py": equipo / "busqueda_eval3.py",
            "motor/nucleo.py": Path("/torneo/sistema/motor/nucleo.py"),
        }.items()
    }
    (cache / "manifest.json").write_text(json.dumps({
        "formato": 1,
        "fuentes_sha256": fuentes,
        "python": [sys.version_info.major, sys.version_info.minor],
        "numba": numba.__version__,
        "numpy": np.__version__,
        "arquitectura": platform.machine(),
    }, sort_keys=True) + "\n", encoding="utf-8")

    archivos = [p for p in cache.rglob("*") if p.is_file()]
    print(json.dumps({
        "cache_dir": str(cache),
        "archivos": len(archivos),
        "bytes": sum(p.stat().st_size for p in archivos),
        "nombres": sorted(p.name for p in archivos),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
