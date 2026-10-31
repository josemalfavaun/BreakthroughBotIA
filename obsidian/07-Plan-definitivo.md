---
tipo: plan-maestro
fecha: 2026-10-28
estado: vigente-autorizado
entrega: 2026-11-04
---

# Plan definitivo: cierre, entrenamiento y validación final

**Estado29/oct:0–4y6cerradas en su alcance;5,7,8,9pendientes.6rechazada por cobertura.7Aterminada con auditoría/generador;7Bdepende del modelo.8A/8B.1completadas/revisadas;8B.2controles técnicos de I0con respaldo encargados para terminal, ejecución pendiente de confirmación.**

## Autoridad y decisión inicial

Este es el mapa operativo vigente, autorizado por Jose el 28 de octubre. Integra [[06-Investigacion-y-plan-semanal]] y los criterios técnicos de [[05-Cierre-de-fases]]. Los protocolos específicos ya congelados prevalecen para sus experimentos. No se cambian umbrales, muestras o reservas mirando resultados.

Se verificaron por lectura y SHA-256 los **164 JSON válidos** de la última serie de Codex: A 41/80, B 48/80, diferencias por semilla +4/+3; cero fallos técnicos. **5A cerrada: utilidad B no pasa el filtro +8, sin promoción ni confirmación reservada.** No demuestra inferioridad ni equivalencia. No ampliar la misma serie hasta obtener una victoria más. Evidencia: [[Experimentos/2026-10-28-Protocolo-utilidad-victoria]] y `/Users/josema/vs code/BreakthroughBotIA-codex/resultados/medicion/utilidad_victoria_20261028_codex/RESULTADOS.md`.

Fases 0,1,3,4 permanecen cerradas en su alcance previo. 2,5,6,7 requieren las evidencias siguientes. Se explicita como **fase 8** el control de integración/entrega que antes era transversal. Se abre **fase 9**, última etapa: pruebas, diagnóstico final y correcciones mínimas de defectos. Ninguna fase se da por cerrada solo por tener este plan.

## Responsables y coordinación

- **Este chat:** diagnóstico contrafactual, receta/etiquetas/modelos, especificación genética, revisión de evidencia y memoria del proyecto.
- **Codex de terminal:** fase 2 primero; después medición de cobertura/finales, aperturas y arneses oficiales. El encargo actual es [[2026-10-28-Encargo-Codex-fase2]]. No enviarle todas las fases como una ejecución automática sin revisiones intermedias.
- **Escritorio:** generación y entrenamiento offline, cuando esté preparado. No está conectado ni ejecutando este plan. Jose realiza el arranque/configuración inicial; instrucciones en [[08-Escritorio-y-entrenamiento]].
- Solo una carga pesada por host para medir tiempos/partidas oficiales. Trabajo ligero y preparación de código pueden avanzar en paralelo; dos máquinas permiten entrenar y medir sin interferencia. No pausar GRIS ni otros programas sin autorización vigente para esa acción.
- Cada experimento: carpeta/variante aislada, manifiesto de fuentes/pesos/datos/entorno, progreso recuperable y decisión aceptar/rechazar/inconcluso. No commit, merge, push o reemplazo del bot principal por tener un candidato prometedor.

## Orden de dependencias

`5B diagnóstico + 5C receta` pueden prepararse mientras `2 TT` se desarrolla en variante aislada. Después: `5D profesor/datos → 5E regresión → 5F genética → decisión 5`. El reconocimiento de finales de `6` puede hacerse antes; su integración espera la versión seleccionada. `7 aperturas` espera esa misma versión. `8 integración` comprueba la combinación. `9 pulido` se ejecuta al final con todos los parámetros congelados.

MCTS pertenece a la fase 5 como rival y profesor experimental. La fase híbrida 4 rechazada no se reabre por este plan. Una sustitución por MCTS necesitaría demostrar una ventaja propia y queda fuera de la ruta crítica de entrega.

## Fase 2 — Ordenar antes las jugadas útiles

**Pregunta:** ¿las pistas TT en nodos internos ahorran trabajo suficiente bajo reloj? **Responsable: Codex.** Fecha objetivo: 29 de octubre.

