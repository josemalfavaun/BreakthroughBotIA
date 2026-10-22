# Conversación: BreakthroughBotIA — qué hacer, estrategias, techo y entrenamiento

Notas completas de la conversación (21 oct 2026). No recorta secciones, tablas ni advertencias de las respuestas.

---

## 1. Qué es el proyecto y qué hay que hacer

Este repo es la plantilla del **torneo de IA O26**: hay que programar, **en equipo de 2**, un bot que juegue *Breakthrough de combate* (peones en 9×9, ataques con dado). El motor, el árbitro y Docker **ya están hechos**. Lo único que debes escribir vive en `estudiantes/<tu_equipo>/`.

Ahora **no hay carpeta de equipo**. Solo existen los bots de referencia `random` y `montecarlo`. Eso significa que el trabajo de ustedes **aún no empieza**.

Estado de *este* workspace al momento de la conversación:

- Rama `main` al día con `origin`.
- Solo `estudiantes/random/` y `estudiantes/montecarlo/`.
- Fechas de entrega **aún no definidas**.
- El primer paso concreto: copiar `montecarlo` a `estudiantes/<nombre_equipo>/`, llenar `equipo.toml` y jugar contra `montecarlo`.

### El juego en un minuto

Cada bando tiene 18 peones. Blancas empiezan en las filas 1 y 2; Negras, en las 8 y 9. Por turno mueves **un peón una casilla hacia adelante**: recto a una casilla vacía, o en diagonal a una casilla vacía o atacando a un peón rival. Nunca hacia atrás ni de lado, y no se ataca recto.

**Combate.** Atacar es tirar un dado. Cada peón tiene un **apoyo**: cuántos peones propios tiene en sus dos diagonales de atrás (0, 1 o 2). La probabilidad de ganar el ataque es

```text
p = 0.5 + 0.15 × (apoyo del atacante − apoyo del defensor)
```

(acotada entre 0.2 y 0.9; con apoyos de 0 a 2 el resultado siempre cae entre 0.2 y 0.8).

| Apoyo atacante − apoyo defensor | −2 | −1 | 0 | +1 | +2 |
|---|---|---|---|---|---|
| p | 0.20 | 0.35 | 0.50 | 0.65 | 0.80 |

Si ganas, el defensor sale del tablero y tu peón ocupa su casilla. Si pierdes, sale **tu** peón.

**Puntos.** Un peón que llega a la última fila rival anota 1 punto y sale del tablero. Gana quien llega a **3 puntos** o deja al rival **sin jugadas**. No hay empates.

Reglas completas: `docs/reglas.md`.

### Qué hay que hacer, en orden

#### 1. Setup (si aún no está listo)

- Repo **privado** creado con *Use this template* (no fork para trabajar; el fork es solo el día de entrega).
- Invitar al compañero y al profesor (`uumami`).
- Docker (o Codespaces). Docker Desktop debe estar corriendo para que `./torneo` use los mismos límites que la liga.

#### 2. Crear su bot

```bash
cp -r estudiantes/montecarlo estudiantes/<tu_equipo>
```

Nombre de carpeta: 3–30 caracteres, minúsculas, dígitos y `_`. No puede ser `random`, `montecarlo`, `humano`, ni empezar con `tier_` o `_`.

Editar `estudiantes/<tu_equipo>/equipo.toml`: nombre igual a la carpeta y **exactamente 2 integrantes** con clave única real.

#### 3. Programar la estrategia

En `strategy.py` solo importan dos funciones:

- `preparar(config)` — una vez por partida (10 s, fuera del reloj).
- `jugar(estado, tiempo_restante) -> Jugada` — cada turno (reloj de **30 s** por partida).

`montecarlo` es el punto de partida: Monte Carlo plano (simula partidas al azar y elige el mejor promedio). Los comentarios `AQUÍ PUEDES MEJORAR` marcan dónde hay margen: tiempo por jugada, cómo tratar el azar de los ataques, calidad de las simulaciones, y cómo elegir (no solo el promedio).

Algoritmos que el curso espera que investiguen: minimax, alfa-beta, profundización iterativa, tablas de transposición, expectiminimax, MCTS/UCT, etc. **No hay un algoritmo obligatorio**; gana quien mida bien.

Probar:

```bash
./torneo jugar <tu_equipo> montecarlo
./torneo mini <tu_equipo>
./torneo validar <tu_equipo>
```

Mientras programan: `--partidas 1` o `2`. Para comparar versiones de verdad: `--partidas 10` o más (con pocas partidas gana el dado).

Tu carpeta:

```text
estudiantes/<tu_equipo>/
├── equipo.toml        nombre del equipo + los 2 integrantes con su clave única
├── strategy.py        tu bot: lo único que se ejecuta (puede importar otros .py de tu carpeta)
├── INFORME.md         obligatorio: qué hace tu bot y por qué (9 secciones)
├── requirements.txt   opcional: librerías extra
├── data/              lo que precomputes (tablas, pesos, aperturas); en la liga es de solo lectura
└── herramientas/      el código con el que generaste data/ (no se ejecuta en la liga)
```

