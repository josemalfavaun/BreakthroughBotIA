---
tipo: experimento
estado: rechazado-en-desarrollo
fecha: 2026-10-27
baseline_commit: 85b2d55e9713bd993d874cfa050c60827580c92a
---

# Tiempo mínimo ante amenazas de anotación

## Hipótesis falsable y cambio aislado

La hipótesis de [[Experimentos/2026-10-27-Analisis-baseline-40]] predice que imponer un factor de tiempo mínimo de 1.0 cuando ≥2 peones rivales estén a ≤2 filas de anotar mejorará la diferencia de puntos contra Montecarlo. Para negras rivales son filas 2–3; para blancas rivales, filas 7–8 (el peón que anota sale del tablero).

Solo cambia el cálculo del factor en `strategy.jugar()`. Búsqueda, evaluación, pesos, libro, reserva y REPARTO permanecen idénticos al control. Se regenera la caché derivada porque su manifiesto comprueba el hash de `strategy.py`; esto no constituye una modificación de búsqueda/evaluación.

## Aislamiento

- Checkout principal: `integracion-tier1-2` en `85b2d55`; cambios locales conservados y snapshot en `/Users/josema/noche_salida/lab/tiempo_carreras/estado_inicial.json`.
- Control: `.worktrees/tiempo-carreras-control`, rama `codex/tiempo-carreras-control`.
- Variante: `.worktrees/tiempo-carreras-variante`, rama `codex/tiempo-carreras`.
- Ambos equipos permanecen en `estudiantes/iacasitegano/` dentro de sus respectivos worktrees. No se crea otro equipo ni se cambia el árbitro. Worktrees excluidos localmente en `.git/info/exclude`.

## Protocolo fijado antes de medir

- Rival: Montecarlo del mismo commit; árbitro oficial con Docker, 1 CPU, 1024 MiB, reloj 30 s, preparar 10 s; una sola carga pesada a la vez.
- Desarrollo: **40 partidas por versión, semilla nueva 20261101**, colores alternados, mismas semillas/dados entre control y variante. Orden: control y luego variante.
- Métrica primaria: `Δ = (puntos propios − rivales)_variante − (puntos propios − rivales)_control`. Prometedor si **Δ ≥6 en 40** y no hay regresión del diferencial con blancas; cero errores, ilegales, preparar o timeouts en ambos bloques.
- Si `0 ≤ Δ <6` y se cumple seguridad y no regresión blanca, ampliar desarrollo a **100 por versión** con 60 adicionales, semilla **20261103**. Umbral proporcional fijado: **Δ ≥15 en 100**. Si Δ<0, hay regresión blanca o fallos técnicos, no pasa desarrollo.
- Si pasa desarrollo: confirmación **40 por versión con semilla reservada 20261102**, orden variante y luego control. Mismo umbral +6 y controles. Si queda estrecha (0 a +5), ampliar confirmación a 100 con 60 adicionales, semilla reservada **20261104**; umbral +15. Si no cumple, no se confirma.
- No se ajustan 1.0, dos peones o dos filas tras observar resultados. `20261031` solo fue diagnóstico y no cuenta como confirmación.
- Registrar puntos netos y victorias totales/por color, conversión al llegar primero a dos puntos (diagnóstico secundario; cambia el subconjunto), `info.prof`, reloj, preparación, errores y timeouts. La preparación real por partida no queda cronometrada en los JSON: informar fallos y medir importación+preparar por separado con el arnés existente, 5 instancias frías por versión, 1 worker/1 CPU.
- Decisión al final: evidencia favorable o hipótesis no confirmada; **ninguna promoción**, edición de INFORME, commit, merge o push.

## Artefactos y resultado

**No pasa desarrollo; no se usaron semillas reservadas.** La variante gana dos partidas más, pero su diferencial de puntos empeora **6** (umbral fijado: mejorar al menos 6). No se amplía ni se confirma porque Δ<0. Esto no prueba inferioridad general con solo 40 juegos por versión; sí incumple el criterio de esta hipótesis.

