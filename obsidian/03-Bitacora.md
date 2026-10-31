---
tipo: bitacora
proyecto: BreakthroughBotIA
actualizado: 2026-10-27
---

# Bitácora breve

## 2026-10-27 — Se prepara memoria para Obsidian

- Se crea esta bóveda en el repositorio para que el equipo y los agentes puedan encontrar el estado y las decisiones.
- Snapshot inicial: rama principal de trabajo `integracion-tier1-2` en `9d3f829`; Codex seguía activo en otra terminal/worktree según el texto compartido.
- Pendiente registrar el cierre del caché horneado y del estimador de reloj a partir de sus resultados completos.
- Fuentes: [[01-Estado]], [[PLAN_TIER_5]], [[estudiantes/iacasitegano/INFORME]].

## 2026-10-27 — Cierre del caché y del reloj adaptativo

- Caché Numba horneado fast-forward a `integracion-tier1-2` en `85b2d55` (incluye `dce1876`). La tanda fría fue 20/20 bajo carga; la liga real fue 10–10/20, sin fallos técnicos. Se acepta por fiabilidad de `preparar()`, sin afirmar mejora de fuerza.
- El reloj adaptativo se rechaza tras 100 partidas por variante: 43–57 candidato, 55–45 base; 22–10 para la base en resultados pareados discordantes. El ahorro de reloj redujo también la profundidad media.
- Quedan cambios de documentación y una prueba Docker local sin seguimiento; revisar antes de preparar entrega. No se hizo commit.
- Fuente del cierre: reporte de Codex compartido por Jose; diff del checkout verificado. Experimento de reloj en `/Users/josema/noche_salida/lab/margen_reloj_adaptativo.md`.

## 2026-10-27 — Revisión del estado de entrenamiento

- Se encontró `candidato_20261024_042150.npy`; `pesos.npy` comparte tamaño de 176 bytes y hora de modificación 2026-10-26 15:38.
- El contenedor `iacasitegano-entrenar-20261023` terminó con `Exited (0)`. Los logs confirman 300/300 partidas (100 por semilla: 1234, 5678, 9012), 14,118 posiciones y guardado del candidato; indican que `pesos.npy` no se modificó.
- El hash del candidato y `pesos.npy` coincide (`d5cc25...570064f`). `INFORME.md` registra una evaluación previa bajo el árbitro de 40 partidas: 22–18, puntos 87–72, sin fallos; luego se promovió.
- El código activo carga `pesos_eval3_ligero.npz`, no `pesos.npy`; el candidato lineal ya es histórico y no afecta la estrategia vigente. Próximo paso: establecer baseline de al menos 40 partidas de la estrategia activa contra `montecarlo` bajo Docker. El checkout continúa en `integracion-tier1-2` (`85b2d55`); la salida de `main` con renombres staged pertenece a otro estado del terminal compartido.

## 2026-10-27 15:15 — Baseline oficial de la estrategia activa

- Checkout confirmado antes y después: `integracion-tier1-2`, `85b2d55`; se conservaron los cambios locales. `strategy.py` carga `data/pesos_eval3_ligero.npz` mediante `busqueda_eval3` (SHA-256 `37678d0b…c2250b`).
- Comando: `rtk ./torneo jugar iacasitegano montecarlo --partidas 40 --semilla 20261031 -v`, Docker y árbitro oficial, 30 s de reloj / 10 s de preparación, ambos colores.
- Resultado iacasitegano–montecarlo: **21–19, puntos 87–75**. Con blancas: **14–6, puntos 48–31**; con negras: **7–13, puntos 39–44** (20 partidas por color).
- Reloj propio máximo: **18.466 s** (blancas 18.466, negras 17.561); media 14.868 s. Las 40 terminaron por puntos; 0 fallos de preparar, errores, ilegales o timeouts en ambos bots y todas las salidas vacías. **La duración exacta de preparar no se registra en la salida ni en los JSON; queda sin medir**, aunque todas las preparaciones cumplieron el límite de 10 s.
- Evidencia primaria: [[resultados/2026-10-27_14-49-49/index.html]] y sus 40 JSON; log completo en `/Users/josema/noche_salida/lab/baseline_40_20261031.log`. Baseline de una semilla, sin inferir una mejora ni promover nada. No se cambió código/pesos ni se hizo commit, merge o push.

## 2026-10-27 — Análisis de las 40 partidas, sin nuevos juegos

- Clasificación de derrotas: 11 remontadas rivales tras ventaja propia, 7 sin ventaja propia y 1 empate 2–2 sin ventaja previa; todas por puntos. Conversión al llegar primero a dos puntos: blancas 13/15, negras 6/13.
- Cautela: 20 pares reutilizan dados por color; blancas ganó 107 combates frente a 83.95 esperados y negras 95 frente a 96.40. La brecha de color no prueba un fallo de apertura.
- Una hipótesis propuesta: piso de presupuesto cuando ≥2 peones rivales estén a ≤2 filas de anotar; medir mejora de puntos totales frente a control pareado, con validación reservada y sin fallos técnicos. Sin cambiar código, pesos o informe ni correr partidas.
- Análisis y JSON enlazados: [[Experimentos/2026-10-27-Analisis-baseline-40]].

## 2026-10-27 16:25 — Piso de tiempo ante carreras: no pasa desarrollo