Todo lo demás del repo (motor, árbitro, Docker) vive en `sistema/`. No necesitas abrirlo.

**Entrada y salida**

```python
from motor import Estado, Jugada

def preparar(config):
    """Una vez por partida, antes de empezar (10 s, fuera del reloj).
    config.color ("blancas" o "negras"), config.carpeta_datos (tu data/),
    config.semilla (para tu propio azar), config.reloj_s (30)."""

def jugar(estado: Estado, tiempo_restante: float) -> Jugada:
    """Te toca. Regresa una jugada de estado.jugadas()."""
```

- **Entrada:** el `estado` completo (tablero, puntos y turno) y los segundos que te quedan de reloj. Cuando se llama `jugar`, siempre es tu turno: `estado.turno == config.color`. No necesitas recordar nada entre turnos.
- **Salida:** una jugada legal (una `Jugada` de `estado.jugadas()` o su texto, como `"e2-e3"`).
- **Lo de en medio es tuyo:** búsqueda, evaluación, manejo del azar y del reloj, precomputación. El motor te ayuda con `estado.jugadas()`, `estado.siguiente(j)` (resultados posibles con su probabilidad), `estado.prob_ataque(j)` y `simular_al_azar(...)`.

#### 4. Informe obligatorio

`INFORME.md`, 2–4 páginas, **9 secciones numeradas**:

1. Integrantes
2. Idea en un párrafo
3. Búsqueda (algoritmo y por qué)
4. Función de evaluación
5. Precomputación (`data/` y cómo regenerarla)
6. Manejo del reloj
7. Resultados vs `random` y `montecarlo` (números reales)
8. Qué intentaron y no funcionó
9. Fuentes y uso de IA

Sin informe completo o `equipo.toml` válido, **el PR no se acepta y la calificación es 0**. Copiar el informe de `montecarlo` falla en la entrega.

#### 5. Entrega (fechas: el profesor las anuncia)

La entrega tiene **dos momentos**:

1. **Antes de la hora límite:** registras el SHA del último commit de tu repo privado. Tu código sigue privado.
2. **En las 24 horas siguientes:** haces un *fork* del repo del torneo, copias tu carpeta **exactamente** como estaba en ese SHA y abres un *pull request* (PR).

Pasos:

1. `./torneo validar <tu_equipo> --entrega` debe pasar.
2. Registrar el **SHA** del último commit **antes** de la hora límite.
3. En las 24 h siguientes: fork del repo del curso, copiar **solo** `estudiantes/<tu_equipo>/` tal cual ese SHA, abrir PR. El PR **no puede tocar nada fuera de esa carpeta**.

Si el PR cambia README, `docs/`, `sistema/`, workflows, carpetas de otros equipos o archivos de la raíz, la revisión `revisar-entrega` falla.

### Cómo se califica

Liga todos contra todos: 4 partidas vs cada rival (2 colores × 2 juegos de dados). Victoria = 1 punto. **Ganarle** a un bot de referencia = terminar con **estrictamente más puntos** que él (empatar no cuenta).

| Mejor rival al que le ganan | Calificación |
|---|---|
| ninguno | 0 |
| `random` | 1 |
| `montecarlo` | 3 |
| Tier 1 | 5 |
| Tier 2 | 6 |
| Tier 3 | 7 |
| Tier 4 | 8.5 |
| Tier 5 | 10 |
| **1º, 2º o 3º entre alumnos** | **10** |

Los tiers 1–5 aparecen el día de la liga; su código no se publica.

Desempates (solo ordenan la tabla; no cambian “ganarle”):

1. Puntos entre los empatados.
2. Sonneborn-Berger (calidad de victorias).
3. Peones anotados.
4. Sorteo con la semilla de la liga.

### Límites y trampas (pierdes la partida o el torneo)

| Recurso | Límite |
|---|---|
| Reloj | 30 s por partida, estilo ajedrez: solo corre en tu turno |
| `preparar` (incluye importar `strategy.py`) | 10 s, fuera del reloj |
| CPU | 1 núcleo |
| Memoria | 1024 MB |
| Tu carpeta | 100 MB en total y 50 MB por archivo |
| Lo que imprimes (`print`) | se guarda hasta 64 KB por partida |
| Librerías de `requirements.txt` | 300 MB instalados |

Por partida: Reloj, jugada ilegal, excepción, memoria o `preparar` lento → **pierdes esa partida** y sigues en la liga.

**Prohibido (0 para todo el equipo):** redes neuronales, ofuscación, código nativo propio (C/Cython/`.so`; numba sí), salir del aislamiento, adivinar dados, copiar o coordinarse con otro equipo.

Sí se vale: búsqueda, evaluación, tablas, modelos que no sean red neuronal, precomputar en `data/`, numpy/scipy/numba, otras libs en `requirements.txt` (con versión fija y fuera de la lista negra). Offline, para generar `data/`: absolutamente todo.

Tu pull request solo puede cambiar archivos dentro de `estudiantes/<tu_equipo>/`.

### Los participantes de referencia

