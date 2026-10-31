---
tipo: estado
proyecto: BreakthroughBotIA
actualizado: 2026-10-29T12:22:10-06:00
confianza: partidas-y-fuentes-verificadas
---

# Estado para retomar

**Modelo adaptado rechazado: N 6/80 frente a U 43/80 contra Montecarlo. El principal conserva código y pesos. Fase 5 sigue abierta.**

## Dónde trabajar

Principal: `/Users/josema/vs code/BreakthroughBotIA`, rama `integracion-tier1-2`, HEAD `85b2d55`. Este chat puede abrir en el worktree experimental `fase5-adaptacion`: **su modelo N fue rechazado; no copiarlo al principal**.

Búsqueda P SHA `ceba365326e5ba8dd102218843f2b92744738d9c8a18db000f9edbc188832b7f`; NPZ activo `37678d0bd700c27a29d0084558158db1a65b01409dbf54828e89706441c2250b`. Cambios locales anteriores preservados; sin commit, merge, push ni promoción.

## Resultado recién verificado

160 partidas de desarrollo +4 técnicas válidas; 23 interrumpidas por carga externa conservadas y excluidas. U: **43–37**; N: **6–74**, 3/40 en cada semilla. Cero fallos técnicos propios; reloj máximo U/N 18.313/17.788 s de 30 s. Ambos validadores y tres arranques fríos por versión correctos. Memoria pico sin medir.

**GRIS desactivado persistentemente por petición de Jose el 29/oct a las 07:30.** Servicios `com.gris.background`, `com.gris.home` y `com.gris.scheduler`: deshabilitados y descargados; cero procesos GRIS al verificar. Se conservan archivos y backups. No reactivarlo con arneses antiguos de pausa temporal. Evidencia y reactivación manual en `resultados/medicion/gris_pausa_persistente_20261029/LEEME.md`. La restauración tras las pruebas de la madrugada es histórica. Comprobar procesos reales antes de medir.

Fuente: [[resultados/medicion/fase5_oficial_20261028/RESULTADOS]]. En esa carpeta: JSON/CSV, manifiesto, auditoría final y respaldo verificado de 187 JSON originales. No repetir la tanda. U es el control de utilidad/TT corregida; P no participó. La confirmación P/N no se ejecuta porque N incumplió su condición de entrada.

## Comprobación adicional del principal — 29 de octubre

**P contra random:20–0**,10 por color,60–1 peones; cero fallos y reloj máximo16.258s. `resultados/medicion/random_principal_20261029/RESULTADOS.md`. No demuestra superar a MC/tiers ni garantiza nota de liga. Revisión oficial/ML y plan PC4: [[Experimentos/2026-10-29-Revision-oficial-validacion-y-PC4]].

## Qué aprendimos en fase 5

- Receta activa regenerada: IRLS λ100 centrado en seis pesos antiguos; error máximo 1.78e-15. Histórico de 77,038 posiciones auditado, con dependencias documentadas; no es un reservado nuevo.
- Panel de 24 estados × horizontes 1/2/3: 72 contrastes correctos; 8 sensibles al horizonte y 16 estables. Ninguna decisión histórica objetivamente peor quedó demostrada.
- Ridge/logística y GA reales evaluados; candidato histórico rechazado. Profesor a profundidad 7 completo en solo 6/18 ramas: no cualificado por cobertura.
- 60 episodios nuevos /6,417 posiciones verificados. Simetría rechazada. N mejoró Brier UCT interno (9 grupos; selección solo 2), pero empeoró mucho al jugar.
- Diagnóstico posterior: Brier histórico visto 0.1847→0.2373; en exactamente los mismos estados U/MC, Brier por grupo 0.2256→0.2965. No se detecta saturación exacta en los 6,060 estados analizados; hojas internas sin instrumentar. No se atribuye una causa única ni se inventan valores óptimos de acciones.

[[Experimentos/2026-10-29-Diagnostico-transferencia-y-proximo-ajuste]] enlaza la evidencia y la siguiente hipótesis. [[Experimentos/2026-10-28-Fase5-datos-modelos]] conserva protocolos y cronología.

## Fases y siguiente acción

**0–4 cerradas en su alcance**: baseline/seguridad; pistas TT rechazadas (ratio 0.982591, no cumple 0.95); Star2 e híbrido rechazados. **5–9 abiertas**. [[07-Plan-definitivo]] y [[05-Cierre-de-fases]] contienen los contratos.

