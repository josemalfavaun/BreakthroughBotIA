---
tipo: diagnostico
fecha: 2026-10-28
estado: panel-24x3-completo-sin-error-real-certificado
---

# Panel reproducible de decisiones

Prioridad 2 del usuario, ejecución ligera sin JIT/compilación ni partidos. El extractor nuevo del equipo usa el motor oficial sin modificarlo; no carga estrategias ni pesos.

```sh
rtk '/Users/josema/vs code/BreakthroughBotIA/.venv/bin/python' -B estudiantes/iacasitegano/herramientas/extraer_casos_decision.py resultados/2026-10-27_14-49-49 --salida resultados/medicion/diagnostico_decisiones_20261028_baseline40
```

Exit 0: **40 partidas / 3,231 plies** reconstruidos. Turno, jugadas legales, combate, probabilidad, ganador y marcador final coinciden con el motor. Exportados **282 estados distintos**, 143 de blancas/139 negras, sin IDs repetidos, todas las jugadas observadas legales; 40 fuentes y 20 grupos por semilla/pareja/juego (ambos colores del par comparten grupo).

Selección declarada: decisiones propias 8/16/24/32, primera decisión propia con 2 puntos, posiciones con rival en 2 y dos últimas decisiones propias. Etiquetas solapadas: 149 muestreo fijo, 30 primer marcador de 2, 65 rival con 2, 80 últimas dos. Son datos vistos y parcialmente seleccionados retrospectivamente; no son un conjunto de confirmación ni una muestra representativa para estimar tasa de errores.

Evidencia primaria: `resultados/medicion/diagnostico_decisiones_20261028_baseline40/manifest.json` y `casos.jsonl`, en el principal. El manifiesto incluye hashes de las 40 fuentes y del extractor. Cada caso conserva estado, jugada observada, alternativas legales, probabilidad, metadatos de búsqueda y estado `pendiente_contrafactual`. No exporta tiradas futuras al caso.

**No se identificó todavía una jugada objetivamente peor ni se ejecutaron búsquedas.** El panel ya se congeló el 28 de octubre: 24 casos, 12 por color, 8 tempranos/8 marcador a dos puntos/8 tardíos, 20 grupos. Selector reproducible `estudiantes/iacasitegano/herramientas/seleccionar_panel_decisiones.py`; datos y regla en `resultados/medicion/panel24_decisiones_20261028/{panel.jsonl,manifest.json}`. SHA del panel `1ca5a56679eda76a6c38e32851e4a5121b89f256e5bd675ad436c0abc00cbc48`. Elegidos por metadatos, menor uso de grupo/fuente e ID, deduplicando estado. Los tardíos son retrospectivos; no se presentan como errores. Próximo: comparar alternativas con referencia independiente, separando exactitud, horizonte, modelo y evidencia insuficiente. Criterio y plan en [[07-Plan-definitivo]] y [[05-Cierre-de-fases]].

## Actualización nocturna — 28 de octubre

El panel congelado ya se evaluó: 24 casos × profundidades 1/2/3, cero discrepancias entre el buscador y el oráculo a igual horizonte. Ocho casos cambian de preferencia al cambiar el horizonte; 16 se mantienen. **Ningún error histórico de decisión quedó demostrado con cotas del valor real.** Evidencia: `resultados/medicion/fase5_20261028/diagnostico_d1_d2/` y `diagnostico_d3/`; resumen por `fase5_resumir_decisiones.py --adicional`.

Seis casos sensibles se congelaron para el profesor, 18 alternativas. Completó 18/18 a profundidad 5 y solo 6/18 a 7; falla cobertura 80%, por lo que no se entrenó con etiquetas parciales escogidas. Ver `seleccion_profesor.json`, `profesor_piloto/` y `PROTOCOLO_PROFESOR.md`. Las menciones anteriores a búsquedas pendientes son historial. Falta una referencia suficientemente profunda/exacta para atribuir un error concreto de evaluación u horizonte.
