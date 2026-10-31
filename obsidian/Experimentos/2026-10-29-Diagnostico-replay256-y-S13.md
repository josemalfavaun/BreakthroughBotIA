---
tipo: experimento
estado: desarrollo-pasado-validacion-independiente-pendiente
fecha: 2026-10-29
baseline_commit: 85b2d55
---

# Diagnóstico replay256 e hipótesis S13

## Hipótesis falsable

La adaptación amplia ajusta patrones a los grupos de entrenamiento y pierde retención; restringirla a13coeficientes puede reducir esa pérdida conservando mejora en datos nuevos. Atribución descriptiva, no prueba causal. El ajuste amplio mejora replaypero empeora82/126grupos retenidos; gradiente convergente.

## Cambio aislado

S13congela243patrones y todos los coeficientes ajenos a puntos/filas/marcador. Una ejecución logística λ100/replay80/20, sin cambiar representación/banderas ni pesos del principal. Se diferencia del GA previo de tres multiplicadores; no se reabre ese experimento.

## Protocolo fijado antes de medir

[[resultados/medicion/fase5_subespacio13_20261029/PROTOCOLO]]. Misma partición de ajuste, evaluación antigua solo desarrollo. El NPZse congeló antes de cargar evaluación. No test ni particiones originales reescritas. Validación independiente nueva prevista DESPUÉS de ventana8B.2, con semillas por auditar; no se está generando.

## Resultado

S13: mejora Brier antiguo0.00214487,retención empeora0.00032692(vs0.00656894del amplio),filtros de desarrollo pasan; gradiente1.74e-13. Replay empeora0.00043590. No fuerza/aceptación: validation antigua y retención ya motivaron la hipótesis.

## Artefactos y comandos

[[resultados/medicion/fase5_diagnostico_replay256_20261029/RESULTADOS]] y [[resultados/medicion/fase5_subespacio13_20261029/RESULTADOS]]. Código herramientas/fase5_diagnosticar_replay256.py y fase5_subespacio13.py, Python.venv/hilos1/sin JIT. SHAaba46e55congelado, activo37678d0bintacto. Datos/fuentes/gradiente y controles enJSON.

## Decisión

Amplio sigue rechazado. S13permanece candidato de desarrollo; siguiente paso validación nueva con candidato fijo, sin rescate ni examen original abierto. Codex8B.2prueba I0con pesos de respaldo en ventana exclusiva; no incorporar S13allí. Fase5/8siguen abiertas.
