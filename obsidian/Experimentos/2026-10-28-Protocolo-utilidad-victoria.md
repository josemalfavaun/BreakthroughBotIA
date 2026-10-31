---
tipo: experimento
estado: serie-desarrollo-completada
fecha: 2026-10-28
baseline_commit: 85b2d55
---

# Comparación de utilidad de victoria frente a logits

## Pregunta y variantes

¿La transformación logística de las hojas, con terminales ±1, aumenta las victorias frente a Montecarlo bajo el reloj oficial?

- **A / control:** `/Users/josema/.codex/worktrees/tt-cotas-exactas/BreakthroughBotIA`. Logits y terminales originales, TT corregida. SHA-256 de `estudiantes/iacasitegano/busqueda_eval3.py`: `cc888a3c7fc7ba896f5145c36c56c77120bc6f0ef0b0ba45f077023bbeb7a177`.
- **B / candidato:** `/Users/josema/.codex/worktrees/utilidad-victoria/BreakthroughBotIA`. Misma TT corregida; hojas `tanh(z/2)` y terminales ±1. SHA-256 de búsqueda: `83997dd323509bbfc2edd92de46a81a3770a6f1d5603daa730352ed56303277e`.
- Ambos parten de `85b2d55`. NPZ activo en ambos: `37678d0bd700c27a29d0084558158db1a65b01409dbf54828e89706441c2250b`.
- Sin hojas optimizadas, reutilización de buffers, otro reparto de tiempo, nuevos pesos o ajuste de temperatura.
- La comparación mide el efecto de la utilidad **condicionado a la TT corregida**. No mide el efecto de la TT frente al bot principal ni autoriza su promoción.

## Comprobaciones antes de jugar

1. Leer el estado y comprobar procesos/contendores; una sola ventana de medición. No interrumpir una serie ajena.
2. Confirmar hashes y diferencias de fuentes. Guardar manifiesto de TODOS los archivos de participante usados, incluidos cachés, IDs de imágenes y hash del rival. Cachés separados y compatibles con cada variante. No copiar el caché de A sobre B.
3. Validación compilada del candidato y validador de entrega de ambas variantes. Tres preparaciones frías en serie por variante, 1 CPU y 1024 MiB, límite 10 s. Conservar logs y resultados; no sustituirlos con pruebas históricas.
4. Configuración oficial: Docker, árbitro sin cambios, 30 s por partida, preparar 10 s, 1 CPU y 1024 MiB por bot, escala 1.0, `TORNEO_SIMULTANEAS=1`. Rival Montecarlo congelado. Registrar configuración efectiva.
5. Ejecutar desde cada worktree con su participante montado. Verificar cómo resuelve las imágenes el CLI y evitar que una etiqueta compartida haga jugar dos veces la misma variante. No modificar el motor para resolverlo.
6. El candidato combinado pasó el validador de entrega, con aviso de timeout en una prueba reducida a 3 s (no es una partida oficial a 30 s). Antes del desarrollo, ejecutar **4 partidas técnicas de B contra Montecarlo, semilla 20261115**, 2 por color y límites oficiales. Son adicionales a las 160 de desarrollo y se excluyen de su métrica por diseño. Si hay fallo técnico propio, conservar evidencia y detener; no corregir B a mitad de la serie. No usar este smoke para decidir fuerza.

## Desarrollo: 160 partidas fijas

| Orden | Semilla | Variante | Partidas | Por color |
|---|---:|---|---:|---:|
| 1 | 20261109 | A | 40 | 20 |
| 2 | 20261109 | B | 40 | 20 |
| 3 | 20261110 | B | 40 | 20 |
| 4 | 20261110 | A | 40 | 20 |

Comando por bloque, desde la raíz de su worktree:

```sh
rtk env TORNEO_SIMULTANEAS=1 ./torneo jugar iacasitegano montecarlo --partidas 40 --semilla SEMILLA -v
```

Usar la gestión de energía ya autorizada para evitar reposo durante la medición. No continuar una partida atravesada por reposo. Si hay interrupción externa, conservar y excluir el bloque completo, registrar motivo antes de repetirlo entero en carpeta nueva. No excluir fallos técnicos del bot: cuentan en el balance y deben describirse. Nunca duplicar JSON.

Sin parada por ventaja ni ampliación por resultado estrecho. Se puede detener por infraestructura o fallo de seguridad para diagnosticar; no reanudar una versión corregida dentro de la misma serie. Una modificación requiere otro protocolo.

## Métricas y filtro de desarrollo

