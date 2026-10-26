# Informe: iacasitegano

## 1. Integrantes

Jose (000213398) y Daphne (000211927).

## 2. Idea en un párrafo

Expectiminimax exacto: en vez de tirar el dado, usamos la probabilidad real que da el motor
(`estado.siguiente(j)`) y promediamos los dos resultados de cada ataque. Sobre eso, poda
alfa-beta, una poda tipo Star1 en los nodos de azar, tabla de transposición y profundización
iterativa *anytime*: abrimos una profundidad más con un tope de nodos y, si no alcanza, la
abandonamos y jugamos la mejor jugada de la última profundidad completa. La posición se mide
con una evaluación lineal de seis características cuyos pesos se ajustan con datos, no a mano.
Todo el núcleo de búsqueda está compilado con numba sobre el tablero crudo.

## 3. Búsqueda (algoritmo y por qué)

Expectiminimax, porque el azar de este juego es acotado y conocido: cada ataque tiene a lo más
dos resultados con probabilidad exacta, así que se puede **integrar** el azar en vez de
muestrearlo. Es una ventaja estructural sobre un Monte Carlo plano como `montecarlo`, que tira
el dado.

- **Poda alfa-beta** en los nodos de decisión y **Star1** en los de azar: conocida la cota real
  de `evaluar()`, la rama "pierde" a veces no puede cambiar la decisión. Verificado contra una
  búsqueda exhaustiva sin podar: mismo valor siempre.
- **Port a numba** sobre `int8[81]`, reusando los kernels de `motor/nucleo.py`: ~630 000
  nodos/s medidos. Sin esto no pasábamos de profundidad 3-4.
- **Tabla de transposición**: arreglo de numpy, mapeo directo, "siempre reemplaza"; solo guarda
  valores exactos (ver el bug de la sección 8).
- **Búsqueda anytime**, el cambio que más subió la fuerza. Antes solo abríamos la profundidad
  siguiente si alcanzaba para 300 veces lo que costó la anterior; medimos que eso dejaba al bot
  usando **~1 % de su presupuesto** y a profundidad media 2.4, no 5-7. Ahora se abre con un
  tope de nodos calibrado con los nodos/segundo reales y, si se pasa, se aborta y se conserva
  la última profundidad completa (dos guardas evitan que la tabla guarde subárboles abortados).
  Medido: de 20 % a ~50 % contra `montecarlo`.

## 4. Función de evaluación

Lineal: `evaluar = PESOS · features`, siempre "propio menos rival":

- **puntos**: diferencia de puntos anotados (domina el resto, como debe ser).
- **avance**: filas ya avanzadas, sumadas sobre todos los peones.
- **apoyo**: peones propios que cubren a otro peón propio (el mismo criterio que usa el motor
  para `prob_combate`).
- **pasado**: avance contando solo peones sin rival en las tres columnas que les faltan. Es
  optimista a propósito: un defensor solo tampoco bloquea de verdad.
- **columnas_vacias**: columnas rivales sin peones menos las propias igual. La agregamos tras
  ver en partidas reales que dejábamos columnas enteras libres.
- **carrera**: distancia del peón propio más avanzado a la meta menos la del rival.

Los pesos no están puestos a mano: salen de mínimos cuadrados con regularización ridge sobre
partidas de self-play (`herramientas/entrenar.py`) y están en `data/pesos.npy`.

Intentamos mejorarlos y **no lo logramos** (sección 8): cuatro barridos de la regularización
quedaron dentro del ruido de su control, y unos pesos reajustados sobre 1 621 partidas reales
midieron 98-102. Se entregan los de self-play.

## 5. Precomputación (qué y cómo regenerarla)

`data/pesos.npy` — los seis pesos de la evaluación:

```bash
cd estudiantes/iacasitegano && python herramientas/entrenar.py
```

Juega self-play (y contra `random`, `montecarlo` y dos rivales propios de `herramientas/`) a
profundidad fija, guarda las características de cada jugada nuestra con el resultado final
(+1/−1) y ajusta por ridge. Escribe un candidato `data/candidato_<fecha>.npy`; nunca pisa el
campeón. ~2 h 37 min para 300 partidas a profundidad 5. No corre en la liga.

`data/libro.json` — jugada recomendada para las primeras 4 jugadas propias, en posiciones donde
self-play la vio ganar claramente más que la segunda opción:

```bash
cd estudiantes/iacasitegano && python herramientas/libro_apertura.py
```

