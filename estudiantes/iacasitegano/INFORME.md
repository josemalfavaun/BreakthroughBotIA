# Informe: iacasitegano

## 1. Integrantes

Jose (000213398) y Daphne (000211927).

## 2. Idea en un párrafo

Expectiminimax exacto: en vez de tirar el dado usamos la probabilidad real del motor
(`estado.siguiente(j)`) y promediamos los dos resultados de cada ataque. Sobre eso: alfa-beta,
poda tipo Star1 en los nodos de azar, tabla de transposición y profundización iterativa
*anytime* (abrimos una profundidad más con un tope de nodos y, si no alcanza, la abandonamos y
jugamos la mejor de la última completa). La posición se mide con una evaluación lineal de seis
características ajustadas con datos. Todo el núcleo está compilado con numba.

## 3. Búsqueda (algoritmo y por qué)

Expectiminimax, porque el azar aquí es acotado y conocido: cada ataque tiene a lo más dos
resultados con probabilidad exacta, así que se puede **integrar** en vez de muestrearlo — ventaja
sobre un Monte Carlo plano como `montecarlo`, que tira el dado. (Las cifras de nodos y
profundidad de esta sección son medición offline del equipo, no incluida en este repositorio.)

- **Alfa-beta** y **Star1** en los nodos de azar: conocida la cota de `evaluar()`, la rama
  "pierde" a veces no cambia la decisión. Verificado contra una búsqueda exhaustiva sin podar.
- **numba** sobre `int8[81]`, reusando los kernels de `motor/nucleo.py`: ~630 000 nodos/s. Sin
  esto no pasábamos de profundidad 3-4.
- **Tabla de transposición** de numpy, mapeo directo; solo guarda valores exactos (bug, §8).
- **Anytime**, el cambio que más subió la fuerza. Antes solo abríamos la profundidad siguiente si
  alcanzaba para 300 veces lo que costó la anterior: el bot usaba **~1 % de su presupuesto** y
  llegaba a profundidad media 2.4, no 5-7. Ahora el tope es de nodos, calibrado con los
  nodos/segundo reales; si se pasa, se aborta conservando la última profundidad completa, y dos
  guardas evitan guardar subárboles abortados. Medido: de 20 % a ~50 %.

## 4. Función de evaluación

Lineal, `evaluar = PESOS · features`, siempre "propio menos rival": **puntos** (diferencia
anotada, domina el resto), **avance** (filas avanzadas sumadas), **apoyo** (peones propios que
cubren a otro propio, el criterio del motor para `prob_combate`), **pasado** (avance contando
solo peones sin rival en las tres columnas que les faltan; optimista a propósito, un defensor
solo tampoco bloquea), **columnas_vacias** (columnas rivales vacías menos las propias vacías) y
**carrera** (distancia del peón propio más avanzado a la meta menos la del rival).

Los pesos no están a mano: salen de mínimos cuadrados con ridge sobre self-play
(`herramientas/entrenar.py`), en `data/pesos.npy`. Intentamos mejorarlos y **no lo logramos**
(sección 8).

## 5. Precomputación (qué y cómo regenerarla)

```bash
cd estudiantes/iacasitegano && python herramientas/entrenar.py       # data/pesos.npy
cd estudiantes/iacasitegano && python herramientas/libro_apertura.py # data/libro.json
```

`entrenar.py` juega self-play (y contra `random`, `montecarlo` y dos rivales de `herramientas/`)
a profundidad fija, guarda las características de cada jugada nuestra con el resultado final
(+1/−1) y ajusta por ridge; escribe `data/candidato_<fecha>.npy` y nunca pisa el campeón. Unas
2 h 37 min para 300 partidas a profundidad 5 (medición offline del equipo, no incluida aquí).
Para variar rivales carga con `importlib` su `strategy.py` (líneas 70 y 72): **solo offline**, no
corre en la liga ni toca el bot entregado.

`libro.json` da la jugada recomendada en las primeras 4 jugadas propias donde self-play la vio
ganar claramente más que la segunda; `strategy.jugar()` la revalida y nunca es obligatoria. El
vigente es mixto (blancas del candidato nuevo, negras del anterior), elegido con 80 partidas en
dos semillas (43-37, 25-15 como blancas) por la asimetría de color, con el bot anterior al
anytime. Los demás `.npy` son checkpoints históricos que el runtime no carga.