1. Partir del control A con TT corregida; registrar también el principal P como referencia de integración posterior. No introducir utilidad B, nuevos pesos, hojas/buffers ni otro reloj.
2. Guardar pistas separadas de valores, incluidas jugadas de nodos completos que devolvieron cotas. El acierto de valor exacto ya retorna: no cuenta como uso útil de ordenamiento. La pista no autoriza una poda ni convierte una cota en valor exacto.
3. Validar identidad completa del estado, legalidad, colisiones y abortos. Oráculo independiente en árboles pequeños; mismas evaluaciones de todos los resultados de combate. Registrar pistas consultadas/usadas, cortes, nodos, memoria y tiempo completo.
4. Panel congelado de 60 posiciones reales, 20 por fase; cinco repeticiones A/B y B/A a profundidad completa igual. Filtro técnico: valores correctos, mediana tiempo candidato/control ≤0.95 y ninguna fase con mediana >1.05. Selección por metadatos, nunca por mejora de velocidad observada.
5. Si no pasa costo o casi no usa pistas: cerrar rechazado, sin liga costosa. Si pasa: escribir un protocolo oficial propio, fijar muestra/semillas/criterio antes de ejecutar y confirmar con datos nuevos. Mínimo de planificación: 80 partidas por versión en desarrollo, 40 por versión de confirmación si pasa; el piloto de costo determina si cabe. Una muestra insuficiente queda inconclusa.

**Cierre:** informe reproducible con decisión de incorporar o descartar. Si solo demuestra velocidad, se informa como velocidad; no como fuerza. Comparar la combinación seleccionada contra P en fase 8: A ya contiene una corrección adicional que P no tiene.

## Fase 5 — Modelo y aprendizaje, con seis entregables

**Responsable principal: este chat; cómputo del escritorio y partidas de Codex en ventanas coordinadas.** Fecha objetivo: 31 de octubre / 1 de noviembre.

### 5A — Escala de utilidad: cerrada sin promoción

Resultado 41/80 frente a 48/80, filtro incumplido. Mantener B archivado como referencia diagnóstica. Ni ajustar temperatura ni utilizar las reservas para rescatar este resultado. Una hipótesis posterior con pesos/datos nuevos compara primero con su control de escala idéntica; su aceptación final requiere comparación con la versión desplegada.

### 5B — Decisiones reproducibles

Congelar 24 de los 282 estados de desarrollo: ocho tempranos, ocho amenazas/marcador de dos puntos y ocho tardíos, ambos colores. Regla estable con desempate por ID, deduplicación y reposición publicada. El resultado de la partida puede describirse después; no se usan dados futuros en el análisis.

**Primer paso completado en esta sesión:** panel de 24 congelado, 12 por color, 20 grupos; artefactos `resultados/medicion/panel24_decisiones_20261028/{panel.jsonl,manifest.json}`, SHA-256 `1ca5a56679eda76a6c38e32851e4a5121b89f256e5bd675ad436c0abc00cbc48`. Herramienta `estudiantes/iacasitegano/herramientas/seleccionar_panel_decisiones.py`. Análisis ya completo en 24×3 horizontes, cero discrepancias con oráculo a igual profundidad; 8 sensibles al horizonte y 16 sin discrepancia. 5B cerrado para su contrato de diagnóstico, sin error histórico demostrado. Ver [[Experimentos/2026-10-28-Diagnostico-decisiones]].

Implementar análisis por alternativa: valor, horizonte, ramas/probabilidades, nodos, aborto y referencia. Resolver exhaustivamente casos pequeños. Etiquetar cada caso como bug demostrado, sensibilidad a horizonte, indicio de error del modelo o evidencia insuficiente. Registrar el nivel de certeza; una etiqueta de búsqueda profunda no es una solución exacta.

**Cierre 5B:** 24 casos analizables, clasificados y reproducibles, incluidos los que no prueban error. No exigir encontrar errores para declarar éxito.

### 5C — Receta y calibración reproducibles

