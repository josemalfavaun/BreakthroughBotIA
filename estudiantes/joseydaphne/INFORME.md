# Informe: joseydaphne

## 1. Integrantes
Jose (000213398) y Daphne (000211927).

## 2. Idea en un párrafo
Expectiminimax exacto: para cada jugada usamos la probabilidad real del dado que ya nos da el
motor (`estado.siguiente(j)`), nunca una tirada muestreada. Buscamos con poda alfa-beta (y una
poda tipo Star1 en los nodos de azar) + tabla de transposición + profundización iterativa, hasta
donde alcance el reloj. La posición se mide con una evaluación lineal (puntos, avance, apoyo,
peones pasados, columnas abandonadas) cuyos pesos se ajustan con self-play, no a mano.

## 3. Búsqueda (algoritmo y por qué)
Expectiminimax con poda alfa-beta en los nodos de decisión y una poda Star1 en los de azar:
como cada ataque tiene como mucho 2 resultados (`[(p, gana), (1-p, pierde)]`), si ya evaluamos
`gana` y sabemos la cota real de `evaluar()` (recalculada en cada llamada, no un número inventado),
podemos saltarnos `pierde` cuando no puede cambiar la decisión. Verificamos la poda con pruebas
diferenciales contra una búsqueda exhaustiva sin podar: mismo valor en todos los casos probados.
Agregamos tabla de transposición (clave: `estado.clave` + profundidad) y profundización iterativa
que mide, no adivina, cuánto cuesta cada profundidad antes de arrancar la siguiente (con margen de
seguridad), para nunca arriesgar el reloj.

Medido en una posición típica de mitad de partida, sin podar: profundidad 2 ≈ 0.2 s, profundidad 3
≈ 6.3 s, profundidad 4 ≈ 89 s. Con la poda: profundidad 3 ≈ 0.27 s (23x más rápido), profundidad 4
≈ 1.7 s (53x más rápido). Con eso alcanzamos profundidad 3-4 de forma confiable con 1-2 s por
jugada, en vez de topar siempre en 2.

No usamos Star2 (bounds más finos por rama) ni quiescencia todavía: quedaron como siguiente paso
si la profundidad lograda no alcanza contra rivales más fuertes.

**Port a numba (`busqueda_numba.py`):** la misma búsqueda (expectiminimax + poda), pero compilada
con numba sobre el tablero crudo (`int8[81]`) en vez de objetos `Estado`, reusando las funciones
numba que ya trae `motor/nucleo.py`. Medido en la misma posición: profundidad 3 ~117x más rápido
que la versión Python podada, profundidad 4 ~200x — alcanzamos profundidad 5-6 en 0.1-0.7 s por
jugada, en vez de topar en 3-4. Verificado con la misma prueba diferencial de antes (contra la
búsqueda exhaustiva de referencia): mismo valor en todos los casos. Confirmamos además que numba
no truena si no puede escribir su caché en la carpeta de solo lectura de la liga (compila en
memoria, ~1.6-1.9 s, cómodo en los 10 s de `preparar`).

**Tabla de transposición:** un arreglo fijo de numpy (hash de mapeo directo, "siempre
reemplaza"), no un `numba.typed.Dict` (mismo patrón de arreglos que el resto del código, menos
riesgo de romper `cache=True`). Solo se guardan valores exactos (si la poda cortó el ciclo de
jugadas a medias, ese valor es una cota, no el real — mismo criterio que ya usábamos sin TT).
Validada con la misma prueba diferencial: 32 comparaciones, idénticas. Medida: profundidad 6
~32% más rápido, profundidad 7 ~47% más rápido que sin TT.

