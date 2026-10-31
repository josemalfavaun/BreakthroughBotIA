---
tipo: diagnostico
fecha: 2026-10-29
estado: adaptacion-rechazada-sin-nuevo-ajuste
---

# Transferencia del modelo: resultado y siguiente hipótesis

**N pierde 74 de 80 partidas; U pierde 37 de 80. N no se promueve.** La mejora predictiva frente al UCT interno no se trasladó a Montecarlo oficial. El principal P conserva código y pesos. U es el control con utilidad y TT corregida, no P.

## Evidencia sobre los mismos estados

Se reconstruyeron las 160 partidas válidas y 6,060 estados anteriores a decisiones propias; legalidad, combate, turno, marcador y ganador coinciden con el motor. Cada modelo predice exactamente las mismas posiciones dentro de cada fila. Brier menor es mejor.

| Datos | Modelo original | Adaptado N | Alcance |
|---|---:|---:|---|
| Estados generados por U frente a MC | 0.22564 | 0.29647 | Brier con igual peso por grupo, 3,187 estados/40 grupos |
| Estados generados por N frente a MC | 0.17574 | 0.69130 | Brier con igual peso por grupo, 2,873 estados/40 grupos |
| Validación histórica vista | 0.18491 | 0.24022 | Brier por grupo, 15,791 estados/312 grupos; solo retención, no confirmación nueva |

La validación histórica sin reponderar pasa de 0.184665 a 0.237346, y logloss de 0.537927 a 0.716535. El evaluador nuevo empeora incluso al medirlo sobre los estados del control. Esto respalda revisar pérdida de generalización y retención; no identifica por sí solo una causa única ni demuestra la jugada óptima en cada estado. Las etiquetas son ganadores bajo las políticas observadas.

Los pesos, banderas, caché y montajes corresponden al candidato entrenado; ambos validadores, arranques y oráculo compilado pasaron. Cero fallos propios en 164 partidas válidas. No se detectó saturación exacta a ±1 en los 6,060 estados analizados con NumPy; las hojas internas de los árboles no se instrumentaron. Por tanto, esta muestra no respalda atribuir el desastre a redondeo a terminales.

La selección del ajuste dependía de solo dos grupos y el examen UCT interno de nueve, con un rival de presupuesto bajo. Faltó un control explícito de retención sobre el dominio histórico y una selección que representara mejor los rivales objetivo. No se cambian retrospectivamente los filtros para presentar este modelo como aceptado.

## Próxima hipótesis dentro de fase 5 — preparada, no entrenada

**Una actualización que conserve datos históricos representativos y valide frente a rivales adecuados debería evitar el deterioro observado al ajustar solo con nuevos episodios.** La penalización hacia los pesos antiguos no bastó en esta versión.

1. Conservar U y P como referencias. N queda rechazado y sus datos/resultados archivados; no variar su lambda, temperatura o genoma para rescatar esta serie.
2. Antes del siguiente ajuste, fijar por escrito la mezcla de datos históricos/nuevos, grupos, purga de espejos, referencia, métrica de selección y puertas de retención. Usar la receta ya reproducida y las mismas características; cambiar solo el tratamiento de datos/retención como una hipótesis delimitada. Los datos históricos y estos 160 juegos son desarrollo visto.
3. Incluir una muestra de rivales con fuerza y presupuesto pertinentes; UCT512 por sí solo no acredita generalización. Cualificar el profesor en un piloto con presupuesto/cobertura prefijados y registrar abortos. El piloto de profundidad7 anterior falló cobertura: no se transforma en profesor fiable por tener más profundidad nominal.
4. Descartar offline cualquier candidato que degrade la retención o la selección prefijadas. Solo entonces valorar costo y nuevas partidas oficiales; no gastar partidas para corregir un deterioro detectable con datos ya disponibles.
5. Confirmación de fuerza sobre semillas y rivales nuevos, con control de misma búsqueda y contraste final con P. Fijar protocolo antes de jugar. No usar las reservas históricas ni la confirmación cancelada de N para retocarlo.

Este diagnóstico completa la evaluación de N y orienta otra hipótesis; no ejecuta un nuevo entrenamiento ni cierra por sí solo toda la fase5. Sigue pendiente un modelo elegido con evidencia suficiente y un profesor cualificado, o el rechazo delimitado que corresponda al contrato.

Evidencia primaria: `resultados/medicion/fase5_20261028/transferencia_mc/{RESULTADO.json,predicciones.npz,DIAGNOSTICO.md}`; herramienta `estudiantes/iacasitegano/herramientas/fase5_diagnostico_transferencia.py`. Partidas y CSV: `resultados/medicion/fase5_oficial_20261028/`; hashes y respaldo de 187 JSON originales verificados. No se duplican copias como partidas extra.
