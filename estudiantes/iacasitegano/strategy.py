"""Bot «iacasitegano»: expectiminimax exacto (usa la probabilidad real del dado,
no una tirada) + evaluación lineal a mano. Fase 1 del plan del equipo.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import shutil
import sys
import time
from pathlib import Path

import numba
import numpy as np

from motor import Estado, Jugada, reportar
from motor import nucleo as _motor_nucleo

import busqueda_eval3 as _busqueda

RESERVA = 0.3  # fracción del reloj que nunca gastamos pensando (la comunicación también cuesta)
# Cuánto más o menos tiempo (relativo al reparto base) le damos a una jugada según qué
# fracción de las jugadas legales son ataques: más ataques disponibles = posición más
# táctica = vale más la pena pensarla. En una posición tranquila (sin ataques) gastamos
# menos de lo normal; en una con TODO ataques, hasta el doble. El tiempo que no se gasta
# en jugadas tranquilas queda disponible (vía `tiempo_restante`) para las tácticas.
PESO_MINIMO = 0.5
PESO_MAXIMO = 2.0
REPARTO = 16
PESOS_EVAL3 = "pesos_eval3_ligero.npz"
CACHE_NUMBA_EQUIPO = "numba_cache"
CACHE_NUMBA_MANIFEST = "manifest.json"


def _cache_numba_vigente(origen):
    """Rechaza cachés generados con otro código o ABI antes de copiarlos al tmpfs."""
    try:
        manifiesto = json.loads((origen / CACHE_NUMBA_MANIFEST).read_text(encoding="utf-8"))
        fuentes = {
            nombre: hashlib.sha256(ruta.read_bytes()).hexdigest()
            for nombre, ruta in {
                "strategy.py": Path(__file__),
                "eval3.py": Path(__file__).with_name("eval3.py"),
                "busqueda_eval3.py": Path(__file__).with_name("busqueda_eval3.py"),
                "motor/nucleo.py": Path(_motor_nucleo.__file__),
            }.items()
        }
        return (
            manifiesto.get("fuentes_sha256") == fuentes
            and manifiesto.get("python") == [sys.version_info.major, sys.version_info.minor]
            and manifiesto.get("numba") == numba.__version__
            and manifiesto.get("numpy") == np.__version__
            and manifiesto.get("arquitectura") == platform.machine()
        )
    except (OSError, ValueError, TypeError, AttributeError):
        return False


def _copiar_cache_numba(carpeta_datos):
    """Precalienta el caché privado de esta versión del equipo en el tmpfs del runner.

    El árbitro crea un contenedor por partida y `NUMBA_CACHE_DIR` empieza vacío. La caché
    compartida del motor ya fue copiada por `runner.py`; aquí se agregan las compilaciones
    de eval3/busqueda_eval3, sin escribir en data/.
    """
    destino = os.environ.get("NUMBA_CACHE_DIR")
    origen = carpeta_datos / CACHE_NUMBA_EQUIPO
    if not destino or not origen.is_dir():
        return
    if not _cache_numba_vigente(origen):
        print(
            "[iacasitegano] Caché numba ausente, obsoleto o incompatible; "
            "se compilará desde el código actual.",
            file=sys.stderr,
        )
        return
    try:
        for carpeta, _, archivos in os.walk(origen):
            nueva = Path(destino) / Path(carpeta).relative_to(origen)
            nueva.mkdir(parents=True, exist_ok=True)
            for nombre in archivos:
                shutil.copyfile(Path(carpeta) / nombre, nueva / nombre)
    except (OSError, shutil.Error) as exc:
        # La caché solo evita compilar durante preparar; si no se puede copiar, Numba
        # compila normalmente en el tmpfs y el bot conserva su comportamiento correcto.
        print(f"[iacasitegano] No se pudo copiar la caché de numba: {exc}", file=sys.stderr)


def preparar(config):
    global color, rng, reserva, libro  # se guardan aquí para usarlos en cada llamada a jugar
    color = config.color  # evaluamos SIEMPRE desde nuestro color
    rng = random.Random(config.semilla)
    reserva = RESERVA * config.reloj_s
    _copiar_cache_numba(config.carpeta_datos)
    # Los pesos eval3 son un NPZ empaquetado con familias de features activas.
    ruta_pesos = config.carpeta_datos / PESOS_EVAL3
    if ruta_pesos.exists():
        with np.load(ruta_pesos) as datos:
            _busqueda.cargar_pesos(datos["pesos"])
    # Libro de apertura (herramientas/libro_apertura.py): {clave del tablero: [origen, destino]},
    # solo para las primeras jugadas. Si no existe el archivo, `libro` queda vacío y `jugar`
    # siempre busca en vivo — el libro nunca es obligatorio.
    ruta_libro = config.carpeta_datos / "libro.json"
    libro = json.loads(ruta_libro.read_text()) if ruta_libro.exists() else {}
    # Calentamos numba: la búsqueda entera es numba ahora (ver busqueda_numba.py), y
    # compilarla tarda segundos — aquí no gasta reloj (10 s aparte para `preparar`).
    _busqueda.calentar()


def jugar(estado: Estado, tiempo_restante: float):
    jugadas = estado.jugadas()
    if len(jugadas) == 1:  # forzada: no hay nada que decidir, no gastamos reloj pensándola
        return jugadas[0]

    entrada_libro = libro.get(str(estado.clave))
    if entrada_libro is not None:
        jugada_libro = Jugada(*entrada_libro)
        if jugada_libro in jugadas:  # por si acaso: nunca confiamos un libro a ciegas
            return jugada_libro

    # Si una jugada gana la partida sin importar el dado, la tomamos sin pensar más.
    for j in jugadas:
        if all(hijo.ganador() == color for _, hijo in estado.siguiente(j)):
            return j

    disponible = tiempo_restante - reserva
    if disponible <= 0:  # solo queda la reserva: no hay tiempo de pensar
        return rng.choice(jugadas)

    n_ataques = sum(1 for j in jugadas if estado.es_ataque(j))
    peso = PESO_MINIMO + (PESO_MAXIMO - PESO_MINIMO) * (n_ataques / len(jugadas))
    inicio = time.perf_counter()
    limite = inicio + peso * disponible / REPARTO
    jugada, valor, profundidad = _busqueda.elegir(estado, color, limite)
    reportar(prof=profundidad, eval=valor, tiempo=time.perf_counter() - inicio)
    return jugada
