# Informe: iacasitegano

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
- **carrera**: distancia del peón propio más avanzado a la meta, menos la distancia del peón rival
  más avanzado. Un peso negativo convierte una distancia propia menor (mejor) en una contribución
  positiva; si un bando no tiene peones, su distancia se toma como 9.

Los pesos NO están puestos a mano: se ajustan con `herramientas/entrenar.py` (self-play + mínimos
cuadrados con regularización ridge) y se guardan en `data/pesos.npy`. `strategy.preparar()` los
carga si el archivo existe.

## 5. Precomputación (qué y cómo regenerarla)
`data/pesos.npy`: los 6 pesos de la evaluación. Se regeneran con:

```bash
cd estudiantes/iacasitegano
python herramientas/entrenar.py
```

La corrida ampliada usa profundidad 5, 100 partidas por semilla y las semillas 1234, 5678 y
9012 (300 partidas en total). El libro usa 100 partidas por cada una de las semillas 4242, 5151
y 6262 (300 en total), acumulando las muestras antes de filtrar por claridad.

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
cd estudiantes/iacasitegano
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
presupuesto base de `1/16` de lo disponible, escalado entre 0.5x y 2.0x según qué fracción de las
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

En la corrida de profundidad 5, el bot ganó `40-0` a `random`, perdió `2-38` contra `montecarlo`
y quedó `21-19` contra el checkpoint de profundidad 4 (puntos `72-77`); por eso el checkpoint
4 se conserva como referencia de profundidad y no se promociona la profundidad 5 por sí sola.
Ese `2-38` no fue una tanda de derrotas por timeout: `liga_interna.py` usa para nuestro bot un
jugador numba de profundidad fija que ignora `strategy.jugar()` y no aplica el reloj de 30 s ni
penaliza jugadas lentas. Fue, por tanto, una comparación offline limpia con los pesos anteriores
sin `carrera`. El `6-14` posterior no es contradictorio: corresponde al bot completo, con la
feature nueva y el reparto de reloj tuneado `0.5/2.0/16`, medido con `./torneo --sin-docker`.

La nueva feature `carrera` se entrenó con 150 partidas y ridge. En 20 partidas a profundidad 5,
la versión nueva ganó `15-5` a los pesos anteriores sin `carrera` (puntos `49-28`), `7-13` a
`montecarlo` (puntos `38-49`) y `16-4` al checkpoint4 (puntos `54-30`). Contra `random` ganó
`20-0` (puntos `60-1`).

Para ajustar el reparto de tiempo medimos tres configuraciones en 20 partidas cada una contra
`montecarlo` (partidas completas, `--sin-docker` porque Docker no estaba disponible):

| PESO_MINIMO / PESO_MAXIMO / REPARTO | Resultado iacasitegano |
|---|---:|
| 0.7 / 2.3 / 20 (baseline) | 3-17 |
| 0.5 / 2.0 / 16 | **6-14** |
| 0.8 / 1.8 / 24 | 4-16 |

Se conserva `0.5/2.0/16`, que fue la configuración con más victorias reales.

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


## Self-play ampliado: decisión de pesos

Paso 3 — decisión tras 40 partidas por comparación
- nuevos vs antes: 27-13 victorias; puntos 96-66
- nuevos vs checkpoint4: 32-8 victorias; puntos 105-70
- márgenes directos: antes=14, checkpoint4=24
- elegido: pesos_nuevos_selfplay_300
- pesos nuevos preservados en data/pesos_selfplay_300.npy

Resultados completos: `paso2_vs_antes.log` y `paso2_vs_checkpoint4.log`.


## Validación real de pesos self-play 300 contra Monte Carlo

Método: `./torneo jugar iacasitegano montecarlo --sin-docker --partidas 40 --semilla 2029 -v`, usando `strategy.jugar()` y el reparto de reloj `PESO_MINIMO=0.5`, `PESO_MAXIMO=2.0`, `REPARTO=16`.

Resultado: Monte Carlo 37 - 3 iacasitegano (3/40 = 7.5%).

