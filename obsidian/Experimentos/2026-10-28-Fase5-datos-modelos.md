---
tipo: experimento
fecha: 2026-10-28
estado: adaptacion-rechazada-serie-oficial-completa
---

# Fase 5: decisiones, datos y modelos reproducibles

> **Cierre 29 de octubre:** 160 desarrollo +4 técnicas válidas: **U43/80, N6/80**, sin fallos técnicos. N rechazado, sin promoción ni confirmación. El diagnóstico muestra deterioro en Montecarlo y retención histórica: [[2026-10-29-Diagnostico-transferencia-y-proximo-ajuste]]. El estado vigente es [[01-Estado]]; las instantáneas siguientes conservan cronología.

> **Instantánea histórica al retomar por la noche (superada por el cierre siguiente):** panel real terminado en horizontes 1/2/3 (72 comparaciones, sin discrepancias con el oráculo; 8 casos sensibles al horizonte). Receta del modelo activo **regenerada**: diferencia máxima de pesos 1.78e-15; el regularizador λ100 estaba centrado en la base antigua. Generados y verificados 60 episodios/6,417 posiciones. El primer reentrenamiento/GA y la proyección simétrica no se promueven. Un segundo ajuste centrado en el modelo activo pasó filtros internos: Brier agrupado en UCT reservado 0.07072→0.04347, mejora en ambos colores, 9 grupos; selección solo 2 grupos. Candidato aislado en `fase5-adaptacion`, peso SHA `ab1a599270424a40ff323dceb3aad3b2358a9ff87979f72db0721ad1fd5b3718`. Python: 12 raíces/12 terminales, diferencia máxima 2.78e-17. **Numba oficial correcto**: 10 hojas, 4 terminales, 12 raíces y 72 ventanas, cero diferencias. Caché N regenerado (30 archivos/1,211,696 bytes); ambos validadores y tres arranques fríos por versión pasaron. **Serie oficial en curso**, sin resultado de fuerza todavía. Evidencia: `resultados/medicion/fase5_oficial_20261028/{progreso.json,manifiesto.json,RESULTADOS.md}`. Protocolo: [[2026-10-28-Protocolo-modelo-adaptado]]. Los apartados siguientes conservan la cronología de la investigación.

## Cronología inicial (superada por los resultados posteriores)

Los estados pendientes de este apartado describen la preparación de la tarde. El estado vigente y la evidencia actual se indican arriba y en la tabla siguiente.

## Alcance inicial

Trabajo autorizado en paralelo a fase 2, ventana indicada por Jose 16:30–18:00. El entrenamiento largo se reserva para casa. Estado confirmado: 5A cerrada sin promoción; 5B analizador listo/panel real pendiente; 5C auditoría reproducida/receta de ajuste histórico todavía incompleta; 5D–F herramientas de datos/modelos/GA listas y probadas sintéticamente, sin entrenamiento real ni partidas nuevas.

Ruta operativa: [[07-Plan-definitivo]]. Evidencia primaria de esta sesión en `resultados/medicion/fase5_20261028/`.

## Pregunta y protocolo prospectivo

¿Mejoran las decisiones y la fuerza al entrenar un evaluador ligero con particiones realmente agrupadas, comparar ridge/logística y ajustar tres parámetros con GA? Primero resolver decisiones y datos; después seleccionar por métricas offline; finalmente pruebas de búsqueda, costo y partidas oficiales independientes. Esta sesión no modifica el bot activo.

Datos históricos: objetivo resultado real de la partida, visto por quien tenía el turno. Son desarrollo ya usado para selección anterior. Las métricas sobre ellos no constituyen una nueva confirmación y no se usan semillas oficiales reservadas.

Nueva preparación: grupos completos de semilla/pareja/juego, hash con sal `_fase5_20261028` y cortes 60/20/20. Grupos con rival `noche_minimax_fijo` enteros en prueba interna; purga de estado/espejo de ajuste si aparece en selección/prueba y de selección si aparece en prueba. Las tres partes siguen siendo históricas. La prueba final de generalización necesitará rivales y partidas nuevos.

