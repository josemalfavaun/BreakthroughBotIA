# Instrucciones para agentes

## Propósito y fuentes

- Ayuda al equipo `iacasitegano` a mejorar su bot de Breakthrough de combate mediante cambios legibles, legales y medidos. No prometas una calificación ni una mejora antes de medirla.
- Para retomar trabajo, usa primero `obsidian/00-Inicio.md` y `obsidian/01-Estado.md` como mapa breve. Después lee solo las secciones de las fuentes oficiales que sean pertinentes y los archivos relacionados con la tarea; consulta todos los documentos completos para una auditoría amplia o cuando falte contexto fiable. No vuelvas a leer archivos ya revisados si siguen vigentes.
- Usa `PLAN_TIER_5.md` como hoja de ruta experimental y los documentos del torneo como autoridad para reglas, límites y entrega. El estado actual del bot se obtiene del código, los datos y las mediciones recientes; no supongas que un resumen o plan antiguo describe la rama activa.
- Registra en `obsidian/03-Bitacora.md` decisiones duraderas y resultados aceptados o rechazados. Usa `obsidian/Experimentos/Plantilla.md` para experimentos nuevos. Mantén notas breves, con enlaces a los archivos/evidencia fuente; no copies informes enteros ni presentes una nota como evidencia primaria.
- Al cerrar una sesión o delegación, actualiza `obsidian/01-Estado.md` con fecha, rama/commit, estado confirmado, trabajo en curso, siguiente acción y dudas. Nunca declares terminado un proceso basándote en un resumen viejo; comprueba su estado actual.
- Las instrucciones directas más recientes del usuario prevalecen sobre estas reglas, salvo las reglas oficiales del torneo.

## Alcance y protección del trabajo

- Para cambios del participante, modifica únicamente `estudiantes/iacasitegano/`. No cambies `sistema/`, el motor o árbitro, workflows, otros equipos ni documentos del curso para obtener ventaja.
- `AGENTS.md`, `PLAN_TIER_5.md` y los archivos de configuración local son instrucciones o documentación del proyecto, no parte de la entrega del equipo. La entrega oficial debe limitarse a `estudiantes/iacasitegano/`, salvo autorización explícita del usuario y las reglas del curso.
- Antes de editar, registra `git status --short --branch` y la revisión actual. Conserva todos los cambios existentes. No uses `git reset`, `git clean`, `git restore`, rebase ni sobrescribas trabajo ajeno.
- Aísla experimentos en su propia rama o worktree cuando sea posible. No hagas commit, push, merge ni cambies la rama de entrega sin petición explícita del usuario.
- Sigue las instrucciones de `rtk` disponibles en el entorno para comandos de shell.

## Reglas del torneo

- Respeta las reglas de `docs/reglas.md`: no uses redes neuronales, no adivines ni manipules los dados, no uses red durante una partida, no persistas información entre partidas, no escribas fuera de los datos permitidos durante la partida y no ofusques código.
- Respeta los límites oficiales vigentes de reloj, preparación, CPU, memoria y tamaño de archivos. Mantén siempre una jugada legal de respaldo y margen para responder antes de agotar el reloj.
- Todo código y dato de la entrega debe ser legible, auditable y regenerable. El informe debe describir exactamente el código, datos y resultados que se entregan.

## Protocolo experimental

1. Formula una hipótesis falsable y define de antemano qué métrica debería cambiar.
2. Cambia una técnica por experimento, salvo que los parámetros formen un único cambio inseparable.
3. Congela el baseline, el protocolo, las semillas, los colores y las métricas antes de medir. Empareja semillas entre candidato y baseline y juega ambos colores.
4. Usa tandas pequeñas como filtro de desarrollo, no como prueba concluyente. Si el resultado es estrecho, amplía la muestra y valida con semillas no usadas durante el ajuste.
5. La decisión final de fuerza debe basarse en partidas completas con el árbitro y los límites oficiales. `--sin-docker` y las búsquedas de profundidad fija sirven para explorar, no para afirmar fuerza oficial.
6. Registra victorias y derrotas, color, puntos anotados, semillas, entorno, tiempo de preparación, reloj máximo, errores y timeouts. Separa resultados estratégicos de fallos técnicos.
7. No aceptes un cambio solo porque aumenta la profundidad, reduce nodos, mejora el acuerdo con la propia búsqueda o parece razonable. Consérvalo únicamente si mejora de forma repetible sin regresiones de reloj, preparación, legalidad o memoria.
8. No corras mediciones de partidas al mismo tiempo que generación de datos, compilaciones u otra carga pesada en la máquina compartida. Coordina ventanas exclusivas para pruebas de rendimiento.

## Validación y entrega del trabajo

- Ejecuta las verificaciones pertinentes al cambio. Para cambios del bot, incluye la validación de entrega del torneo; para una mejora de fuerza, incluye además partidas completas bajo el árbitro. No presentes una exploración como validación final.
- Actualiza `estudiantes/iacasitegano/INFORME.md` solo cuando se acepte una mejora y haya evidencia reproducible. No borres resultados rechazados que expliquen decisiones anteriores.
- Al terminar, informa brevemente: hipótesis, archivos cambiados, qué se hizo, comandos y entorno de validación, resultados por color, reloj/preparación máximos y limitaciones pendientes.