- `random` elige una jugada legal al azar.
- `montecarlo` hace Monte Carlo plano: para cada jugada simula partidas al azar y elige la de mejor promedio. Es el punto de partida; sus comentarios marcan dónde puedes mejorar.
- **Tier 1 a Tier 5:** bots más fuertes. Su código no se publica.

### API del motor (lo que usas en el bot)

| Qué | Para qué |
|---|---|
| `estado.jugadas()` | Lista de jugadas legales del jugador en turno |
| `estado.siguiente(j)` | `[(1.0, nuevo)]` sin ataque; `[(p, si_gana), (1 − p, si_pierde)]` con ataque |
| `estado.aplicar(j)` | Estado después de `j`. En un ataque: `aplicar(j, gana_ataque=True)` |
| `estado.prob_ataque(j)` | `p` si `j` es ataque; `1.0` si no |
| `estado.es_ataque(j)` | `True` si ataca a un peón rival |
| `estado.turno` | `"blancas"` o `"negras"` |
| `estado.puntos` | Por ejemplo `{"blancas": 1, "negras": 0}` |
| `estado.piezas(color)` | Casillas de los peones de ese color |
| `estado.terminado()`, `estado.ganador()` | Si ya hay ganador, y cuál |
| `estado.clave` | Número de 64 bits (Zobrist): llave para tabla de transposición |
| `simular_al_azar(estado, n, semilla, para)` | Fracción de `n` partidas al azar que gana `para` (numba) |
| `prob_combate(apoyo_atacante, apoyo_defensor)` | La fórmula de `p` |
| `reportar(**datos)` | Para el visor y `-v`. Ejemplo: `reportar(prof=4, nodos=12000, eval=0.62)` |

`jugar` puede regresar una `Jugada` o su texto (`"e4-f5"`).

### Comandos útiles

```bash
./torneo jugar los_alfa_beta montecarlo
./torneo jugar los_alfa_beta montecarlo --partidas 10
./torneo jugar los_alfa_beta random --semilla 7 -v
./torneo mini los_alfa_beta
./torneo validar los_alfa_beta
./torneo validar los_alfa_beta --entrega
./torneo liga los_alfa_beta random montecarlo --juegos-dados 3
./torneo jugar los_alfa_beta montecarlo --sin-docker
```

`--sin-docker` no tiene límites: sirve para depurar, **no** para medir tiempos. Lo que cuenta es Docker o GitHub.

Guías: `README.md`, `docs/empezar.md`, `docs/probar.md`, `docs/entregar.md`, `docs/calificacion.md`, `docs/reglas.md`, `docs/avanzado.md`, `docs/preguntas.md`.

---

## 2. Estrategias considerando todo el proyecto

La geometría del juego, el azar de los combates y el reloj de 30 s (1 núcleo, ~40 jugadas propias) deciden qué funciona. `montecarlo` ya te dice dónde pierde: reparte tiempo igual, **tira el dado** en vez de tomar esperanza, evalúa con partidas al azar y elige solo el promedio.

### Qué hace especial a este juego

- **No hay empate** y se gana con **3 puntos** o dejando al rival sin jugadas. Una pieza que anota **sale**: material y carrera tiran en sentidos opuestos.
- Solo se avanza. Un peón adelantado no vuelve; el “peón pasado” (camino libre o poco interceptable en su columna y las dos vecinas) vale mucho.
- El combate es un **nodo de azar** con `p` conocida (`estado.siguiente(j)` ya te da las dos ramas). Tratar eso como un dado que tiras una vez es el error de `montecarlo`.
- **Apoyo** (diagonales de atrás, 0–2) mueve `p` de 0.20 a 0.80. Atacar mal apoyado es casi un suicidio; atacar +2 vs 0 es un negocio.
- No se ataca de frente: un peón **bloquea el archivo**. Formar una pared y romper la ajena importa más que “comer por comer”.
- Alta ramificación al inicio (hasta ~54), baja al final. El mismo buscador no debe gastar igual en apertura y en 2–2.

Por eso el núcleo fuerte no es “más simulaciones al azar”, sino **expectiminimax (o MCTS con esperanza) + una evaluación que entienda carrera, apoyo y bloqueo**.

### Estrategia recomendada (camino único)

Una pila, no cinco bots distintos. Cada capa ya debería ganarle a `random`; a partir de la 2 deberías pelear con `montecarlo`; la 3–4 es territorio de tiers.

#### Capa 0 — Táctica barata (obligatoria, 20 líneas)

Antes de pensar:

1. Si alguna jugada **gana sí o sí** (las dos ramas de `siguiente` te dan `ganador() == tu color`), júgala. `montecarlo` ya lo hace.
2. Si el rival anota en el siguiente turno con probabilidad 1 (avance a meta vacío, o ataque que anota con `p` alta), **para ese avance** o mata al peón.
3. Si tú anotas con probabilidad 1, hazlo (salvo que el rival anote antes y tú no llegues a 3).

Esto solo no gana la liga, pero evita derrotas ridículas.

#### Capa 1 — Función de evaluación (lo que más te separa de `montecarlo`)

Evalúa **siempre desde tu color**. Escala tipo “probabilidad de ganar”, no puntos de ajedrez sueltos.