En 5 están resueltos el panel, la receta/auditoría y las decisiones de los experimentos anteriores. Faltan profesor cualificado y selección/confirmación del modelo. Antes del próximo ajuste: fijar retención histórica, mezcla de datos y rivales pertinentes; no rescatar N variando λ/temperatura tras ver sus partidas. Toda aceptación necesita nuevas pruebas oficiales. Se puede preparar fase 6 sin modificar el bot; coordinar CPU para mediciones.

Esta serie usó 20261116/17 y técnica18. Confirmación19/20/21 sin ejecutar aquí. **No usar reservas históricas 20261102–04 ni 20261111–14.** Sin nuevos entrenamientos en curso.

**Validación5V reforzada y comprobada en Linux — 29/oct.** Se corrigió el cruce potencial de estados nuevos con replay/retención históricos; purga registrada en contrato. Kubernetes:8tests de validación+6 de modelos correctos; receta activa reproducida en77,038 posiciones con diferencia0;8episodios funcionales/776filas y60históricos/6417filas, replay sin errores. N archivado rechazado sin abrir test. No son mejoras de fuerza ni entrenamiento nuevo aceptado.

Paquete vigente: `resultados/medicion/fase5_mac_k8s_20261029/laboratorio_pc_validado_linux_20261029_v2.tar` (16,947,200bytes,236entradas; SHA `7475911a4e9e84f1ee4256f97fd68607530244dd5e20065bd133a1faf5e66f86`). Extracción limpia y ocho tests Mac correctos; código probado en Linux ARM64, Windows/x86 pendiente. Sustituye el paquete de infra_pc_20261029 para próximos trabajos.

**Piloto real Mac completo:**16episodios/1495posiciones,8grupos,4familias/ambos colores; replay0errores, procesos0/0, lock liberado, reanudación durable y originales verificados.750decisiones del profesor:prof4=23,5=448,6=205,7=74; no cualifica profundidad7universal.23filas purgadas; grupos3train/3validation/2test, insuficientes para5V; no se entrenó modelo. Brier por grupo MC propio0.2458 frente a estilos0.08aprox yUCT0.1298, solo2grupos por rival: diagnóstico de desarrollo, no fuerza. Fuente [[resultados/medicion/fase5_mac_k8s_20261029/RESULTADOS]] y PILOTO_MAC_CIERRE.json. Siguiente: lote prospectivo mayor con MC/UCT/diversidad y controles5V, sin reutilizar este piloto como examen.

**Kubernetes integrado en Docker Desktop activo —29/oct.** Configurado por GUI con kind1nodo/v1.31.1, estadoActive/Ready y4tareas Succeeded visibles en namespace default. Contexto docker-desktop; cliente compatible privado `$HOME/.kube/bin/kubectl-desktop` con checksum oficial. El externo anterior sigue detenido. [[resultados/medicion/docker_integrado_20261029/LEEME]]. Se deja integrado activo por petición de Jose; no medir liga con otras cargas.

**Fase5 siguiente paso EN CURSO:** lote nuevo256episodios/128grupos,4trabajadores, semillas94/95/96/97millones y fuentes/receta/puertas congeladas antes de generar. Sesión inicial60min, checkpoints por ply; conteo teórico72train/24val/32test sujeto a purga real. Flujo automatizado generar→verificar→ajustar1candidato→selección→test si pasa; datos incompletos pausan sin entrenar, no promoción. [[resultados/medicion/fase5_lote256_mac_20261029/LEEME]]. Revisar ESTADO.json/progreso/PIDs para estado real, no usar esta nota como prueba de finalización. Caffeinate ligado al PID12755 durante esta sesión; Mac debe permanecer despierta.

Fase2 certificada cerrada/rechazada, sin bloqueos: [[resultados/medicion/cierre_fase2_20261029/CIERRE]]. Corrección TT deA pendiente de integración8, principalP intacto. Siguiente encargo de terminal: [[2026-10-29-Encargo-Codex-fase6]] para cobertura→dominio→decisión de finales, sin benchmarks mientras corre5. **Preparado, no enviado**: API rechaza por escritor activo deCLI y CUA prohíbe Terminal; Jose debe pegarlo. No afirmar que fase6 está ejecutándose.

La versión extensa anterior se conserva en [[Archivo/2026-10-29-Estado-antes-cierre-fase5]] y [[03-Bitacora]]. Leerla solo si hace falta contexto histórico.