Recuperar generador/dataset, características, etiquetas, IRLS, penalización, particiones y exportación del NPZ activo. Portar lo necesario a herramientas del equipo. Reproducir arrays/predicciones con tolerancia publicada; un NPZ puede variar de hash por metadatos del ZIP. Si faltan datos históricos, declarar esa limitación y producir una receta nueva reproducible sin afirmar que reproduce exactamente el original.

Separar por partidas/grupos de dados, con espejos juntos. Medir Brier/logloss y calibración por fase, marcador y rival, con conteos por grupo. La validación histórica que eligió múltiples ablaciones pertenece a desarrollo. No convertirla en reservado.

### 5D — Profesor externo y generación dirigida

El profesor inicial será **búsqueda offline con más presupuesto**, apoyada por finales exactos donde sea posible y contraste con una segunda política/evaluación. NumPy/SciPy/Numba para cálculo; scikit-learn offline para referencias de regresión/árboles. OpenSpiel como referencia para un MCTS correcto; requiere adaptar tablero, puntuación y azar, no utilizar su Breakthrough estándar como si fuera el nuestro.

Piloto: 24 estados, comparar las mejores alternativas y medir segundos/estado durante diez minutos. Solo después calcular el lote de una hora/siete horas/24 horas. Guardar estado, acciones, valor estimado o intervalo, método, perspectiva, presupuesto, semilla privada, versiones y confianza. Ninguna etiqueta exacta si el solver agota su límite.

MCTS: primero comparar implementación con oráculos pequeños y probabilidades correctas; luego usarlo como rival independiente, y como profesor solo si sus decisiones resisten el panel. Para juego fuerte, valorar búsqueda precisa de defensas frente al muestreo aleatorio. No asumir que UCT o más visitas lo hacen superior.

Población de entrenamiento: campeón, versión anterior, agresivo por apoyo, corredor/defensor y Montecarlo público. Reservar una familia de política y semillas completas para evaluación. Random solo para funcionamiento. Mantener muestra general más casos difíciles; no generar únicamente derrotas o desacuerdos.

Una red neuronal profesora queda permitida offline según las reglas consultadas, pero no es dependencia de esta entrega. Si la herramienta neuronal no produce mejores etiquetas en el piloto, consume tiempo sin beneficio. El estudiante final sigue siendo logística/ridge, patrones o un árbol legible. No empezar por instalar una pila GPU.

### 5E — Regresión y representación

Comparaciones secuenciales, con buscador y escala congelados:

1. Logística reproducida con etiquetas de victoria frente al modelo actual, para obtener una referencia.
2. **Ridge sobre las mismas características actuales**, no volver al vector antiguo de seis pesos. Si el objetivo es retorno esperado del profesor, fijar escala y acotamiento antes de entrenar; registrar el enlace de salida al buscador. No comparar directamente logits con retornos como si fueran iguales.
3. Si 5B muestra error estructural, un candidato adicional con dos tablas de patrones según presencia de marcador a dos puntos. Penalizar diferencias respecto al modelo común. Simetría horizontal tras comprobar equivalencia; mantener estados reflejados en la misma partición.

Modificar etiquetas, arquitectura o escala en pasos separados para poder atribuir resultados. Máximo dos candidatos completos que pasen a partidas; reducir por datos/costo primero. Selección por datos de desarrollo agrupados y por costo de búsqueda. Un mayor acuerdo con el profesor no acepta el modelo.

### 5F — Genéticos autorizados como ajuste offline

Usaremos un **algoritmo genético real de parámetros continuos**: población, selección, cruce, mutación y elitismo. NumPy para implementación sencilla, sin dependencia de una librería genética en la liga. Evolución diferencial de SciPy queda como comparador opcional; es otro algoritmo evolutivo, no se presentará como un GA clásico.

Primer genoma pequeño: tres multiplicadores positivos relativos para familias puntos, filas y marcador; la familia patrones queda de referencia fija, evitando que multiplicar todos los pesos cree una dimensión redundante. Rango inicial propuesto [0.75,1.25] para cada multiplicador, a congelar antes de medir. No añadir a la vez reloj, podas ni temperatura.

