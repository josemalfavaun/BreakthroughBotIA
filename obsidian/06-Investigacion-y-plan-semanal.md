---
tipo: investigacion
proyecto: BreakthroughBotIA
actualizado: 2026-10-28
estado: propuestas-sin-validacion-de-fuerza
---

# Investigación y plan hasta el 4 de noviembre

> Investigación fuente. Desde la aceptación de Jose del 28 de octubre, ejecución vigente en [[07-Plan-definitivo]]; escritorio en [[08-Escritorio-y-entrenamiento]]. Utilidad 5A ya terminó sin promoción: +7 frente a +8 exigido. Las referencias a medirla más abajo describen el plan previo.

## Decisión para retomar en dos minutos

Mantener expectiminimax como línea principal. Primero cerrar utilidad, obtener contrafactuales de decisiones y recuperar/calibrar el modelo. La investigación favorece gastar más cómputo **offline** para mejorar un evaluador pequeño, entrenarlo contra rivales diversos y después probar pistas TT. No hay evidencia para sustituir hoy el buscador por MCTS ni para lanzar una evolución grande de pesos.

La primera hipótesis nueva de modelo será **interacción entre patrones y fase del marcador**, únicamente si el diagnóstico confirma un error que el modelo aditivo actual no representa. Alternativa: distilar análisis más fuertes a los patrones existentes, conservando la arquitectura. Son experimentos distintos, no un paquete de mejoras.

Entrega comunicada por Jose: **4 de noviembre de 2026; hora pendiente**. Disponibilidad: sesiones de 1 h, noches de 7 h y posible escritorio dedicado 24 h, con Windows, i5 aproximadamente de octava generación, 16 GB RAM DDR4 y Radeon RX 570. El escritorio todavía no está configurado ni conectado desde este chat. Plan inicial por CPU; GPU innecesaria para la línea propuesta.

Esta nota contiene investigación y propuestas. **No añade victorias medidas, no cambia el A/B de utilidad ni sus semillas y no promueve candidatos.** Estado experimental: [[01-Estado]], [[05-Cierre-de-fases]] y [[Experimentos/2026-10-28-Protocolo-utilidad-victoria]].

## Autoridad y compatibilidad con el curso

