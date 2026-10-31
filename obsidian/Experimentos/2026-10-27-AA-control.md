---
tipo: experimento
estado: completado
fecha: 2026-10-27
baseline_commit: 85b2d55
---

# Variación A/A del control

## Hipótesis falsable

Las repeticiones del mismo control a reloj muestran variación de puntos netos. Hipótesis previa: mediana de diferencias absolutas ≥6 puntos por bloque de 40. Esto no mide una mejora del bot.

## Cambio aislado

Ninguno. Worktree existente `codex/tiempo-carreras-control`, HEAD `85b2d55`; fuentes, pesos, libro y árbitro verificados contra el commit. Hay 25 archivos derivados de caché Numba modificados previamente; se conservan y se congelan por hash. No se regeneran cachés del participante ni se cambia el informe oficial.

## Protocolo fijado antes de medir

- Rival: Montecarlo del mismo commit; mismo control en las seis ejecuciones.
- Orden serial: 20261105 R1, R2; 20261106 R1, R2; 20261107 R1, R2.
- 40 partidas por bloque, 20 por color, alternando y emparejando 20 juegos de dados. Total fijo: 240; sin parada por resultado ni ajuste.
- Docker y árbitro oficiales: reloj 30 s, preparar 10 s, 1 CPU, 1024 MiB por bot, escala 1.0. CLI jugar secuencial, nice 19 y TORNEO_SIMULTANEAS=1. Mismas imágenes por ID y todos los archivos del participante congelados.
- Semillas 20261031 y 20261101–20261104 excluidas. Reservas previas intactas.
- Métrica principal: por semilla, |neto R2 − neto R1|, donde neto = puntos propios − puntos Montecarlo; mediana de las tres diferencias.
- Seguridad: motivos, errores, ilegales, timeouts, salidas y relojes total/por color. Preparar exacto y pico de memoria no se guardan en el JSON oficial; no se inventan ni se mezclan con pruebas históricas.
- Si falla infraestructura o faltan JSON, conservar evidencia y detener la serie para revisar; los fallos técnicos de partidas se cuentan y se informan.

## Artefactos y comandos

- Evidencia y arnés externo: `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806`. JSON originales en el worktree de control; rutas exactas en `progreso.json` y `resumen.json`.
- Comando por bloque: `rtk nice -n 19 ./torneo jugar iacasitegano montecarlo --partidas 40 --semilla SEMILLA -v`.
- Docker estaba detenido al inicio; arrancado antes de medir. macOS recién iniciado con indexación Spotlight visible; se registran muestras de carga al inicio/final de cada bloque. Sin entrenamiento o compilación propios concurrentes. No se garantiza carga/temperatura idéntica ni determinismo bajo reloj.

## Resultado

| Semilla | Neto R1 | Neto R2 | Diferencia absoluta |
|---|---:|---:|---:|
| 20261105 | +54 | +33 | 21 |
| 20261106 | +11 | -13 | 24 |
| 20261107 | +4 | -6 | 10 |

**Métrica principal: mediana = 21 puntos netos por bloque de 40.**

| Bloque / color | V–D | Puntos propios–rival | Neto | Reloj propio medio / máx. (s) | Reloj rival máx. (s) |
|---|---:|---:|---:|---:|---:|
| 20261105 R1 / total | 28–12 | 103–49 | +54 | 15.397 / 18.207 | 19.555 |
| 20261105 R1 / blancas | 13–7 | 50–26 | +24 | 15.797 / 18.207 | 19.555 |
| 20261105 R1 / negras | 15–5 | 53–23 | +30 | 14.996 / 17.311 | 19.247 |
| 20261105 R2 / total | 25–15 | 95–62 | +33 | 14.853 / 18.435 | 19.695 |
| 20261105 R2 / blancas | 14–6 | 50–27 | +23 | 15.253 / 18.435 | 19.289 |
| 20261105 R2 / negras | 11–9 | 45–35 | +10 | 14.454 / 17.735 | 19.695 |
| 20261106 R1 / total | 19–21 | 85–74 | +11 | 15.210 / 18.724 | 19.789 |
| 20261106 R1 / blancas | 11–9 | 47–34 | +13 | 15.442 / 18.494 | 19.554 |
| 20261106 R1 / negras | 8–12 | 38–40 | -2 | 14.977 / 18.724 | 19.789 |
| 20261106 R2 / total | 15–25 | 75–88 | -13 | 14.568 / 17.693 | 19.015 |
| 20261106 R2 / blancas | 6–14 | 33–46 | -13 | 14.699 / 17.693 | 19.015 |
| 20261106 R2 / negras | 9–11 | 42–42 | +0 | 14.438 / 17.033 | 18.893 |
| 20261107 R1 / total | 20–20 | 82–78 | +4 | 14.736 / 17.790 | 19.192 |
| 20261107 R1 / blancas | 12–8 | 43–37 | +6 | 14.536 / 17.790 | 19.192 |
| 20261107 R1 / negras | 8–12 | 39–41 | -2 | 14.935 / 17.474 | 19.016 |
| 20261107 R2 / total | 15–25 | 78–84 | -6 | 14.044 / 17.834 | 19.148 |
| 20261107 R2 / blancas | 6–14 | 35–44 | -9 | 13.630 / 16.666 | 19.148 |
| 20261107 R2 / negras | 9–11 | 43–40 | +3 | 14.458 / 17.834 | 18.919 |