Presupuesto piloto: población de 12, máximo cinco generaciones (≤72 evaluaciones incluyendo población inicial), elitismo 2, semillas de optimizador fijadas. Conservar sin alterar el vector base como candidato de referencia y ejecutar una búsqueda aleatoria de igual presupuesto. Fijar cruce/mutación y objetivo antes de la primera evaluación; no ajustar mirando el reservado.

Fitness inicial barato: pérdida de decisión respecto a referencias fiables del banco de desarrollo, o Brier si solo hay etiquetas de resultado, más una restricción de costo. La elección se congela según los datos disponibles. No optimizar decenas de individuos con ligas completas por fitness durante esta semana. Evaluar los dos mejores fuera del conjunto usado por evolución; solo uno pasa a partidas oficiales contra el mismo modelo sin ajuste.

**Cierre 5F:** GA ejecutado, historia/checkpoints/genoma reproducibles, comparación con referencia y azar, y decisión sobre el candidato. Un GA que no mejora se descarta. Si no cabe en el plazo se registra incompleto, no «cerrado por falta de tiempo».

**Cierre de fase 5:** receta disponible, 24 decisiones documentadas, datos y particiones auditados, regresión y GA evaluados, modelo elegido con confirmación independiente. Conservar el actual si ninguno mejora; no hace falta aceptar una técnica para cerrar su pregunta. Las reservas de utilidad no se consumen en estos ajustes.

## Fase 6 — Finales que realmente aparezcan

**Responsable: Codex, con referencias de este chat.** Fecha objetivo: 30–31 de octubre.

1. Instrumento offline sobre todas las decisiones propias de las trazas disponibles, separando originales, desarrollo, técnicas y excluidas. Medir frecuencia del detector existente, turnos de activación y cobertura de amenazas de tercer punto.
2. Si no hay cobertura útil, cerrar la tabla anterior sin integrar y guardar el motivo. Si hay posiciones frecuentes, delimitar **un dominio** ampliado y presupuesto máximo antes de construir.
3. Solver: valor esperado exacto con turno, puntos, bloqueo, peón retirado al puntuar y ambas ramas de ataque. Cortar por presupuesto devuelve desconocido. Oráculo en subdominio pequeño y comprobación de todas las transiciones incluidas en la tabla.
4. Medir tamaño, preparación, consulta y activaciones. Solo pasar a partidas si cubre casos y cabe; comparación con/sin solver congelado y confirmación nueva.

**Cierre:** solver útil confirmado o rechazo documentado por cobertura/costo. Una búsqueda parcial de amenazas no se etiqueta como tabla exacta.

## Fase 7 — Libro coherente con el modelo elegido

**Responsable: Codex.** Fecha objetivo: 1–2 de noviembre; empieza generación después de fase 5.

1. Adaptar el generador a eval3/buscador seleccionado. Generar en archivo nuevo; conservar el libro actual. Guardar versión de motor/modelo y procedencia por entrada.
2. Analizar respuestas distintas por color, no solo self-play simétrico. Puntuar candidatos con profesor offline y contraste de continuaciones; abandonar entradas inciertas y usar búsqueda normal fuera del libro.
3. Medir cobertura por color, legalidad y costo; verificar turno y puntos en claves. No inventar entradas para inflar cobertura.
4. Congelar libro y comparar con/sin libro bajo árbitro oficial, ambos colores, más de un estilo y semillas nuevas. Registrar fuerza y reloj ahorrado. Si no aporta, elegir sin libro o conservar únicamente la versión previamente validada, especificando evidencia.

**Cierre:** generador reproducible y decisión confirmada sobre el libro de la versión final.

## Fase 8 — Integración y preparación de entrega

Esta fase explicita el control transversal anterior; no es otra investigación. **Responsables: este chat revisa, Codex ejecuta.** Fecha objetivo: 2 de noviembre.

Crear candidato de integración aislado con solo cambios aceptados. Compararlo contra el principal P original y contra el control técnico corregido cuando corresponda. No sumar porcentajes de mejoras medidas por separado. Una mejora de exactitud requiere conservar su regresión aunque se rediseñe por costo.