Señales, de más a menos importantes:

| Señal | Por qué |
|---|---|
| Puntos (tú / rival), sobre todo 2 vs 1 | El juego es una carrera a 3 |
| Distancia a anotar del peón más avanzado | Un peón en fila 7–8 (blancas) vale una pieza |
| Suma de avances (PST por fila, más peso cerca de la meta) | Breakthrough clásico |
| Peones con camino relativamente libre | Solo avanzan; interceptar es caro |
| Apoyo medio / peones con apoyo 2 | Combates futuros |
| Ataques disponibles: `p * valor − (1−p) * valor` | No atacar a 0.20 “porque se puede” |
| Peones bloqueados (0 jugadas) | Victoria por ahogo existe |
| Material | Importa, pero **menos** que anotar; perder un peón para anotar suele ser bueno |
| Amenaza inmediata del rival (`p` de que anote ya) | Urgencia |

Empieza con pesos a mano. Luego, **offline**, ajusta un modelo **lineal o logístico** con partidas de autojuego y guarda `pesos.npy` en `data/` (redes neuronales están prohibidas en la liga; lineal sí).

Hojas del árbol: si la posición terminó, 1 o 0; si no, esta eval.

#### Capa 2 — Expectiminimax de 1–2 ply (ya debería superar a `montecarlo`)

Para cada jugada legal:

```text
valor(j) = Σ p * eval(hijo)     # estado.siguiente(j)
```

Elige el máximo. En ataques **no samples**: usas `p` real.

A 1 ply, con eval decente, dejas de desperdiciar muestras en jugadas basura y de “ganar” combates imposibles en la simulación. A 2 ply (tú + rival) ves contraataques.

Ordena jugadas: anotar, ataques con `p ≥ 0.65`, avances de peones adelantados, el resto. Eso acelera cualquier poda después.

#### Capa 3 — Búsqueda seria (territorio Tier 2–4)

**Expectiminimax + profundización iterativa + tabla de transposición (`estado.clave`) + reserva de reloj.**

- Nodo MAX: tu turno. Nodo CHANCE: ataque. Nodo MIN: rival.
- Profundización iterativa: siempre tienes una jugada lista; el reloj solo corta el siguiente ply.
- Extiende **ataques** (quiescencia de combates): un “quieto” que ignora un `p=0.80` al lado miente.
- Poda: alfa-beta en MAX/MIN; en chance, Star1/Star2 si te da tiempo (no es obligatorio al principio).
- Copia de `nucleo.py` en tu carpeta (`mi_motor.py`) si el cuello es crear objetos `Estado` a millones; la jugada que regresas sigue pasando por el motor oficial.

Reloj (idea concreta, no 1/25 fijo):

- Reserva **25–30 %** (comunicación ~7 ms/jugada, como dice `montecarlo`).
- Más tiempo si hay muchos ataques, si alguien tiene 2 puntos, o si el ply anterior cambió de jugada.
- Menos tiempo en apertura masiva si tienes libro.
- Si `tiempo_restante` es bajo: 1 ply + táctica, nunca `rng.choice` salvo emergencia.

Esto es el diseño que mejor encaja con el API del curso (`siguiente`, `clave`, `prob_ataque`, 1 núcleo).

#### Capa 4 — MCTS/UCT (alternativa o complemento, no el primer intento)

Útil si la eval de capa 1 aún es floja y quieres que el árbol se construya solo.

Hay que **no** copiar `montecarlo`:

- UCB1 (o UCT) para gastar muestras en jugadas inciertas/prometedoras, no round-robin.
- En ataques: o **esperanza** (ramas ponderadas), o un descendiente chance en el árbol; no un único `rng.choices`.
- Política por defecto sesgada por la eval, no uniforme.
- Rollouts: pocos y cortos, o **sin rollout** (eval en la hoja). `simular_al_azar` es rápido pero **optimista**: los dos juegan a lo loco y no se defienden.
- Calienta numba en `preparar`, como ya hace `montecarlo`.

Un MCTS bien hecho pega a tiers altos; uno plano **es** `montecarlo` y te deja en 3.

### Ideas de dominio (ganan partidas aunque el buscador sea simple)

1. **Formar cadenas de apoyo** (peones en diagonales) antes de pelear. Atacar con apoyo 2 vs 0/1; no iniciar pelea 0 vs 2.
2. **Carrera, no matanza.** Si vas 2–1 y un peón está a un paso, el resto del tablero es ruido.
3. **Bloquear archivos** del peón más avanzado rival (recto no se come).
4. **No regalar `p=0.20–0.35`** salvo para impedir un 3.º punto.
5. **Flancos `a`/`i`:** una sola diagonal; más fácil bloquear y más frágil el apoyo. Centro (`d–f`) concentra combates.
6. **Ahogo:** contar peones sin jugadas; a veces un avance “tonto” libera al rival o te deja sin movimiento.
7. **Color:** blancas salen; mide si tu eval tiene sesgo. En la liga juegas 2+2, así que el bot tiene que ser bueno con ambos.

### Precomputación que sí vale los 100 MB

