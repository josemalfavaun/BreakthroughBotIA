---
tipo: experimento
fecha: 2026-10-28
estado: cerrado-rechazado
---

# Fase 2: pistas TT en nodos internos

Base A con TT corregida preservada íntegramente antes de editar; candidato aislado en /Users/josema/.codex/worktrees/2559/BreakthroughBotIA-codex. P registrado para integración posterior. Utilidad anterior cerrada sin promoción, ampliación ni reservas; evidencia intacta.

Solo pistas de orden en nodos internos tras fallar valor exacto, firma completa y legalidad. Sin cambios de utilidad, pesos, reloj, hojas, buffers o libro. No se pausan aplicaciones ajenas.

[Protocolo previo](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/PROTOCOLO.md>) · [Manifiesto previo](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/antes.json>) · [Diferencia respecto a A](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/candidato_vs_A.patch>) · [Progreso](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/progreso.json>).

Las comprobaciones y mediciones técnicas están completas. Este candidato se rechaza según el filtro fijado; no procede liga ni confirmación deportiva.

## Resultado del experimento

**Rechazado sin liga:** mediana global candidato/control **0.982591**, frente al requisito ≤0.95. Ninguna fase superó 1.05. Diferencia máxima de valor 0 (tolerancia absoluta 1e-10).

| Fase | Mediana candidato/control |
|---|---:|
| temprana | 0.946921 |
| media | 0.998289 |
| tardia | 1.003224 |

Panel de 60 estados reales congelado por metadatos, 20 por fase y 10 por color/fase, 47 partidas y 40 grupos. Profundidad 5 completa, cinco pares A/B y cinco B/A por posición: 600 pares /1200 búsquedas. Valores y nodos del pase de contadores coinciden con producción. Regresiones TT extendidas de A/B y oráculo adicional completos, sin errores.

Contadores (60 búsquedas por versión): nodos A 29,453,968, candidato 25,753,468; 2,223,685 consultas de pistas, 522,269 legales y 370,202 movimientos realmente adelantados; 260,047 cortes con primera jugada adelantada (asociación, sin afirmar causalidad). La reducción de nodos no alcanza el filtro prefijado de tiempo total.

Tablas: A 16 MiB; candidato 50 MiB. Creación mediana A 0.001368813 s /candidato 0.001872771 s, incluida además en el tiempo total de cada búsqueda. RSS máximo observado del proceso de medición con JIT: 292436 KiB, que no es memoria pico de entrega del bot.

Un primer intento de tiempos falló en calentamiento por caché de alias de oráculo, sin producir pares; se conservó y se separó el caché por ejecución. No hubo ajuste del candidato, panel o criterios después de observar rendimiento. Se esperó a cargas ajenas; no se pausó ninguna aplicación.

La verificación final conserva A íntegro y constata que el único archivo distinto entre candidato y A es busqueda_eval3.py. Los 112 artefactos y los 223 JSON de la utilidad anterior (164 válidos +59 excluidos) conservan SHA-256; también los archivos originales de utilidad B. La utilidad sigue cerrada por +7 < +8. No partidas nuevas, reservas, commit, merge, push, promoción o reemplazo del principal. Plan y estado global no editados.

- [Resultados reproducibles y hashes](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/RESULTADOS.md>)
- [Resumen JSON](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/resumen.json>)
- [Fases CSV](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/fases.csv>)
- [Posiciones CSV](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/posiciones.csv>)
- [Pares CSV](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/pares.csv>)
- [Manifiesto final](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/MANIFIESTO_FINAL.json>)
- [Recuperación](</Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/fase2_tt_pistas_20261028/RECUPERAR.md>)

Pendiente: ninguna liga de este candidato al fallar el filtro. Su caché/paquete de entrega no se preparó, porque no se propone integrar. Cualquier rediseño abre otro experimento. El chat director decide el cierre global.

<!-- CERTIFICACION_FASE2_20261029_INICIO -->
## Certificación de cierre — 29 de octubre de 2026

**Cerrado/rechazado certificado con evidencia existente.** Auditoría independiente de lectura/estadística: 600 pares únicos /1200 búsquedas históricas, 60 posiciones y selector reproducidos; ratio global 0.982591135511 frente a ≤0.95. Fases temprana/media/tardía: 0.946920677853 /0.998288672344 /1.003224053401. Diferencia máxima de valor 0. Se verificaron las 284 entradas del catálogo SHA-256 y los 47 JSON fuente de las posiciones; no se repitieron búsquedas, compilación, liga ni reservas.

**Separación obligatoria para fase 8:** el principal P sigue en búsqueda `ceba3653…`, NPZ `37678d0b…`; no contiene las pistas `adb347a1…` ni la corrección TT de A `cc888a3c…`. Los logs históricos compilados reproducen dos fallos del P actual con idéntica fuente/pesos; A y candidato pasan las regresiones. Rechazar ordenamiento no certifica que P esté corregido. El parche exacto P→A queda registrado y comprobado únicamente con `git apply --check`, sin aplicar. Revisar/portar esa corrección en integración aislada, conservar regresiones estrecha/amplia/abortos/oráculo y repetir seguridad/validación de fase 8 antes de promover.

- [Certificado, límites, pendientes y párrafo de traspaso](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/cierre_fase2_20261029/CIERRE.md>)
- [Auditoría, identidades completas y hashes reales](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/cierre_fase2_20261029/auditoria.json>)
- [Parche TT P→A pendiente de fase 8; no aplicado](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/cierre_fase2_20261029/P_a_A_correccion_TT.patch>)

Principal y cambios existentes intactos durante la auditoría. No se pausaron/mataron aplicaciones o contenedores; sin medición de tiempos nueva ni fase 6. No se editaron 01-Estado, 03-Bitacora o 07-Plan-definitivo. El chat de fase 5 puede incorporar el párrafo breve de traspaso de CIERRE.md.
<!-- CERTIFICACION_FASE2_20261029_FIN -->
