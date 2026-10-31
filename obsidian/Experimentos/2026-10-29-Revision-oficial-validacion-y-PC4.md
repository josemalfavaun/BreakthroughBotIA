---
tipo: revision-y-plan
fecha: 2026-10-29
estado: revision-completa-plan-PC-no-ejecutado
---

# Reglas, fuerza actual y validación ML

Principal P comprobado hoy contra random: **20–0**,10 por color,60–1 peones, cero fallos; reloj máximo16.258s. Evidencia `resultados/medicion/random_principal_20261029/RESULTADOS.md`. No prueba calificación de liga ni tiers. P frente a MC21/40 no acredita mayoría estable; U43/80 es otro control. Tiers privados, sin pruebas propias. La calificación compara puntos totales de liga, no solo el enfrentamiento.

Revisión amplia de documentación/componentes oficiales y comparación del inventario145 archivos: `resultados/medicion/revision_oficial_20261029/REVISION.md`; fuentes y cambios locales/curso identificados allí. No se actualizó sistema ni se hizo commit. Hay actualizaciones de instalación/WSL/BotLocal que deben tratarse por separado de la evidencia congelada.

Fase2 cerrada con rechazo de pistas TT, no de la corrección matemática: P conserva dos fallos reproducidos en consultas TT; A corregido pasa y su integración final sigue pendiente. Fase5 permanece abierta. Ninguna de las dos propuestas recientes mejoró el principal.

Validación: el histórico activo usó61247/15791 train/validation, con grupos compartidos; nuevo pipeline agrupado44120/14021/15602, pero el histórico ya fue visto. Adaptación N4014/408/1645, solo18/2/9 grupos: selección insuficiente y rival UCT de presupuesto bajo. Sí existe validación; falta hacerla más representativa y comprobar estabilidad por pliegues agrupados. El20% usado para escoger modelos no es test intacto.

Próxima iteración: grupos y espejos separados/purgados; train para ajuste, validation para selección, test sin consultar;60/20/20 objetivo por grupos con tamaños publicados; control de retención histórica y una familia de rival reservada. Partidas oficiales nuevas para aceptar. No cambiar filtros de N ni reutilizar sus reservas para rescatarlo.

PC: cuatro generadores offline con un hilo interno cada uno, semillas/shards independientes y aprendizaje posterior sobre datos reunidos/verificados. Piloto2→4 y medir RAM/rendimiento. No escribir cuatro procesos al mismo NPZ. Árbitro oficial:4/6/8/10 CPU visibles permiten1/2/3/4 partidas, respectivamente; no confundir generación offline con validación a reloj. PC aún sin conectar. El generador actual necesita rivales pertinentes antes de escalar la mezcla anterior.

ML permitido: regresión/logística y árboles; NumPy/SciPy/Numba actuales, scikit-learn para referencias/validación agrupada, boosting como profesor offline; Optuna opcional acotado. Herramientas neuronales solo offline, estudiante de liga no neuronal. No se instalaron modelos/librerías nuevos.

Reparto propuesto: Codex fase6/cobertura y seguimiento de integración TT; este chat validación/retención; escritorio generación cuando esté preparado. No se enviaron mensajes a Codex ni se iniciaron trabajos allí. [[07-Plan-definitivo]] y [[08-Escritorio-y-entrenamiento]].