| Qué | Para qué | Prioridad |
|---|---|---|
| Pesos de eval (`pesos.npy`) | Capa 1 viva | Alta |
| Libro de apertura (primeras 6–10 jugadas, de autojuego) | Ahorra reloj cuando hay 50+ movimientos | Media |
| PST / patrones de apoyo | Eval más barata | Media |
| Finales chicos (2–4 peones) | Poco estado, perfecto para tablas | Baja, si sobra tiempo |

El generador va en `herramientas/`; en la liga solo lees `data/` en `preparar` (10 s). Offline puedes usar lo que quieras; **en la liga no puede ser una red**.

### Qué no haría (con este proyecto)

- Clonar `montecarlo` y subir `SIMULACIONES`. Eso no te saca del 3.
- Minimax **sin** nodos de azar: elige ataques “ganadores” que en realidad son 50–50.
- Redes (numpy a mano incluido): 0 en el torneo.
- Multiproceso: 1 núcleo, no ganas.
- Optimizar numba **antes** de tener eval + 1 ply medido con Docker.
- Confiar en `--sin-docker` o en `./torneo mini` (2 partidas): es suerte de dados. Compara con `--partidas 20+` y reloj real.

### Cómo medirlo

1. Capa 0+1 vs `random` — debe ser casi 100 %.
2. Capa 2 vs `montecarlo` con Docker, `--partidas 20`, misma semilla al repetir bugs.
3. `./torneo mini` solo como humo; la nota real es **más puntos de liga** que el rival, no un 2–0 ruidoso.
4. `reportar(prof=..., nodos=..., eval=...)` y mira **Reloj máx**; ⚠ cerca de 27 s es perder partidas en la liga.
5. Cambia **una** cosa (eval, profundidad, UCB) y vuelve a medir.

Calificación práctica: **eval + expectiminimax 1 ply** apunta a pasar de `random` (1) a pelear `montecarlo` (3). **ID + TT + quiescencia de ataques** es lo más creíble para Tier 1–3. MCTS fino o motor propio en numba es la apuesta a 8.5–10, cuando lo anterior ya es estable.

---

## 3. La “mejor estrategia posible” / algoritmo techo (incluidas redes)

No existe un bot **imbatible** en este juego. Cada ataque es un dado con `p` entre 0.20 y 0.80: la estrategia óptima **maximiza la probabilidad de ganar**, no garantiza la victoria. En una partida puedes jugar perfecto y perder un 0.80. En la liga (muchas partidas) sí se ve quién está más cerca del óptimo.

Lo que sí existe es un **techo teórico** y un sistema que, con suficiente entrenamiento y búsqueda, le gana a casi cualquier cosa que quepa en 30 s y 1 núcleo — incluida una red sola.

**En la liga del curso una red neuronal es trampa y vale 0 para el equipo.** Lo de abajo es el diseño “de laboratorio”, no lo que deben entregar.

### El techo: el juego es un DAG con azar conocido

Los peones **solo avanzan o desaparecen**. No hay ciclos ni empates. El modelo de chance **no hay que aprenderlo**: `p` sale del apoyo.

El valor de una posición es exactamente:

