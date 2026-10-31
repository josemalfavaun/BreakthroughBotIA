---
tipo: plan-de-cierre
fecha: 2026-10-28
revision_base: 85b2d55
estado: vigente
---

# Fases, prioridades y criterios de cierre

> Actualización del 28 de octubre: el mapa operativo vigente es [[07-Plan-definitivo]], que integra la investigación, GA/regresión/profesor offline, explicita la fase 8 de integración y abre la fase 9 final. Este documento conserva el detalle técnico original; las tareas de utilidad de abajo son históricas: **5A terminó 41/80 frente a 48/80, +7, no pasa +8, sin promoción**. Los 164 JSON válidos se verificaron por hash y recuento. Panel 24×3 ya analizado y clasificado; 5B cerrado en su alcance, sin error histórico demostrado.

## Cómo se declara una fase terminada

Una fase se cierra cuando su pregunta delimitada tiene evidencia y una decisión registrada: incorporar una mejora o rechazarla y conservar la base. Un rechazo no demuestra que toda la familia de técnicas sea inútil. Una nueva hipótesis puede abrir una subetapa, con protocolo propio.

«100%» se refiere al alcance probado de la etapa y a la versión identificada. No significa seguridad en cualquier ordenador, fuerza superior a Tier 5 ni que todos los prototipos estén integrados. La entrega final exige volver a validar la combinación elegida. No asignar porcentajes subjetivos a tareas pendientes.

## Registro de fases

| Fase | Estado a esta revisión | Evidencia / límite |
|---|---|---|
| 0. Baseline medible | Cerrada para el criterio de salida original | 40 partidas oficiales, ambos colores, semillas identificadas y reservas separadas; 240 A/A adicionales. El diagnóstico contrafactual nuevo pertenece al trabajo de evaluación, no se da por resuelto. |
| 1. Seguridad y reloj | Cerrada operativamente para el baseline evaluado | Caché integrado en `85b2d55`; 20 preparaciones frías históricas y tandas oficiales sin fallos técnicos, incluidas 240 A/A. Los nuevos candidatos y el entorno final requieren su propia validación. Memoria pico exacta no medida. |
| 2. Ordenamiento | Cerrada: no incorporar pistas TT probadas | Codex: 60 posiciones, 1200 búsquedas, diferencia de valor 0. Mediana B/A 0.982591 frente al filtro ≤0.95. Menos nodos no justificaron el costo; no se ejecutó liga. [[Experimentos/2026-10-28-TT-pistas-internas]]. |
| 3. Star2 | Cerrada: no incorporar la versión probada | 2,000 posiciones sin diferencias; +0.032 niveles con presupuesto fijo, insuficiente para incorporarla. No se afirma mejora en partidas oficiales. Corrección TT nueva se trata como requisito común de los experimentos actuales. |
| 4. Híbrido | Cerrada: rechazado | Desarrollo 100/versión: 55 victorias híbrido, 49 base. Reservado 40/versión: 24 híbrido, 29 base; no sostuvo la mejora. Informe en rama `codex/fase4-hibrida`, revisión `750b6c82db7438e261525801d787412d3776c393`, `estudiantes/iacasitegano/herramientas/FASE4_HIBRIDA.md`. |
| 5. Evaluación/aprendizaje | Abierta, prioridad principal | 5A cerrada sin promoción; 5B cerrado, receta/auditoría reproducidas, ridge/GA evaluados, datos nuevos verificados. Adaptación centrada N rechazada: U43/80, N6/80; cero fallos. Profesor cualificado y selección/confirmación de modelo pendientes. |
| 6. Finales | Cerrada: no integrar tablas ni ampliación examinada | 890trazas/36,730raíces,35,094estados únicos,0errores de replay. Tablas pequeñas/dominio≤6:0raíces;25carreras privadas ya cubiertas por victoria segura inmediata. Hojas sin medir. `resultados/medicion/fase6_cobertura_20261029/CIERRE.md`. |
| 7. Aperturas | Abierta, después de estabilizar modelo/búsqueda | Libro existente; generador usa `busqueda_numba`/`eval`/`pesos.npy` antiguos, no el pipeline activo. Falta adaptar, medir cobertura y comparar libro frente a búsqueda. |
| 8. Integración/entrega | Abierta; explicita el control antes transversal | Probar la combinación, validar entrega y congelar finalista/respaldo. [[07-Plan-definitivo]]. |
| 9. Calibración comprobada y pulido | Abierta; última fase | Examen de versión congelada, rivales/semillas nuevos, seguridad e informe; no entrenar sobre el examen. [[07-Plan-definitivo]]. |