- Experimento aislado desde `85b2d55`: control y variante mantienen `estudiantes/iacasitegano/` en sus worktrees; solo ocho líneas de reparto de tiempo cambian, más la regeneración de cachés derivados. Equipo original y cambios locales conservados.
- Árbitro oficial/Docker, semilla nueva `20261101`, 40 por versión: control **21–19, 91–69 puntos (+22)**; variante **23–17, 93–77 (+16)**. Δ neto **−6**, frente al requisito prefijado ≥+6. Blancas Δ0, negras Δ−6. Se rechaza en desarrollo, sin usar las semillas reservadas ni ajustar el umbral.
- 80/80 por puntos, cero fallos técnicos oficiales. Reloj propio máximo: control 17.419 s, variante 18.405 s. Cinco preparaciones frías separadas por versión: máximos 0.033/0.073 s, todas correctas; duración real de preparación por partida no registrada. El validador del control avisó de un timeout en su prueba reducida de 3 s contra random; se registra aparte.
- Más profundidad local y más victorias no bastaron para mejorar puntos. Conversión, métricas por color, JSON y limitaciones: [[Experimentos/2026-10-27-Tiempo-carreras]]. Sin promoción, edición del informe oficial, commit, merge o push.

## 2026-10-27 — Revisión causal del experimento de carreras

- Lectura pareada: 40/40 primeras divergencias son de Montecarlo, en plies 1–5 y antes del piso. Hay 30 decisiones buscadas propias en prefijo compartido, ninguna con presupuesto extra; no se observa un efecto directo comparable sobre jugada o profundidad. Con negras, 018 y 020 cambian puntos aunque la regla nunca actúa.
- El −6 negro se descompone en +8 al convertir tres derrotas, −7 por dos victorias perdidas, −5 en victorias compartidas y −2 en derrotas compartidas. Es descripción del balance, no atribución causal.
- Única hipótesis nueva: medir ruido A/A del control; mediana de diferencia absoluta de puntos netos ≥6 por bloque de 40, con tres semillas nuevas repetidas. Solo propuesta. No se usan reservas ni se ajusta la hipótesis rechazada.
- Evidencia, activaciones y ejemplos: [[Experimentos/2026-10-27-Revision-pareada-tiempo-carreras]]. Fuentes y worktrees conservados; sin cambios de código, partidas, promociones ni commits.

## 2026-10-27 — Auditoría de entrega durante la corrida A/A informada por Jose

- Revisión estática en `integracion-tier1-2`, `85b2d55`; no se iniciaron partidas ni compilaciones. No se verificó el proceso A/A.
- Pendientes: receta/generador del modelo eval3 activo ausente de la carpeta del equipo; informe de ~4,326 palabras frente a 2–4 páginas; aclarar distribución del caché Numba compilado y su portabilidad.
- Inventario y acciones concretas en [[04-Preparacion-entrega]]. Solo se modificó memoria de proyecto; código, pesos e informe oficial conservados.

## 2026-10-27 — Prototipo de búsqueda mientras corre el A/A informado por Jose

- Se creó un worktree aislado en `/Users/josema/.codex/worktrees/hojas-sin-duplicado/BreakthroughBotIA`, desde `85b2d55`, para eliminar generación repetida de jugadas en hojas con quiescencia apagada.
- Cinco líneas; 1,152 comprobaciones de rutas Python con auxiliares simuladas, sin diferencias. No es validación de motor real/Numba ni prueba de velocidad; quedan pendientes al cierre del A/A. Sin partidas, entrenamiento, promoción o commit.
- Se corrige el criterio para futuros experimentos: victorias/puntos de liga como métrica de fuerza primaria; diferencial de peones secundario. Los criterios históricos se conservan.
- Detalle y oportunidades de TT: [[Experimentos/2026-10-27-Hojas-sin-duplicado]].

## 2026-10-27 — Validación ligera de hojas y caso de exactitud TT

- Hojas: 96 comprobaciones con motor/eval3 reales y JIT apagado, sin diferencias; arnés de diferencial compilado/benchmark preparado, sin ejecutar esos modos.
- TT: posición válida y profundidad 2, ventana estrecha seguida de amplia reutilizando tabla: original devuelve 210.203 frente a referencia prácticamente 0. Ventanas deliberadas; frecuencia real desconocida. Corrección conservadora separada en `/Users/josema/.codex/worktrees/tt-cotas-exactas/BreakthroughBotIA`.
- Diez casos de ventanas, original falla dos/corregido ninguno; oráculo exhaustivo y comprobación de aborto. Sin Numba, nuevas partidas, entrenamiento, regeneración de caché, commit o promoción. Pendientes compilación/diferencial amplio/integración tras A/A.
- Fuentes y comandos: [[Experimentos/2026-10-27-TT-exactitud]] y [[Experimentos/2026-10-27-Hojas-sin-duplicado]].

## 2026-10-27 — Buffers y utilidad de victoria, desarrollo paralelo sin JIT

- Se prepararon dos candidatos independientes desde `85b2d55`: reutilización de buffers en `/Users/josema/.codex/worktrees/buffers-busqueda/BreakthroughBotIA` y transformación logística/terminales ±1 en `/Users/josema/.codex/worktrees/utilidad-victoria/BreakthroughBotIA`.
- Buffers: 64 comparaciones reales sin JIT, cero diferencias en valores/jugadas/nodos/abortos, entradas intactas; menos llamadas explícitas a reservar arrays en un fixture. Sin medición de velocidad.
- Utilidad: entrenador logístico localizado y NPZ original coincide por hash. Diez hojas, cuatro terminales y ocho raíces contra oráculo con utilidad nueva, sin fallos; siete posiciones de trazas vistas a profundidad 1 no cambiaron de jugada. Sin evidencia de fuerza.
- No hubo compilación, nuevas partidas, entrenamiento, cambios al principal ni commit. Validar TT primero tras A/A, después probar cada hipótesis con control común y victorias como métrica principal.
- Detalle: [[Experimentos/2026-10-27-Buffers-busqueda]], [[Experimentos/2026-10-27-Utilidad-victoria]].