Comparaciones fijadas: características actuales ligeras; logística con objetivo y y ridge con retorno 2y−1, sin intercepto; escalas calculadas solo con ajuste; igual peso por grupo; lambdas 1/10/100/1000. Selección por Brier con igual peso por grupo. GA sobre el modelo seleccionado, tres multiplicadores puntos/filas/marcador en [0.75,1.25], patrones fijos; población 12, cinco generaciones más población inicial, 72 evaluaciones. Torneo 3, dos élites, cruce aritmético, mutación gaussiana σ0.05 y probabilidad 1/3 por gen. Semilla 20261028; referencia aleatoria de 72 con semilla +1. Fitness: Brier agrupado de ajuste. Variante final elegida en selección. No variar estas decisiones tras ver la prueba interna.

Ridge requiere enlace de retorno acotado y terminales ±1; sus pesos no se pueden interpretar como logits. Logística requiere declarar escala de búsqueda para cada comparación. Ningún artefacto se promueve solo por mejorar Brier.

## Auditoría del modelo activo

Dataset encontrado: `/Users/josema/noche_salida/lab/posiciones_resultado.npz`, 77,038 posiciones de 1,985 partidas; 705 grupos de dados. Se encontraron las 1,985 fuentes originales; ninguna faltante. Se reconstruye la partición histórica con hash SHA-256 de ID + `_principal`: **61,247 ajuste / 15,791 validación**, coincidente con el informe anterior.

La extracción vectorizada de las cuatro familias activas reproduce el modelo y su **logloss 0.5379266399**. Brier 0.1846647579. Igualando peso por grupo: logloss 0.5379858156 y Brier 0.1849069691.

Hallazgos de dependencia:

- **288 grupos de dados aparecen en ambas particiones**. 13,956 filas de validación corresponden a alguno de esos grupos. Es una agrupación conservadora por dado compartido entre colores/configuraciones; no son 13,956 errores de etiqueta.
- **462 estados exactos aparecen a ambos lados**, sumando 1,272 filas de validación repetidas en ajuste.
- 71,689 estados distintos en el dataset completo; 499 tienen resultados observados distintos entre sus apariciones. El azar y las políticas pueden explicar esas diferencias: no se declaran etiquetas equivocadas.
- Al excluir estados repetidos en ajuste, el logloss de validación baja a 0.52582. Por tanto, no se afirma que el solapamiento infló necesariamente el resultado publicado ni se estima aquí el efecto causal del sobreajuste.

| Subconjunto de validación histórica | Posiciones | Logloss | Brier |
|---|---:|---:|---:|
| Inicio, ply <20 | 4,060 | 0.68458 | 0.24576 |
| Medio, ply 20–59 | 7,670 | 0.55490 | 0.19034 |
| Tardío, ply ≥60 | 4,061 | 0.35925 | 0.11286 |
| Alguien con dos puntos | 1,671 | 0.24512 | 0.07297 |
| Frente a minimax histórico | 290 | 0.64480 | 0.22639 |

Estos cortes no tienen la misma dificultad ni tamaño. Inicio cerca de 0.5 puede reflejar incertidumbre real; una pérdida mayor no demuestra por sí sola un error estratégico. El pequeño conjunto minimax aconseja ampliar diversidad, sin concluir inferioridad de fuerza a partir de la calibración.

El intento inicial con regularización hacia cero produjo λ inferida87.54 y residuo0.1787; aquel supuesto era incorrecto. Después se recuperó el prior de seis pesos antiguos y se regeneró la receta λ100: error máximo de pesos1.78e-15 y logits3.55e-15. Ver `reproduccion_activo/RESULTADO.json`. El NPZ activo no se reemplazó.

Evidencia vigente: `auditoria_particion_principal/{auditoria.json,predicciones_y_grupos.npz}`. La carpeta `auditoria_historica/` conserva una exploración inicial **sin la sal `_principal`**, con una partición distinta; no es la reproducción histórica ni entra en los resultados de esta nota.

## Diagnóstico de decisiones

`fase5_diagnostico.py` carga el panel congelado y el control A con TT corregida, sin modificarlo. Oráculo exhaustivo independiente con motor oficial y características Python, sin JIT ni poda. Contrasta valor/jugada de A a igual horizonte. Evalúa cada acción y sus ramas de combate.

