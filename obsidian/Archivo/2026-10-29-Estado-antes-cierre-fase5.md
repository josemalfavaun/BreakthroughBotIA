---
tipo: archivo-historico
estado: superado
---

Estado anterior conservado para trazabilidad. El estado vigente es [[01-Estado]].

---
tipo: estado
proyecto: BreakthroughBotIA
actualizado: 2026-10-28
confianza: checkout-y-baseline-oficial-verificados
---

# Estado del proyecto

> [!warning] Límite de esta actualización
> El checkout local y el baseline oficial de 40 partidas se verificaron el 2026-10-27. Los resultados anteriores del caché y del reloj adaptativo se conservan del reporte de Codex; la tanda nueva tiene sus propios JSON y log.

## Objetivo

Mejorar `iacasitegano` para competir en la liga de Breakthrough de combate, midiendo cada cambio con el árbitro y respetando las reglas del curso. No asumir que una mejora local garantiza superar Tier 5.

## Último estado confirmado del checkout principal

- Rama local: `integracion-tier1-2`.
- HEAD: `85b2d55`, con `dce1876` y `85b2d55` integrados desde la rama del caché horneado. El worktree local de `codex/cache-numba-horneado` también apunta a `85b2d55`.
- Cambios locales pendientes observados: `INFORME.md` y `herramientas/README_CACHE_NUMBA.md` modificados; `herramientas/test_preparar_cache_docker.py` sin seguimiento.
- También están sin seguimiento `AGENTS.md`, `.obsidian/` y `obsidian/`; son memoria e instrucciones de trabajo, no parte de la entrega oficial.
- No se hizo commit. No se tocó `main`.

## Comprobación posterior del entrenamiento (2026-10-27)

- En `data/` existen `candidato_20261024_042150.npy`, `pesos_selfplay_300.npy`, `pesos_antes_selfplay_300.npy` y `pesos.npy`.
- El contenedor `iacasitegano-entrenar-20261023` figura detenido con `Exited (0)`. Sus logs confirman 300/300 partidas, 100 por semilla (1234, 5678, 9012), 14,118 posiciones y candidato guardado en `data/candidato_20261024_042150.npy`.
- `candidato_20261024_042150.npy` y `pesos.npy` tienen el mismo SHA-256 (`d5cc25...570064f`). El informe registra que el candidato se evaluó 40 partidas contra el campeón (22–18, 87–72 puntos, sin fallos) y después se promovió.
- Esa promoción es histórica: el `strategy.py` activo carga `pesos_eval3_ligero.npz` mediante `busqueda_eval3`, no el vector lineal de seis elementos de `pesos.npy`. Por tanto, volver a evaluar o reentrenar este candidato no cambia la estrategia de juego vigente.
- El texto de terminal compartido contiene además una salida antigua de `main` con renombres staged, que no coincide con este checkout: aquí la rama activa sigue siendo `integracion-tier1-2` en `85b2d55`. No inferir que los cambios de `main` están presentes o autorizados en esta rama.

## Resultados recién reportados por Codex

- **Caché horneado — aceptado como mejora operativa:** 20/20 preparaciones frías con 7 workers, 0.5 CPU y 1024 MiB; p50 0.063 s, p95 0.097 s y máximo 0.123 s en el resumen final (el informe registra 0.124 s). La liga real contra `montecarlo` fue 10–10 en 20 partidas, todas por puntos y sin fallos técnicos. Esto valida seguridad de arranque, no mejora de fuerza.
- **Reloj adaptativo — rechazado:** 100 partidas por variante; candidato 43–57 (IC Wilson 95%: 33.7–52.8%), base 55–45 (45.2–64.4%). En bloques pareados discordantes, la base ganó 22 frente a 10. El candidato redujo reloj medio por partida de 14.62 s a 9.45 s, pero profundidad media bajó de 4.93 a 4.64. No se hizo validación con semillas aparte; el resultado no se añadió al informe.
- La prueba de regresión Docker de una instancia se ejecutó y pasó, según el reporte. No se repitió en esta revisión.
- Detalle del experimento de reloj: `/Users/josema/noche_salida/lab/margen_reloj_adaptativo.md`.

## Decisiones conocidas del snapshot

- Se rechazaron una búsqueda híbrida con rollouts y una tabla MDP de carreras por no mejorar en la validación reservada o en partidas, pese a que una implementación podía ser correcta.
- Se rechazaron varias pruebas de self-play/épsilon por resultados desfavorables o aún por reconciliar.
- Se mantiene la regla: promover solo cambios con resultados repetibles, semillas reservadas y sin regresiones técnicas.

