# Informe: iacasitegano

## 1. Integrantes

Jose (000213398) y Daphne (000211927).

## 2. Idea en un párrafo

Expectiminimax exacto: en vez de tirar el dado usamos la probabilidad real que da el motor
(`estado.siguiente(j)`) y promediamos los dos resultados de cada ataque. Sobre eso, poda
alfa-beta, poda tipo Star1 en los nodos de azar, tabla de transposición y profundización
iterativa *anytime*: abrimos una profundidad más con un tope de nodos y, si no alcanza, la
abandonamos y jugamos la mejor de la última profundidad completa. La posición se mide con una
evaluación lineal de seis características cuyos pesos se ajustan con datos. Todo el núcleo está
compilado con numba sobre el tablero crudo.

## 3. Búsqueda (algoritmo y por qué)

Expectiminimax, porque el azar aquí es acotado y conocido: cada ataque tiene a lo más dos
resultados con probabilidad exacta, así que se puede **integrar** en vez de muestrearlo. Es una
ventaja estructural sobre un Monte Carlo plano como `montecarlo`, que tira el dado. (Las cifras
de nodos y profundidad de esta sección son medición offline del equipo, no incluida aquí.)

- **Poda alfa-beta** en los nodos de decisión y **Star1** en los de azar: conocida la cota de
  `evaluar()`, la rama "pierde" a veces no cambia la decisión. Verificado contra una búsqueda
  exhaustiva sin podar: mismo valor siempre.
- **Port a numba** sobre `int8[81]`, reusando los kernels de `motor/nucleo.py`: ~630 000
  nodos/s. Sin esto no pasábamos de profundidad 3-4.
- **Tabla de transposición**: arreglo de numpy, mapeo directo, "siempre reemplaza"; solo guarda
  valores exactos (ver el bug, sección 8).
- **Búsqueda anytime**, el cambio que más subió la fuerza. Antes solo abríamos la profundidad
  siguiente si alcanzaba para 300 veces lo que costó la anterior: el bot usaba **~1 % de su
  presupuesto** y llegaba a profundidad media 2.4, no 5-7. Ahora se abre con un tope de nodos
  calibrado con los nodos/segundo reales y, si se pasa, se aborta conservando la última
  profundidad completa; dos guardas evitan guardar subárboles abortados en la tabla. Medido en
  partidas: de 20 % a ~50 %.

## 4. Función de evaluación

Lineal: `evaluar = PESOS · features`, siempre "propio menos rival":

- **puntos**: diferencia de puntos anotados; domina el resto, como debe ser.
- **avance**: filas ya avanzadas, sumadas sobre todos los peones.
- **apoyo**: peones propios que cubren a otro propio (el criterio que usa el motor para
  `prob_combate`).
- **pasado**: avance contando solo peones sin rival en las tres columnas que les faltan.
  Optimista a propósito: un defensor solo tampoco bloquea de verdad.
- **columnas_vacias**: columnas rivales vacías menos las propias vacías. La agregamos tras ver
  en partidas que dejábamos columnas enteras libres.
- **carrera**: distancia del peón propio más avanzado a la meta menos la del rival.

Los pesos no están puestos a mano: salen de mínimos cuadrados con ridge sobre self-play
(`herramientas/entrenar.py`), en `data/pesos.npy`. Intentamos mejorarlos y **no lo logramos**
(sección 8).

## 5. Precomputación (qué y cómo regenerarla)

`data/pesos.npy` — los seis pesos de la evaluación:

```bash
cd estudiantes/iacasitegano && python herramientas/entrenar.py
```

Juega self-play (y contra `random`, `montecarlo` y dos rivales de `herramientas/`) a
profundidad fija, guarda las características de cada jugada nuestra con el resultado final
(+1/−1) y ajusta por ridge. Escribe un candidato `data/candidato_<fecha>.npy`; nunca pisa el
campeón. Unas 2 h 37 min para 300 partidas a profundidad 5 (medición offline del equipo, no
incluida aquí). Para variar rivales, carga con `importlib` el `strategy.py` de los rivales de
entrenamiento (líneas 70 y 72): **solo offline**, no corre en la liga ni toca el bot entregado.

`data/libro.json` — jugada recomendada para las primeras 4 jugadas propias, donde self-play la
vio ganar claramente más que la segunda:

```bash
cd estudiantes/iacasitegano && python herramientas/libro_apertura.py
```

`strategy.jugar()` lo consulta primero y revalida que la jugada sea legal; nunca es
obligatorio. El vigente es mixto (blancas del candidato nuevo, negras del anterior), elegido con
80 partidas en dos semillas (43-37, 25-15 como blancas) por la asimetría de color. Los demás
`.npy` son checkpoints históricos que el runtime no carga.

## 6. Manejo del reloj

Reserva fija del 30 % que nunca se gasta pensando; una jugada forzada no gasta reloj. Del resto,
cada jugada arranca con `1/16` de lo disponible, escalado entre 0.5× y 2.0× según qué fracción de
las jugadas legales son ataques (más ataques = más táctica). Dentro de ese presupuesto manda el
anytime de la sección 3; sin tiempo, se juega una legal al azar.

Medido en las 200 partidas del bot tal como se entrega: reloj medio **14.3 s**, p95 16.7 s y
máximo **18.2 s de 30 s**, con cero timeouts y cero jugadas ilegales. El reparto `0.5/2.0/16` se
eligió midiendo tres configuraciones.

## 7. Resultados vs random y montecarlo

Contra `random`: la validación de entrega juega 2 partidas (una por color) y las ganamos. No
medimos una tanda grande contra `random`: todo el esfuerzo fue contra `montecarlo`, que es el
rival que discrimina.

Contra `montecarlo`, con el árbitro, 30 s por partida, alternando colores, 1 CPU por bot y
semillas distintas por tanda. Intervalos de Wilson al 95 %:

| Configuración | Partidas | Resultado | Victorias | IC 95 % |
|---|---:|---|---:|---|
| Baseline (antes del anytime) | 200 | 40-160 | 20.0 % | 15.0 – 26.1 % |
| Búsqueda anytime | 400 | 199-201 | 49.8 % | 44.9 – 54.6 % |
| Anytime + progreso parcial de raíz | 200 | 105-95 | 52.5 % | 45.6 – 59.3 % |
| La misma, otras dos tandas | 200 y 200 | 103-97 y 94-106 | 51.5 % y 47.0 % | 44.6 – 58.3 y 40.2 – 53.9 |
| **Bot tal como se entrega** | 200 | 95-105 | **47.5 %** | 40.7 – 54.4 % |

El salto de **20 % a ~50 %** viene de que la búsqueda use el presupuesto de reloj que ya tenía.
Los intervalos de las tandas de 200 se solapan: **no afirmamos que ninguna sea mejor que otra**;
a ese tamaño el margen es de ±7 puntos.

La última fila es el bot tal como se entrega (semillas 8600-8609): 435 puntos, profundidad media
4.549, **cero timeouts, jugadas ilegales o excepciones**, las 200 por puntos, blancas 45-55 y
negras 50-50. Ese mismo código, byte por byte, midió **105-95** en las semillas 8000-8009: juntas
son **200-200 en 400 partidas**, **50.0 %** (IC 45.1 – 54.9 %). El intervalo incluye el 50 %, así
que queda **a la par** de `montecarlo`, no por encima. Contra un `montecarlo` más fuerte propio
(`noche_montecarlo_fuerte`) midió **53-47** en 100 partidas (53.0 %; IC 43.3 – 62.5 %).

Lo que esto **no** dice: nunca jugamos contra los Tiers ni contra otros equipos (son bots
ocultos), así que no hay evidencia sobre el resultado de la liga.

## 8. Qué intentamos y no funcionó

Todo se midió con partidas completas bajo el árbitro o con una prueba offline determinista; las
partidas son contra `montecarlo`. Las cifras de nodos, aciertos y conteos de posiciones de esta
sección son medición offline del equipo, no incluida en este repositorio.

