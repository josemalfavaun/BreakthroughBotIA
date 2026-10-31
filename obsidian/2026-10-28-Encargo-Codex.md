# Encargo para Codex de terminal

Continúa con el experimento de utilidad de victoria. Lee primero:

`/Users/josema/vs code/BreakthroughBotIA/obsidian/Experimentos/2026-10-28-Protocolo-utilidad-victoria.md`

Ese protocolo ya fija las dos rutas, hashes, orden, semillas, 160 partidas de desarrollo y filtro. Ejecútalo de principio a fin: revisa el estado real, conserva cambios previos, termina las comprobaciones técnicas necesarias (incluidas 4 partidas técnicas previas con semilla 20261115) y corre los cuatro bloques en serie bajo límites oficiales, sin otros trabajos pesados simultáneos. Las variantes ya tienen la misma corrección TT; no vuelvas a modificar sus fuentes ni mezcles otras optimizaciones. Consulta la validación ya realizada en `resultados/medicion/utilidad_victoria_20261028/VALIDACION.md` del worktree B para no repetir comprobaciones sin motivo.

Antes del primer bloque guarda un manifiesto de archivos e imágenes y verifica que cada ejecución carga realmente A o B, aunque las etiquetas Docker sean compartidas. Guarda logs, JSON y progreso recuperable. Si el equipo entra en reposo o hay una interrupción externa, conserva el bloque parcial excluido y repite el bloque completo; los fallos del bot sí se cuentan. Sin duplicar resultados ni ajustar criterios durante la serie.

No ejecutes las reservas 20261111–20261114 ni 20261102–20261104. No hagas promoción, commit, merge, push ni edites el informe oficial. Al terminar, recalcula desde los JSON y reporta victorias por versión, semilla y color, diferencia sobre 80 por versión, peones como secundarios, seguridad/relojes/preparación, hashes y si pasa el filtro. Actualiza la nota del experimento con enlaces a evidencia. Si falta un dato, márcalo sin medir.