Ver [[02-Decisiones]] y [[03-Bitacora]]; verificar siempre los informes fuente.

## Baseline oficial verificado (2026-10-27 15:15)

- Estrategia activa: `busqueda_eval3` y `data/pesos_eval3_ligero.npz`, SHA-256 `37678d0bd700c27a29d0084558158db1a65b01409dbf54828e89706441c2250b`. Checkout al cierre: `integracion-tier1-2` en `85b2d55`, cambios locales conservados.
- Árbitro oficial y Docker, 40 partidas, semilla `20261031`, 20 por color: **21–19, puntos 87–75**. Blancas: 14–6 y 48–31 puntos; negras: 7–13 y 39–44 puntos.
- Reloj propio máximo 18.466 s (media 14.868 s). Las 40 terminaron por puntos, sin fallos de preparación, errores, ilegales ni timeouts en ambos bots. Duración exacta de `preparar()` **sin medir**: no aparece en la salida ni en los registros.
- Evidencia: [[resultados/2026-10-27_14-49-49/index.html]], los 40 JSON de esa carpeta y `/Users/josema/noche_salida/lab/baseline_40_20261031.log`. Detalle breve en [[03-Bitacora]]. Esa tanda terminó sin cambiar código o pesos; el estado de corridas posteriores se indica abajo. Sin commit, merge o push.

## Próxima acción

**Último avance de fase 5 / reanudación nocturna:** [[Experimentos/2026-10-28-Fase5-datos-modelos]]. Panel 24×profundidades1/2/3 terminado sin discrepancias de búsqueda; 8 sensibles al horizonte, sin error de decisión demostrado. Modelo activo regenerado con IRLS λ100 centrado en pesos antiguos (error máximo 1.78e-15). Datos históricos auditados; 60 episodios nuevos/6,417 filas verificadas. Ridge/GA inicial y simetría no se promueven. Adaptación con prior activo pasa filtros internos UCT: Brier agrupado 0.07072→0.04347 (9 grupos; selección 2). Candidato `/Users/josema/.codex/worktrees/fase5-adaptacion/BreakthroughBotIA`, búsqueda `83997d…77e`, NPZ `ab1a59…3718`, sin promoción. Validación Python 12 raíces/12 terminales correcta; **caché regenerado y oráculo Numba oficial correcto; ambos validadores y 3 preparaciones frías por variante pasaron; serie 4+160 oficial en curso** según [[Experimentos/2026-10-28-Protocolo-modelo-adaptado]]. Este chat retoma esa validación; el encargo a Codex permanece preparado, no enviado. Fase 2 cerrada rechazada, ratio 0.982591. Principal sigue en 85b2d55; estrategias/pesos activos intactos. Los estados pendientes anteriores son historial.

**Plan vigente y resultado de Codex — 2026-10-28:** [[07-Plan-definitivo]]. Verificados los hashes y recuentos de 164 JSON válidos: A 41/80, B 48/80, +7 (+4/+3 por semilla), sin fallos; máximo reloj A/B 18.540077/20.299246 s. **5A cerrada sin promoción por faltar el +8 exigido**; reservas intactas. Los párrafos anteriores sobre partidas pendientes quedan como historial. Fases abiertas 2/5/6/7 más integración 8 explícita y nueva 9 final. Codex: siguiente encargo [[2026-10-28-Encargo-Codex-fase2]], preparado para pegar, no enviado/ejecutado desde este chat. Este chat: 5B/receta/profesor/regresión/GA. Escritorio: [[08-Escritorio-y-entrenamiento]], aún sin configurar/conectar. Panel de 24 estados congelado en `resultados/medicion/panel24_decisiones_20261028/`, 12 por color, 8 por categoría y 20 grupos, SHA `1ca5a56679eda76a6c38e32851e4a5121b89f256e5bd675ad436c0abc00cbc48`; análisis pendiente. Modelo y búsqueda del principal sin cambios.