## 2026-10-27 — Cierre A/A contrastado y validaciones compiladas

- Se recalcularon los 240 JSON aceptados del A/A: mediana absoluta 21 peones netos, y secundariamente 4 victorias (diferencias R2−R1: −3/−4/−5). Tres parejas, todas R2 inferiores: descripción limitada, sin demostrar causa ni umbral universal.
- Con Docker sin actividad se validó TT en la imagen oficial: 10 casos originales, 192 ventanas adicionales y 15 raíces de prof. 1–3, cero fallos de corrección. Caché del candidato regenerado, validador de entrega aprobado (avisos de importación dinámica offline), 3 preparaciones frías máximo 0.017623 s.
- Cuatro partidas técnicas TT vs Montecarlo, semilla 20261108: 1–3/peones 8–10, máximo propio 16.655153 s, todas por puntos y sin fallos técnicos. No mide fuerza ni implica promoción.
- Los otros arneses también pasaron con Numba. Microbenchmarks exploratorios: hojas ratio 1.019199 y buffers 1.011176, paneles pequeños y resultados modestos. Priorizar utilidad de victoria frente a perseguir porcentajes de velocidad no confirmados.
- Logs/protocolos: `/Users/josema/.codex/worktrees/tt-cotas-exactas/BreakthroughBotIA/resultados/medicion/tt_validacion_20261027/`. Próximo: fijar control y candidato con la misma TT corregida antes de medir fuerza de utilidad. Principal intacto; sin commit, merge o promoción.

## 2026-10-28 — Utilidad con TT común y encargo de medición

- Corrección TT idéntica en control/candidato, comprobada por AST. NPZ y estrategia iguales; B SHA `83997dd323509bbfc2edd92de46a81a3770a6f1d5603daa730352ed56303277e`.
- Python/Numba oficial: 10 hojas, 4 terminales, 12 raíces hasta prof. 3 y 72 consultas con TT reutilizada, cero diferencias. Caché B regenerado; validador aprobado con aviso de timeout reducido a 3 s. Tres arranques fríos: 3/3, máximo importación+preparar 0.372181 s; memoria pico no medida.
- Protocolo fijado: 4 partidas técnicas (20261115) y 160 de desarrollo (80 por versión), semillas 20261109/10, orden A/B y B/A; primaria victorias. Filtro práctico +8/80, mayoría y ninguna semilla negativa; no es prueba estadística. Reservas 20261111–14 sin usar.
- Codex de terminal: medición exclusiva y arnés recuperable. Este chat: preparación técnica, lectura de receta/modelo y revisión posterior sin carga pesada concurrente. [[Experimentos/2026-10-28-Protocolo-utilidad-victoria]], [[2026-10-28-Encargo-Codex]]. Sin partidas nuevas, promoción, commit o cambios al bot principal.

## 2026-10-28 — Criterios de cierre y diagnóstico iniciado

- [[05-Cierre-de-fases]] concreta ocho fases y las prioridades pedidas: utilidad, contrafactuales, receta/calibración/modelo y jugada TT. Cerradas 0/1 en baseline y 3/4 con rechazo; 2 reabierta y 5/6/7 pendientes. Informe híbrido contrastado directamente en rama `codex/fase4-hibrida`, revisión `750b6c8`: reservado híbrido 24–16/base 29–11; no se integra.
- Extractor offline nuevo: replay oficial sin JIT de 40 JSON/3,231 plies, final y probabilidades correctos; 282 casos distintos y legales (143 B/139 N), 20 grupos de pares. No se ejecutó búsqueda ni se identificaron aún errores de decisión. Artefactos en `resultados/medicion/diagnostico_decisiones_20261028_baseline40/`; [[Experimentos/2026-10-28-Diagnostico-decisiones]].
- NPZ de ablación final `noche_salida/lab/_pesos_ligero5_solo_puntos_patrones_filas_marcador.npz` coincide byte a byte con el activo; modelo `ligero5_solo_puntos_patrones_filas_marcador`, pesos 275/crudo 267. Aún falta la receta completa.
- Hallazgo de diseño TT: un acierto exacto ya retorna directamente; el experimento de pistas debe aprovechar nodos con cotas u otras profundidades y mantener separada su semántica. Sin cambio al buscador, al NPZ o a las variantes congeladas; sin partidas, entrenamiento, commit, merge o promoción.

## 2026-10-28 — Investigación externa y planificación de entrega

- Página del profesor y reglas/FAQ/calificación oficiales leídas: los tiers tienen las mismas restricciones, el entrenamiento offline admite cualquier herramienta y la referencia se supera por puntos totales de liga. Se revisaron fuentes primarias de Logistello, MCTS/minimax en Breakthrough, evolución/CMA-ES, VIPER, PSRO, TDLeaf y pruebas de motores; repositorios OpenSpiel, Breakthrough académico, Fishtest/SPSA. No se encontró una solución verificada idéntica a nuestra variante y límites.
- Se conserva expectiminimax como línea principal. Propuestas nuevas: patrones condicionados por marcador, profesor offline con estudiante pequeño, selección activa de datos y simetría; validar contra familias de rivales reservadas. No repetir como nuevas las mezclas de rollouts o preferencias rechazadas. Detalles, fuentes, condiciones de rechazo y calendario en [[06-Investigacion-y-plan-semanal]].
- Jose confirma fecha 4 de noviembre, sesiones 1 h/7 h y posible escritorio Windows, i5 aproximadamente 8.ª, 16 GB RAM y RX 570. Plan por CPU; configuración y hora exacta de entrega pendientes. Congelar el 3 de noviembre. No se inició entrenamiento ni se verificó el estado actual de la corrida de terminal.
- Checkout principal `integracion-tier1-2`/`85b2d55`, cambios existentes conservados. Solo memoria del proyecto modificada; ningún cambio de algoritmo/pesos/protocolo congelado, partida, compilación, promoción, commit, merge o push.