| Versión / color | V–D | Puntos propios–rival (neto) | Conversión primero a 2 | Prof. media | Reloj medio / máximo |
|---|---:|---:|---:|---:|---:|
| Control, total | 21–19 | 91–69 (+22) | 21/29 | 4.997 | 14.726 / 17.419 s |
| Variante, total | 23–17 | 93–77 (+16) | 20/25 | 4.971 | 15.480 / 18.405 s |
| Control, blancas | 12–8 | 47–32 (+15) | 12/13 | 5.124 | 14.997 / 17.173 s |
| Variante, blancas | 13–7 | 48–33 (+15) | 11/12 | 5.107 | 15.300 / 17.919 s |
| Control, negras | 9–11 | 44–37 (+7) | 9/16 | 4.862 | 14.454 / 17.419 s |
| Variante, negras | 10–10 | 45–44 (+1) | 9/13 | 4.839 | 15.660 / 18.405 s |

En pares con idéntica semilla/juego/color, solo gana la variante en 7 y solo el control en 5; ambos ganan 16 y ambos pierden 12. Los dos bloques son de **20261101**, no de la tanda usada para formular la hipótesis.

- Conversión al **alcanzar** dos puntos, aunque el rival llegara antes: control 21/33 (blancas 12/16, negras 9/17), variante 23/33 (13/17, 10/16). La conversión al llegar **primero** sube de porcentaje por cambios de denominador: con negras son las mismas nueve victorias en 16 frente a 13 casos. No implica siete derrotas específicas reparadas.
- El piso afectaría 149 decisiones del control y afectó 185 de la variante. En esas poblaciones, tiempo medio 0.258→0.390 s y profundidad 4.993→5.200; los tableros son distintos, no un microbenchmark pareado. La profundidad global no subió y el reloj medio aumentó 0.755 s.
- **80/80 partidas oficiales por puntos; cero fallos de preparar, errores, ilegales o timeouts en ambos bots; salidas vacías.** Preparación real por partida sin duración registrada. En cinco pruebas frías separadas por versión (1 CPU/1024 MiB), importación+preparar: control p50 0.0235 s / máximo 0.0331 s; variante 0.0258 / 0.0726 s; 5/5 correctas en cada una.
- Nota técnica: el caché original recompilaba en el checkout nuevo (control, cinco pruebas preliminares: máximo 4.215 s). Se regeneraron ambos cachés antes de medir. El validador pasó para ambos; avisó de los imports ya existentes de `entrenar.py` y, solo en el control, de un timeout en su smoke reducido de **3 s contra random**, separado de las partidas oficiales de 30 s. No se modificó el bot para corregir ese aviso.

Fuentes: [control, repeticiones y JSON](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_15-39-23/index.html), [variante, repeticiones y JSON](../../.worktrees/tiempo-carreras-variante/resultados/2026-10-27_16-01-30/index.html); [primera partida control](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_15-39-23/001_0_0_iacasitegano_vs_montecarlo.json) / [variante pareada](../../.worktrees/tiempo-carreras-variante/resultados/2026-10-27_16-01-30/001_0_0_iacasitegano_vs_montecarlo.json). Logs, `desarrollo_40.json`, arnés de resumen y reporte completo: `/Users/josema/noche_salida/lab/tiempo_carreras/`.

Se conservan los dos worktrees para revisión, con las modificaciones sin commit; no se promovió la variante ni se editaron pesos o INFORME. Los 156 archivos del equipo original conservan sus hashes iniciales.

**Revisión posterior de causalidad:** [[Experimentos/2026-10-27-Revision-pareada-tiempo-carreras]] encontró que los 40 pares divergen por Montecarlo antes de la primera oportunidad de piso; ninguna posición compartida permite medir directamente su efecto. Se mantiene el rechazo por el criterio prefijado, sin atribuir causalmente todo el −6 al cambio. Reservas y umbral intactos.
