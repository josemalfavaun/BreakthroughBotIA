---
tipo: indice
proyecto: BreakthroughBotIA
actualizado: 2026-10-28
---

# BreakthroughBotIA — inicio

Vault de trabajo para Jose, Daphne y agentes. Mantiene el contexto que hace falta para retomar el proyecto sin volver a leer todo el historial.

## Trabajo actual30/oct

[[resultados/medicion/fase5_validacion_S13_64_20261029/RESULTADOS]] — S13pasó validación nueva y equivalencia Python/Numba, principal intacto;faltan examen reservado, controles técnicos y partidas oficiales. No hay modelo nuevo aceptado.8B.2técnicaI0terminada, sin certificarS13; seguimiento terminado. Lee [[01-Estado]] antes de ejecutar: no repetir lotes cerrados ni abrir test automáticamente.

## Primero

Plan de ejecución vigente: [[07-Plan-definitivo]]. Para usar el escritorio: [[08-Escritorio-y-entrenamiento]]. Fase 2 cerrada sin aceptar pistas TT. Este chat completó la tanda U/N de fase 5 con rechazo del candidato: [[Experimentos/2026-10-28-Fase5-datos-modelos]] y [[Experimentos/2026-10-28-Protocolo-modelo-adaptado]]. El encargo de fase5 fue preparado, no enviado; su tanda ya terminó en este chat. No repetirla. Diagnóstico siguiente: [[Experimentos/2026-10-29-Diagnostico-transferencia-y-proximo-ajuste]]. El experimento anterior de utilidad terminó sin promoción.

1. Lee [[01-Estado]] para el último resumen confirmado.
2. Verifica el estado real del checkout y de la terminal activa antes de ejecutar o cerrar tareas.
3. Consulta [[AGENTS]] (archivo `AGENTS.md` de la raíz) para las reglas de trabajo.
4. Abre solo la evidencia necesaria para la tarea; esta bóveda resume y enlaza, no sustituye las fuentes.

## Fuentes de verdad

- Reglas y límites: [[docs/reglas]]
- Calificación: [[docs/calificacion]]
- Uso del motor y ejecución: [[docs/avanzado]]
- Hoja de ruta experimental: [[PLAN_TIER_5]]
- Estado del bot e informe medido: [[estudiantes/iacasitegano/INFORME]]
- Código activo: [[estudiantes/iacasitegano/strategy]], [[estudiantes/iacasitegano/eval3]], [[estudiantes/iacasitegano/busqueda_eval3]] (verifica los nombres/estado en la rama actual)
- Instrucciones para agentes: [[AGENTS]]

## Memoria de proyecto

- [[02-Decisiones]] — decisiones duraderas y razones.
- [[03-Bitacora]] — cronología corta de cambios aceptados/rechazados.
- [[04-Preparacion-entrega]] — pendientes de informe, regeneración y contenido de la entrega.
- [[05-Cierre-de-fases]] — estado de las fases 0–9, responsables, dependencias y pruebas para cerrarlas; prioridades riesgo, diagnóstico, modelo y ordenamiento TT.
- [[06-Investigacion-y-plan-semanal]] — fuentes sobre regresión, MCTS, evolución, profesores offline y generalización; hipótesis nuevas y calendario hasta la entrega del 4 de noviembre.
- [[07-Plan-definitivo]] — responsabilidades, dependencias y cierre de fases 2/5/6/7, integración 8 y examen/pulido final 9; incorpora GA, ridge y profesor offline.
- [[Validacion-y-laboratorio-PC]] — validación5V implementada, paquete nuevo de234 archivos, cola CPU y Kubernetes de pruebas; Windows pendiente.
- [[08-Escritorio-y-entrenamiento]] — configuración Windows/WSL, paquetes de trabajo y lotes recuperables; preparación pendiente en esa máquina.
- [[Experimentos/Plantilla]] — plantilla para una hipótesis nueva.
- [[Plantillas/Handoff de agente]] — traspaso de contexto entre sesiones y agentes.

## Reglas de mantenimiento

- Actualiza el estado al empezar o cerrar una etapa significativa, no en cada comando.
- Incluye fecha, rama/commit y enlaces a JSON, logs, PR o archivos cuando existan.
- Distingue “hecho”, “en curso”, “propuesto” y “rechazado”. Una tanda exploratoria no es validación final.
- No dupliques código, resultados completos ni reglas oficiales. Enlaza la fuente primaria.
- La bóveda está dentro del checkout para que los agentes puedan leerla. Sus notas no forman parte de la entrega del equipo; la entrega oficial se limita a `estudiantes/iacasitegano/` salvo autorización explícita.