Resultado actualizado: **6 etapas cerradas (0,1,2,3,4,6), 4 pendientes (5,7,8,9)**. En fase 5: 5A cerrada sin promoción; panel5B y receta/auditoría5C completados en su alcance; Nrechazado y lote256nuevo generando, sin candidato nuevo aún. Fase 8 explicita integración y fase 9 será la última. Ver [[Experimentos/2026-10-28-Fase5-datos-modelos]].

## Prioridad 1 — Utilidad y riesgo (fase 5A)

**Responsable de medición: Codex de terminal.** Alcance y reglas ya congelados en [[Experimentos/2026-10-28-Protocolo-utilidad-victoria]]. No cambiar ese protocolo por este plan.

1. Verificar identidad de A/B, modelo, libro, imágenes y cachés; misma corrección TT y reparto de tiempo. No tocar fuentes congeladas.
2. Aprovechar validación ya realizada: B pasó Python y Numba (10 hojas, 4 terminales, 12 raíces y 72 ventanas reutilizadas), caché regenerado y 3 preparaciones frías, máximo 0.372181 s. Aviso del validador a 3 s pendiente de contraste con reloj oficial.
3. Completar preparaciones pendientes de A y 4 partidas técnicas de B, semilla 20261115, límites oficiales. Un fallo propio detiene para revisar, sin ocultarlo.
4. Desarrollo fijo: 160 partidas, 80/versión; semillas 20261109/10, orden A-B/B-A. Primaria victorias, secundarios peones, desglose por semilla/color y seguridad.
5. Filtro ya fijado: B ≥8 victorias adicionales/80, >40 victorias/80 y ninguna semilla con diferencia negativa, sin fallos propios. Es un filtro práctico, no significancia estadística.
6. Si falla: cerrar esta versión de utilidad como no promovida y conservar datos. Si pasa: congelar B y fijar un protocolo separado de confirmación antes de tocar reservas 20261111–14; incluir comparación con el bot principal original, porque A ya contiene otra corrección TT.

**Cierre 5A:** decisión reproducible sobre esta escala de utilidad. «Pasó desarrollo» no equivale a aceptar. Para una aceptación hacen falta confirmación y seguridad de la combinación final. No interpretar la sigmoide como probabilidad verdadera sin revisar calibración/política de entrenamiento.

## Prioridad 2 — Diagnóstico de decisiones (fase 5B)

**Responsable: este chat.** Primera herramienta implementada: `estudiantes/iacasitegano/herramientas/extraer_casos_decision.py`.

Hecho: 40 trazas y 3,231 plies reconstruidos con motor oficial, probabilidades/ganador/puntos verificados; 282 estados distintos previos a decisiones, 143 blancos/139 negros, IDs sin duplicados. Artefactos: `resultados/medicion/diagnostico_decisiones_20261028_baseline40/{manifest.json,casos.jsonl}` en el principal. Son datos vistos de desarrollo; no reservarlos después como confirmación.

Siguiente trabajo:

