# Instrucciones locales para Claude Code

## Objetivo

Ayudar al equipo `iacasitegano` a mejorar su bot de Breakthrough de combate con experimentos reproducibles, legales y medidos. El objetivo de calificación es 10: superar a Tier 5 en puntos de liga o quedar entre los tres primeros equipos de alumnos. No prometas que una técnica o un cambio garantiza ese resultado.

## Lectura obligatoria al comenzar

Antes de proponer o hacer cambios de estrategia, lee completos y en este orden:

1. `README.md`
2. `docs/reglas.md`
3. `docs/calificacion.md`
4. `docs/avanzado.md`
5. `estudiantes/iacasitegano/INFORME.md`
6. Los módulos y herramientas de `estudiantes/iacasitegano/` relacionados con el cambio.

El plan detallado está en `PLAN_TIER_5.md`; úsalo como hoja de ruta, pero aplica siempre el protocolo de un solo experimento y medición antes de implementar la siguiente fase.

Respeta también `AGENTS.md` y las instrucciones locales del repositorio. Usa `rtk` al ejecutar comandos de shell, como indica `/Users/josema/.codex/RTK.md`.

## Alcance y reglas del torneo

- El bot de trabajo es `estudiantes/iacasitegano/`.
- Para cambios del participante, edita solo `estudiantes/iacasitegano/`. No alteres `sistema/`, `docs/`, `README.md`, workflows, otros equipos ni el árbitro para mejorar resultados.
- `CLAUDE.local.md` es una guía local del proyecto. La entrega oficial solo puede cambiar archivos dentro de `estudiantes/<equipo>/`; no incluyas este archivo raíz en el PR de entrega.
- Conserva todos los cambios que ya existan en el árbol de trabajo. No limpies, restaures, rebases ni sobrescribas cambios ajenos al experimento.
- No uses redes neuronales en el bot, ni intentes predecir/manipular los dados, acceder a la red, escribir fuera de la carpeta del bot durante la partida, persistir entre partidas, ofuscar código ni compartir código/datos con otros equipos.
- Las partidas usan 1 núcleo, 1024 MB, 30 s de reloj por partida, 10 s para `preparar` e importación, 100 MB totales de carpeta y 50 MB por archivo. Deja margen de reloj; una jugada ilegal, excepción o timeout pierde la partida.
- `data/` es de solo lectura durante la liga. Los generadores de datos se guardan en `herramientas/` y el informe debe explicar cómo regenerar los datos.
- El informe final debe seguir teniendo sus nueve secciones y corresponder exactamente al código, los datos y los resultados medidos.

## Protocolo para cada experimento

1. **Registra el baseline.** Anota `git status`, revisión/cambio de referencia, pesos y libro usados, comandos, rivales, número de partidas, semillas, colores, resultados, puntos y reloj máximo. No confundas el estado actual del árbol con un commit limpio: el usuario puede tener renombrados y cambios sin terminar.
2. **Formula una hipótesis falsable.** Ejemplo: “la búsqueda deja escapar una carrera rival porque la evaluación estática no estima el tiempo hasta anotar”. Explica qué métrica debería cambiar si es cierta.
3. **Aísla una variable.** Un experimento modifica una técnica o grupo inseparable de parámetros. No cambies a la vez búsqueda, evaluación, libro y reparto de reloj.
4. **Fija el protocolo antes de medir.** Alterna colores y empareja semillas/dados entre candidato y baseline. Usa un conjunto de semillas para desarrollo y otro, no visto, para validación. Reporta victorias, derrotas, puntos anotados, errores, timeouts, reloj máximo y muestras por color. 40 partidas son un filtro inicial; usa 100 o más cuando el resultado sea estrecho o ruidoso.
5. **Mide el bot real bajo el árbitro.** Prioriza `./torneo jugar ...` con Docker y límites oficiales. Si Docker no está disponible, `--sin-docker` sirve para depurar o explorar, pero no certifica reloj, memoria ni rendimiento oficial. No digas que un cambio ganó si solo mejoró una búsqueda offline.
6. **Interpreta con cautela.** Los dados agregan ruido: una tanda pequeña no demuestra superioridad. Compara el mismo juego de dados y ambos colores, reporta el total y cada desglose; conserva una validación con semillas nuevas. Un cambio no pasa solo por mayor profundidad, más nodos o una evaluación que “se ve mejor”.
7. **Decide con evidencia.** Acepta solo si mejora el resultado de partidas completas de forma repetible, no causa regresiones por color/puntos y mantiene margen de reloj y preparación. Si no mejora, vuelve al baseline del experimento sin borrar trabajo previo del usuario.
8. **Actualiza el informe.** Al aceptar una mejora, registra metodología, semillas, rival, número de partidas, límites usados, resultados y qué no funcionó. No conviertas resultados de `--sin-docker` o de búsqueda fija en resultados oficiales.