## 2026-10-28 — Plan definitivo autorizado, utilidad cerrada y panel congelado

- Jose autoriza incorporar investigación, regresión lineal, genéticos, profesor offline y cómputo de escritorio al cierre de fases. [[07-Plan-definitivo]] fija responsables, dependencias, presupuestos y criterios de cierre 2/5/6/7, explicita integración 8 y abre 9 como última fase de pruebas/pulido. [[08-Escritorio-y-entrenamiento]] define preparación Windows/WSL y paquetes; no hay acceso ni entrenamiento iniciado en el escritorio.
- Se verificaron por lectura y hash los 164 JSON válidos del informe de Codex: A 41/80, B 48/80, +7 total (+4/+3 por semilla), cero fallos. 5A se cierra sin promoción, respetando +8 exigido. Reservas no ejecutadas. Máximos de reloj A/B 18.540077/20.299246 s; preparación por partida y memoria pico siguen sin medir. Evidencia en `BreakthroughBotIA-codex/resultados/medicion/utilidad_victoria_20261028_codex/`.
- Herramienta offline nueva `seleccionar_panel_decisiones.py`: 24 estados congelados por metadatos, 8 por categoría/12 por color/20 grupos; manifest y panel en `resultados/medicion/panel24_decisiones_20261028/`, SHA `1ca5a56679eda76a6c38e32851e4a5121b89f256e5bd675ad436c0abc00cbc48`. No son errores comprobados; contrafactuales pendientes.
- Encargo listo [[2026-10-28-Encargo-Codex-fase2]], no enviado ni ejecutado. Sin partidas, compilaciones, entrenamiento, cambios al algoritmo o pesos activos, promociones, commit, merge o push en esta sesión. Cambios previos conservados.

## Plantilla para nuevas entradas

```markdown
## YYYY-MM-DD — Título
- Cambio/decisión:
- Evidencia primaria:
- Resultado y limitaciones:
- Próximo paso:
```

## 2026-10-27 — Variación A/A del control medida

- Control `codex/tiempo-carreras-control`, fuentes/pesos `85b2d55`; seis bloques oficiales Docker seriales, 40 partidas y 20 por color cada uno. Semillas nuevas 20261105, 20261106 y 20261107, dos repeticiones cada una.
- Diferencias absolutas de puntos netos: 21, 24, 10; **mediana 21** por bloque de 40. Medición de variación del control, sin inferir mejora ni atribuir causalmente el resultado anterior de la variante.
- Fallos técnicos: 0; reloj máximo propio/rival 18.724/19.789 s de 30. Preparación exacta y memoria pico no medidas; carga del host variable, Spotlight activo al inicio. Detalle por color, motivos, relojes y evidencia en [[Experimentos/2026-10-27-AA-control]].
- 240 JSON aceptados y 20 excluidos conservados. El intento parcial 20261106 R2 se detuvo a petición del usuario y se repitió completo tras el reposo, sin duplicar puntos. Recuperación de etiquetas Docker a los mismos IDs; sin prototipos. Fuentes, pesos, cachés e informe oficial intactos; worktrees y artefactos previos preservados; sin promoción, commit, merge o push. Semillas excluidas y reservas sin usar.

## 2026-10-28 — fase 5 nocturna y comienzo de validación oficial

Principal `integracion-tier1-2`/`85b2d55`, fuentes/pesos activos intactos. Receta exacta regenerada (máx. error 1.78e-15); panel 24×3 sin discrepancias ni mala decisión real certificada. Ridge/logística+GA real y simetría conservados sin promoción; profesor profundidad 7 no alcanza cobertura. Generados y verificados 60 episodios/6,417 posiciones contra UCT/agresivo/carrera. Adaptación con prior activo λ100 pasa filtro interno (UCT Brier 0.07072→0.04347, nueve grupos; selección solo dos).

N aislado en `/Users/josema/.codex/worktrees/fase5-adaptacion/BreakthroughBotIA`, fuente `83997d…77e`, NPZ `ab1a59…3718`; U usa la misma fuente y NPZ original. Numba oficial 12 raíces/72 ventanas correcto; 3 arranques fríos y validador por versión pasaron. Serie oficial 4 técnicas seed20261118 +160 desarrollo seed20261116/17 iniciada por este chat a las 23:15; medir resultado en `resultados/medicion/fase5_oficial_20261028/progreso.json`, no inferirlo de esta nota. Filtro congelado N−U≥8/80, N>40, sin semilla negativa y cero fallos. P no participa; no demuestra superar P.

Reparación reversible de etiquetas Docker sobre los mismos IDs existentes, sin build/pull; evidencia `REPARACION_ETIQUETAS.json`. Paquete portátil completo verificado, pendiente probar en Windows. [[Experimentos/2026-10-28-Fase5-datos-modelos]]. Sin commit, merge, push, uso de reservas ni promoción.

