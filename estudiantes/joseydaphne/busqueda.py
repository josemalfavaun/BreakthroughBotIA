"""Expectiminimax exacto (usa la probabilidad real del dado, nunca la tirada)
con poda alfa-beta, poda tipo Star1 en los nodos de azar, tabla de
transposición y profundización iterativa.

Fase 1 (profundidad fija 1-2, sin poda) perdía 4-0 contra `montecarlo`: no
veía un peón rival escapándose por un costado hasta que ya era imparable.
Medimos el costo de profundizar sin podar (profundidad 3 ≈ 6 s, profundidad 4
≈ 90 s en una posición típica) y confirmamos que la poda no es opcional.

Cómo se poda un nodo de azar (Star1): cada ataque tiene como mucho 2
resultados, `[(p, gana), (1-p, pierde)]`. Si ya evaluamos `gana` y sabemos que
`pierde` no puede valer más de `ganancia` ni menos de `-ganancia` (la cota real
de `evaluar()` con los pesos actuales, ver `eval.cota()`), podemos acotar el
valor esperado de la jugada SIN mirar `pierde`: si incluso en el mejor caso
para `pierde` la jugada no le gana a `alfa`, no hace falta la cifra exacta.
`ganancia` se recalcula en cada llamada a `elegir()` (no es una constante):
unos pesos entrenados con otra magnitud volverían insegura una cota vieja.

# ponytail: la ventana alfa/beta no se re-acota al entrar a cada hijo (se pasa
# tal cual, sin la derivación completa de Star2 por rama). Más simple y
# seguro; menos nodos podados que una Star2 completa. Subir a eso si con esto
# no alcanza la profundidad.
"""

from __future__ import annotations

import time

from motor import Estado, Jugada

from eval import cota, evaluar

PROFUNDIDAD_MAXIMA = 12
MARGEN_SEGURIDAD = 1.6  # no empezar una profundidad si no sobra este margen sobre lo estimado
FACTOR_INICIAL = 20.0  # estimado a ojo para el primer salto de profundidad (sin medición previa)


def _valor_jugada(
    estado: Estado,
    j: Jugada,
    color: str,
    profundidad: int,
    tt: dict,
    contador: list[int],
    alfa: float,
    beta: float,
    ganancia: float,
) -> float:
    """Valor esperado de la jugada `j` (una o dos ramas de azar), acotado en [alfa, beta]."""
    resultados = estado.siguiente(j)
    if len(resultados) == 1:
        _, hijo = resultados[0]
        return _valor(hijo, color, profundidad - 1, tt, contador, alfa, beta, ganancia)

    (p1, hijo1), (p2, hijo2) = resultados
    v1 = _valor(hijo1, color, profundidad - 1, tt, contador, -ganancia, ganancia, ganancia)
    mejor_caso = p1 * v1 + p2 * ganancia  # si `hijo2` valiera lo más posible
    if mejor_caso <= alfa:
        return mejor_caso  # no le gana a alfa ni en el mejor caso: no hace falta ver hijo2
    peor_caso = p1 * v1 - p2 * ganancia  # si `hijo2` valiera lo menos posible
    if peor_caso >= beta:
        return peor_caso  # ya es demasiado bueno para el rival de arriba: tampoco hace falta
    v2 = _valor(hijo2, color, profundidad - 1, tt, contador, -ganancia, ganancia, ganancia)
    return p1 * v1 + p2 * v2


def _valor(
    estado: Estado,
    color: str,
    profundidad: int,
    tt: dict,
    contador: list[int],
    alfa: float,
    beta: float,
    ganancia: float,
) -> float:
    contador[0] += 1
    ganador = estado.ganador()
    if ganador is not None:
        return ganancia if ganador == color else -ganancia
    if profundidad == 0:
        return evaluar(estado, color)
    llave = (estado.clave, profundidad)
    if llave in tt:
        return tt[llave]

    es_max = estado.turno == color
    mejor = -ganancia - 1.0 if es_max else ganancia + 1.0
    exacto = True
    for j in estado.jugadas():
        v = _valor_jugada(estado, j, color, profundidad, tt, contador, alfa, beta, ganancia)
        if es_max:
            if v > mejor:
                mejor = v
            alfa = max(alfa, mejor)
        else:
            if v < mejor:
                mejor = v
            beta = min(beta, mejor)
        if alfa >= beta:
            exacto = False  # quedaron jugadas sin revisar: esto es una cota, no el valor real
            break

    if exacto:  # solo guardamos valores exactos: uno podado podría ser solo una cota
        tt[llave] = mejor
    return mejor


def _mejor_jugada(
    estado: Estado, color: str, profundidad: int, tt: dict, contador: list[int], ganancia: float
) -> tuple[Jugada, float]:
    mejor_jugada, mejor_valor = None, -ganancia - 1.0
    alfa = -ganancia
    for j in estado.jugadas():
        valor = _valor_jugada(estado, j, color, profundidad, tt, contador, alfa, ganancia, ganancia)
        if valor > mejor_valor:
            mejor_valor, mejor_jugada = valor, j
            alfa = max(alfa, mejor_valor)
    return mejor_jugada, mejor_valor


def elegir(estado: Estado, color: str, limite_tiempo: float) -> tuple[Jugada, float, int]:
    """Mejor jugada para `color` en `estado`, subiendo la profundidad mientras alcance el tiempo.

    `limite_tiempo` es un tope de `time.perf_counter()`: nunca arranca una
    profundidad nueva si, por el factor de crecimiento medido en la anterior,
    estima que no la va a terminar a tiempo. Regresa (jugada, valor, profundidad
    alcanzada).
    """
    ganancia = cota() + 100.0  # recalculada: los pesos entrenados pueden cambiar de magnitud
    tt: dict = {}
    jugadas = estado.jugadas()
    mejor_jugada, mejor_valor, mejor_profundidad = jugadas[0], 0.0, 0
    nodos_anteriores = 0
    profundidad = 1

    while profundidad <= PROFUNDIDAD_MAXIMA:
        contador = [0]
        inicio = time.perf_counter()
        jugada, valor = _mejor_jugada(estado, color, profundidad, tt, contador, ganancia)
        duracion = time.perf_counter() - inicio
        mejor_jugada, mejor_valor, mejor_profundidad = jugada, valor, profundidad
        if time.perf_counter() >= limite_tiempo:
            break
        factor = contador[0] / nodos_anteriores if nodos_anteriores else FACTOR_INICIAL
        nodos_anteriores = contador[0]
        if limite_tiempo - time.perf_counter() < duracion * factor * MARGEN_SEGURIDAD:
            break
        profundidad += 1

    return mejor_jugada, mejor_valor, mejor_profundidad