1. **Congelar un panel inicial de 24 casos antes de evaluar alternativas:** 8 con muestreo fijo temprano, 8 con amenazas/2 puntos, 8 tardíos; ambos colores y presencia de victorias/derrotas. Elegir por metadatos, con regla estable e IDs publicados; sin seleccionar solo casos donde gana el candidato. Las categorías pueden solaparse: deduplicar y reponer con regla documentada.
2. Crear un analizador que reciba solo tablero, turno, puntos y jugadas legales. Resultado real, tiradas posteriores y semilla del árbitro no entran en el cálculo contrafactual. Enumerar ramas de combate con sus probabilidades, no repetir el dado que ocurrió como si fuera el futuro conocido.
3. Ejecutar base/candidato a igual profundidad y a igual presupuesto de nodos, registrando valor de **cada alternativa**, mejor conjunto de jugadas, nodos, cortes/TT y abortos. Usar ventanas exclusivas para compilación/búsqueda. Estas comparaciones no sustituyen partidos a reloj.
4. En posiciones pequeñas comparar con expectiminimax exhaustivo independiente a la misma profundidad. Separar cuatro resultados: **bug comprobado de búsqueda**, **sensibilidad al horizonte**, **indicio de fallo del modelo**, **sin evidencia suficiente**. Si se resuelve todo el final, se puede hablar de valor óptimo de juego; profundidad fija solo prueba el árbol truncado.
5. Registrar para cada caso: estado e ID fuente, jugada observada, alternativa, probabilidades, diferencia de valor, referencia, profundidad/presupuesto, hash de código/modelo y nivel de certeza. Una derrota final o dos ataques fallidos no demuestran mala decisión.
6. Convertir contraejemplos confirmados en regresiones pequeñas. No contar varios estados de una misma partida como réplicas independientes. Publicar también casos sin discrepancias.

**Cierre 5B:** 24/24 casos reproducibles y clasificados con su límite de certeza, comandos y manifiesto; herramienta capaz de ampliar al resto de 282. No exigir «encontrar N errores»: si la muestra no prueba errores, ese es un resultado válido. No vender un cambio de jugada como mejora sin referencia.

## Prioridad 3 — Modelo reproducible y mejora dirigida (fase 5C)

**Responsable de receta/análisis: este chat; entrenamiento y partidas: ventana exclusiva posterior.**

Hallazgo adicional: el artefacto de ablación `/Users/josema/noche_salida/lab/_pesos_ligero5_solo_puntos_patrones_filas_marcador.npz` coincide byte a byte con el activo (`37678d...2250b`), no solo con una copia de despliegue. Claves: `pesos[275]`, `crudo[267]`, modelo `ligero5_solo_puntos_patrones_filas_marcador`. El entrenador IRLS y validación por resultado están localizados, pero la receta exacta de esa ablación sigue pendiente.

1. Inventariar fuentes, dataset/generación, columnas, etiquetas desde la perspectiva correcta, familias activas, normalización, penalización, semillas, partición, versiones y comando que genera el NPZ. El entrenador lineal de seis features del equipo no reproduce este modelo.
2. Portar a herramientas offline del equipo solo dependencias necesarias, sin rutas privadas ni dependencia de otros equipos experimentales. Hacer una regeneración aislada. Comparar arrays y predicciones con tolerancia fijada; registrar el hash del artefacto original. Un ZIP NPZ puede cambiar de hash aunque conserve los arrays: distinguir identidad de archivo de equivalencia numérica.
3. Auditar partición por **partida, par de dados y repeticiones**; todas sus posiciones permanecen juntas. Deduplicar estados equivalentes entre conjuntos. La validación histórica usada para elegir varias ablaciones ya no es confirmación nueva. Documentar excepciones si no se puede reconstruir la genealogía de los datos.
4. Diagnóstico de calibración del modelo fijo: Brier/logloss y curvas por bandas de probabilidad, fase de partida y marcador; tamaños de muestra por grupo. Reponderar/resumir por partida e intervalos agrupados, para que una partida larga no finja muchas muestras independientes. Evaluar bajo la política que generó los datos y declarar sus diferencias con la actual.
5. Elegir **una** limitación respaldada por 5B/esta auditoría. Candidatos posibles: recalibrar escala, corregir cobertura de carreras o ajustar la penalización. No mezclarlos ni añadir features por intuición. Recalibrar puede afectar decisiones bajo azar aunque preserve el orden estático.
6. Si hacen falta datos de acciones, comparar alternativas desde el mismo estado con continuaciones/presupuestos equivalentes y varias semillas privadas ajenas a los dados oficiales. Separar etiquetas exactas, aproximaciones de búsqueda y estimaciones bajo una política de rollout. Recuperar primero por qué las preferencias anteriores no mejoraron; acuerdo con nuestra propia búsqueda no es evidencia independiente de fuerza.
7. Congelar entrenamiento/selección/prueba final antes de ajustar; no entrenar sobre las reservas de partidas ni ajustar tras verlas. Revisar que el modelo siga siendo no neuronal, legible y barato dentro de la búsqueda completa.
8. Un candidato pasa de métricas offline a una comparación oficial con el modelo vigente, mismo buscador. Muestra y criterio fijados antes de jugar; confirmar en datos/semillas nuevos y sin fallos técnicos.