### Incidencia CPU y reanudación autorizada

Primer U16: GRIS96.4%CPU detectado por supervisor tras 23 JSON; bloque entero excluido, evidencia preservada. Jose autorizó pausar temporalmente solo GRIS y restaurarlo al terminar; nuevo wrapper/guardián con identidad de PID. Repetición completa con misma semilla, sin tocar modelo/criterios. `REVISION_INTERRUPCION_01.json`, `pausa_gris.json` y `progreso.json` documentan el estado. Prueba de relocalización de receta portátil en Mac correcta durante la ventana detenida; Windows no probado.

## 2026-10-29T01:01:03.080712-06:00 — serie fase5 cerrada sin promocion

164 JSON validos verificados,328 inspecciones de contenedores;23 excluidos por carga externa preservados y respaldados. U 43–37, N 6–74; filtro fallido, ambas semillas N3/40. Cero fallos propios; GRIS restaurado. Principal conserva fuente y NPZ. Diagnostico de transferencia/retencion ejecutado sin entrenamiento; evidencia `fase5_20261028/transferencia_mc/`. Confirmacion19/20/21 no ejecutada. Se compacta01-Estado y conserva version anterior en Archivo. Fase5 sigue abierta; no se declara mejora por Brier.

### Diagnóstico de transferencia ya ejecutado

160 juegos reconstruidos/6,060 estados propios. Evaluando ambos modelos sobre los mismos estados U/MC, Brier agrupado0.22564→0.29647; sobre estados N/MC0.17574→0.69130. Histórico visto sin reponderar0.184665→0.237346. No saturación exacta en raíces analizadas; hojas internas sin instrumentar. Evidencia respalda controles de retención/generalización antes de otro ajuste; no prueba causa única ni acción óptima. [[Experimentos/2026-10-29-Diagnostico-transferencia-y-proximo-ajuste]].

## 2026-10-29T07:30:50.488568-06:00 — GRIS desactivado persistentemente

Jose pidió pausar GRIS definitivamente para evitar interferencia. Identificados tres LaunchAgents con KeepAlive/RunAtLoad; se ejecutó disable y bootout solo para `com.gris.background`, `com.gris.home` y `com.gris.scheduler`. Verificado: desactivados persistentemente, descargados y cero procesos GRIS; plists idénticos por SHA. Se conserva el job de backups. No reactivar por instrucciones antiguas de pausa temporal. Evidencia y comandos reversibles en `resultados/medicion/gris_pausa_persistente_20261029/`. No se modificó el bot.

## 2026-10-29T07:55:22.173587-06:00 — revisión oficial y comprobación random

Principal P sin cambios:20–0 contra random,10 por color,60–1 peones, cero fallos, máximo16.258s, semilla20261201;40 contenedores inspeccionados. No se consumieron reservas previas. Revisión de reglas/calificación/planificador confirma tiers privados y nota por puntos totales de liga. Documentados límites de validación histórica y selección de2 grupos de N; plan PC4 para generación offline, no cuatro escrituras al mismo modelo. Fuentes/evidencia en `revision_oficial_20261029/` y `random_principal_20261029/`. [[Experimentos/2026-10-29-Revision-oficial-validacion-y-PC4]]. Sin cambios al bot ni actualización de sistema/commit.

## 29 de octubre — validación5V, Kubernetes y paquete PC

Petición de Jose: instalar Kubernetes, implementar validación y dejar escritorio preparado. Homebrew: kubectl1.37.2/kind0.33.0, clúster independiente1.37.0 sobre Docker; cuatro tareas correctas. Detenido después y política de reinicio=no; kubeconfig privado fuera del repo. La cola CPU local será la ruta de generación: Kubernetes no añade capacidad de hardware ni sustituye el árbitro.

Implementados lanzador1–4 procesos/checkpoints, MC plano/UCT reforzados offline, preparación por grupos/familia reservada, contrato de validación/retención/test de una exposición y entrenador logístico con prior activo/replay80/20. Siete tests y cadena sintética correctos; cuatro procesos arrancados/parados; dos partidas reanudadas,183 filas verificadas sin errores. Auditoría retrospectiva rechaza N sin abrir test. Estas pruebas no demuestran fuerza.

Paquete final16,936,960bytes/234archivos con hashes comprobados desde extracción limpia en Mac; Windows aún pendiente. [[Validacion-y-laboratorio-PC]] y [[resultados/medicion/infra_pc_20261029/LEEME]] contienen contrato, SHA y órdenes. Fase5 sigue abierta; siguiente: PCinstalación/piloto→datos nuevos→ajuste→puertas→partidas oficiales si pasa. Búsqueda/NPZ principal conservan hashes; sin promoción/commit/push, reservas intactas, GRIS sigue deshabilitado.

## 29 de octubre — fase5 en Mac y Kubernetes; encargo de cierre2

Jose pidió prompt para cerrar2 y trabajo real de5 desde Mac, confirmando terminal Codex parado. Se preparó [[2026-10-29-Encargo-Codex-cierre-fase2]] para certificar rechazo ya medido y distinguir corrección TT pendiente de8; no se envió a otro chat.

Se detectó/fijó cruce potencial entre nuevos datos y replay/retención históricos; contrato purga/registra descartes. Regresión nueva,8tests. Kubernetes Linux:14tests totales, receta exacta sobre77,038posiciones,8partidas funcionales/776filas y replay histórico60/6417sin errores. N archivado rechaza sin test. Tarea3 falló por informe sobre copia de solo lectura y canceló2; conservado, arnés reparado, solo2/3 reintentadas correctamente. Resultados exportados y clúster detenido antes de piloto Mac2trabajadores/2min por sesión con presupuestos reales. Ver estado real del piloto en fuente.