Congelar manifiesto del candidato, modelo, libro y dependencias. Validador, arranques fríos en entorno objetivo, memoria pico, 100 MB/50 MB, rutas, legibilidad, nueve secciones del informe y coherencia de datos. Adaptar caché a Linux/arquitectura objetivo y comprobarlo: el caché de una máquina no se presume portable.

**Cierre:** un único candidato íntegro, reproducible y evaluable por la fase 9, más respaldo identificado. Las acciones de registrar SHA/publicar PR requieren la autorización de publicación, no están implícitas en redactar este plan.

## Fase 9 — Calibración comprobada y pulido final

**Abierta y última. Responsables: Codex mide; este chat audita y decide.** Ventana: 2–3 de noviembre, entrega 4 (hora pendiente).

La calibración de parámetros/modelos ocurre en fase 5; aquí **se comprueba la calibración del modelo congelado**. No se vuelve a entrenar, no se optimizan genomas ni se selecciona un nuevo umbral usando el examen final.

1. Publicar antes del examen el manifiesto y protocolo: finalista y respaldo, rivales, semillas nuevas verificadas, orden alternado, ambos colores, muestra, métricas, reglas de interrupción y criterio. No usar reservas antiguas sin un protocolo que lo autorice.
2. Muestra de planificación: cuatro familias de rival (MC oficial, campeón histórico, UCT validado, estilo reservado), 20 partidas por color y versión: **320 partidas totales**. Es un mínimo operativo para buscar regresiones, no una demostración de superioridad universal. Estimar duración en fase 8. Si no cabe, fijar y publicar una muestra menor antes de ver resultados y declarar la menor precisión; no fingir 320 completadas.
3. Puertas técnicas: cero fallos propios observados, reloj <30 s, preparar <10 s, memoria <1024 MB, siempre jugada legal de respaldo. Criterios deportivos propuestos: finalista supera al respaldo en victorias agregadas, mayoría frente a MC y ninguna familia pierde más de 4 victorias de 40 respecto al respaldo. Fijarlos con la muestra definitiva antes de jugar; son filtros prácticos, no significancia estadística.
4. Mostrar intervalos y dependencia por grupos, resultados por rival/color, preparación/reloj/memoria, activaciones del libro/solver y calibración sin reajustar. El examen se ejecuta una vez por candidato congelado. Si falla, elegir el respaldo conforme al protocolo o reabrir explícitamente la fase causante; no usar el mismo examen como entrenamiento.
5. Pulido permitido: corregir un defecto localizado reproducible, mensajes/documentación, rutas o empaquetado. Toda corrección genera nuevo hash y repite controles afectados. Si altera decisiones, invalidar el examen deportivo anterior para esa nueva versión y usar datos nuevos; si no hay tiempo, usar el respaldo.
6. Simulacro de entrega desde carpeta limpia, sin red durante juego, sin archivos externos, contenido permitido e informe final. Registrar limitaciones reales y comando de regeneración. Congelar a más tardar el 3 de noviembre.

**Cierre fase 9:** checklist completo, informe final reproducible y versión recomendada para entregar, o respaldo elegido con motivos. No promete ganar a Tier 5. No dejar trabajo obligatorio oculto detrás de «100%».

## Calendario y límites de alcance

| Fecha | Resultado objetivo |
|---|---|
| 28 oct. | Registrar cierre 5A; panel 24; encargo TT; preparar traslado al escritorio. |
| 29 oct. | TT con filtro técnico; receta/piloto profesor; particiones y población de rivales. |
| 30 oct. | Datos dirigidos; comparaciones de regresión; cobertura y decisión de finales. |
| 31 oct. | GA acotado y selección de modelo; confirmaciones de candidatos que pasen desarrollo. |
| 1 nov. | Cierre 5 y 6; libro candidato y prueba de fase 7. |
| 2 nov. | Cierre 2/7 e integración 8; iniciar examen 9 si está listo. |
| 3 nov. | Terminar 9, empaquetar y congelar. |
| 4 nov. | Entregar antes de la hora oficial confirmada por Jose. |

