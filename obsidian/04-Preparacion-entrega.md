---
tipo: auditoria
fecha: 2026-10-27
revision: 85b2d55
estado: pendientes-identificados
---

# Preparación de entrega

Revisión estática del checkout `integracion-tier1-2`, mientras Jose informa que Codex ejecuta el A/A. No se iniciaron partidas, compilaciones ni entrenamiento. Fuentes oficiales: [[docs/entregar]], [[docs/reglas]] y [[docs/avanzado]]. Las notas de Obsidian quedan fuera del PR oficial.

## 1. Recuperar la regeneración del modelo activo

`strategy.py` carga `data/pesos_eval3_ligero.npz`. El entrenador incluido en `herramientas/entrenar.py` produce el vector lineal anterior de seis pesos, no ese modelo. No se localizó el entrenador de eval3 en la carpeta activa del equipo; la sección de integración del informe remite al laboratorio externo.

Antes de entregar: recuperar el generador exacto y su procedencia, documentar datos de entrada o su generación, semillas, familias activas, dependencias y comando de entrenamiento/ablación. Incluir el código pertinente en `herramientas/`. No regenerar ni sustituir pesos durante el A/A. La reproducción puede requerir datos y versiones fijados; no prometer identidad de hash sin comprobarla.

Actualización: se localizaron el entrenador IRLS y la validación logística en `/Users/josema/vs code/BreakthroughBotIA-claude/estudiantes/iacasitegano_eval3/herramientas/lab/`. El NPZ de ese laboratorio coincide por hash con el activo. Falta reconstruir la receta completa y portar fuentes/datos pertinentes; ver [[Experimentos/2026-10-27-Utilidad-victoria]].

## 2. Preparar un informe breve y vigente

El informe actual tiene 457 líneas y aproximadamente 4,326 palabras; contiene registros históricos extensos. `docs/entregar.md` pide 2–4 páginas y nueve secciones. Hace falta una versión final concisa; el historial y evidencia detallada pueden conservarse en la memoria del proyecto.

Correcciones de contenido identificadas:

- Sección 5: incluir la regeneración del modelo activo, además del entrenador lineal histórico y del caché.
- Distinguir resultados del modelo vigente de pruebas históricas; las 800 partidas de eval3 incluyen 16 fallos de preparación y presupuesto de nodos, por lo que no deben describirse como una tanda limpia con el reloj oficial de la estrategia actual.
- El cierre del informe dice que eval3 está sin commit; está integrado en el historial de `85b2d55`. Actualizar ese estado.
- Sustituir rutas privadas `/Users/josema/...` por referencias portables a evidencia accesible o describir el protocolo sin depender de archivos del equipo local.
- Actualizar la sección de uso de IA para reflejar el trabajo de Codex además de Claude.

La preparación de un borrador editorial no supone aceptar nuevas mejoras. No se editó `INFORME.md` en esta revisión.

## 3. Resolver la distribución y portabilidad del caché

Hay 15 archivos `.nbc` y 14 `.nbi` dentro de `data/numba_cache/`. Numba está expresamente permitido; las reglas también exigen datos auditables y prohíben código nativo propio/código escondido. Los documentos revisados no autorizan expresamente distribuir el caché Numba compilado. Aclarar ese caso antes de cerrar la entrega; pasar el validador técnico no resuelve por sí solo la interpretación de las reglas.

El manifiesto actual es de Linux `aarch64`, Python 3.12, Numba 0.67.0 y NumPy 2.4.6. El código tiene fallback a compilación si no coincide. El experimento de carreras reportó recompilación al copiar el caché a otro worktree. Cuando finalice el A/A, verificar el arranque desde una copia limpia y el entorno real de entrega; no extrapolar los ~0.03–0.12 s a un entorno diferente. Ver [[Experimentos/2026-10-27-Tiempo-carreras]].

## 4. Inventario y alcance

- Inspección local: 84 archivos y 2,128,486 bytes, excluyendo `__pycache__`; ningún enlace simbólico. Es un inventario, no una validación oficial.
- Git lista 60 archivos del equipo; hay archivos locales ignorados y la prueba Docker nueva sigue sin seguimiento. La carpeta de trabajo completa y el contenido de un futuro commit no son equivalentes.
- Mantener los cambios locales y respaldos hasta revisar su procedencia y decidir la lista final. No borrar ni añadir todo automáticamente.
- La entrega se prepara desde el SHA registrado y cambia exclusivamente `estudiantes/iacasitegano/`, como exige [[docs/entregar]]. La validación oficial final, el commit y el registro del SHA quedan para cuando el candidato y los pendientes anteriores estén cerrados.

## Orden de trabajo paralelo

1. Recuperar el código y la receta del modelo activo, sin ejecutarlos.
2. Preparar un borrador de nueve secciones con resultados del bot vigente y límites explícitos.
3. Resolver el caso del caché precompilado y planificar comprobación de arranque portable después del A/A.

Esta auditoría no comprobó el estado vivo ni el avance de la corrida A/A.