[[resultados/medicion/fase5_mac_k8s_20261029/RESULTADOS]] enlaza fuentes/protocolos y paquete actualizado234entradas. Windows no probado, reservas/modelo principal intactos, ninguna mejora de fuerza declarada ni promoción/commit/push. Fase5 abierta.

Piloto Mac terminado:2procesos con salida0,2partidas completas y2parciales; lote16incompleto y lock liberado. Profundidad7completa solo6/86decisiones de checkpoints (no muestra representativa); predominan5/6. No se cualifica profesor ni se entrena. Reanudar solo con mismo contrato; siguiente decisión tras completar/verificar el piloto.

### Certificación de fase2 recibida — 29/oct

Fase 2 certificada cerrada/rechazada el 29/oct: 60 posiciones, 600 pares/1200 búsquedas, mediana candidato/control 0.982591 >0.95 y diferencia máxima de valor 0; no procede liga. P conserva búsqueda ceba3653 y NPZ 37678d0b; las pistas adb347a1 no se integraron. La corrección TT de A cc888a3c es independiente y sigue pendiente para fase 8: portar/revisar el parche P_a_A_correccion_TT.patch en candidato aislado, conservar las regresiones de ventana estrecha/amplia y repetir seguridad/integración; no declarar que P ya esté corregido. Evidencia: resultados/medicion/cierre_fase2_20261029/CIERRE.md.

Cierre definitivo piloto Mac:16/16episodios,1495filas,8grupos, replay0errores, ambas reanudaciones preservaron SHA de originales. Prof7solo74/750decisiones; predominan5/6. Partición3/3/2grupos insuficiente: no ajustar modelo. Brier MC propio0.2458 con2grupos indica necesidad de población pertinente, sin conclusión deportiva. [[resultados/medicion/fase5_mac_k8s_20261029/RESULTADOS]]. Procesos propios terminados y clúster apagado.

## 29/oct — Docker integrado y lote256de fase5

Jose confirmó cierre2 y pidió Kubernetes visible en Docker, siguiente encargo terminal y continuar5. Se creó porGUI el integrado kind1nodo1.31.1:Active/Ready,4tareasSucceeded; cliente1.31.1 separado/verificado, sin sustituir Homebrew1.37. Externo anterior detenido/conservado. Fuente [[resultados/medicion/docker_integrado_20261029/LEEME]].

Preparado [[2026-10-29-Encargo-Codex-fase6]]. No se pudo enviar: sesiónCLI mantiene bloqueo de escritor; CUA no permite Terminal. Pendiente pegado humano; no ejecución afirmada.

Fase5: automatizado flujo recuperable con hashes y4tests, incluida cadena real sintética y examen una vez. Lote256nuevo iniciado4×64, semillas94–97millones, contrato prospectivo72/24/32grupos, sesión60min. Generación/checkpoints reales verificados; aún sin nuevo modelo entrenado. Al completar datos aplicará receta/puertas previamente fijadas; incompleto pausa. No promoción. [[resultados/medicion/fase5_lote256_mac_20261029/LEEME]]. Caffeinate temporal ligado al PID del flujo, sin cambio de energía persistente. Principal/reservas intactos.

## 29/oct — continuación de fase5 y preparación posterior a selección

Jose confirmó inicio manual de Codex6 y autorizó seguir5. Generación avanza sin cambiar fuentes/semillas/receta; última comprobación41/256. Añadido supervisor que espera sesión60min y reanuda una vez360minsolo en pausa por datos incompletos; no rescata errores/rechazos/interrupciones. Dos tests correctos, incluido subproceso real/idempotencia. SupervisorPID15969 y caffeinate temporal; no crear flujos duplicados.

Nueva puerta funcional: features→logit→utilidad comparados sobre piloto visto;288Python+288Numba, errores5.33e-15/6.66e-16; cambiar y restituir pesos correcto. Cinco entradas incompatibles rechazadas antes de kernels. Activo intacto, sin candidato nuevo aún. [[resultados/medicion/fase5_postseleccion_20261029/LEEME]].

Protocolo deportivo previo fijado:U/Vigual búsqueda, solo pesos distintos; desarrollo160y confirmación160condicional con filtros prácticos, seguridad y ventana exclusiva. Seis semillas revisadas en19worktrees,sin conflictos; repetir antes de congelar. No partidas nuevas ni reservas usadas. Memoria01condensada con archivo íntegro previo para reducir relectura.

## 29/oct — cierre6, prompt7A y cotas tácticas5B

Revisados CIERRE/AUDITORIA_FINAL/MANIFIESTO_FINAL de6:890replays válidos,36,730raíces/35,094únicos, sin cobertura pequeña/≤6y25carreras privadas ya resueltas por guardia.6cerrada/rechazada en alcance, sin solver ni integración. Prompt7Apreparado para auditoría del libro8entradas y generador eval3;7Bespera modelo5. Usuario debe pegarlo; no envío automático afirmado.

Fase5continúa:71/256. La primera hora finalizó0/0/0/0y el supervisor reanudó360minconPID18837, mismo contrato/fuentes. Snapshot de archivos ya finalizados guardado tras el relevo; no se presenta como hash anterior.