Se consultó la [página del proyecto del profesor](https://rayalucaria.org/ia_o26/juegos/proyecto/index.html), enlazada desde la página que proporcionó Jose. Esa página declara que prevalece el repositorio oficial. Se leyeron también sus [reglas vigentes](https://github.com/raya-lucaria/ia_o26_torneo_adversarial/blob/main/docs/reglas.md), [preguntas frecuentes](https://github.com/raya-lucaria/ia_o26_torneo_adversarial/blob/main/docs/preguntas.md) y [calificación](https://github.com/raya-lucaria/ia_o26_torneo_adversarial/blob/main/docs/calificacion.md), el 28 de octubre.

- Liga: 30 s por partida, preparación/importación 10 s, un núcleo, 1024 MB. Modelos lineales/logísticos, patrones y árboles de decisión admitidos. Redes neuronales en liga prohibidas.
- Offline: cualquier herramienta y todos los núcleos. Esto permite estudiar un profesor costoso, incluso neuronal, y entregar un estudiante realmente no neuronal, legible y reproducible. No equivale a ocultar una red en una tabla o en código.
- Los tiers respetan las mismas reglas. Una red neuronal rival sería un caso de laboratorio, salvo que el profesor cambie las reglas.
- La nota depende de **puntos totales en la liga**: superar a una referencia significa terminar con más victorias totales que ella. Por eso necesitamos generalización, además del enfrentamiento contra Montecarlo.

La página no publica la hora de cierre: indica que la anuncia el profesor. Tomamos el día indicado por Jose y dejamos margen de entrega el 3 de noviembre.

## Qué tenemos y qué ya salió mal

El principal sigue en `integracion-tier1-2`, HEAD `85b2d55e9713bd993d874cfa050c60827580c92a`, con cambios locales conservados. Estrategia: expectiminimax con alfa-beta/Star1, profundización iterativa, TT, Numba y eval3. El NPZ activo tiene SHA-256 `37678d0bd700c27a29d0084558158db1a65b01409dbf54828e89706441c2250b`.

**Ya usamos regresión:** el modelo vigente procede de un ajuste logístico, con patrones locales, filas y marcador. Tiene 267 posiciones de pesos crudos y 275 valores empaquetados, incluidas banderas; no son 275 parámetros activos independientes. El modelo ridge de seis pesos es histórico y `strategy.py` no lo carga. Fuentes: `estudiantes/iacasitegano/eval3.py`, `strategy.py` y [[Experimentos/2026-10-27-Utilidad-victoria]].

El baseline oficial de 40 partidas dio 21–19; el A/A posterior mostró variación considerable entre repeticiones. No hemos demostrado dominar a Montecarlo. Ya se rechazaron reloj adaptativo, piso de tiempo de carreras, ordenamiento táctico genérico y una búsqueda híbrida con rollouts. La quiescencia amplia no justificó su costo; tablas minúsculas de finales apenas se activaron. Preferencias y self-play ya se exploraron: reintentarlos exige explicar qué cambia en los datos, el profesor o la validación. Fuentes y resultados en [[03-Bitacora]] y [[05-Cierre-de-fases]].

## Regresión lineal: sí, pero el nombre no determina la fuerza

Una suma de pesos puede representar interacciones complejas si sus entradas son patrones de tablero. Lo lineal es la combinación de esas entradas. Nuestro patrón de cinco celdas ya distingue 243 configuraciones; volver a seis números globales perdería información.

El autor de [Logistello](https://skatgame.net/mburo/log.html) documenta evaluaciones con patrones, primero regresión logística y luego lineal, integradas con búsqueda y tablas. Es un antecedente sólido de evaluación barata; Othello es otro juego y esos resultados no predicen nuestro porcentaje de victorias.

Propuesta: comparar ridge y logística solo como ablación controlada, con **las mismas características, particiones y objetivos**, si los diagnósticos lo justifican. Para etiquetas de victoria, logística produce una probabilidad acotada de forma natural; ridge necesita definir cómo interpretar/acotar su salida. Un menor error de ajuste no demuestra mejor juego.

Con azar, la escala sí cambia decisiones. El candidato de utilidad usa `u = 2*sigmoid(logit)-1 = tanh(logit/2)`, terminales ±1 y esperanza en combates. Eso alinea la interpretación de hoja y terminal; no garantiza que las probabilidades estén calibradas ni que representen juego óptimo. No añadiría una penalización genérica al riesgo: el objetivo primario es ganar, y una apuesta puede ser correcta cuando la alternativa pierde.

## Nuestro propio Monte Carlo: tres usos diferentes

El [bot público del curso](https://github.com/raya-lucaria/ia_o26_torneo_adversarial/blob/main/estudiantes/montecarlo/strategy.py), contrastado con la copia local, toma una muestra de resultado de combate y promedia continuaciones aleatorias; reparte muestras cíclicamente entre jugadas. Comprueba victorias inmediatas seguras. Es **Monte Carlo plano**, no UCT/MCTS.

1. **Rival de laboratorio:** recuperar una variante por número fijo de simulaciones facilita comparar decisiones reproducibles. Eso no sustituye la validación oficial a reloj.
2. **Generador/profesor offline:** continuaciones con políticas diversas y mayor presupuesto pueden aportar etiquetas o comprobar alternativas. Una simulación aleatoria estima el resultado de esas políticas, no el valor óptimo de la posición.
3. **Nuevo bot MCTS:** alternativa válida, pero costosa de construir y validar en una semana. Primero necesitaría un prototipo correcto y competitivo; añadir UCT no asegura superar al bot actual.

Lanctot y colaboradores estudiaron [MCTS con valores minimax implícitos](https://mlanctot.info/files/papers/cig14-immcts.pdf). En su Breakthrough determinista, con la evaluación efMS, el MCTS base ganó 27.55% contra alfa-beta a 1 s por jugada; la variante implícita ganó 45.05%. A 5 s, fueron 39% y 61.6%. El presupuesto y la combinación importan. No son nuestro tablero 9×9, combates ni tres puntos, y 5 s por jugada no equivalen a 30 s por partida.

Nuestra adaptación, **si llegamos a probarla**, conservaría separados el promedio de simulaciones y el valor heurístico; incorporaría probabilidades reales en nodos de azar, perspectiva correcta por jugador y límites de memoria. No sería repetir la mezcla de rollouts anteriormente rechazada. El primer ensayo tendría un plazo de un día y se abandonaría si no supera corrección, costo y filtros de desarrollo.

## Genéticos y optimización de parámetros

Sí son legales offline y pueden ajustar pesos, pero cada valoración mediante partidas es cara y ruidosa. Una población enorme puede seleccionar al que tuvo mejores dados. Para etiquetas supervisadas, ajustar cientos de pesos mediante regresión suele ofrecer una referencia mucho más barata.

Los trabajos de [Szubert, Jaśkowski y colaboradores](https://mszubert.github.io/publications.html) incluyen evolución/CMA-ES y aprendizaje temporal en Othello. Muestran tanto resultados favorables como diferencias entre vencer a un rival fijo y generalizar a rivales desconocidos. La selección de adversarios es parte del problema, no un detalle del optimizador.

Uso propuesto: optimizar **5–12 parámetros** una vez establecidas sus funciones y rangos; por ejemplo, regularización o coeficientes de una familia bien motivada. No cambiar simultáneamente reloj, representación y búsqueda. Comparar con muestreo simple antes de adoptar optimizadores elaborados. Herramientas posibles: [evolución diferencial de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html), [SPSA](https://github.com/zamar/spsa) y [CLOP](https://www.remi-coulom.fr/CLOP/), diseñado para ajuste con resultados ruidosos. Ninguno elimina la necesidad de confirmación aparte.

## Oportunidades nuevas, priorizadas por mecanismo y prueba

Estas son propuestas nuestras apoyadas por la investigación; no mejoras demostradas en este proyecto. La búsqueda en notas/código revisados no encontró validaciones de las cuatro primeras como se definen aquí.

| Oportunidad | Qué cambia y por qué puede ayudar | Primera prueba y motivo para descartarla |
|---|---|---|
| **Evaluación condicionada por marcador** | Elegir una de dos tablas de patrones según si alguien ya tiene dos puntos. Actualmente el marcador se suma a los mismos pesos de patrón: no cambia su importancia relativa. Una regla simétrica conserva la perspectiva por color. | Comparar con el mismo modelo compartido, datos y regularización. Penalizar desviaciones respecto a pesos comunes. Si no mejora diagnóstico fuera de muestra, especialmente amenazas de tercer punto, o encarece demasiado la búsqueda, descartar. |
| **Profesor caro, estudiante barato** | Analizar decisiones con búsqueda más profunda y otra política/evaluación; ajustar patrones/logística o un árbol pequeño con esas etiquetas. | Piloto de 24 estados y costo de etiquetado. Comparar alternativas, no solo copiar la jugada elegida. Si los profesores discrepan sin resolución, etiquetar incertidumbre. Sin mejora posterior en partidas independientes, rechazar. |
| **Selección activa de posiciones** | Dedicar análisis a estados donde modelos/búsquedas discrepan y a fallos de decisiones, conservando también una muestra representativa. | Medir por hora cuántas decisiones se aclaran. Si solo aumentan los ejemplos raros o se empeora la distribución habitual, reducir el sesgo de selección. |
| **Simetría horizontal en los datos** | Vincular patrones reflejados o aumentar datos con el espejo izquierda/derecha. Reduce parámetros/libera datos para casos escasos. | Verificar equivalencia de jugadas, probabilidades y resultados al reflejar. Original y espejo deben permanecer en la misma partición. Medir utilidad: los datos duplicados no son nuevas partidas independientes. |
| **Ordenamiento aprendido de jugadas** | Modelo lineal pequeño para sugerir qué acción explorar primero, sin podar por su consejo. Distinto de evaluar el tablero. | Evaluar ranking y tiempo total, incluyendo costo del modelo; valor a profundidad completa debe coincidir con referencia. Después de pistas TT, como hipótesis separada. |
| **Extensión de amenazas de tercer punto** | Seguir una secuencia corta de amenazas/defensas, incluidas jugadas sin captura; distinta de extender todos los ataques. | Solo si contrafactuales demuestran un error de horizonte relevante. Contar nodos, activaciones y efecto sobre reloj. No declarar una variante probabilística como victoria forzada. |
| **Caché útil entre búsquedas** | Pistas TT en nodos internos; después, como otro experimento, conservar pistas entre iteraciones/turnos de la misma partida. | Un acierto exacto ya devuelve valor: la pista debe servir en nodos con cotas/otra profundidad. Separar sugerencia de valor exacto; claves incluyen tablero, turno y puntos. Medir el panel establecido en [[05-Cierre-de-fases]]. |
| **Árboles de decisión/boosting offline** | Capturar interacciones como profesor o probar pocos árboles exportados a arrays legibles. | Comparar mejora predictiva con pérdida de profundidad por costo. [HistGradientBoosting](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html) es una herramienta candidata offline, no dependencia nueva obligatoria de la liga. |

[VIPER](https://arxiv.org/abs/1805.08328) es un antecedente de extraer políticas de árboles de decisión a partir de un profesor neuronal. Sus experimentos son de control/Pong, no Breakthrough. Nuestra primera versión puede usar un profesor de búsqueda sin redes, aprovechando infraestructura existente. No afirmamos que un estudiante conserve toda la capacidad del profesor.

[TDLeaf](https://arxiv.org/abs/cs/9901001) ofrece otra vía de aprendizaje que utiliza resultados de búsqueda. Queda como alternativa posterior: habría que adaptar perspectivas y nodos de azar, estabilizar los objetivos y evitar usar como prueba de fuerza el acuerdo con la propia evaluación. No lo añadiría junto con un cambio de representación esta semana.

## Cómo intentar ganar a rivales más complejos

La complejidad no ordena automáticamente la fuerza. Queremos un evaluador rápido, búsqueda correcta de respuestas relevantes y conocimiento offline suficiente para aprovechar el reloj. Contra el Monte Carlo plano, una oportunidad es una posición donde pocas defensas evitan el tercer punto: sus continuaciones aleatorias pueden infravalorar esa defensa. **Es una hipótesis sobre decisiones, no una explicación probada de nuestras derrotas ni una estrategia que garantice ganar.**

Un caso útil debe incluir estado exacto, jugada observada, alternativas, respuestas del rival, ambos resultados de cada ataque con su probabilidad, método de referencia y límite de incertidumbre. No usar el dado futuro de una partida para decidir qué habría sido correcto antes del ataque. Una derrota tras una decisión buena no es necesariamente un error.

Contra un agente entrenado, entrenar respuestas a varios estilos y encontrar sus errores reproducibles puede servir. El trabajo [Adversarial Policies Beat Superhuman Go AIs](https://arxiv.org/abs/2211.00241) demuestra fallos estratégicos graves de sistemas fuertes de Go, pero sus atacantes también se entrenaron con redes y acceso específico al rival. No demuestra que nuestro bot pueda vencer a cualquier red. Con tiers ocultos, priorizamos solidez general; no podemos diseñar una explotación comprobada de un código que no conocemos.

No copiaría por nombre técnicas selectivas de ajedrez como null-move o poda estadística agresiva. En carreras de peones, pasar puede cambiar totalmente el resultado; con azar, las cotas requieren cuidado adicional. Primero aprovechar ordenamiento que preserve la búsqueda completa.

## Entrenamiento efectivo y defensa contra sobreajuste

Los trabajos de [PSRO/poblaciones de políticas](https://arxiv.org/abs/1711.00832) estudian el sobreajuste a otros agentes y respuestas a mezclas de políticas. Nuestra adaptación sería pequeña y no neuronal, sin implementar su infraestructura de aprendizaje profundo.

1. **Receta reproducible.** Recuperar datos, filtros, características, particiones, regularización y exportación del NPZ vigente. Guardar hashes y versiones. El archivo activo ya se localizó; falta cerrar la receta completa.
2. **Datos agrupados.** Separar por partida y grupo de dados/colores; mantener estados relacionados y espejos juntos. La validación antigua usada para elegir numerosas ablaciones es desarrollo, no una nueva confirmación.
3. **Población pequeña de rivales propios/públicos.** Montecarlo oficial; campeón actual; una versión anterior; agresivo por apoyo; corredor/defensor; búsqueda más profunda o UCT correcto. Random solo comprueba funcionamiento: no debe dominar el promedio.
4. **Reservar estilos completos.** Dejar fuera del entrenamiento al menos una familia de rival y semillas nuevas. Hacer validación por familia durante desarrollo; después una sola confirmación congelada. Evitar que cambiar solo la semilla se presente como generalización a otra estrategia.
5. **Etiquetas con procedencia.** Resultado observado, solución exacta o estimación de profesor son tipos distintos. Guardar horizonte, política y confianza. No mezclar retornos de políticas diferentes como si fueran el mismo valor óptimo.
6. **Diversidad y foco.** Tomar una muestra general más posiciones de carreras, amenazas y ventaja. Muestrear por partida para que las largas no dominen. Enriquecer donde falle el modelo; no entrenar únicamente con derrotas ni con el patrón de un rival.
7. **Medir antes de jugar cientos.** Brier/logloss y calibración por fase, pérdida de calidad de decisión en casos resueltos, costo por hoja y búsqueda. Un ajuste mejor contra sus etiquetas es un filtro, no una promoción.
8. **Partidas oficiales finales.** Mismo hardware y límites para A/B; colores equilibrados y bloques alternados. Victorias como primaria, reloj/errores como restricciones, puntos anotados como secundaria. Mostrar cada rival y color además del promedio. No esconder una regresión fuerte tras muchas victorias contra un rival fácil.

Tenemos 282 estados legales de desarrollo extraídos de 40 partidas; no son 282 errores ni un conjunto reservado. El primer panel de 24 debe congelarse antes de comparar candidatos, cubrir apertura/carrera/ventaja y evitar escoger después los casos donde mejora el nuevo modelo. Ver [[Experimentos/2026-10-28-Diagnostico-decisiones]].

## Pruebas que reducen ensayo y error

Cada candidato necesita una cadena comprobable: **error observado → mecanismo propuesto → prueba en posiciones → costo bajo reloj → victorias contra varios rivales → confirmación**. Si falla una etapa, se registra y se detiene; no se arregla el criterio después de ver el resultado.

Mantener dos bancos: uno determinista, con profundidad/nodos/simulaciones fijas, para atribuir cambios; otro oficial a reloj para fuerza. Misma semilla no fija cuántas simulaciones hará Montecarlo ni garantiza trayectorias iguales. No reemplazar decisiones de protocolos ya congelados por esta propuesta.

El flujo de pruebas de [Fishtest](https://github.com/official-stockfish/fishtest) es una referencia de disciplina experimental; Stockfish moderno no es aquí un ejemplo de motor sin red neuronal. No hace falta copiar toda su plataforma ni aplicar una prueba secuencial retrospectivamente. Para futuros paneles, fijar tamaño o regla de parada antes de observar y respetar la dependencia entre partidas emparejadas; confirmar un único finalista reduce selección por suerte.

Para corrección, [Hypothesis](https://hypothesis.readthedocs.io/en/latest/stateful.html) puede generar y reducir secuencias que revelen fallos. Priorizar comparación con motor oficial, invariancia al espejo, suma de probabilidades, resultados terminales, entradas inmutables, aborto por tiempo y consultas TT con ventanas distintas. Eso reduce fallos; no certifica ausencia universal de errores. La regresión TT ya encontrada merece conservarse permanentemente.

## Qué encontré en GitHub y qué podemos reutilizar

| Fuente revisada | Utilidad | Límite de transferencia |
|---|---|---|
| [adamgracikowski/Breakthrough](https://github.com/adamgracikowski/Breakthrough) | Proyecto académico con alfa-beta, UCT, RAVE, simulaciones guiadas y torneos reproducibles. | Breakthrough habitual, primer peón gana y sin dados. Implementación Rust: no entregar su binario. README no basta para demostrar superioridad bajo nuestro presupuesto. |
| [OpenSpiel, implementación MCTS](https://github.com/google-deepmind/open_spiel/blob/master/open_spiel/python/algorithms/mcts.py) | Referencia para perspectivas, evaluadores, UCT/PUCT y nodos de azar. | Necesita adaptar nuestra variante. El paquete usa componentes nativos; estudiar el algoritmo o usarlo offline, sin asumir instalación legal/útil en la entrega. |
| [Fishtest](https://github.com/official-stockfish/fishtest) y [SPSA](https://github.com/zamar/spsa) | Gestión de pruebas y ajuste numérico. | Herramientas de proceso; no son estrategias para nuestro tablero. |

No encontré una solución verificada que reúna exactamente 9×9, combates probabilísticos, tres puntos, 30 s, un núcleo y ausencia de redes. Sí hay precedentes útiles; adaptar, citar y medir es necesario. Respetar licencias cuando se incorpore código. No se descargó ni integró un motor externo en esta investigación.

## Calendario propuesto y uso de las computadoras

| Fecha | Trabajo principal | Evidencia para avanzar |
|---|---|---|
| **28–29 oct.** | Cerrar resultado de utilidad con su protocolo; completar receta; congelar 24 casos y preparar rivales de laboratorio. | Resultado aceptado/rechazado/inconcluso explícito; referencias de decisiones y medición de costo del profesor. No inventar que la corrida de terminal terminó. |
| **29–30 oct.** | Etiquetado dirigido y diagnóstico de calibración. Configurar escritorio y medir rendimiento durante diez minutos. | Datos versionados, familias de rivales y particiones fijadas; errores concretos que justifiquen un candidato. |
| **30–31 oct.** | Probar un cambio de modelo: interacción de fase **o** nuevas etiquetas con representación existente. Pistas TT en un experimento separado. | Corrección, validación fuera de muestra y costo aceptable. No sumar ganancias de cambios que todavía no se probaron juntos. |
| **1–2 nov.** | Elegir finalista y confirmar con rivales/semillas reservados bajo condiciones oficiales; comparar con baseline original. | Mejora repetible o decisión explícita de conservar baseline. Si hay integración de dos cambios, probar también la combinación. |
| **3 nov.** | Congelar candidato; regeneración, cache en plataforma objetivo, tamaño, importación, reloj, informe y simulacro de entrega. | Entrega verificable y respaldo conocido. Ninguna arquitectura nueva. |
| **4 nov.** | Entrega antes de la hora indicada por el profesor. | SHA y contenido coherentes según procedimiento oficial, con autorización del usuario para acciones de publicación. |

El calendario limita el alcance; no garantiza cerrar investigación inconclusa. Si el 1 de noviembre ningún cambio supera desarrollo, se dedica el resto a robustez, validación y entrega del mejor bot conocido.

**Sesión de 1 h:** analizar el panel, ejecutar pruebas de corrección, ajustar modelos sobre datos ya generados o filtrar un candidato. No gastar toda la sesión en recompilar o buscar parámetros sin hipótesis.

**Noche de 7 h:** lote recuperable de etiquetado o evaluación, con manifiesto, checkpoints y límite de tiempo. Calcular el volumen después del piloto de diez minutos; no prometer un número de partidas sin medir el costo del árbitro y de ambos bots.

**Escritorio 24 h:** en Windows, seguir la [ruta oficial WSL2/Ubuntu](https://github.com/raya-lucaria/ia_o26_torneo_adversarial/blob/main/docs/empezar.md#windows-wsl2). Empezar con un trabajador y luego dos para generar datos; aumentar solo si rendimiento/memoria lo permiten. Las pruebas oficiales de fuerza corren en una ventana sin entrenamiento pesado en ese mismo host. Entrenar en escritorio y medir en la laptop permite paralelismo sin contaminar el reloj.

Mantener idénticos datos/especificación y registrar plataforma. No comparar porcentajes de A en una máquina contra B en otra como si fueran un A/B controlado. Rehacer y validar caché Numba para el entorno objetivo; no asumir que el caché de macOS/ARM sirve en Windows/Linux/x86.

## Próxima acción concreta

Preparar el banco de 24 decisiones y completar la receta, mientras el dueño del experimento de utilidad termina su protocolo. Después, elegir la hipótesis de modelo según los errores observados. La computadora adicional aumenta capacidad de análisis; la prioridad sigue siendo producir decisiones mejor justificadas y victorias verificadas.

No se ejecutaron entrenamientos, partidas, compilaciones ni cambios de algoritmo en esta sesión de investigación. Solo documentación; sin commit, merge, push ni promoción.