Criterio fijado antes de la corrida: al menos 16 victorias de 40 para superar claramente el 6-14 histórico (30%); en otro caso se restaura la versión anterior.

Decisión: **restaurar pesos_antes_selfplay_300**.

Nota de protocolo: `herramientas/liga_interna.py` ejecuta una búsqueda numba de profundidad fija y su jugador ignora el reloj; sirve para comparar valores/pesos offline. `strategy.jugar()` sí aplica el reparto de reloj y es el bot real que debe usarse para comparar contra el 6-14.


## Fase 2 limpia: orden de jugadas con el campeón correcto

La prueba anterior `36-4` queda descartada para juzgar el ordenamiento: se ejecutó con los pesos self-play 300, posteriormente rechazados.

Esta prueba usa el campeón restaurado `pesos_antes_selfplay_300`, ordenamiento de jugadas activado, `strategy.jugar()`, reparto de reloj `0.5/2.0/16`, 40 partidas reales, semilla 2030 y `--sin-docker`.

Resultado: Monte Carlo 31 - 9 iacasitegano (9/40 = 22.5%), contra la referencia histórica de iacasitegano 6-14 (30%).

**Decisión: orden de jugadas rechazado, 22.5% vs 30% baseline.** Se desactiva en el código activo (`ORDENAMIENTO_JUGADAS = False`); la implementación queda conservada solo como experimento revisable.

## Oponentes simples para diversificar self-play

`herramientas/entrenar.py` incorpora dos rivales sencillos, únicamente para generar posiciones
con estilos distintos:

- `rival_voraz.py`: toma una anotación inmediata o un ataque con probabilidad máxima (`0.80`) si existe; si no, elige una jugada legal al azar.
- `rival_minimax2.py`: expectiminimax puro de profundidad fija 2, sin Star1, tabla de transposición ni numba.

La mezcla queda en 50% uno mismo, 20% `random`, 20% `montecarlo`, 5% `voraz` y 5% `minimax2`.
El entrenamiento guarda siempre `data/candidato_<timestamp>.npy`; nunca sobrescribe
`data/pesos.npy`. Ningún candidato se promueve sin partidas reales contra `montecarlo` y el
campeón actual. Los rivales y la nueva mezcla están implementados y verificados por smoke test.


## Registro de promoción: candidato 20261024

### Qué cambió

Se promovió `data/candidato_20261024_042150.npy` a `data/pesos.npy`. El candidato modifica los
seis pesos de la evaluación lineal; la búsqueda, el manejo del reloj, el libro de apertura y el
código de la estrategia no cambiaron en esta promoción.

Pesos registrados por el entrenamiento (`antes -> entrenados`):

| Feature | Antes | Candidato |
|---|---:|---:|
| `puntos` | 0.52 | 0.5896 |
| `avance` | -0.01 | 0.0110 |
| `apoyo` | 0.01 | 0.0143 |
| `pasado` | 0.01 | 0.0046 |
| `columnas_vacias` | 0.08 | 0.0160 |
| `carrera` | -0.15 | -0.1386 |

### Log de self-play

El contenedor `iacasitegano-entrenar-20261023` ejecutó `python herramientas/entrenar.py` con
profundidad propia 5, 300 partidas totales y las semillas `1234`, `5678` y `9012` (100 partidas
por semilla). La mezcla de oponentes fue 50% uno mismo, 20% `random`, 20% `montecarlo`, 5%
`voraz` y 5% `minimax2`. El log reportó 4,785, 4,717 y 4,616 posiciones por tanda:
14,118 posiciones en total. El ajuste fue ridge con `lambda=1.0` y guardó el candidato en
`data/candidato_20261024_042150.npy`; durante el entrenamiento `data/pesos.npy` no se modificó.

### Evaluación oficial candidato-vs-campeón

Se ejecutó el bot real bajo el árbitro y Docker, alternando colores, con 40 partidas y semilla
2026:

```bash
./torneo jugar iacasitegano_candidato iacasitegano --partidas 40 --semilla 2026
```