\[
V(s) = \max_a \sum_{s'} P(s'\mid s,a)\, V(s')
\]

(en tu turno; el rival minimiza). En terminales, \(V\in\{0,1\}\). Esa \(V\) es la estrategia “imbatible en esperanza”: cualquier otra pierde en valor esperado.

No se puede tabular el juego entero (81 casillas × material × puntos × turno), pero **sí se puede resolver porciones**. Ahí está la ventaja contra “una red adelante”.

### El sistema que más se acerca (y le gana a una red)

Una red **sin búsqueda** es el oponente débil. El techo práctico es **tablas exactas + dinámica conocida + política/valor + MCTS con nodos de azar**, entrenado offline a lo bestia y comprimido al reloj de 30 s.

```text
offline (ilimitado)                    liga (30 s, 1 núcleo)
─────────────────                      ────────────────────
1. Tablebase retrógrada                cargar TB + pesos
   (finales, 2 puntos, pocas piezas)
2. Self-play AlphaZero/MuZero          expectiminimax / PUCT
   con chance EXACTO                   sobre la red + TB
3. Destilar red chica + libro          profundización hasta el reloj
```

#### 1. Resolver lo resoluble (esto “no se alucina”)

Retrogrado / expectimax exacto, guardado en `data/`:

- Todas las posiciones con **pocas piezas** (por ejemplo ≤6–8 peones).
- Todas con **marcador 2–2 o 2–1** y pocos peones cerca de la meta (el árbol se acorta: un anote termina).
- Amenazas de mate-en-1 / anote-en-1, ya no heurísticas.

En esas posiciones \(V\) es la verdad. Una red, por muy entrenada, **aproxima**; la tabla no. Ahí le ganas sí o sí en esperanza.

Como el grafo es acíclico, la retrógrada es más limpia que en ajedrez: no hay repeticiones ni zugzwang hacia atrás.

#### 2. Red política + valor (el medio juego)

Arquitectura típica superhumana para *este* tablero, no ImageNet:

- Entrada 9×9 con planos: blancas, negras, apoyo 0/1/2, ataques legales, `p` de cada combate, puntos, color, “peón pasado”, distancia a meta.
- Salidas: **política** sobre ≤54 jugadas `(origen, destino)` y **valor** = \(P(\text{ganar})\).
- Residual pequeño (el tablero es 9×9; una red enorme no aporta tanto como más MCTS).

Entrenamiento:

- Self-play de millones de partidas con la **misma** `p` del motor.
- El azar se trata como **nodo chance**, no como un dado que tiras una vez en el árbol (el error de `montecarlo`).
- No hace falta MuZero para aprender la física: `siguiente(j)` ya es el modelo perfecto. Eso es más fácil que Go o ajedrez.
- Currículum: primero finales (mezcla con la tablebase), luego medio, luego apertura.

Offline puedes usar torch, 16 núcleos, lo que sea. Eso es legal **para generar datos**; meter la red en `strategy.py` en la liga no.

#### 3. Búsqueda en el turno (aquí se mata a la red cruda)

En cada jugada, no “confíes en la red”:

1. Si la tablebase tiene el estado → juega el óptimo.
2. Si no: **PUCT / Gumbel** con:
   - prior = política de la red,
   - hoja = valor de la red (o exacto si caíste en TB),
   - ataques = **las dos ramas ponderadas por `p`**, no un sample.
3. Profundización hasta el reloj, reserva ~25 % para el protocolo.
4. Quiescencia de combates: no cortes en medio de un `p=0.80`.

Una red sola = 1 ply. La misma red + 10⁴–10⁵ visitas de MCTS con chance exacto le gana a esa red, y a un expectiminimax con eval lineal, y a `montecarlo`.

Eso es el resultado de AlphaZero: **búsqueda + modelo > modelo**.

#### 4. Libro de apertura generado por el propio sistema

Las primeras 8–12 jugadas salen de las visitas del self-play, no de ocurrencias. Ahorra los 30 s para el medio, donde el tablero ya no es simétrico y hay combates.

#### 5. Política de riesgo, no “el promedio”

Con dados, el objetivo de liga es **puntos de victoria**, no belleza.

- Si vas arriba en la liga / en la partida (2–0, 2–1): juega **bajo sesgo** (ataques solo con `p` alta, evita coin-flips).
- Si vas 0–2 o necesitas alcanzar un tier: **sube varianza** (ataques a 0.50 que anotan).
- `montecarlo` maximiza un promedio ruidoso; el óptimo maximiza \(P(\text{ganar la partida})\) y, a nivel torneo, \(P(\text{quedar arriba del rival de referencia})\).

Eso no lo da una red de valor a ciegas; lo da el valor *calibrado* + el marcador.

### Por qué esto le gana “aunque le pongas una red delante”

| Oponente | Por qué pierde contra este stack |
|---|---|
| Red sola | 1 ply vs árbol con chance exacto |
| `montecarlo` / MCTS plano | Rollouts uniformes, samplea el dado, reparte visitas igual |
| Expectiminimax + eval lineal | La red (o la TB) estima mejor las hojas |
| Red + búsqueda, menos compute | Más visitas, TB exacta, dinámica conocida |
| Trampa de dados / heurística rara | El modelo de `p` es el verdadero; no hay que adivinar |

La única cosa que no le ganas de forma sistemática es **el mismo algoritmo con más entrenamiento y más visitas**, o la solución exacta completa (que nadie tiene).

### Lo que no puedes esperar

- **100 % de partidas.** Un 0.20 que sale a favor del rival existe.
- **Calificación 10 automática.** La nota es “más puntos de liga que el tier”; una mala racha de dados en 4 partidas vs un rival concreto puede doler. El stack de arriba minimiza eso, no lo anula.
- **Meterlo al PR.** Red en la liga = 0. Ofuscarla en `data/` también: el validador y un agente revisan que informe, código y datos cuenten la misma historia.

### Si la pregunta es “entonces qué entregamos para acercarnos”

El **reflejo legal** del diseño de arriba, sin red:

1. Tablebases / patrones de finales y de “anota ya” (precomputados).
2. Eval lineal o logística **entrenada offline** (sí se vale) que imite un valor \(P(\text{ganar})\).
3. Expectiminimax / PUCT **con esperanza**, no sampleo del dado.
4. TT con `estado.clave`, profundización iterativa, reloj con reserva.
5. Libro de apertura de autojuego.

Eso es lo más cerca que el reglamento te deja del sistema “imbatible”. La red sería el mismo esqueleto con mejores hojas y mejores priors; el salto no es mágico, es **aproximar \(V(s)\) mejor y buscar más**.

---

## 4. Cómo mejorar y entrenar el algoritmo (y por qué no “nunca pierde”)

No pueden hacer que **nunca pierda**. El dado está en las reglas: un ataque a `p=0.80` falla 1 de cada 5 veces. Lo que sí pueden hacer es subir \(P(\text{ganar})\) hasta que, en una liga de muchas partidas, casi nadie les saque más puntos.

Entrenar mal es fácil: si solo le ganan a `montecarlo`, aprenden a explotarlo y se deshacen contra un tier que sí se defiende. El entrenamiento bueno es **una liga interna contra ustedes mismos**, y `random`/`montecarlo` son solo exámenes, no compañeros de gym.

### Cómo se mejora (ciclo, no “un entrenamiento”)

Una sola regla: **un cambio, una medida, se queda o se tira**.

```text
versión N  →  genera partidas  →  aprende  →  versión N+1
                │
                └→ liga interna vs N, N-1, N-5, agresivo, pasivo
                     si Elo sube de verdad: N+1 es el nuevo principal
                     si no: deshacer
```

1. Congelan un bot **principal** (el que entregarían mañana).
2. Cambian **una** cosa (un peso, profundidad, UCB, libro).
3. Juegan **muchas** partidas (20 es poco; 100–400 entre versiones).
4. Si gana por un margen claro (no 11–9), promociona. Si no, revertir.

Sin este ciclo, “entrenar” es adivinar.

Métrica útil: **Elo interno** o porcentaje de victorias, no una corrida de `mini`. Misma semilla de dados cuando depuran; semillas **nuevas** cuando miden fuerza (si no, memorizan esos dados).

### ¿Contra qué se entrena?

| Rival | Sirve para | No sirve para |
|---|---|---|
| `random` | ¿El bot está roto? | Nada de estrategia |
| `montecarlo` | Examen de nota 3 | Entrenar: es ruidoso y no se defiende |
| **Ustedes mismos (self-play)** | El grueso del aprendizaje | — |
| **Versiones viejas** (N-1, N-5, “el de la semana pasada”) | No olvidar lo que ya sabían | — |
| Bots **sesgados** (siempre ataca, nunca ataca, solo flanco, solo carrera) | Cubrir estilos que un tier puede traer | Ser el único rival |
| Posiciones **armadas** (2–2, peón en 8, ahogo) | Táctica y finales | Apertura |

El oponente correcto es **una población**:

- 40–60 % de las partidas: principal vs principal (self-play).
- 20–30 %: vs un *pool* de checkpoints (así no se sobreajusta al último yo).
- 10–20 %: vs “personalidades” (agresivo / cobarde / come-todo).
- Al final, **examen** vs `random` y `montecarlo` con Docker y 30 s. Eso no entrena; **califica**.

Self-play puro al inicio es flojo (los dos juegan mal). Por eso: primero un bot táctico + eval a mano que ya le gane a `random`, y **después** self-play. Curriculum:

1. Finales y “anota ya / para el anote”.
2. Medio juego con combates.
3. Apertura (libro al último; si lo hacen primero, memorizan basura).

### Cómo se entrena (versión legal del curso)

Red neuronal en la liga = 0. Offline pueden generar datos con lo que sea; lo que corre el día del torneo es búsqueda + **eval lineal/logística** + tablas.

#### A. Maestro de búsqueda (lo más rentable)

En cada posición de un lote:

- El “profesor” es su propio expectiminimax **más profundo** (o más tiempo), offline, sin reloj de 30 s.
- La etiqueta: jugada elegida y/o valor \(P(\text{ganar})\) del árbol.
- Ajustan los pesos de la eval para que a **1 ply** se parezca al profesor de 4 ply.

Eso es destilación. Gana más que “jugar vs montecarlo y tocar números a ojo”.

#### B. Aprendizaje temporal (TD)

Juegan self-play. Tras cada partida, para cada posición \(s_t\):

\[
V(s_t) \leftarrow V(s_t) + \alpha \big( z - V(s_t) \big)
\]

donde \(z = 1\) si ganaron esa partida, \(0\) si no (o \(V\) del padre en el árbol, TD-Leaf).

La eval es algo del estilo:

```text
V ≈ sigmoid(w · features)
```

features = puntos, avance, apoyo, peones pasados, ataques con su `p`, bloqueos, etc.

`scipy.optimize` o un logístico con numpy basta. Guardan `pesos.npy` en `data/`. El código que arma el dataset va en `herramientas/`.

#### C. Evolución de pesos (si TD se atasca)

CMA-ES / búsqueda local: mutan `w`, juegan 100 partidas vs el principal, se quedan el mutante si gana. Lento pero no se sobreajusta a una función rara. Bueno cuando hay **pocos** pesos (20–50), no 10 000.

#### D. Tablebases (el trozo que “no pierde”)

Offline, de atrás hacia adelante:

- Posiciones con pocos peones y/o 2 puntos.
- Para cada una, el `max`/`min` de la esperanza **exacta**.
- En la liga: si `estado` está en la tabla, juegan esa jugada. Cero error.

Ahí sí pueden decir “en este final no nos equivocamos”. En el resto, no.

#### E. Libro de apertura

Cuando el principal ya es fuerte: de las partidas de self-play, para cada posición de las primeras ~8 jugadas, guardan la jugada más visitada / con mejor \(V\). En la liga, si hay hit, la juegan en milisegundos y ahorran reloj.

Si el bot aún es débil, el libro **congela errores**. El libro es lo último.

### Cómo se acerca a “casi no perder” (sin mentir)

Nunca 0 derrotas. Sí pueden **cerrar las derrotas estúpidas**, que son la mayoría contra un bot bueno:

1. **Táctica forzada** cada turno: anote seguro, parar anote seguro, no atacar a `p=0.20` si no es la única forma de no perder ya.
2. **Tablebase** en finales y 2–2.
3. **Búsqueda con esperanza**, no un dado sampleado.
4. **Gestión de riesgo:**
   - Van ganando 2–0 / 2–1 → solo combates buenos (`p` alta), avanzar y bloquear.
   - Van perdiendo 0–2 → subir varianza (ataques que anotan a 0.50).
   - Eso maximiza puntos de **liga**, que es lo que califica.
5. **Reloj:** nunca `rng.choice` por timeout; profundización iterativa + reserva 25–30 %. Una derrota por reloj es una derrota gratis.
6. **Examen de regresión:** 50 posiciones fijas (“si no juegas e8-e9, fallas”). Cada commit las corre. Así el entrenamiento no les borra lo obvio.
7. Medir **con Docker y 30 s**, no `--sin-docker`. El bot entrenado en CPU libre se pasa de reloj el día de la liga y “pierde siempre” por el peor motivo.

La fórmula honesta:

```text
P(perder) = P(error nuestro) + P(el dado nos mata)
```

El entrenamiento y la TB bajan el primer término hacia 0. El segundo **no se puede bajar de un piso** (salvo no aceptar combates malos, que sí es decisión suya).

### Plan de entrenamiento realista (equipo de 2)

**Semana A — bot que ya no es `montecarlo`**  
Eval a mano + táctica + expectiminimax 1–2 ply + reloj. Gate: aplastar a `random`; ser competitivos vs `montecarlo` en 40+ partidas con Docker.

**Semana B — datos**  
Self-play del principal, 5k–50k partidas offline (`--sin-docker` o un script que llame al motor). Mezclan posiciones de apertura/medio/final. Profesor = la misma búsqueda con más tiempo.

**Semana C — pesos**  
Ajustan `w` (logístico o TD). Nueva eval. Liga: N+1 vs N, 200 partidas. Si no gana, no hay promoción.

**Semana D — profundidad y TB**  
Más ply / TT / quiescencia de ataques. Tablebase chica. Otra liga interna.

**Semana E — pulido**  
Libro, riesgo según marcador, reloj fino, `./torneo validar --entrega`, informe con **números** de esas ligas.

Dos personas: uno busca/reloj, el otro eval/datos. El principal es único; no fusionen dos ideas no medidas.

### Si hablamos del algoritmo “de laboratorio” (red)

Mismo ciclo, distinto modelo: self-play AlphaZero, prior = red, hojas = red, chance exacto, checkpoints en un pool, TB igual. Se entrena **contra sí mismo y contra su historia**, no contra `montecarlo`. Tampoco ese sistema deja de perder partidas; deja de **regalarlas**. Y no entra al PR.

### Resumen de esta parte

Se mejora con **liga interna y un cambio a la vez**; se entrena sobre todo con **self-play + versiones viejas + posiciones de finales**; `random`/`montecarlo` son el examen del curso; “nunca perder” se traduce en **cero errores tácticos + TB + no suicidarse al dado + no perder por reloj**. El resto es varianza que se gana en el aggregate de la liga, no en una partida.

---

## 5. Debilidades explícitas de `montecarlo` (lo que el curso ya marca)

En `estudiantes/montecarlo/strategy.py`, comentarios `AQUÍ PUEDES MEJORAR`:

1. ¿Todas las jugadas merecen el mismo tiempo?
2. ¿Tirar el dado es la única manera de tratar el azar?
3. ¿Qué tan buenas son esas partidas al azar? (`simular_al_azar`: ambos lados eligen uniforme; es ruidoso y optimista.)
4. ¿Es el promedio lo único que importa para elegir?

Además: reserva fija del 30 %; cada jugada usa `1/25` de lo disponible; `SIMULACIONES = 20`; si una jugada gana sin importar el dado, la toma.

---

## 6. Trampas y zona gris (repetido porque importa)

**Trampa o intento = 0 para todo el equipo:**

1. Redes neuronales de cualquier tipo en la liga, aunque estén escritas a mano con numpy, y librerías de *deep learning* (`torch`, `tensorflow`, `keras`, `jax`, `onnxruntime`…).
2. Código ofuscado o ilegible; datos en `data/` que en realidad son código.
3. Código nativo propio: C, Cython, `.so`, binarios. (numba sí se vale.)
4. Salir del aislamiento: leer fuera de tu carpeta, usar la red, guardar información entre partidas, atacar al árbitro.
5. Adivinar o manipular los dados.
6. Copiar código o datos de otro equipo, o compartir los tuyos antes de la entrega.
7. Ponerse de acuerdo con otro equipo (perder a propósito): 0 para **los dos**.

Offline (generar `data/`): absolutamente todo. Lo que corre en la liga no puede ser una red, aunque la hayas entrenado offline.

¿Duda? Preguntar **antes** de entregar (issue del repo del torneo o correo al profesor). La respuesta se publica para todos.
