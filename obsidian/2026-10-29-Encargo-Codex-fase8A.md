# Encargo para Codex — 8A: preparar correcciones de exactitud, sin integración activa

Trabaja explícitamente en `/Users/josema/vs code/BreakthroughBotIA`. Lee AGENTS.md, obsidian/01-Estado.md, la sección8 de07-Plan-definitivo y los certificados de cierre2/7A. Usa rtk y registra rama, HEAD y status antes de editar. Conserva cambios existentes. Sin commit, merge, push, promoción ni cambios en el participante activo.

**Objetivo:** dejar dos correcciones mínimas independientes, reproducibles y revisables para la futura integración. Es preparación8A: no cierra8, no selecciona modelo y no demuestra mejora deportiva. 7A terminó; 7B sigue esperando modelo y ventana exclusiva. Fases2/6 no se reabren.

## Convivencia con fase5

Fase5 sigue generando256episodios y después ejecutará entrenamiento/validación/test condicionado. No detener sus procesos ni tocar ninguna fuente enumerada en `resultados/medicion/fase5_lote256_mac_20261029/PROTOCOLO.json`, datos, pesos, cachés o locks. No examinar el test nuevo ni usar sus estados. No iniciar árbitro, partidas, benchmarks, compilación JIT, generación masiva ni pruebas de arranque frío mientras siga esa carga. Las comprobaciones funcionales deben ser pequeñas, sin JIT y con CPU acotada como en7A; nice por sí solo no es un límite de CPU. Si una comprobación necesita carga sostenida, deja el comando y estado pendiente.

## 1. Congelar y preparar copias

Salidas NUEVAS bajo `resultados/medicion/fase8A_preintegracion_20261029/`; herramientas nuevas solo en `estudiantes/iacasitegano/herramientas/`. Congela por SHA las fuentes actuales P, estrategia, evaluación, NPZ y libro, así como los parches y regresiones de origen. No editar `strategy.py`, `busqueda_eval3.py`, `eval3.py`, libro o pesos activos. Usa copias experimentales identificadas por ruta absoluta; no basta importar módulos con el mismo nombre para afirmar que probaste la copia. Guardar el archivo realmente cargado y su SHA. No reutilizar N ni sus pesos.

## 2. Corrección TT independiente

Fuente: `resultados/medicion/cierre_fase2_20261029/CIERRE.md`, parche `P_a_A_correccion_TT.patch`, SHA `38591003cb9be5dc6513289310f8823310575aac9f88855e72610a2675842abd`. Revisarlo y aplicarlo EXCLUSIVAMENTE a una copia P. Guardar parche limpio/reproducible y verificar que el resultado de búsqueda coincide byte a byte con A esperado, SHA `cc888a3c7fc7ba896f5145c36c56c77120bc6f0ef0b0ba45f077023bbeb7a177`; cualquier diferencia debe explicarse antes de continuar. No añadir pistas internas rechazadas, cambiar utilidad, reloj, hojas o pesos.

Conservar la regresión original `verificar_cotas_tt.py` y procedencia por SHA, sin sobrescribirla. Preparar/adaptar un pase funcional pequeño sin JIT: reproducir los dos contraejemplos P de ambas perspectivas; confirmar que la copia corregida coincide con un oráculo independiente sin TT; incluir ventanas estrechas/amplias, límites de alfa/beta, aborto sin almacenar exactos y terminales. Mantener los valores y estados originales, no sustituir el defecto por un ejemplo que nunca falló. Si la suite completa no cabe bajo carga, ejecutar solo los contraejemplos y fixtures diminutos, y registrar el resto pendiente con comando. No repetir el panel de tiempos de fase2.

## 3. Prioridad de victoria segura sobre libro, parche separado

Fuente: `resultados/medicion/fase7A_aperturas_20261029/CIERRE_7A.md` y su contraejemplo/regresión. Crear OTRA copia independiente de la estrategia P, sin corrección TT incorporada, con un cambio mínimo: comprobar victoria inmediata garantizada antes de aceptar una entrada legal de libro. Usar la definición existente: todos los hijos probabilísticos de la jugada deben ganar para nuestro color, sin asumir éxito de un ataque. Mantener jugada forzada, comprobación de legalidad, búsqueda y resto del comportamiento.

Regresiones pequeñas en memoria, sin preparar/calentar: el P original reproduce la entrada de libro que desplaza una victoria segura, el corregido elige una victoria segura; incluir ambos colores, ataque con éxito/fracaso, ataque ganador en una sola rama que NO es seguro, libro legal sin victoria que conserva su decisión, entrada de libro ilegal con búsqueda simulada y jugada forzada. Comprobar que se invoca realmente el código de cada variante y restaurar cualquier modificación temporal de globals. No convertir este arreglo en una reescritura del cargador ni del libro.

## 4. Traspaso para integración8B y evidencia

Guardar `PROTOCOLO.md`, controles negativos/positivos, fixtures, resultados JSON, dos parches independientes, manifiesto de originales/copias/herramientas/entorno y `CIERRE_8A.md`. Verificar de nuevo todos los SHA de fuentes congeladas de fase5 y del runtime activo al terminar. No escribir caches en rutas activas.

Preparar checklist8B: decidir modelo según fase5 (no asumir que existirá V aceptado), revisar composición de cambios, mantener experimento de pesos U/V con idéntica estrategia/libro en ambos, validar paquete/ABI/caché en Linux, arranques fríos, legalidad/respaldo, reloj, memoria y tamaño bajo límites oficiales, y fijar comparación contra P/control corregido antes de jugar. Este encargo NO ejecuta esas mediciones ni autoriza sustituir fuentes activas. El parche de prioridad del libro no se inserta a mitad de la comparación de pesos5.

Nota específica en `obsidian/Experimentos/2026-10-29-Fase8A-preintegracion.md`; no editar01-Estado/03-Bitacora/07-Plan-definitivo simultáneamente con el chat director. Termina con hechos comprobados, pendientes, comandos y párrafo de traspaso. Si falla una regresión, conservar evidencia, localizar el defecto dentro de la copia y no ampliar alcance ni tocar runtime para rescatarlo.