| Intento | Qué se midió y qué salió |
|---|---|
| **Star2** | Correcto (480 pruebas diferenciales vs exhaustivo) y **0 % de ahorro de nodos** a prof. 4-6, conteos idénticos: la cota `±ganancia` es ~15× el rango de la eval. 200 partidas: 103-97 |
| **Orden de jugadas** | Ahorra 70/76/83 % de nodos a prof. 4/5/6 pero cuesta ~8× por nodo (recalcula prioridad en cada nodo). 200 partidas: **85-115**, menos profundidad (4.6 vs 5.2-5.5) |
| **Rollouts en la raíz** | En 50 posiciones de final aciertan la mejor de 4 candidatas el **36 %** vs **76 %** de la búsqueda; donde ésta empata, 44 % vs 78 % |
| **Pesos de partidas reales** | Ajustados sobre 1 621 partidas y 160 234 posiciones (partición por partida): mejor signo en el retenido, pero **98-102** en 200 partidas (49.0 %; IC 42.2-55.9), y se especializarían en `montecarlo` |
| **Barrido ridge** | 4 configuraciones × 100 partidas, cada una vs su control: 46-54 (45-55), 48-52 (47-53), 47-53 (41-59), 44-56 (51-49). Ninguna gana |
| **`ventaja_carrera_exacta`** | 40 partidas sin Docker: **3-37**. El peso salió negativo, alerta antes de medir. Muestra chica, margen enorme |
| **Tablas de finales** | Verificadas (simetría sobre 92 178 estados, cross-check independiente), pero **0 de 80 partidas llegaron a ese material**. No se entregan |
| **Quiescencia** | A/B en partidas: mismas victorias, menos puntos. Desactivada |
| **Arreglo de la tabla de transposición** | Correcto y necesario, pero 200 partidas dan **94-106**: sin mejora en el marcador |

**Dos bugs que encontramos midiendo, y que importan más que varias de esas técnicas:**

1. **El bot tiraba el 99 % de su reloj.** Abrir la profundidad siguiente exigía 300× el tiempo
   de la anterior; como cada salto cuesta 5-30×, se cortaba enseguida: 7.4 ms por jugada de un
   presupuesto de 660-2 620 ms, profundidad media 2.4. Eso explica por qué Star2, orden de
   jugadas y quiescencia midieron neutro o peor: su beneficio es más profundidad por unidad de
   tiempo, y el bot se detenía por una razón ajena al costo de buscar.
2. **La tabla de transposición guardaba cotas como valores exactos.** El corte Star1 devuelve
   una cota, y se almacenaba marcada como exacta. Consecuencia medible: el valor de la raíz
   dependía del **orden de las jugadas**, imposible en alfa-beta. A profundidad 6 el bot erraba
   1 de 35 posiciones con su orden normal y 4 de 35 reordenadas. Diagnosticado por eliminación
   (descartando primero la clave de la tabla) y corregido con la condición estándar: guardar solo
   si el valor cae estrictamente dentro de la ventana original.

## 9. Fuentes y uso de IA

**Fuentes.** Russell y Norvig, *Artificial Intelligence: A Modern Approach*, capítulo de juegos
(expectiminimax, alfa-beta). Ballard, B. W. (1983), «The \*-minimax search procedure for trees
containing chance nodes», *Artificial Intelligence* 21(3), para Star1/Star2. Sutton y Barto,
*Reinforcement Learning: An Introduction*, para ajustar una evaluación lineal con datos. La
condición de exactitud de la tabla de transposición es la estándar de los motores de ajedrez.

**Uso de agentes de IA.** Trabajamos con dos agentes (Claude Code y Codex) coordinados por el
equipo, en worktrees separados del repositorio.

- **El equipo decidió**: qué hipótesis probar y en qué orden, el protocolo (tamaño de muestra,
  semillas de desarrollo contra semillas de validación reservadas, alternar colores), los
  criterios de aceptación *antes* de medir, y qué se promueve. También corrigió el método:
  exigir 200 partidas en vez de 20 para el baseline destapó que la referencia de "30 %" con la
  que se rechazaron dos técnicas era 20 %.
- **Los agentes hicieron**: implementación (numba, anytime, tablas de finales, arneses),
  pruebas diferenciales, ejecución de tandas y análisis offline. Codex construyó el arnés
  paralelo con Docker y midió los baselines; Claude Code implementó el anytime, el laboratorio
  de evaluación y encontró los dos bugs de la sección 8.
- **No se delegó**: ninguna promoción sin revisión del equipo, ni resultado dado por bueno sin
  partidas completas bajo el árbitro.

Toda la estrategia es del equipo: no se copió código de otros equipos ni de internet, no hay
redes neuronales, y el bot no accede a la red ni persiste nada entre partidas.