Las fechas son objetivos, no evidencia de cierre. Si no hay tiempo para confirmar una técnica, conservar el respaldo. MCTS como sustituto completo, red profesora desde cero, tablas enormes y una población genética grande quedan fuera de la ruta crítica; las ideas siguen registradas para después de entregar.

## Contrato de cierre para todos los agentes

Cada entrega incluye: pregunta, versión/control, archivos, comandos/entorno, fuentes de datos, métricas por color/rival, fallos/tiempos, incertidumbre y decisión. Actualizar [[01-Estado]] y [[03-Bitacora]] enlazando evidencia. Nunca anunciar que el escritorio o Codex están ejecutando una tarea que solo se dejó como encargo.

## Actualización de ejecución — noche del 28 de octubre

Fase 2 cerrada sin incorporar pistas (ratio 0.982591). Dentro de fase 5: 5A cerrada sin promoción; **5B cerrado** con los 24 casos clasificados y reproducibles, incluidos los no concluyentes; **5C receta/auditoría completadas** con regeneración numérica exacta; ridge/logística y GA real ya evaluados, candidato histórico rechazado. El piloto del profesor profundo no cumplió cobertura, y no se inventaron etiquetas. Sesenta episodios nuevos contra tres familias se generaron y verificaron; adaptación centrada pasa filtros internos y está jugando el protocolo oficial U/N. El cierre global de 5 sigue pendiente del resultado y decisión de fuerza; si pasa desarrollo requiere confirmación independiente. No queda cerrada por buenas métricas supervisadas.

Evidencia y limitaciones: [[Experimentos/2026-10-28-Fase5-datos-modelos]]. Ejecutor único de este chat: `resultados/medicion/fase5_oficial_20261028/`. No iniciar otra carga pesada mientras el progreso indique un bloque activo. Los encargos preparados de terminal no se han enviado automáticamente.

## Resultado final de la adaptación — 29 de octubre

Serie completa U43/80 frente a N6/80; N3/40 en cada semilla, cero fallos propios. Candidato rechazado, no se ejecuta confirmación19/20/21 y no se altera el principal. Retención histórica y predicción en los mismos estados U/MC empeoran: [[Experimentos/2026-10-29-Diagnostico-transferencia-y-proximo-ajuste]]. 5B y receta/auditoría están resueltos; ridge/GA/simetría y adaptación tienen decisiones de rechazo. **Fase5 permanece abierta** por profesor cualificado y selección/confirmación de modelo pendientes. El próximo ajuste debe incorporar controles de retención y rivales pertinentes antes de nuevas partidas; no retocar N con sus reservas.

## Etapa5V — validación obligatoria antes de aceptar el próximo modelo

Autorizada por Jose e implementada el29/oct; [[Validacion-y-laboratorio-PC]] enlaza código/contrato/evidencias. Esta etapa forma parte de fase5 y no sustituye el examen final9.

- Datos nuevos por partidas/grupos completos; UCT entero reservado como familia no entrenada. Estados y espejos cruzados purgados. Mínimo24 grupos train,12 validación,12 test y4 por estrato. Proporciones reales publicadas; no se llama CV de múltiples pliegues.
- Hipótesis única previa: logística λ100 centrada en el activo, replay80%histórico/20%nuevo con igual peso por grupo. Entrenador solo recibe train/replay.
- Contrato y hashes antes del ajuste. Selección limitada a dos candidatos; mejora Brier≥.002, logloss no peor, retención histórica y controles por color/fase. Histórico ya visto es retención, no confirmación.
- Test se abre una vez tras selección; no reajustar con su resultado. Aprobar permite controles de costo/seguridad y comparación oficial NUEVA, nunca promoción automática. N y reservas previas siguen cerrados.
- Pruebas funcionales listas en Mac; no datos nuevos de producción ni candidato aceptado. Próxima acción: instalación/piloto2→4 en PC, lote recuperable, auditoría y ajuste. El profesor sigue requiriendo cualificación; resultados de políticas no equivalen a valores óptimos de acciones.