Nuevo oráculo intervalar racional, sin modelo, horizonte3y presupuesto por acción sobre8tardíos prefijados del panelvisto.5tests correctos;0dominancias reales demostradas,3observadas alcanzan valor1y5no resueltas. No atribuir errores ni fuerza desde desconocidos; no entrenar ni reajustar usando este diagnóstico. [[resultados/medicion/fase5_cotas_tacticas_20261029/RESULTADOS]]. Principal intacto y test256sin analizar.

## 29/oct — seguimiento del cierre de datos/entrenamiento de5

Jose confirma Codex terminal activo y pide continuar5. Comprobación 2026-10-29T13:33:16-06:00: 91/256episodios,4trabajadores sin salida final, 0fuentes congeladas alteradas. Sin candidato entrenado/aceptado y pesos principales intactos. Activado y verificado seguimiento de este chat cada20min (`revisar-cierre-de-datos-y-validaci-n-fase-5`): comprobar finalización, entrenamiento/selección y examen condicionado; comprobar runtime funcional solo si pasa, sin promoción ni partidas bajo carga. Rechazo/error/plazo agotado detienen seguimiento y se informan sin rescates. Equipo encendido/app abierta necesarios. Receta y fuentes del flujo sin cambios.

## 29/oct — entrega7A revisada y siguiente encargo8A

2026-10-29T13:36:34-06:00: Jose entrega cierre7A de terminal. Leídos certificado/auditoría y verificados SHA de4herramientas,2protocolos y nota.35 regresiones registradas,890trazas/36730raíces,470 coincidencias potenciales de3estados únicos; no inferencia de fuerza. Riesgo de prioridad libro/victoria segura reproducido sin runtime modificado.7sigue abierta. Preparado [[2026-10-29-Encargo-Codex-fase8A]]: copias y parches independientes TT P→A y prioridad de victoria segura, pruebas pequeñas sin JIT, sin integración activa. Pendiente pegado humano; no enviado.5continúa 95/256, fuentes congeladas intactas; el proceso genera/entrena/valida, la automatización solo revisa. Sin cambiar receta, modelo ni reservas.

## 29/oct — pausa del entrenamiento solicitada por traslado

2026-10-29T15:46:48-06:00: Jose pidió estimar minutos restantes y detenerse al256/256para ir a casa; entrenar solo cuando él avise. CoordinadorPID18837 identificado por comando y suspendido con SIGSTOP a ese PID, statTs confirmado;4generadores propios siguenRs. Sin candidato entrenado y todas las fuentes congeladas intactas. No se editaron herramientas ni protocolo. `fase5_lote256_mac_20261029/PAUSA_USUARIO.json` documenta la pausa. Contador directo actual 227/256; ETA orientativa30–45min desde15:45. La automatización fue actualizada para leer progreso individual (agregado congelado), avisar al terminar datos y eliminarse; no SIGCONT ni entrenamiento automático. Reanudar solo tras nueva orden de Jose, verificando identidad/fuentes/checkpoints; no borrar locks por estar detenido el padre.

## 29/oct — pausa inmediata de generación por traslado

2026-10-29T15:47:41-06:00: Jose cambió la orden: pausar ahora, sin esperar256. Detenidos conSIGSTOP los4generadores18838–18841; confirmadoTs en cada uno y en coordinador18837ya detenido. Contador real227/256(57/57/57/56), fuentes intactas, sin candidato entrenado. Señales solo a procesos propios identificados. Evidencia `fase5_lote256_mac_20261029/PAUSA_USUARIO.json`; pausa previa archivada enPAUSA_USUARIO_ANTERIOR.json. Automatización cambiada aPAUSED y sin reanudación automática. Esperar aviso de llegada antes de continuar; conservar locks. Al reanudar comprobar fuentes, identidad, memoria/checkpoints y límite de sesión de reloj de pared.

## 29/oct — retorno a casa, reanudación5 y entrega8A

2026-10-29T19:33:12-06:00: Jose autoriza terminar256y entrenar después; pausa revocada. Identidad/SHA verificados,227completos preservados y SIGCONT a4generadores+coordinador. Viejo supervisor15969ausente, lock conservado; nuevo32262solo puede añadir60minsi flujo termina incompleto por plazo, sin repetir episodios ni errores/rechazos. Seguimiento app reactivado ACTIVE cada20min, caffeinate temporal. Fuentes intactas, aún sin modelo aceptado.

Certificado8Aleído y catálogo de35archivos SHA verificado sin discrepancias; no se repiten suites. TT/oráculo y20llamadas de prioridad de victoria registradas.8sigue abierta. Preparado [[2026-10-29-Encargo-Codex-fase8B1]] para composición de ensayo/paquete y controles estáticos mientras5genera; no enviado, sin JIT/liga bajo carga ni promoción.

## 29/oct —256completos y entrenamiento rechazado por retención

2026-10-29T19:54:55-06:00: flujo completado19:51,4salidas0,256episodios sin errores de replay. λ100/replay80/20ejecutado sin cambios; validación24grupos Brier por grupo0.14348033→0.13465573, retención126grupos0.17400779→0.18057672: empeora0.00656894>0.005y rechaza selección. TestUCTNOabierto; no promoción, liga ni rescate.17fuentes/datos/contrato/candidato/particiones verificados por SHA; NPZ principal37678d0bintacto. [[resultados/medicion/fase5_lote256_mac_20261029/RESULTADOS]]. Supervisor casa cerró sin reiniciar ni necesitar60minextra. Seguimiento termina; fase5global sigue abierta. Próximo diagnóstico solo desarrollo/retención antes de otra hipótesis;8B.1puede preparar respaldo sin asumirV.

## 29/oct — diagnóstico amplio y nueva hipótesis S13

