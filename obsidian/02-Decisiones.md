---
tipo: decisiones
proyecto: BreakthroughBotIA
actualizado: 2026-10-27
---

# Registro de decisiones

Decisiones vigentes o pendientes, con su motivo. Añade decisiones duraderas; los resultados completos van en informes y artefactos.

## Vigentes

- **Métrica de fuerza en próximos experimentos: victorias/puntos de liga.** `docs/calificacion.md` asigna un punto por victoria; los peones anotados son desempate. Los peones y su diferencial quedan como secundarios. No se cambian retrospectivamente los criterios de carreras ni del A/A en curso; sus JSON permiten calcular variación de victorias como diagnóstico adicional.

- **Una hipótesis por experimento.** Evita mezclar cambios de búsqueda, evaluación, reloj y aperturas; así el resultado se puede atribuir.
- **Partidas completas para decidir fuerza.** Las búsquedas fijas y `--sin-docker` son exploratorias; no sustituyen al árbitro y los límites oficiales. Ver [[PLAN_TIER_5]].
- **Semillas y colores pareados.** Reducen varianza entre candidato y baseline; reservar semillas para validación.
- **Seguridad del reloj es requisito de aceptación.** Un timeout, preparación excesiva, jugada ilegal o excepción cuenta como regresión aunque mejore la profundidad.
- **No ampliar ahora la arquitectura por intuición.** Híbrido con rollouts y tabla MDP ya tuvieron experimentos rechazados; cualquier reintento necesita hipótesis nueva y protocolo separado.
- **No incluir notas de raíz en la entrega oficial.** La entrega del equipo se limita a `estudiantes/iacasitegano/`, salvo confirmación explícita de que las reglas permiten más.

## Decisiones recientes

- **Caché numba horneado: aceptado en `integracion-tier1-2` como mejora de fiabilidad.** Prueba fría 20/20 bajo concurrencia y liga real 10–10 sin errores. No atribuirle mejora de fuerza. Revisar el diff final y decidir si se incluye la prueba Docker nueva sin seguimiento.
- **Estimador adaptativo de reloj probado: rechazado.** En 100 partidas por variante, el candidato perdió 43–57 y bajó la profundidad media de 4.93 a 4.64; ahorrar reloj no compensó la pérdida observada. No promover ni documentar como mejora aceptada.

## Pendientes de decisión

- Sincronización de ramas y entrega: comparar `integracion-tier1-2`, `main` remoto y rama de entrega; no hacer merge automático.
- Confirmar que el informe del caché y el artefacto/regeneración corresponden al mismo código y ABI antes de preparar el PR.