Kubernetes de laboratorio instalado y verificado en Mac, dejado detenido. La cola local CPU es suficiente para la ruta crítica; no trasladar árbitro ni forzar cuatro partidas oficiales con recursos insuficientes. Fase2 sigue cerrada; fase5 abierta. Fase6 puede avanzar en preparación/cobertura con coordinación de CPU.

### Evidencia5V en Linux — 29/oct

Purga cruzada de datos nuevos con replay/retención históricos implementada y con regresión; contrato registra filas eliminadas. Batería Kubernetes completada:14tests, reproducción exacta del activo,8episodios funcionales reanudados con replay y60históricos verificados. [[resultados/medicion/fase5_mac_k8s_20261029/RESULTADOS]]. No demuestra fuerza ni cualifica un profesor; no entrenar con el lote funcional. Paquete PC actualizado y piloto Mac separado con presupuestos reales para dimensionar generación. La certificación documental de2 tiene encargo propio; integración de corrección TT sigue en8.

### Certificación de fase2 recibida — 29/oct

Fase 2 certificada cerrada/rechazada el 29/oct: 60 posiciones, 600 pares/1200 búsquedas, mediana candidato/control 0.982591 >0.95 y diferencia máxima de valor 0; no procede liga. P conserva búsqueda ceba3653 y NPZ 37678d0b; las pistas adb347a1 no se integraron. La corrección TT de A cc888a3c es independiente y sigue pendiente para fase 8: portar/revisar el parche P_a_A_correccion_TT.patch en candidato aislado, conservar las regresiones de ventana estrecha/amplia y repetir seguridad/integración; no declarar que P ya esté corregido. Evidencia: resultados/medicion/cierre_fase2_20261029/CIERRE.md.

Piloto Mac de presupuestos reales finalizado:16episodios/1495posiciones, replay correcto,2reanudaciones con originales intactos.8grupos, partición3/3/2: desarrollo insuficiente para selección5V. No modelo ajustado. Profesor completó7solo74/750decisiones, guardar profundidad efectiva. Siguiente: lote prospectivo mayor con rivales pertinentes; este piloto calibrado completo no es examen independiente. Fase5 permanece abierta.

### Ejecución29/oct — siguiente lote5y encargo6

Lote prospectivo256episodios iniciado en Mac con4trabajadores, contrato/semillas/receta fijos; preflight72/24/32grupos, purga/cobertura reales pendientes. Sesión60min recuperable y flujo automático hasta selección/test si completa, sin promoción. [[resultados/medicion/fase5_lote256_mac_20261029/LEEME]]. No inspeccionar calibración del test antes de seleccionar. [[2026-10-29-Encargo-Codex-fase6]] preparado para terminal; envío bloqueado por sesiónCLI, no se afirma ejecutado. Docker integrado activo/verificado; separar cargas de futuras mediciones oficiales.

### Continuación acotada de5 y evaluación posterior prefijada

Supervisor independiente espera la sesión60min y solo en pausa por datos incompletos reanuda una vez360minmás, manteniendo256episodios/fuentes/semillas/receta. No repetir errores/rechazos/interrupciones. Funciones/PIDs/progreso reales en fuente de lote256. Codex6en marcha confirmado por Jose; ninguna liga o medición oficial durante esas cargas.

[[resultados/medicion/fase5_postseleccion_20261029/PROTOCOLO_PARTIDAS]] se fija antes deV:equivalencia representación/runtime, controles técnicos, desarrollo160y confirmación160condicional, sin promoción. El candidato aún no existe. El modelo activo pasó288comparacionesPython+288Numba con cambio/restauración;5entradas inválidas rechazadas. Repetir conV tras puertas5V, no diagnosticar con su test. Fase5abierta.

### Cierre6y encargo7A —29/oct

[[resultados/medicion/fase6_cobertura_20261029/CIERRE]] cierra6:890trazas/36,730raíces,0errores; sin oportunidad adicional del dominio, no solver integrado. [[2026-10-29-Encargo-Codex-fase7A]] encarga cobertura del libro y herramienta compatible, sin reemplazar activos ni generar libro definitivo antes del modelo5. No se afirma7Aejecutado.