Además propaga cotas del valor real del juego: terminales exactos; hojas no resueltas con intervalo [-1,1]; MAX/MIN y esperanza ponderada por probabilidades. Un certificado requiere que el límite inferior de una alternativa supere el superior de la jugada observada. Es independiente de la puntuación de eval3. Los valores heurísticos a profundidad fija se etiquetan como tales. Los límites de tiempo/nodos producen parcial/desconocido, nunca una solución exacta inventada.

Prueba sintética validada: blancas a8/e4 y negras i2/f5, ambos con dos puntos. La observada e4-e5 no se demuestra mala a horizonte 1; a horizonte 2 permite tercer punto negro con certeza, frente a a8-a9 que gana con certeza. Se verificó el certificado [0,0] frente a [1,1] y coincidencia del buscador. **No es un error encontrado en las partidas reales.**

Completado: 24 casos reales a horizontes1/2/3, ocho sensibles al horizonte y16 sin discrepancias; ningún error histórico certificado. Un certificado sobre una jugada histórica demuestra una decisión peor en ese estado, pero atribuirla a un bug, horizonte o modelo requiere contrastar la configuración y profundidad reales.

## Herramientas y verificación

Dentro de `estudiantes/iacasitegano/herramientas/`:

- `fase5_features.py`: características ligeras vectorizadas, particiones y métricas agrupadas.
- `fase5_auditar_dataset.py`: auditoría, predicciones y perfiles, sin entrenar.
- `fase5_diagnostico.py` / `fase5_resumir_decisiones.py`: alternativas, cotas y resumen del panel.
- `fase5_preparar_datos.py`: particiones por grupo y purga de estados/espejos.
- `fase5_modelos.py` / `fase5_entrenar.py`: ridge, logística, GA y checkpoints.
- `fase5_empaquetar.py`: paquete explícito y portátil para CPU.
- `test_fase5.py`: cuatro pruebas de características/perspectiva, regresiones, grupos y GA.

Verificado: 24 estados del panel y 18 combinaciones de marcador/perspectiva contra referencia; predicciones coincidentes a tolerancia 1e-10. Ridge sintético recupera pesos con error máximo 5.18e-11; logística satisface gradiente en su test; GA reproducible con 72 evaluaciones y referencia base incluida. Prueba completa sintética de CLI, exportación y reanudación correcta. No representan evidencia de fuerza.

## Entrega de trabajo para casa/escritorio

Paquete preparado y verificado por manifiesto: `resultados/medicion/fase5_20261028/paquete_entrenamiento_cpu.tar`, **5,621,760 bytes**, SHA-256 `3a1e5f95ff70c7ee52695ada6adffa710d03916ec9cffec51962028fc8fe17fc`. Incluye datos históricos, base, auditoría, cuatro herramientas de entrenamiento y LEEME. Excluye Git, credenciales y cachés. El entrenamiento del paquete no requiere GPU, motor ni red; Python/NumPy deben estar preparados. [[08-Escritorio-y-entrenamiento]].

No se inició el ajuste sobre los datos reales mientras fase 2 medía tiempos. El comando inicial `nice` no pudo bajar prioridad en el sandbox; la auditoría terminó con pausas entre lotes. Se hicieron lecturas y pruebas técnicas breves; no se midió rendimiento propio. No afirmar aislamiento físico perfecto de la máquina compartida.

## Plan inicial y resultados posteriores

1. Reservar una ventana CPU y ejecutar panel real (al menos dos horizontes completos por caso o registrar la limitación).
2. Preparar datos purgados y ejecutar un ajuste piloto con checkpoint; medir costo de entrenamiento y dimensionar la noche.
3. Completar selección ridge/logística y GA según contrato; revisar candidato, enlace y costo de búsqueda.
4. Generar nuevas posiciones/etiquetas dirigidas por los casos y ampliar rivales; protocolo oficial independiente antes de partidas.

Fase5 completa sigue abierta: diagnóstico/pipeline/datos/GA ya ejecutados; falta un profesor cualificado y una elección del modelo con confirmación suficiente. Modelo/buscador activos, reservas y ramas de entrega conservados; sin commit, merge, push ni promoción.

## Resultados de la ejecución nocturna