2026-10-29T20:16:07-06:00: Jose autoriza avanzar y pide siguiente prompt. Diagnóstico solo train/replay/validation/retención: amplio mejora replay0.00134485pero empeora82/126grupos retenidos; gradiente5.27e-12correcto. Atribución por segmento de logits apunta patrones(+0.00729038),no causal. Fuentes/métricas reproducidas,sin test. Protocolo S13previo: patrones congelados y13coeficientes libres,λ100/replay80/20,UNAejecución. SHAaba46e55fijado antes de evaluación; desarrollo visto mejoraBrier0.00214487y retención+0.00032692, filtros pasan. NOvalidación nueva ni aceptación; antiguo conjunto ya guio hipótesis. Nuevo lote64previsto solo después de8B.2y auditoría de semillas/purgas; no empezó. Principal intacto y test256sellado. [[Experimentos/2026-10-29-Diagnostico-replay256-y-S13]].

8B.1entrega revisada,60SHA sin discrepancias. Preparado [[2026-10-29-Encargo-Codex-fase8B2]], decisión técnicaI0con respaldo37678d0bpara controles reales de ejecución; no finalista niS13. Sin envío automático. Ventana exclusiva al ejecutar, este chat no genera/entrena durante reloj.

## 29/oct — validación nueva S13preparada durante controles de Codex

2026-10-29T20:43:09-06:00: Jose confirma Codex corriendo y autoriza siguiente paso en paralelo. Preparados controlador recuperable y5regresiones pequeñas(guardia ventana, espejo/puntos/turno,purga,UCTopaco,cobertura/exposición única). Primera búsqueda de semillas respetaba ignore: corregida ANTES de generar, incluyendo ignorados en19worktrees/12666archivos/321.8MB;0usosdetectados,4referencias propias nuevas clasificadas como intención/fixtures. Auditoría y contrato inicial conservados, contrato final recongeladoSHA2ebabfcecon24fuentes; ninguna muestra/puerta/modelo cambió ni se generaron datos. [[resultados/medicion/fase5_validacion_S13_64_20261029/LEEME]].

Seguimiento app creado/verificado ACTIVE cada10min:validar-s13-despu-s-de-controles-t-cnicos. Solo arranca4×16/90mintrasliberación verificada de8B.2yCPUlibre;24gruposval/8UCTreservados,modeloaba46e55fijo,no entrenamiento/test256. Pausa/rechazo/error/inconcluso sin reintento automático; espera8horasmáxima. Principal y17fuentes256intactos. Codex8B.2sigue con ventana; memoria corregida a ejecución confirmada por Jose, no cierre supuesto.

## 29/oct — cierre técnico8B.2y arranque de validación S13

2026-10-29T21:14:58-06:00: certificado final8B.2y169SHA verificados,ventana finalizada. I0LinuxARM64pasa controles,frío2.717s,pico142.54MiB,humo2y4técnicasrandomsin fallos,preparar3.032s/reloj14.375s/pico143.36MiBtanda. No fuerza niS13ni promoción;20261221consumida.3muestraspssin carga pesada/procesosdeensayo yDocker0contenedores propios confirmaron ventana libre.

S13arrancado21:13:50conPID43192/4generadores,90minsin ampliación/reintento,caffeinate43193. Liberación/comando/SHA guardados en directorio de validación; contrato24fuentesintacto,NPZprincipal37678d0b. Seguimiento10minsigue activo, sin conteos rutinarios ni apertura de test256/UCTnuevo. Últimoconteo0/64,verificarreal.

## 30/oct — demoras de S13por suspensión con tapa cerrada

2026-10-30T00:55:12-06:00: comprobación actual52/64,coordinador y4trabajadores propios vivos,fuentes congeladas intactas,sin errores detectados. ioregconfirma tapa cerrada,AC100%;pmsetregistra18sueños/~170.8mindesde lanzamiento,de220mincalendario. CPUde cada trabajador~46.7min. No se amplió --minutos90ni reinició. El contador monotónico del generador no avanza en sueño profundo deestaMac. Caffeinate-i sigueactivo pero no evita cierre de tapa; no cambiar políticas globales ni intentar forzarclamshell. Avisar una vez al usuario que abra tapa/conecte. Sigue seguimiento hasta desenlace,sin reentrenar/test.


## 30/oct — S13 pasa validación nueva y equivalencia funcional

2026-10-30T14:21:18-06:00: auditado cierre del flujo64/64delas04:26:18,cuatrosalidas0.4512filas/24grupos,purga225;Brierigualpesogrupo0.13163538→0.12574267(mejora0.00589271),logloss0.40312045→0.39003946,amboscoloresmejoran,todaslaspuertaspasan. Inicio+0.00039721: pequeña regresión descriptiva, sin reajuste.8gruposUCTnuevosytest256sin evaluación. S13aba46e55conservado;288checksPython+288Numbaen48estadoshistóricos correctos,errorlogit5.33e-15/utilidad4.44e-16.24fuentesactuales+17del256/principal intactos,manifiestos/hashescorrectos. [[resultados/medicion/fase5_validacion_S13_64_20261029/RESULTADOS]].

No promoción ni liga/examen ejecutados;fase5sigueabierta. Próximo paso: protocolo de examen reservado,seguridad/costo del candidato concreto y deporte oficial;I0/8B.2no equivale a certificarS13. Seguimiento concluido y automatización validar-s13-despu-s-de-controles-t-cnicos eliminada,confirmado por la app. Las suspensiones explican demora; no hubo ampliación ni reinicio.