**2026-10-28 — investigación y plazo:** Jose confirma entrega el **4 de noviembre** (hora pendiente), sesiones de 1 h/7 h y posible escritorio dedicado Windows/i5 aproximadamente 8.ª generación/16 GB/RX 570. Página del profesor y repositorio oficial consultados: offline admite cualquier herramienta; liga no admite redes; tiers con las mismas reglas; calificación por victorias totales. Investigación y calendario: [[06-Investigacion-y-plan-semanal]]. Priorizar utilidad → 24 decisiones contrafactuales → receta/calibración → un candidato dirigido de modelo → pistas TT. Hipótesis nueva: interacción patrones×fase del marcador; también profesor costoso/estudiante pequeño y rivales reservados. Todo propuesto, sin nuevas mediciones de fuerza. Escritorio aún no configurado; corrida de terminal no verificada en esta sesión. A/B vigente y reservas intactos.

**Cierre de fases y prioridades solicitado:** registro vigente [[05-Cierre-de-fases]]. Cuatro fases cerradas en su alcance original (0/1 sobre baseline; 3/4 con rechazo), cuatro pendientes (2 reabierta, 5/6/7). No implica fuerza o entrega final cerradas. La prioridad 2 ya tiene extractor: 40 partidas/3,231 plies reconstruidos y 282 estados de desarrollo exportados (143 blancos/139 negros), sin errores de replay. Comparación contrafactual pendiente; [[Experimentos/2026-10-28-Diagnostico-decisiones]]. Artefacto de ablación `noche_salida/lab/_pesos_ligero5_solo_puntos_patrones_filas_marcador.npz` coincide por hash con el activo; receta completa pendiente. No modificar A/B de utilidad mientras Codex tenga esa medición. Herramienta offline añadida al principal; fuentes de juego y pesos intactos.

**2026-10-28 — reparto fijado:** utilidad ya tiene la misma TT corregida que el control. Ver [[Experimentos/2026-10-28-Protocolo-utilidad-victoria]] y [[2026-10-28-Encargo-Codex]]. Python/Numba: 12 raíces hasta prof. 3 y 72 pruebas de TT, cero diferencias. Caché B regenerado; validador pasó con aviso de reloj reducido a 3 s. Tres preparaciones frías, máximo importación+preparar 0.372181 s (límite 10 s). Pendientes 4 partidas técnicas oficiales y 160 de desarrollo (80 por versión), orden A/B y B/A. Reservas 20261111–14 sin ejecutar. Codex de terminal será dueño de la ventana de CPU; este chat hará solo lecturas ligeras de receta/modelo durante la medición. Sin partidas nuevas ni cambios al principal. Detalle en el worktree B, `resultados/medicion/utilidad_victoria_20261028/VALIDACION.md`. La cola anterior se conserva como historial.

**Validación técnica cerrada en este chat:** A/A contrastado en 240 JSON; mediana de diferencia absoluta 21 peones netos y, secundariamente, 4 victorias. TT pasó Numba ampliado, validador de entrega, tres preparaciones frías y cuatro partidas técnicas (1–3, sin fallos). Los otros tres candidatos también pasaron sus arneses Numba. Microbenchmarks de hojas/buffers modestos; no hay mejora de fuerza demostrada ni promoción.


- **A/A completado y verificado:** seis bloques aceptados, 240 partidas; diferencias absolutas 21, 24 y 10, mediana **21 puntos netos por 40**. No quedan procesos o contenedores de la serie activos. El intento parcial de 20 partidas se conserva excluido, sin duplicar resultados. Evidencia: [[Experimentos/2026-10-27-AA-control]]. Ningún prototipo se incorporó al control.
- **Principal:** `integracion-tier1-2`, `85b2d55`; código de búsqueda y NPZ activo conservan sus hashes. Cambios locales previos intactos. Prototipos adjuntos a este chat, sin commit/promoción:

| Prioridad | Candidato | Evidencia actual | Estado |
|---|---|---|---|
| 1 | [[Experimentos/2026-10-27-TT-exactitud]] | Numba: 10 regresiones, 192 ventanas adicionales, 15 raíces; validador y 4 partidas técnicas correctos | Integración técnica validada; frecuencia natural/efecto en fuerza sin medir |
| 2 | [[Experimentos/2026-10-27-Utilidad-victoria]] | Numba: 10 hojas, 4 terminales, 8 raíces contra oráculo | Próxima hipótesis estratégica; preparar base común TT |
| 3 | [[Experimentos/2026-10-27-Hojas-sin-duplicado]] | Numba: 96 casos y 12 raíces; microbenchmark ratio 1.019199 | Ganancia pequeña, panel real pendiente |
| 4 | [[Experimentos/2026-10-27-Buffers-busqueda]] | Numba: hasta 128 casos; microbenchmark ratio 1.011176 | Ganancia pequeña; prioridad baja |