## 4. Función de evaluación
Lineal: `evaluar(estado, color) = PESOS @ features(estado, color)`. Las features (siempre "propio
menos rival"):
- **puntos**: diferencia de puntos anotados.
- **avance**: filas ya avanzadas, sumadas sobre todos los peones.
- **apoyo**: peones propios que cubren a otro peón propio (mismo campo que usa el motor para
  `prob_combate`).
- **pasado**: igual que avance, pero solo contando peones sin ningún rival en las tres columnas
  (la suya y las vecinas) que le faltan por recorrer. Es optimista a propósito: un solo defensor
  sin apoyo tampoco detiene de verdad (se le puede atacar en diagonal), así que no cuenta como
  bloqueo real, solo como aviso.
- **columnas_vacias**: columnas rivales completamente sin peones, menos las propias en la misma
  situación. La agregamos después de ver, jugando partidas reales, que nuestro bot dejaba columnas
  enteras sin nadie y un peón rival se paseaba sin oposición varias jugadas antes de que la
  búsqueda lo viera venir.

Los pesos NO están puestos a mano: se ajustan con `herramientas/entrenar.py` (self-play + mínimos
cuadrados con regularización ridge) y se guardan en `data/pesos.npy`. `strategy.preparar()` los
carga si el archivo existe.

## 5. Precomputación (qué y cómo regenerarla)
`data/pesos.npy`: los 5 pesos de la evaluación. Se regeneran con:

```bash
cd estudiantes/joseydaphne
python herramientas/entrenar.py
```

El script juega partidas de self-play (y, para variar las posiciones, también contra `random` y
`montecarlo`) con nuestra propia búsqueda a profundidad fija (barata, para poder generar muchas),
guarda el vector de features de cada jugada nuestra y el resultado final de esa partida (+1/-1), y
ajusta los pesos por mínimos cuadrados con una penalización L2 (ridge) para frenar pesos
inestables por colinealidad entre features (p. ej. `avance` y `pasado` están correlacionados).
No corre en la liga.

`data/libro.json`: jugada recomendada para las primeras 4 jugadas propias, en posiciones donde
self-play la vio ganar claramente más que la segunda opción (mínimo 10 muestras, ventaja mínima
8 puntos porcentuales — si no está claro, no entra). Se regenera con:

```bash
cd estudiantes/joseydaphne
python herramientas/libro_apertura.py
```

Al final, no antes (mismo motivo que los pesos: si la búsqueda o la eval todavía tuvieran un bug,
un libro construido antes lo congelaría). `strategy.jugar()` lo consulta primero; si la posición
no está, busca en vivo como siempre — el libro nunca es obligatorio ni se confía a ciegas (se
revalida que la jugada sea legal antes de jugarla).

**Tablas de finales: NO se hicieron, a propósito.** Probamos una posición de final real (pocos
peones, cerca de la meta): la búsqueda normal ya resuelve el valor EXACTO en profundidad 6, en
menos de 1 ms — con pocas piezas cerca de la meta la ramificación es tan chica que la búsqueda ya
actúa como tabla de finales perfecta. Construir una tabla dedicada no agregaría nada ahí.

**Antes de aceptar un `data/pesos.npy` nuevo**, `herramientas/liga_interna.py` es el gate:
juega el bot actual contra `random` y `montecarlo`, y si se le da `--checkpoint`, también
contra la versión anterior de los pesos, reportando victorias y puntos de cada lado. Nació de
que "se ve mejor" no fue suficiente dos veces esta sesión (ver 8b) — todo cambio se mide con
partidas completas, no se acepta a ojo.

## 6. Manejo del reloj
Reserva fija del 30 % del reloj (igual que el bot de referencia). Una jugada forzada (una sola
legal) se juega sin pensar, sin gastar nada de reloj. Del resto, cada jugada arranca con un
presupuesto base de `1/20` de lo disponible, escalado entre 0.7x y 2.3x según qué fracción de las
jugadas legales son ataques — una posición con muchos ataques disponibles es más táctica y vale
más la pena pensarla; una tranquila gasta menos de lo normal, dejando ese tiempo disponible (vía
`tiempo_restante`) para cuando de verdad importe. Dentro de ese presupuesto, la profundización
iterativa solo empieza una profundidad nueva si, por el factor de crecimiento medido en la
anterior **con un piso pesimista** (`FACTOR_PESIMISTA = 150`: nunca asumimos que el próximo salto
será más barato que eso, después de que un salto real nos costó una partida por reloj — ver
sección 8b), le alcanza el tiempo con margen de seguridad. Si no queda tiempo de pensar, juega al
azar entre las legales.

## 7. Resultados vs random y montecarlo
Con Docker real (condiciones oficiales), contra `random` ganamos siempre. Contra `montecarlo`,
en liga interna de 20 partidas (semilla fija, ambos colores):

| Configuración | Resultado |
|---|---|
| Pesos a mano (primer intento) | 0-20 |
| Pesos a mano (con feature `columnas_vacias`) | 0-20 |
| Pesos entrenados (60 partidas self-play) | 0-20 |
| Pesos entrenados (300 partidas, rivales variados, ridge) | 0-20 |
| Búsqueda numba (profundidad 5-6), mismos pesos entrenados | 1-19 (primera victoria) |
| + tabla de transposición + pesos reentrenados con self-play numba (profundidad 4) | **4-40 en total (dos semillas, ~10%)** |

El salto real no fue ajustar pesos: fue profundidad. `montecarlo`, pese a tirar el dado en vez de
usar la probabilidad exacta, compensa con volumen de muestreo (miles de simulaciones por jugada
gracias a numba) y efectivamente "ve" hasta el final de la partida en cada simulación. Una eval
estática a profundidad 3-4, por bien calibrada que esté, no puede ver una carrera de peón que se
resuelve en 10-20+ jugadas. Portar la búsqueda a numba (profundidad 5-7 real) fue lo que empezó a
cerrar la brecha; TT + pesos reentrenados con self-play de la propia búsqueda numba la siguieron
cerrando un poco más. Los marcadores también son mucho más parejos ahora (1-3, 2-3 en vez de 0-3
casi siempre), y una de las victorias fue porque montecarlo se quedó sin reloj en una partida de
149 jugadas. `montecarlo` sigue ganando la mayoría. Pendiente si se sigue: poda Star2 (bounds más
finos que Star1), orden de jugadas para que la poda alfa-beta corte más, y self-play más profundo
ahora que generar partidas también es barato.

## 8b. Refinamiento incremental: quiescencia, orden de jugadas, y un bug de reloj real
Dos técnicas de libro, probadas con A/B real contra montecarlo (no solo validadas por
corrección) y las dos sin mejora clara:
- **Quiescencia** (seguir ataques encadenados en la hoja, con "stand pat"): implementada y
  validada (comparada contra una referencia en Python con la misma poda, mismos valores). En
  partidas reales, mismo número de victorias pero MENOS puntos totales — cada hoja de la
  búsqueda principal ahora dispara un sub-árbol completo, y eso resta profundidad neta de lo
  que gana en precisión. Desactivada por default (`QUIESCENCIA_MAX = 0`).
- **Orden de jugadas** (probar primero la mejor jugada de la profundidad anterior): no cambia
  el valor nunca (propiedad de alfa-beta), sin costo medible — pero al probarlo en partidas
  reales **perdimos una partida por reloj**: un salto de profundidad costó ~123x en vez de los
  ~15-30x "típicos" (la posición se volvió táctica de golpe). El estimador de profundización
  iterativa solo miraba la última transición medida. Arreglado con un piso pesimista
  (`FACTOR_PESIMISTA = 150`, por arriba del peor caso visto): nunca se asume que el próximo
  salto será más barato que eso. Confirmado sin más timeouts en 40 partidas tras el arreglo.
  Costo: el conteo de victorias volvió a los niveles de antes del orden de jugadas — la
  seguridad resta algo de profundidad en el caso típico, y es el trade correcto (perder por
  reloj es categóricamente peor que buscar un poco menos profundo).

La conclusión de esta ronda no es "estas técnicas no sirven": es que **medir con A/B real
contra el rival, no solo validar que el valor es correcto, encontró un bug de reloj genuino**
que de otra forma hubiera llegado a la liga oficial sin que lo notáramos.

## 8. Qué intentamos y no funcionó
- **Peones pasados detectados solo por presencia rival en el camino:** nuestro primer intento de
  `pasado` marcaba un peón como bloqueado si había CUALQUIER peón rival en su camino. No sirve:
  en Breakthrough se puede atacar en diagonal una casilla ocupada, así que un solo defensor sin
  apoyo no bloquea nada de verdad. Lo dejamos (es útil como aviso temprano) pero agregamos
  `columnas_vacias`, que no depende de dónde esté el rival.
- **Perseguir profundidad sin podar:** antes de la poda, medimos que profundidad 3 ya costaba 6.3 s
  y profundidad 4 cerca de 90 s en una posición típica — profundizar sin podar no era viable con el
  factor de ramificación de este juego. La poda (Star1 + alfa-beta) fue la mejora que de verdad
  compró profundidad.
- **Pesos a mano, dos veces:** los pusimos a ojo en dos iteraciones distintas (incluyendo subir el
  peso de "pasado" tras el primer diagnóstico) y las dos veces perdimos 0-20 contra `montecarlo`
  en partidas reales. Primera corrida de entrenamiento (60 partidas solo contra uno mismo) tampoco
  alcanzó; ver sección 7.

## 9. Fuentes y uso de IA
Russell y Norvig, *Artificial Intelligence: A Modern Approach*, capítulo de juegos (expectiminimax,
poda alfa-beta). Ballard, B. W. (1983), «The *-minimax search procedure for trees containing chance
nodes», Artificial Intelligence 21(3) — base de la poda Star1 usada en los nodos de azar. Sutton y
Barto, *Reinforcement Learning: An Introduction*, para el enfoque de ajustar una función de
evaluación lineal con datos de self-play en vez de pesos fijos. Escrito por el equipo con ayuda de
Claude Code: diseño de la arquitectura, implementación, pruebas de corrección de la poda (contra
una búsqueda exhaustiva de referencia) y diagnóstico de los resultados fueron iterativos,
verificados jugando partidas reales en cada paso, no solo pedidos de una vez.