`strategy.jugar()` lo consulta primero y revalida que la jugada sea legal; nunca es
obligatorio. El vigente es un libro mixto (blancas del candidato nuevo, negras del anterior),
elegido con 80 partidas en dos semillas (43-37, con 25-15 como blancas), por la asimetría de
color; el detalle quedó en el informe al promoverlo.

Los demás `.npy` de `data/` son checkpoints históricos que el runtime no carga.

## 6. Manejo del reloj

Reserva fija del 30 % que nunca se gasta pensando. Una jugada forzada no gasta reloj. Del
resto, cada jugada arranca con `1/16` de lo disponible, escalado entre 0.5× y 2.0× según qué
fracción de las jugadas legales son ataques (más ataques = posición más táctica). Dentro de ese
presupuesto manda el anytime de la sección 3. Sin tiempo, se juega una legal al azar.

Medido en las 200 partidas del bot tal como se entrega: reloj medio **14.3 s**, p95 16.7 s y
máximo **18.2 s de 30 s**, con cero timeouts y cero jugadas ilegales. El reparto `0.5/2.0/16` se
eligió midiendo tres configuraciones.

## 7. Resultados vs random y montecarlo

Contra `random`: la validación de entrega juega 2 partidas (una con cada color) y las ganamos.
No medimos una tanda grande contra `random` con este código: todo el esfuerzo de medición fue
contra `montecarlo`, que es el rival que de verdad discrimina.

Contra `montecarlo`, con el árbitro, 30 s por partida, alternando colores, 1 CPU por bot y
semillas distintas por tanda. Intervalos de Wilson al 95 %:

| Configuración | Partidas | Resultado | Victorias | IC 95 % |
|---|---:|---|---:|---|
| Baseline (antes del anytime) | 200 | 40-160 | 20.0 % | 15.0 – 26.1 % |
| Búsqueda anytime | 400 | 199-201 | 49.8 % | 44.9 – 54.6 % |
| Anytime + progreso parcial de raíz | 200 | 105-95 | 52.5 % | 45.6 – 59.3 % |
| La misma, otras dos tandas | 200 y 200 | 103-97 y 94-106 | 51.5 % y 47.0 % | 44.6 – 58.3 y 40.2 – 53.9 |
| **Bot tal como se entrega** | 200 | 95-105 | **47.5 %** | 40.7 – 54.4 % |

El salto de **20 % a ~50 %** viene de una sola cosa: que la búsqueda use el presupuesto de
reloj que ya tenía. Los intervalos de las tandas de 200 se solapan entre sí: **no afirmamos que
ninguna sea mejor que otra**; a ese tamaño el margen es de ±7 puntos.

Contra un `montecarlo` más fuerte preparado por nosotros (`noche_montecarlo_fuerte`), el bot
anytime midió **53-47** en 100 partidas (53.0 %; IC 43.3 – 62.5 %), sin Docker.

La última fila es el bot exactamente como se entrega (semillas 8600-8609): 435 puntos,
profundidad media 4.549, reloj máximo 18.2 s de 30 s y **cero timeouts, jugadas ilegales o
excepciones**; las 200 partidas terminaron por puntos. Por color, blancas 45-55 y negras 50-50.

Ese mismo código, byte por byte, es el que midió **105-95** en la tanda de semillas 8000-8009
(verificado comparando los archivos). Juntando las dos tandas: **200-200 en 400 partidas**, o
sea **50.0 %** (IC 95 %: 45.1 – 54.9 %). El intervalo incluye el 50 %, así que lo que se puede
afirmar es que el bot queda **a la par** de `montecarlo`, no por encima.

Lo que esto **no** dice: nunca jugamos contra los Tiers ni contra otros equipos (son bots
ocultos), así que no hay evidencia sobre el resultado de la liga.

## 8. Qué intentamos y no funcionó

Todo se midió con partidas completas bajo el árbitro o con una prueba offline determinista, y se
rechazó con datos. Las partidas son contra `montecarlo`.