## Seguridad, relojes y limitaciones

- 240/240 JSON verificados por semilla, juego y color; emparejamiento de las dos repeticiones completo. Reconstrucción independiente de legalidad y puntos: 240/240.
- Fallos técnicos de partidas (ambos bots): **0**. Salidas no vacías: **0**. Motivos exactos por bloque en `resumen.json`.
- Reloj propio máximo: **18.724 s**; Montecarlo: **19.789 s**, límite 30 s. Duración total de cada bloque y muestras de carga: JSON de ejecución.
- Preparación: límite oficial 10 s; duración exacta por partida no registrada por el formato oficial. Pico de memoria no medido. No se sustituyen estas medidas con pruebas históricas.
- Tres semillas y una sola pareja de repeticiones por semilla: estimación descriptiva limitada de variación, sin intervalo fiable ni atribución causal individual. Semilla idéntica no fija profundidad, rollouts ni jugadas bajo reloj.
- Bloques y partidas ejecutados en serie, sin entrenamientos o compilaciones propios concurrentes. Misma configuración e imágenes por ID, pero carga, temperatura y planificación del host pueden variar; Spotlight activo al inicio. No hay aislamiento físico exclusivo de la máquina.
- Docker estaba detenido al preparar el experimento; las consultas iniciales fallaron por socket ausente. Se inició Docker Desktop antes del primer bloque; esto no es un fallo del bot ni una partida adicional.
- No se reutilizaron 20261031 ni 20261101–20261104. No se modificó el criterio ni se reabre el experimento de la variante.

## Evidencia primaria

- 20261105 R1: [40 JSON e índice](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_18-06-49/index.html); log `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806/20261105_R1.log`; duración 1452.0 s; 2026-10-27T18:06:47.358551-06:00 → 2026-10-27T18:30:59.499165-06:00.
- 20261105 R2: [40 JSON e índice](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_18-31-01/index.html); log `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806/20261105_R2.log`; duración 1393.5 s; 2026-10-27T18:30:59.862378-06:00 → 2026-10-27T18:54:13.270303-06:00.
- 20261106 R1: [40 JSON e índice](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_18-54-15/index.html); log `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806/20261106_R1.log`; duración 1396.9 s; 2026-10-27T18:54:13.687000-06:00 → 2026-10-27T19:17:30.584667-06:00.
- 20261106 R2: [40 JSON e índice](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_21-16-21/index.html); log `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806/20261106_R2_reinicio1.log`; duración 1311.3 s; 2026-10-27T21:16:20.426753-06:00 → 2026-10-27T21:38:11.866410-06:00.
- 20261107 R1: [40 JSON e índice](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_21-38-12/index.html); log `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806/20261107_R1.log`; duración 1321.0 s; 2026-10-27T21:38:12.079446-06:00 → 2026-10-27T22:00:13.209288-06:00.
- 20261107 R2: [40 JSON e índice](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_22-00-14/index.html); log `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806/20261107_R2.log`; duración 1280.0 s; 2026-10-27T22:00:13.414726-06:00 → 2026-10-27T22:21:33.419256-06:00.

## Pausa, recuperación y exclusiones