**Cierre 5C y de fase 5:** pipeline regenerable, diagnóstico de calibración documentado, decisiones sobre los candidatos delimitados y versión elegida confirmada. Si ninguno mejora, conservar el modelo actual y documentar esa decisión; no prolongar ajustes sobre el mismo reservado. Nuevas ideas abren otra iteración, no alteran resultados ya cerrados.

## Fase 2 reabierta — Ordenamiento mediante jugadas TT

**Responsable: este chat, después de disponer de la base estratégica elegida; prototipo separado.** Diseño e instrumentación ligera se pueden preparar mientras termina la medición, sin modificar A/B.

1. Mantener idénticos utilidad, pesos, tiempo, libro y corrección de valores exactos. El cambio será únicamente examinar primero una jugada sugerida en nodos internos; no ordenar toda la lista con una evaluación cara.
2. Resolver el detalle actual: un acierto exacto devuelve directamente y la tabla se crea por llamada a la raíz/profundidad. Guardar jugadas solo en esos mismos aciertos no aporta ordenamiento. Prototipo inicial: pistas separadas de los valores, también en nodos completos que hicieron corte y devolvieron cotas. La pista puede cambiar el orden; **jamás** convierte una cota en valor exacto.
3. Validar clave completa, turno/puntos, procedencia/profundidad, colisiones y legalidad antes de usar la pista. No guardar valores parciales tras aborto. Ninguna pista se comparte entre partidas ni entre objetivos incompatibles. Contabilizar memoria y costo de crear tablas.
4. Registrar consultas, pistas útiles que se usan sin devolver un valor exacto, movimientos efectivamente adelantados, cortes obtenidos, nodos y tiempo completo. Si casi nunca se usa, cerrar no-go antes de una liga costosa. Compartir pistas entre iteraciones sería otra variante posterior; no mezclarla inicialmente.
5. Corrección: posiciones pequeñas exhaustivas, ataques y terminales, MAX/MIN, ventanas estrechas/amplias, colisiones, entradas obsoletas y abortos. Valores deben coincidir dentro de tolerancia numérica fijada; con empates aceptar cualquiera de las jugadas óptimas. No exigir mismo número de nodos, que precisamente puede cambiar.
6. Congelar un panel de 60 posiciones reales, 20 por fase, sin seleccionarlo por velocidad. Medir compilado y calentado, A/B y B/A, 5 repeticiones por posición, búsquedas completas de igual profundidad, incluyendo asignaciones/inicialización. Filtro de costo propuesto para fijar antes de medir: mediana de tiempo B/A ≤0.95 y ninguna fase con mediana >1.05; cero fallos de exactitud. No sumar el supuesto beneficio con el 1–2% de otros prototipos.
7. Si pasa, fijar A/B oficial y confirmación con semillas nuevas. Una mejora de nodos/tiempo sola no cierra aceptación de fuerza.

**Cierre fase 2:** incorporar con evidencia repetida y seguridad, o rechazar y conservar el orden actual. El rechazo anterior de ordenamiento general permanece; este experimento responde una pregunta distinta.

## Fase 6 — Finales, con una decisión de costo/beneficio