| Intento | Qué se midió | Resultado |
|---|---|---|
| **Star2** (ventanas finas en nodos de azar) | 480 pruebas diferenciales contra expectiminimax exhaustivo; nodos a prof. 4-6; 200 partidas | Correcto pero con **0 % de ahorro de nodos** (conteos idénticos): la cota trivial `±ganancia` es ~15× el rango real de la eval y la ventana nunca corta. 103-97 |
| **Orden de jugadas** | nodos a prof. 4-6; 200 partidas | Ahorra 70/76/83 % de nodos pero cuesta ~8× por nodo (la prioridad se recalcula en cada nodo): **85-115** y menos profundidad (4.6 contra 5.2-5.5) |
| **Rollouts en la raíz** (Monte Carlo con probabilidad exacta) | 50 posiciones de final contra una búsqueda de referencia | Aciertan la mejor de 4 candidatas el **36 %** contra el **76 %** de la búsqueda; donde la búsqueda empata, 44 % contra 78 % |
| **Pesos reajustados con partidas reales** | 1 621 partidas, 160 234 posiciones, partición por partida; 200 partidas | Mejor exactitud de signo en el retenido, pero **98-102** (49.0 %; IC 42.2-55.9), y se especializarían en `montecarlo` |
| **Barrido de la regularización ridge** | 4 configuraciones × 100 partidas, cada una contra su control | 46-54 (45-55), 48-52 (47-53), 47-53 (41-59), 44-56 (51-49): ninguna gana |
| **`ventaja_carrera_exacta`** (tabla 1v1 como característica) | 40 partidas, sin Docker | **3-37**. El peso aprendido salió negativo, señal de alerta antes de medir. Muestra chica, pero el margen es enorme |
| **Tablas exactas de finales** (1v1, 2v1, 1v2) | simetría sobre 92 178 estados, cross-check con solver independiente; 80 partidas | **0 de 80 partidas llegaron a ese material**. No se entregan |
| **Quiescencia** en las hojas | A/B en partidas | Mismas victorias, menos puntos. Desactivada |
| **Arreglar la tabla de transposición** | 200 partidas | Correcto y necesario, pero **94-106**: sin mejora en el marcador |

**Dos bugs que encontramos midiendo, y que importan más que varias de esas técnicas:**

1. **El bot tiraba el 99 % de su reloj.** La regla que decidía si abrir la profundidad siguiente
   exigía tener 300× el tiempo de la anterior; como cada salto real cuesta 5-30×, se cortaba de
   inmediato. Medido: 7.4 ms por jugada de un presupuesto de 660-2 620 ms, profundidad media
   2.4. Eso explica de forma coherente por qué tres técnicas de libro (Star2, orden de jugadas,
   quiescencia) midieron neutro o peor: su beneficio es más profundidad por unidad de tiempo, y
   el bot se detenía antes por una razón ajena al costo de buscar.
2. **La tabla de transposición guardaba cotas como si fueran valores exactos.** El corte Star1
   devuelve una cota, no el valor, y se almacenaba marcada como exacta. Consecuencia medible: el
   valor de la raíz dependía del **orden de las jugadas**, algo imposible en alfa-beta. A
   profundidad 6 el bot se equivocaba en 1 de 35 posiciones con su orden normal y en 4 de 35 con
   las jugadas reordenadas. Se diagnosticó por eliminación (descartando primero la clave de la
   tabla) y se corrigió con la condición estándar: guardar solo si el valor cae estrictamente
   dentro de la ventana original del nodo.

## 9. Fuentes y uso de IA

**Fuentes.** Russell y Norvig, *Artificial Intelligence: A Modern Approach*, capítulo de juegos
(expectiminimax, poda alfa-beta). Ballard, B. W. (1983), «The \*-minimax search procedure for
trees containing chance nodes», *Artificial Intelligence* 21(3), para las podas Star1/Star2 en
nodos de azar. Sutton y Barto, *Reinforcement Learning: An Introduction*, para la idea de
ajustar una evaluación lineal con datos en vez de pesos fijos. La condición de exactitud de la
tabla de transposición es la estándar de los motores de ajedrez.

**Uso de agentes de IA.** El trabajo se hizo con dos agentes (Claude Code y Codex) coordinados
por el equipo, en worktrees separados del repositorio.

- **El equipo decidió**: qué hipótesis probar y en qué orden, el protocolo de medición (tamaño
  de muestra, semillas de desarrollo contra semillas de validación reservadas, alternar
  colores), los criterios de aceptación *antes* de medir, y qué se promueve. También corrigió
  el método cuando un agente midió mal: exigir 200 partidas en vez de 20 para el baseline
  destapó que la referencia de "30 %" con la que se habían rechazado dos técnicas era 20 %.
- **Los agentes hicieron**: implementación (numba, anytime, tablas de finales, arneses),
  pruebas diferenciales de corrección, ejecución de las tandas y análisis offline. Codex
  construyó el arnés paralelo con Docker y midió los baselines; Claude Code implementó el
  anytime, el laboratorio de evaluación y encontró los dos bugs de la sección 8.
- **Lo que no se delegó**: ninguna promoción sin revisión del equipo, y ningún resultado dado
  por bueno sin partidas completas bajo el árbitro.

Toda la estrategia es del equipo: no se copió código de otros equipos ni de internet, no se usan
redes neuronales, y el bot no accede a la red ni persiste nada entre partidas.
