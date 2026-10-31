---
tipo: experimento
fecha: 2026-10-29
estado: cerrado-rechazado-en-alcance
---

# Fase 6: cobertura y decisión de finales

**Cerrado sin integrar tablas ni construir solver nuevo**, por falta de oportunidad adicional en el dominio examinado. No es una mejora de fuerza aceptada ni una afirmación sobre todos los finales.

Se congelaron y reprodujeron **890 trazas completas**, incluidas las **16 del piloto Mac** (1495 plies /750 decisiones del profesor). Resultado: **36,730 decisiones propias, 35,094 estados únicos, cero errores**. Oficiales, privados, técnicos, excluidos y versiones P/A/U/N permanecen separados, sin mezclar fuerza. Lote nuevo activo de fase 5 totalmente excluido; 76 checkpoints .parcial no usados.

- Tablas 1v1/2v1/1v2: **0/36,730** oportunidades de raíz.
- Histórico del detector: **0/3323** reproducido por motor y campo registrado. Ninguna carrera pura en las poblaciones oficiales observadas.
- Carrera pura: **25 oportunidades privadas** (24/3222 en episodios 60; 1/750 en piloto 16), todas con victoria segura inmediata del tercer punto ya cubierta por la guardia actual de P, sin entrada del libro que la preceda. No se confunden oportunidades matemáticas con consultas reales de solver.
- Ampliación exacta única examinada, tablero completo de hasta 6 peones: **0 oportunidades**, también 0 con hasta 8; mínimo global 11. No supera el filtro de frecuencia fijado antes del replay (1% y 5 partidas relevantes, descontando victorias inmediatas). No se construye ni se mide un solver.

Amenazas propias/rivales del tercer punto, ataques probabilísticos y victorias seguras se calcularon con transiciones legales y ambas ramas del motor, separadas por población/color. El turno rival es hipotético sobre ese tablero, no pérdida forzada. Las 25 raíces privadas se documentan íntegramente; no son un contrafactual deportivo de P. La MDP histórica con apoyos congelados sigue rechazada y no se etiqueta como exacta con escoltas.

**Hojas internas: sin medir.** El principal no contiene hooks a solvers históricos; ninguna tasa de raíces se presenta como activación en búsqueda. Memoria pico/preparación/rendimiento de integrado nuevo: sin medir. Código, pesos, reloj, libro y motor del principal intactos; corrección TT de A continúa pendiente de fase 8. No se repite fase 2 ni se reabre N.

Análisis sin JIT, nice19 y límite aproximado 12% de un núcleo; se respetó la generación activa de fase 5, sin benchmarks, partidas nuevas, reservas, pausas de servicios/contenedores ni cambios a sus fuentes. Nueve regresiones analíticas ligeras de cobertura pasaron. Sin commit/merge/push/promoción.

- [CIERRE y párrafo de traspaso](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/CIERRE.md>)
- [Protocolo previo](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/PROTOCOLO.md>)
- [Inventario y hashes de trazas](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/inventario.json>)
- [Manifiesto de fuentes](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/manifiesto.json>)
- [Cobertura JSON](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/cobertura.json>)
- [Cobertura por población CSV](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/cobertura.csv>)
- [Distribuciones](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/distribuciones.csv>)
- [Dominios históricos](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/DOMINIOS.md>)
- [Auditoría final](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase6_cobertura_20261029/AUDITORIA_FINAL.json>)

Pendiente obligatorio de esta decisión: ninguno. Otros dominios, instrumentación de hojas o una política seleccionada diferente requieren otro protocolo y ventana exclusiva si se mide rendimiento o fuerza. El chat director puede integrar el párrafo de CIERRE.md; no se editan 01-Estado, 03-Bitacora ni 07-Plan-definitivo.
