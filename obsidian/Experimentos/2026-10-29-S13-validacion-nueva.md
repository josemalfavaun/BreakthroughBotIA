---
tipo: experimento
estado: validacion-y-equivalencia-aprobadas
fecha: 2026-10-29
baseline_commit: 85b2d55
---

# Validación nueva de S13fijo

## Hipótesis falsable y cambio aislado

El único modeloS13aba46e55ya entrenado y congelado conserva mejoraBrier≥.002/logloss no peor en datos nuevos,con colores dentro de+.005. No ajustar al conocer este lote. Comparar base37678d0b, sin cambiar pesos/algoritmos.

## Protocolo fijado antes de medir

[[resultados/medicion/fase5_validacion_S13_64_20261029/PROTOCOLO]] yCONTRATO.json.64episodios4×16,mismo profesorU7/3M,rivalesfijos,semillas98–101millones auditadas incluyendo ignorados.24grupos MC/agresivo/carrera para validación,8UCTnuevos reservados sin evaluar. Purga estado/espejo contra desarrollo previo y entre familias; cobertura min12global/4familia/4color×fase. Una exposición. No test256 ni promoción.

## Resultado

64/64episodios terminados30/oct04:26:18, cuatro salidas0. Validación nueva pasó las puertas congeladas:4512filas/24grupos después de purga225filas; Brier por grupo0.13163538→0.12574267, mejora0.00589271≥0.002; logloss0.40312045→0.39003946. Ambos colores mejoran; inicio empeora ligeramente0.00039721. No reentrenar ni cambiar umbrales con estas métricas. Los8gruposUCTnuevos permanecen sin evaluación del modelo, test256sin abrir.

Comprobación funcional posterior sobre48estados del piloto HISTÓRICO visto,NPZS13fijo y buscadorU:288comparacionesPython y288Numba correctas; máximos errores logit5.33e-15/utilidad4.44e-16. No mide costo oficial ni fuerza. Auditoría final:24fuentesactuales+17del256yprincipal intactos, contrato/dataset/modelo/64paresdearchivosporSHA correctos. Primera auditoría de semillas se corrigió para incluir ignorados ANTES de generar;0usospreviosdetectados. Suspensiones de tapa demoraron la sesión sin cambiar su presupuesto/reiniciarla.

## Artefactos y comandos

[[resultados/medicion/fase5_validacion_S13_64_20261029/LEEME]] enlaza comando con liberación,estado,tests,auditoría y fuentes. Herramientas/pc/validar_s13_nuevo.py y test_validar_s13_nuevo.py. Sin JITenfixtures,CPUacotada; no medir tiempos de estas pruebas como rendimiento del bot.

## Decisión

S13pasa validación prospectiva y equivalencia funcional; todavía NOes modelo aceptado. Falta protocolo de examen reservado, controles técnicos específicos y partidas oficiales. No abrir test ni liga automáticamente. I0/8B.2no certifica los pesosS13. Seguimiento terminado y automatización eliminada con confirmación de la app; fase5global sigue abierta. Evidencia primaria y comandos: [[resultados/medicion/fase5_validacion_S13_64_20261029/RESULTADOS]], RESULTADO_VALIDACION.json,AUDITORIA_CIERRE.json,funcional_python.jsonyfuncional_numba.json.