- Se preservaron los tres bloques completos anteriores al reposo: 20261105 R1/R2 y 20261106 R1. Sus 120 JSON, hashes, puntos y legalidad se validaron antes de retomar. Docker y procesos anteriores sin actividad al reanudar.
- El intento original 20261106 R2 se interrumpió por solicitud del usuario a las 19:29:27 del 2026-10-27 (salida 130). Contiene 20 JSON completos; se excluye íntegro de la métrica y se conserva con su log. La partida 21, semilla 20261106/pareja 0/juego 10, control blanco, quedó incompleta sin JSON final. Docker registró el cierre de sus contenedores. No se interpreta como fallo del bot.
- Se repitió únicamente ese bloque completo en carpeta nueva y log `20261106_R2_reinicio1.log`, seguido de los dos bloques 20261107. La métrica usa exactamente seis bloques aceptados y 240 partidas, sin sumar ni duplicar los 20 resultados excluidos. Se conservan 260 JSON terminados en total más la evidencia de la partida interrumpida.
- Al retomar, Docker listaba las imágenes originales pero sus etiquetas devolvían «No such image». Se reasignaron las cuatro etiquetas a los IDs originales y se verificaron antes de jugar. Sin reconstruir imágenes ni incorporar prototipos. `fallo_reanudacion.json` registra esa comprobación previa; `fallo_arnes.json` corresponde a la pausa solicitada. Ninguno es un fallo en las 240 partidas aceptadas.
- La pausa rompe la continuidad temporal de la medición. `reposo_host.log` conserva eventos del host; configuración, fuentes, pesos e IDs de imágenes se mantienen, pero carga y temperatura antes/después del reposo no están controladas.
- Auditoría final de eventos de energía: ningún bloque aceptado se solapa con intervalos de reposo del host (`auditoria_reposo.json` y `reposo_host_final.log`).
- Respaldo previo a la reanudación: `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806/checkpoint_antes_reanudar.tar.gz`. Avance original: `progreso_antes_pausa.json`; exclusión con hashes y resumen parcial por color: `intento_interrumpido_excluido.json`; validación: `validacion_checkpoint.json`; cierre Docker: `eventos_interrupcion.jsonl`; recuperación: `reanudacion_inicial.json`; instrucciones: `RETOMAR.md`.

- Agregado, hashes iniciales, muestras de carga, comandos exactos y validación: `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/aa_control_20261027_1806`.
- `ejecutar.py` es un arnés externo; `cerrar.py` recalcula la métrica directamente desde los JSON y usa el analizador existente para reconstruir legalidad y puntos. No importa el motor ni ejecuta búsquedas.

## Decisión

### Revisión independiente posterior de este chat

Se recalcularon los seis bloques desde sus 240 JSON aceptados: metadatos de semilla/juego/color, 20 juegos por color y repetición, ausencia de duplicados, motivos y salidas. Se confirma la mediana de 21 peones netos. Las diferencias de **victorias R2−R1** fueron −3, −4 y −5; mediana absoluta **4 victorias por bloque de 40**, como diagnóstico secundario, sin cambiar el protocolo principal. Total descriptivo: 122 victorias y 118 derrotas.

Las tres R2 salieron peor en victorias y peones netos. Con este orden serial y solo tres parejas no se distingue azar de deriva temporal/carga/temperatura. No interpretar 21 o 4 como umbral universal ni como estimación precisa de varianza. Para próximas comparaciones considerar alternar el orden control/candidato y ampliar muestra; fijar criterios antes de observar resultados. El experimento previo de carreras conserva su decisión histórica.

Medición A/A completada. La hipótesis descriptiva previa de mediana ≥6 se observa en estas tres semillas. **El valor mide variación del control; no acredita una mejora del bot ni demuestra la causa del resultado de la variante.**

Fuentes, pesos, libro, cachés preexistentes y todos los archivos versionados del control permanecen con los hashes iniciales. Los archivos versionados del checkout principal se verificaron sin cambios durante la etapa reanudada; se conservan los cambios previos del usuario. Se conservan los dos worktrees, resultados anteriores, 240 JSON aceptados y 20 excluidos. Informe oficial intacto; sin promoción, commit, merge o push.

Cierre verificado: 2026-10-27T22:30:54.630456-06:00. Sin mediciones pendientes de esta serie.
