"""Bot «iacasitegano»: expectiminimax exacto (usa la probabilidad real del dado,
no una tirada) + evaluación lineal a mano. Fase 1 del plan del equipo.
"""

from __future__ import annotations

import json
import random
import time

import numpy as np

from motor import Estado, Jugada, reportar

import busqueda_numba as _busqueda
import eval as _eval

RESERVA = 0.3  # fracción del reloj que nunca gastamos pensando (la comunicación también cuesta)
# Cuánto más o menos tiempo (relativo al reparto base) le damos a una jugada según qué
# fracción de las jugadas legales son ataques: más ataques disponibles = posición más
# táctica = vale más la pena pensarla. En una posición tranquila (sin ataques) gastamos
# menos de lo normal; en una con TODO ataques, hasta el doble. El tiempo que no se gasta
# en jugadas tranquilas queda disponible (vía `tiempo_restante`) para las tácticas.
PESO_MINIMO = 0.5
PESO_MAXIMO = 2.0
REPARTO = 16


def preparar(config):
    global color, rng, reserva, libro  # se guardan aquí para usarlos en cada llamada a jugar
    color = config.color  # evaluamos SIEMPRE desde nuestro color
    rng = random.Random(config.semilla)
    reserva = RESERVA * config.reloj_s
    # Si `herramientas/entrenar.py` ya generó pesos con self-play, los usamos;
    # si no existe el archivo (antes de entrenar, o en --sin-docker sin carpeta
    # de datos), seguimos con los pesos a mano de `eval.py`.
    ruta_pesos = config.carpeta_datos / "pesos.npy"
    if ruta_pesos.exists():
        _eval.cargar_pesos(np.load(ruta_pesos))
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