Los cuatro worktrees parten de `85b2d55` y cada uno contiene un cambio independiente. Arneses compilados ejecutados en serie en imagen oficial, 1 CPU/1024 MiB; solo el caché del candidato TT se regeneró. Logs y protocolos en su `resultados/medicion/tt_validacion_20261027/`. La semilla 20261108 se usó para integración técnica y deja de ser reservada. Sin mejora de fuerza demostrada.

Siguiente paso vigente: ejecutar el protocolo de utilidad fijado el 2026-10-28. Base TT común y protocolo preparados; fuerza/costo en partidas pendientes. Las optimizaciones de velocidad necesitan panel real antes de promover. No modificar criterios históricos a posteriori, ni mezclar cambios distintos en una comparación.

El piso de tiempo de carreras sigue rechazado por su criterio de desarrollo, con causalidad limitada por Montecarlo a reloj; conservar sus dos worktrees y reservas. Ver [[Experimentos/2026-10-27-Revision-pareada-tiempo-carreras]].

Trabajo auxiliar: [[04-Preparacion-entrega]] (receta del modelo, informe breve y caché); fuentes IRLS/localización del NPZ original ya recuperadas, portado completo pendiente. Comparar ramas y lista permitida antes de una entrega; sin merge automático.


## Cierre A/A verificado — 2026-10-27

- Rama `codex/tiempo-carreras-control`, HEAD `85b2d55`; fuentes, pesos y libro iguales al commit. Los 25 archivos de caché modificados previamente se conservaron byte a byte. Checkout principal `integracion-tier1-2`/`85b2d55`, cambios anteriores conservados e informe intacto.
- Seis bloques completados, 240 JSON aceptados: 20261105/06/07 × R1/R2, árbitro oficial y Docker, 30 s/10 s/1 CPU/1024 MiB. Se conservaron aparte 20 JSON del intento interrumpido 20261106 R2; su repetición completa reemplaza ese intento en la métrica. **Mediana de diferencias absolutas: 21 puntos netos por 40 partidas**. Fallos técnicos 0; reloj máximo propio/rival 18.724/19.789 s. No mide mejora del bot.
- No quedan bloques en curso. Siguiente acción: usar esta variación descriptiva para diseñar futuras comparaciones; cualquier experimento nuevo requiere protocolo y semillas nuevas. Preparación exacta, memoria pico, carga idéntica, discontinuidad por reposo y generalización siguen limitadas.
- Evidencia y desglose por color: [[Experimentos/2026-10-27-AA-control]]. Ambos worktrees y artefactos preservados; no se usaron reservas, no se promovió ni se hizo commit, merge o push.

## Incidencia y recuperación de fase 5 — 28 oct. 23:31

Cuatro técnicas N completas sin fallos. Primer bloque U interrumpido por GRIS (PID1020, 96.4% CPU), 23 JSON conservados y excluidos; motivo registrado antes de repetir, exclusión automática por carga, sin usar el resultado deportivo como criterio. Se detuvo solo su contenedor huérfano propio. Jose autorizó pausar temporalmente solo ese proceso y restaurarlo al terminar. Nuevo ejecutor `con_gris_pausado.py` con restauración `finally` y guardián independiente; **comprobar pausa_gris.json antes de cerrar sesión**. Se repite bloque U completo, misma semilla, candidato/umbrales intactos. Estado real en `fase5_oficial_20261028/progreso.json`. Restaurar GRIS si no hay supervisor vivo y no figura restaurado; verificar identidad del proceso antes de señalizar.

Durante la interrupción se ejecutó la receta activa desde el paquete extraído fuera del repo: pesos/logits coinciden a 1.78e-15/3.55e-15. Evidencia `fase5_20261028/portabilidad_mac/`; Windows sigue pendiente. No se entrenó durante partidas activas.

## 29 de octubre — resultado deportivo parcial inequívoco

N completó 80 partidas: **6–74, 3/40 en cada semilla**, cero fallos propios. Primer control U: 19–21; último U40 aún en curso. N ya incumple el filtro por semilla; no habrá confirmación ni promoción. La serie fija se completa para cerrar la evidencia; el filtro del analizador permanece sin evaluar formalmente hasta 160. Al terminar: restaurar GRIS, verificar/resguardar los JSON y ejecutar diagnóstico de transferencia/retención sin entrenamiento. No iniciar otra lambda ni mezclar este resultado con GA. `fase5_oficial_20261028/RESULTADOS.md` y `progreso.json` mandan sobre esta instantánea.