1. Medir aplicabilidad del detector existente en **todas** las decisiones de las nuevas trazas, no solo en los 282 casos seleccionados. Registrar contador y denominador, material, puntos y duración restante. Cero activaciones anteriores sigue siendo evidencia contra aquel dominio.
2. Si hay oportunidades frecuentes, delimitar un único dominio ampliado por material/puntos con presupuesto de tiempo/tamaño explícito. Si no las hay, cerrar como no prioritaria y conservar el solver fuera de la entrega; no invertir en una tabla grande sin casos donde se vaya a usar.
3. Para el dominio elegido, solver con turno, puntos, reglas de puntuación/bloqueo y probabilidades reales. Un límite de nodos que se alcanza devuelve «no resuelto», nunca un valor etiquetado exacto. Verificar todos los estados de un subdominio pequeño y casos frontera contra motor/oráculo.
4. Medir frecuencia, costo de preparación, consulta y bytes. Después A/B oficial con y sin solver, seguido de confirmación si hay señal. Datos de tabla auditables y regenerables.

**Cierre fase 6:** solver útil validado e integrado, o decisión documentada de no incorporarlo por cobertura/costo/resultados. Su cierre no requiere que gane una técnica que apenas se activa.

## Fase 7 — Aperturas con el algoritmo final

1. Congelar primero modelo/buscador; adaptar el generador antiguo a ese pipeline y sus firmas actuales. Prueba de generación a carpeta nueva, sin sobrescribir `libro.json`.
2. Medir cobertura por color/posición. El baseline mostró 21 consultas de libro blancas y ninguna negra; no deducir causalidad sobre victorias de esa asimetría.
3. Comparar alternativas desde una misma apertura y múltiples continuaciones, incluidas respuestas distintas al self-play. Guardar muestras e incertidumbre por entrada; evitar fijar una jugada por una racha de dados favorable.
4. Congelar entradas y probar con árbitro **libro frente a sin libro**, mismo algoritmo. Medir victorias, ambos colores, tiempo ahorrado y comportamiento fuera del libro. Confirmar con semillas nuevas.

**Cierre fase 7:** libro reproducible y confirmado o estrategia final sin libro si no aporta. Una cobertura alta por sí sola no es criterio de aceptación.

## Entrega y coordinación

- Código/NPZ del principal no se sustituyen por una tanda prometedora. Sin commit, merge o push sin petición explícita.
- Una sola ventana para árbitro, compilación, entrenamiento y benchmarks. Codex de terminal tiene la medición de utilidad; este chat hace lectura, documentación y herramientas ligeras hasta disponer de ventana. No iniciar trabajos pesados automáticamente por ver un instante sin contenedores.
- Orden: cerrar utilidad de desarrollo; en paralelo preparar diagnóstico/receta; confirmar estrategia; entrenar un candidato dirigido; evaluar TT; decidir finales; aperturas al final. Los hallazgos pueden cambiar el siguiente experimento, dejando constancia antes de medir.
- Antes de entregar, repetir seguridad del candidato final desde copia limpia/entorno de entrega, medir memoria pico, comprobar ABI/caché y aclarar su distribución según reglas, validar alcance de archivos e informe de 2–4 páginas con nueve secciones. Todo regenerable y sin rutas privadas. [[04-Preparacion-entrega]].
- Cada cierre debe enlazar fuentes/manifiesto, comandos y entorno, resultados por color, fallos/tiempos, limitaciones y decisión. La aplicación de la mejora y su publicación son acciones separadas de la evaluación.

## Evidencia nueva de fase5 — 29 de octubre

N6/80 frente a U43/80, sin fallos técnicos; no pasa, sin promoción. La confirmación condicionada no se ejecuta. Diagnóstico en [[Experimentos/2026-10-29-Diagnostico-transferencia-y-proximo-ajuste]]. Cinco fases0–4 siguen cerradas; 5–9 abiertas. Ningún porcentaje supervisado sustituye victorias; el estado de5 no se cambia a100% por haber terminado esta tanda. GRIS restaurado y originales respaldados/verificados.

Actualización29/oct: cierre6certificado por falta de oportunidad útil en el dominio prefijado; encargo7Aprepara auditoría/generador sin cerrar7hasta modelo y prueba deportiva. [[2026-10-29-Encargo-Codex-fase7A]].