## Herramientas actuales y límites de interpretación

- `estudiantes/iacasitegano/strategy.py` carga pesos y libro, detecta victorias inmediatas, reparte reloj y llama a `busqueda_numba`.
- `busqueda_numba.py` implementa expectiminimax con probabilidades del motor, poda alfa-beta, poda Star1, tabla de transposición, orden sugerido de la iteración previa y profundización iterativa. La quiescencia está apagada (`QUIESCENCIA_MAX = 0`) porque el informe registra que no mejoró resultados.
- `eval.py` usa una evaluación lineal con puntos, avance, apoyo, peones pasados, columnas vacías y carrera. Los pesos se cargan de `data/pesos.npy`.
- `herramientas/entrenar.py` genera partidas de self-play y contra `random`/`montecarlo`, y ajusta pesos por ridge usando el resultado final de la partida. Esto no identifica directamente el valor causal de cada acción.
- `herramientas/libro_apertura.py` genera el libro a partir de self-play; no asumas que una apertura funciona contra rivales distintos sin validarla.
- `herramientas/liga_interna.py` es una herramienta offline de comparación: su jugador propio usa profundidad fija y no reproduce el reloj ni toda la lógica de `strategy.jugar()`. Úsala para análisis exploratorio/checkpoints, no como sustituto de partidas oficiales con Docker.
- El informe existente documenta resultados aproximados de 6–14 contra `montecarlo` en 20 partidas para un ajuste de tiempo, y otras tandas con métricas distintas. No mezcles esos protocolos ni presentes una tanda corta como fuerza concluyente.
- Tier 1–5 no están incluidos como código público. La meta intermedia comprobable ahora es superar `montecarlo`, y después medir contra los tiers cuando estén disponibles.

## Orden de investigación sugerido

No implementes esta lista en bloque. Toma una sola hipótesis por experimento, empezando por las de mayor valor medible:

1. Crear una evaluación base reproducible por color, reloj y posición, y medir a `iacasitegano` contra `montecarlo` con partidas completas. Revisar primero el presupuesto de reloj y los casos que pierden por carrera/amenaza.
2. Mejorar ordenamiento de jugadas dentro de la búsqueda: victorias, anotaciones posibles, probabilidad de ataque, piezas amenazadas y bloqueo de carreras; medir nodos por segundo y partidas ganadas, no solo el tiempo de búsqueda.
3. Probar valores Star2/bounds de nodos de azar con tests diferenciales contra expectiminimax exhaustivo en posiciones pequeñas. Aceptar solo si los valores coinciden y las partidas reales mejoran sin timeouts.
4. Comparar búsqueda exacta con rollout Monte Carlo y un híbrido adaptativo. La política de rollout debe ser competitiva y usar el presupuesto real; no asumir que más simulaciones ganan. Medir por separado posiciones tácticas y tranquilas.
5. Sustituir o complementar el entrenamiento por resultado final con aprendizaje de preferencias de acciones: comparar acciones desde la misma posición y estimar valor esperado con seeds repetidas. Mantener los datos y scripts auditables, con división por semillas/posiciones entre ajuste y evaluación.
6. Resolver finales pequeños o carreras forzadas mediante búsqueda exacta/tablas, con claves que incluyan turno y puntos. Validar exhaustivamente contra el motor oficial en posiciones reducidas.
7. Ajustar el reloj según riesgo y dificultad, siempre con respuesta legal de respaldo y reserva. Medir el percentil alto y máximo, no solo el promedio.

## Entrega de cada cambio

Al terminar, informa: hipótesis, archivos editados, cambio conceptual, comando y entorno de pruebas, resultados desglosados por color, clock/preparación máximos, semillas de validación y limitaciones. No hagas commit, push, cambios de cuenta ni acciones sobre la entrega oficial salvo petición explícita del usuario.