Resultado: el candidato ganó `22-18` y sumó `87-72` puntos. Por color, el candidato quedó
`9-11` como blancas y `13-7` como negras. No hubo errores, jugadas ilegales ni timeouts; el
reloj máximo fue 3.54 s para el candidato y 3.58 s para el campeón, frente al límite de 30 s.
La promoción se hizo después de esta evaluación.


## Evaluación del libro regenerado y mezcla por color (2026-10-24)

Se regeneró el libro con los pesos promovidos usando el protocolo de `herramientas/libro_apertura.py`:
300 partidas de self-play, semillas `4242`, `5151` y `6262`, profundidad 4, cuatro primeras
jugadas propias, mínimo 10 muestras y ventaja mínima de 0.08. Produjo 8 entradas. El libro previo,
respaldado antes de regenerar, también tenía 8.

La comparación aisló el libro: las variantes tenían el mismo código y los mismos pesos
(`pesos.npy`, SHA-256 `d5cc25eefa365de7f912fc65615576e8fbdb8c646bff8da96283bedeb570064f`), y solo
cambiaba `data/libro.json`. Se usó `./torneo jugar ... --partidas 40` con Docker y colores
alternados:

| Semilla | Variante nueva | Actual | Puntos nueva–actual | Nueva como blancas | Nueva como negras |
|---:|---:|---:|---:|---:|---:|
| 2031 | 25–15 | 15–25 | 92–77 | 17–3 | 8–12 |
| 2032 | 16–24 | 24–16 | 78–89 | 9–11 | 7–13 |
| **Total, 80 partidas** | **41–39** | **39–41** | **170–166** | **26–14** | **15–25** |

No hubo errores ni timeouts. El reloj máximo fue 2.03 s para la variante nueva y 1.95 s para la
actual en la semilla 2031; 4.51 s y 3.87 s, respectivamente, en la 2032. El resultado combinado
casi empata y la diferencia por color se repitió: el libro nuevo rinde mejor como blancas y peor
como negras. Visores: [semilla 2031](../../resultados/2026-10-24_18-16-37/index.html) y
[semilla 2032](../../resultados/2026-10-24_18-27-37/index.html).

### Prueba de libro mixto

El formato permite seleccionar entradas por color: la clave Zobrist incluye turno, y el par
`[origen, destino]` también lo identifica porque Blancas avanzan a un índice mayor y Negras a uno
menor (`fila * 9 + columna`). `herramientas/mezclar_libros_eval.py` construye una variante con las
4 entradas blancas del libro nuevo y las entradas negras del libro actual; el total quedó en 8.
Esta mezcla se evaluó en 40 partidas oficiales con Docker, colores alternados y semilla `2033`,
contra el libro actual completo:

| Variante | Victorias | Puntos | Blancas | Negras | Reloj máximo |
|---|---:|---:|---:|---:|---:|
| Mixto | 21 | 80 | 12–8 | 9–11 | 2.90 s |
| Libro actual | 19 | 75 | 11–9 | 8–12 | 2.81 s |

La tanda de confirmación repitió el protocolo con semilla `2034`:

| Semilla | Variante | Victorias | Puntos | Blancas | Negras | Reloj máximo |
|---:|---|---:|---:|---:|---:|---:|
| 2034 | Mixto | 22 | 90 | 13–7 | 9–11 | 3.55 s |
| 2034 | Libro actual | 18 | 81 | 11–9 | 7–13 | 3.40 s |

No hubo errores ni timeouts en ninguna tanda. **Agregado de 80 partidas mixto-vs-actual:** el
mixto ganó `43–37` y anotó `170–156` puntos. Por color, el mixto quedó `25–15` como blancas y
`18–22` como negras. Ganó ambas tandas (21–19 y 22–18), cumpliendo el criterio de evidencia. Tras
la confirmación del usuario, el libro mixto se promovió a `data/libro.json`. El JSON del libro
mixto se conservó en el historial de Git; los libros de evaluación permanecen respaldados fuera
del equipo.

Visores: [mixto, semilla 2033](../../resultados/2026-10-24_18-59-07/index.html) y
[mixto, semilla 2034](../../resultados/2026-10-24_19-16-17/index.html).