## 6. Manejo del reloj

Reserva fija del 30 %; una jugada forzada no gasta reloj. Del resto, cada jugada arranca con
`1/16` de lo disponible, escalado entre 0.5× y 2.0× según qué fracción de las jugadas legales son
ataques. Dentro de ese presupuesto manda el anytime; sin tiempo, se juega una legal al azar.

Medido en las 200 partidas del bot tal como se entrega: reloj medio **14.3 s**, p95 16.7 s,
máximo **18.2 s de 30 s**, cero timeouts y cero jugadas ilegales. El reparto `0.5/2.0/16` se
eligió con tres pruebas de 20 partidas **del bot anterior al anytime** (3-17, 6-14 y 4-16); no se
volvió a medir con anytime.

## 7. Resultados vs random y montecarlo

Contra `random`: la prueba de humo del validador (2 partidas, una por color, con reloj de 3 s en
vez de 30 s) **pasa**, pero da un aviso intermitente de reloj, porque el costo mínimo por jugada
(~49 ms) no escala con un reloj tan corto. Con 30 s medimos **0 timeouts en 400 partidas**. No
hay una tanda grande contra `random`.

Contra `montecarlo`, con el árbitro, 30 s por partida, alternando colores y semillas distintas
por tanda. Cada trabajo corrió en un contenedor con `--cpus=1 --memory=1024m --network=none`
(`herramientas/medir_liga.py`), con el torneo invocado `--sin-docker` dentro; la memoria máxima
no se instrumentó. Intervalos de Wilson al 95 %:

| Configuración | Partidas | Resultado | Victorias | IC 95 % |
|---|---:|---|---:|---|
| Baseline (antes del anytime) | 200 | 40-160 | 20.0 % | 15.0 – 26.1 % |
| Búsqueda anytime | 400 | 199-201 | 49.8 % | 44.9 – 54.6 % |
| Anytime + progreso parcial de raíz | 200 | 105-95 | 52.5 % | 45.6 – 59.3 % |
| **Bot tal como se entrega** | 200 | 95-105 | **47.5 %** | 40.7 – 54.4 % |

El salto de **20 % a ~50 %** viene de que la búsqueda use el presupuesto de reloj que ya tenía.
Los intervalos de las tandas de 200 se solapan: **no afirmamos que ninguna sea mejor que otra**;
a ese tamaño el margen es de ±7 puntos.

La última fila es el bot tal como se entrega (semillas 8600-8609): 435 puntos, profundidad media
4.549, **cero timeouts, jugadas ilegales o excepciones**, las 200 por puntos, blancas 45-55 y
negras 50-50. La tanda de 105-95 (`mediciones/anytime2_1_200`) corrió con los mismos SHA-256 que
se entregan, comparados y confirmados: `busqueda_numba.py` `e97dae60…`, `strategy.py`
`bdcca0a4…`, `eval.py` `437b8c48…`, `data/pesos.npy` `d5cc25ee…`, `data/libro.json` `00fd209f…`.
Juntas son **200-200 en 400 partidas**, **50.0 %** (IC 45.1 – 54.9 %): el intervalo incluye el
50 %, así que queda **a la par** de `montecarlo`, no por encima. Contra un `montecarlo` más
fuerte propio midió **53-47** en 100 partidas (53.0 %; IC 43.3 – 62.5 %).

Nunca jugamos contra los Tiers ni contra otros equipos (son bots ocultos): no hay evidencia sobre
el resultado de la liga.

## 8. Qué intentamos y no funcionó

Partidas completas bajo el árbitro contra `montecarlo`, o pruebas offline deterministas. Las
cifras de nodos, aciertos y conteos de posiciones son medición offline del equipo, no incluida en
este repositorio.