| Trabajo | Resultado confirmado | Evidencia en `resultados/medicion/fase5_20261028/` |
|---|---|---|
| Receta activa | IRLS λ100, escalas de ajuste sin centrar datos, prior de pesos antiguos; máximo error pesos 1.78e-15 y logits 3.55e-15 | `reproduccion_activo/RESULTADO.json`; `fase5_reproducir_activo.py` |
| Panel 24 estados | 72 contrastes a horizontes 1/2/3, cero discrepancias; 8 sensibles al horizonte; sin decisión histórica objetivamente peor demostrada | `diagnostico_d1_d2/`, `diagnostico_d3/` |
| Ridge/logística y GA | Entrenamiento real con grupos/purga; logística λ100 gana selección; GA 72 evaluaciones apenas mejora selección; no supera filtro interno frente al activo | `ajustes_reales/DECISION.json` |
| Profesor profundo | 18/18 ramas completas a profundidad 5; 6/18 a 7, insuficiente para cobertura prefijada 80%; sin etiquetas parciales inventadas | `profesor_piloto/`, `PROTOCOLO_PROFESOR.md` |
| Datos nuevos | 60 episodios, 6,417 posiciones; rivales UCT512, agresivo y carrera; ambos colores; replay independiente completo correcto | `episodios_60/VERIFICACION.json`, `dataset_060.npz` |
| Simetría | Proyección exacta mejora invariancia pero falla filtro en seis episodios: Brier 0.05865→0.06911; rechazada | `simetria/`, `PROTOCOLO_SIMETRIA.md` |
| Adaptación centrada | λ100, prior activo completo; selección 2 grupos; UCT test 9 grupos, Brier 0.07072→0.04347 y ambos colores mejoran; pasa filtros internos | `adaptacion_nueva/RESULTADO.json`, `PROTOCOLO_ADAPTACION.md` |
| Fuerza oficial | Puerta técnica superada; 4 técnicas y 160 de desarrollo en curso; sin promoción | carpeta hermana `fase5_oficial_20261028/` |

La receta antes pendiente se resolvió: el error estaba en suponer regularización hacia cero; el entrenamiento histórico se centraba en `pesos.npy` de seis elementos. La reproducción no cambia el NPZ desplegado. El ajuste inicial y la adaptación posterior son experimentos distintos, con protocolos guardados antes de consultar su prueba interna; no se alteró un umbral después de ver resultados.

El profesor y los episodios usan búsqueda de utilidad U, no una referencia perfecta. Las etiquetas de episodios son resultados de políticas concretas con presupuesto diferente al oficial. No atribuir el cambio de Brier a decisiones corregidas ni a victorias nuevas hasta jugar. El subconjunto de selección de la adaptación tiene solo dos grupos, limitación material.

Paquete completo portátil verificado: `laboratorio_fase5_sesion.tar`, 10,844,160 bytes, SHA `803f45a4a30b684c3caf8de15f88e41716ec6369461940ef27e3fe2faee10a27`. Incluye motor público sin modificar, herramientas, receta, 60 episodios y fuentes del profesor; 217 hashes correctos al extraer. Sin Git, credenciales ni cachés. No ejecutado todavía en el escritorio Windows. Paquete solo NumPy con receta: `paquete_entrenamiento_cpu_v2.tar` (5,632,000 bytes). No transferido automáticamente.

Fase 5 permanece abierta: falta resultado oficial, confirmación independiente si pasa desarrollo y diagnóstico causal de errores reales. Fases 6/7/8/9 conservan sus contratos. No hubo commit, merge, push ni promoción.

## Cierre oficial de esta adaptacion — 2026-10-29T01:01:03.080712-06:00

N 6/80, U 43/80, delta-37; N3/40 en cada semilla, sin fallos propios. **NO PASA**; sin promocion ni confirmacion.160 desarrollo+4 tecnicas validas;23 interrumpidas por GRIS excluidas antes de repetir todo el bloque. GRIS restaurado. Informe en `resultados/medicion/fase5_oficial_20261028/RESULTADOS.md`, auditoria final y respaldo de originales en la misma carpeta. Diagnostico posterior `transferencia_mc/DIAGNOSTICO.md`; no se ajusto el modelo ni el filtro. Los apartados sobre partidas pendientes son cronologia, no estado vigente.