- **Primaria:** victorias/puntos de liga sobre las 80 partidas de cada versión. Reportar `V_B − V_A` y diferencia de porcentajes; el denominador es 80 por versión, no 160.
- Por semilla y color: victorias/derrotas, peones anotados/concedidos, motivos, errores, ilegales, timeouts y salidas; reloj propio y rival, media/máximo. Preparación exacta y memoria pico solo si realmente medidas.
- Pasa a propuesta de confirmación si B obtiene **al menos 8 victorias adicionales sobre 80** (+10 puntos porcentuales), gana **más de 40/80** y su diferencia de victorias frente a A no es negativa en ninguna de las dos semillas. Cero fallos técnicos propios y límites oficiales cumplidos.
- Este es un filtro práctico fijado antes de jugar, **no un umbral de significancia ni derivado de la mediana A/A**. Un fallo del filtro significa no avanzar esta versión; no demuestra equivalencia ni inferioridad general.
- El A/A mostró 3–5 victorias de diferencia entre repeticiones de 40 y todas las R2 peores. Alternar el orden reduce una fuente de sesgo, pero no garantiza igual carga, temperatura o duración. Misma semilla no fija las jugadas de un oponente a reloj.
- No usar el diferencial de peones para rescatar un candidato que falle la métrica primaria. No afinar pesos, temperatura o umbrales tras ver resultados.

## Confirmación y promoción

Reservas propuestas para una etapa posterior: **20261111–20261114**. No ejecutarlas en esta tarea; tampoco usar 20261102–20261104, reservadas por el experimento antiguo. Semilla técnica separada: 20261115. Comprobar que no existan resultados previos para las semillas nuevas antes del primer bloque; si están usadas, detener preparación y documentar el conflicto, sin elegir reemplazos mirando sus resultados.

Si pasa el filtro, conservar B intacto y reportar. Antes de confirmación fijar muestra, orden, métricas y criterios propios; incluir una comparación con el bot principal original para no atribuir una ganancia a la TT sin medirla. No promover, editar el informe oficial, hacer commit, merge o push por esta tanda de desarrollo.

## Trabajo paralelo

- Codex de terminal: dueño de compilaciones pendientes, preparación, árbitro y medición; crear sus arneses en una carpeta de medición externa al código congelado. Actualizar únicamente esta nota con resultados y enlazar artefactos; evitar sobrescribir `01-Estado.md` mientras otro agente lo edita.
- Chat director: candidato y oráculo preparados; análisis de procedencia/receta del modelo y revisión posterior de trazas. Durante las partidas, solo lecturas ligeras: sin entrenar, compilar, buscar posiciones o lanzar benchmarks. No modificar A/B mientras se estén midiendo.

Evidencia técnica previa: [[2026-10-27-Utilidad-victoria]], [[2026-10-27-TT-exactitud]]. Resultados de esta serie: pendientes, cero partidas ejecutadas al fijar el protocolo.

<!-- CODEX_RESULTADOS_INICIO -->
## Ejecución y evidencia de Codex

Estado: **serie completada**. Desarrollo válido: **160/160**; técnicas B: **4/4**, fuera de la métrica de fuerza.

| Versión | Semilla | Blancas V–D | Negras V–D | Victorias |
|---|---:|---:|---:|---:|
| A | 20261109 | 8–12 | 14–6 | 22 |
| A | 20261110 | 8–12 | 11–9 | 19 |
| B | 20261109 | 12–8 | 14–6 | 26 |
| B | 20261110 | 9–11 | 13–7 | 22 |

Total: **A 41/80; B 48/80**. B − A: **+7 victorias, +8.75 puntos porcentuales**. Diferencias por semilla: {'20261109': 4, '20261110': 3}.
Filtro fijado: **NO PASA**. Detalles de cada criterio y seguridad en la evidencia. Sin promoción ni ejecución de reservas.

Se conservan **59 JSON** de intentos excluidos/incompletos, separados de las métricas: interrupción del supervisor, falso positivo de ruta equivalente Docker Desktop, carga externa de GRIS y reposo por cierre de tapa. Cada repetición es de bloque completo, sin seleccionar por resultado. Motivos y hashes en progreso.json.

GRIS se pausó por autorización explícita del usuario; ya fue reanudado al terminar la serie. Su estado y restauración quedan en pausa_gris.json. La prevención de reposo por inactividad no impidió el reposo forzado por cierre de tapa.

Preparación: A, tres frías nuevas (máximo 0.044651417 s); B, tres del mismo protocolo reutilizadas tras comprobar identidad (máximo 0.372180125 s). Validador A en log propio; compilación/oráculo y entrega B reutilizados de VALIDACION.md. Preparación exacta por partida y memoria pico: **sin medir**.

- [Resultados, peones, motivos, relojes y hashes](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/utilidad_victoria_20261028_codex/RESULTADOS.md>)
- [Resumen recalculado desde JSON](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/utilidad_victoria_20261028_codex/resumen.json>)
- [Progreso, exclusiones y rutas canónicas](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/utilidad_victoria_20261028_codex/progreso.json>)
- [Manifiesto previo de participantes e imágenes](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/utilidad_victoria_20261028_codex/manifiesto.json>)
- [Recuperación y arneses externos](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/utilidad_victoria_20261028_codex/RECUPERAR.md>)

A/B, rival y árbitro permanecen congelados; no se editaron fuentes, pesos, cachés ni informe oficial, ni se hicieron commit, merge o push.
<!-- CODEX_RESULTADOS_FIN -->