| Intento | Qué se midió y qué salió |
|---|---|
| **Star2** (`anytime2_2`) | Correcto (480 pruebas diferenciales vs exhaustivo) y **0 % de ahorro de nodos** a prof. 4-6: la cota `±ganancia` es ~15× el rango de la eval. 103-97, prof. 4.566 (`mediciones/anytime2_2_200`) |
| **TT corregida** (`anytime2_3`) | El arreglo del bug 2: necesario, pero **94-106**, prof. 4.477 (`mediciones/anytime2_3_200`) |
| **TT corregida + orden de jugadas** (`anytime2_4`) | El orden ahorra 70/76/83 % de nodos a prof. 4/5/6 pero cuesta ~8× por nodo. La tanda combina ambas: **85-115**, prof. **4.233** contra 4.545 de `anytime2_1` (`mediciones/anytime2_4_200`) |
| **Rollouts en la raíz** | En 50 posiciones de final aciertan la mejor de 4 candidatas el **36 %** vs **76 %** de la búsqueda |
| **Pesos de partidas reales** | 1 621 partidas y 160 234 posiciones (partición por partida): mejor signo en el retenido, pero **98-102** (IC 42.2-55.9) y se especializarían en `montecarlo` (`medicion/pesosreales_200_20261025_164748`) |
| **Barrido ridge** | 4 × 100 partidas vs su control: 46-54 (45-55), 48-52 (47-53), 47-53 (41-59), 44-56 (51-49). Ninguna gana (`mediciones/ridge_*`) |
| **`ventaja_carrera_exacta`** | 40 partidas sin Docker **con el bot anterior al anytime**: **3-37**, con peso aprendido negativo. Muestra chica, margen enorme |
| **Tablas de finales** (1v1, 2v1, 1v2) | Verificadas (simetría sobre 92 178 estados), pero **0 de 80 partidas llegaron a ese material** (bot anterior al anytime). No se entregan |
| **Quiescencia** | Mismas victorias, menos puntos, con el bot anterior al anytime. Desactivada |

**Dos bugs que encontramos midiendo:**

1. **El bot tiraba el 99 % de su reloj.** Abrir la profundidad siguiente exigía 300× el tiempo
   de la anterior; como cada salto cuesta 5-30×, se cortaba enseguida: 7.4 ms por jugada de un
   presupuesto de 660-2 620 ms, profundidad media 2.4. Eso explica por qué Star2, orden de jugadas
   y quiescencia midieron neutro o peor: su beneficio es profundidad por unidad de tiempo, y el
   bot se detenía por una razón ajena al costo de buscar.
2. **La tabla de transposición guardaba cotas como valores exactos.** El corte Star1 devuelve una
   cota y se almacenaba como exacta, así que el valor de la raíz dependía del **orden de las
   jugadas**, imposible en alfa-beta: a profundidad 6 erraba 1 de 35 posiciones con el orden
   normal y 4 de 35 reordenadas. Corregido con la condición estándar: guardar solo si el valor
   cae estrictamente dentro de la ventana original.

## 9. Fuentes y uso de IA

**Fuentes.** Russell y Norvig, *Artificial Intelligence: A Modern Approach*, capítulo de juegos.
Ballard, B. W. (1983), «The \*-minimax search procedure for trees containing chance nodes»,
*Artificial Intelligence* 21(3), para Star1/Star2. Sutton y Barto, *Reinforcement Learning: An
Introduction*, para ajustar una evaluación lineal con datos. La condición de exactitud de la
tabla de transposición es la estándar de los motores de ajedrez.

**Uso de agentes de IA.** Trabajamos con dos agentes (Claude Code y Codex) coordinados por el
equipo, en worktrees separados.

- **El equipo decidió** qué hipótesis probar y en qué orden, el protocolo (tamaño de muestra,
  semillas de desarrollo contra semillas de validación reservadas, alternar colores), los
  criterios de aceptación *antes* de medir, y qué se promueve. También corrigió el método: exigir
  200 partidas en vez de 20 para el baseline destapó que la referencia de "30 %" con la que se
  rechazaron dos técnicas era 20 %.
- **Los agentes** implementaron, hicieron las pruebas diferenciales y corrieron tandas y análisis
  offline. Codex construyó el arnés paralelo con Docker y midió los baselines; Claude Code
  implementó el anytime, el laboratorio de evaluación y encontró los dos bugs.
- **No se delegó** ninguna promoción sin revisión, ni se dio por bueno un resultado sin partidas
  completas bajo el árbitro.

Toda la estrategia es del equipo: no se copió código de otros equipos ni de internet, no hay
redes neuronales, y el bot no accede a la red ni persiste nada entre partidas.