Fase5:71/256en última comprobación; relevo automático inicial60→360minverificado,4salidas0, fuentes intactas. Oráculo táctico racional nuevo sobre8casos históricos:3observadas valor1,5no resueltas,0dominancias. Sin cambio de receta ni uso del test. [[resultados/medicion/fase5_cotas_tacticas_20261029/RESULTADOS]].

## Resultado del lote256 —29/oct19:51

Datos256/256y ajuste prefijado completados; candidato d5a28046 rechazado por retención histórica (+0.00656894Brier por grupo>0.005permitido), aunque validación mejora0.00882460. TestUCTsin abrir, principal intacto, sin liga U/Vni promoción. [[resultados/medicion/fase5_lote256_mac_20261029/RESULTADOS]]. No rescatar la misma hipótesis moviendo puertas ni lanzando otro ajuste automático; fase5global sigue abierta y el siguiente paso requiere diagnosticar train/validación/retención y una limitación concreta.8B.1construye solo ensayo con respaldo, no suponeVaceptado.

## Diagnóstico y nueva hipótesis S13 —29/oct20:16

[[Experimentos/2026-10-29-Diagnostico-replay256-y-S13]]: el amplio converge y mejora replay, pero pierde82/126grupos retenidos. Patrones explican descriptivamente la mayor parte de la pérdida; no atribución causal. Nueva hipótesis prefijada S13con13coeficientes libres y patrones congelados, una ejecución, mismas λ100/masas80/20, SHAaba46e55. Desarrollo ya visto: mejoraBrier0.00214487y retención+0.00032692; pasa filtro de desarrollo, NOvalidación independiente ni modelo aceptado. Hace falta lote NUEVO64tras controles8B.2, candidato sin retocar, semillas/purgas/cobertura auditadas antes de evaluar. Test256yrechazoanteriores intactos.

8B.1verificada(60artefactos). [[2026-10-29-Encargo-Codex-fase8B2]] y DECISION_TECNICA.json seleccionan I0con pesos de respaldo37678d0bSOLO para pruebas técnicas; sinS13, utilidad nueva o promoción. Este chat termina trabajo NumPy y deja ventana exclusiva al pegar el encargo; no genera datos mientras se midan frío/reloj/memoria.

## Validación prospectiva S13preparada —29/oct

[[Experimentos/2026-10-29-S13-validacion-nueva]]: flujo64episodios congelado,semillas auditadas en19worktrees incluyendo ignorados,5regresiones,24fuentesporSHA. Iniciará solo DESPUÉS de cierre/ventana8B.2verificados mediante seguimiento local10min;90minsin reintento,modeloS13fijo,24gruposval/8UCTreservados. No dataset nuevo ni validación ejecutada al preparar, no test256abierto, principal intacto.

## 29/oct21:13 —8B.2técnico terminado y validación S13iniciada

Certificado8B.2y169artefactos verificados;I0respaldo pasa LinuxARM64/frío/humo/técnicas acotadas, sin integrar ni certificar fuerza.20261221consumida. Ventana/procesos/Docker comprobados libres. [[resultados/medicion/fase5_validacion_S13_64_20261029/LEEME]]: flujo nuevo4×16/90mininiciado21:13:50,modeloS13fijo,no reentrenamiento,principal intacto,test256sellado. Seguimiento10minsigue hasta resultado; no más cargas o partidas mientras genere.


## 30/oct — S13 supera validación nueva; fase5sigue abierta

[[resultados/medicion/fase5_validacion_S13_64_20261029/RESULTADOS]]:64/64 completos,24grupos/4512filastraspurga;mejoraBrierporgrupo0.00589271,logloss yamboscoloresmejoran,coberturapasa.288comparacionesPython+288Numba en piloto histórico visto correctas. Fuentes, modelo y principal intactos;test256y8gruposUCTnuevos sin evaluar. No promoción/fuerza/cierre5global. Pendiente protocolo de examen,controles técnicos específicos ypartidas oficiales;8B.2solo certificóI0de respaldo. Seguimiento terminado y automatización eliminada, no reabrir generación/validación ni reajustarconeste lote.
