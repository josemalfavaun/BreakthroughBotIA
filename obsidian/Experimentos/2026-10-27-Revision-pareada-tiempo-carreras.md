---
tipo: experimento
estado: revision-concluida-hipotesis-AA-propuesta
fecha: 2026-10-27
baseline_commit: 85b2d55
---

# Revisión pareada del presupuesto ante carreras

Lectura de los 80 JSON de [[Experimentos/2026-10-27-Tiempo-carreras]]: 40 pares control/variante con semilla `20261101`, juego y color iguales. Reconstrucción de tablero, puntos, ataques y factor; ninguna búsqueda o partida nueva. Se conservan worktrees, fuentes, pesos y artefactos.

## Resultado que limita la atribución causal

**40/40 pares divergen antes de la primera oportunidad de aplicar el piso, por una jugada distinta de Montecarlo.** Con blancas ocurre en ply 2 (3 casos) o 4 (17); con negras en 1 (8), 3 (10) o 5 (2). La primera decisión de Montecarlo parte de un tablero idéntico: cambia el número de muestras en 40/40 pares (mediana de diferencia absoluta 529) y la jugada inicial en 11/40. Su código termina el muestreo por reloj, por lo que emparejar semillas no fija cuántas simulaciones utiliza.

Antes de divergir hay **30 decisiones buscadas propias comparables**, ninguna con piso activo. La profundidad coincide en 29; en el juego negro 032, ply 2, cae de 5 a 4 con la misma jugada `b8-c7`, todavía sin amenaza ni presupuesto extra. No hay una comparación en posición e historia compartidas que permita decir «el piso cambió esta jugada» o «añadió este nivel». Tras divergir, comparar el mismo número de ply mezcla tableros distintos. Tampoco se registran nodos, abortos o aceptación de raíces parciales; `info.prof` no describe todo el trabajo del anytime.

## Cuándo se activó

- Variante: **185 decisiones en 31/40 juegos**; blancas 85/14 juegos, negras **100/17 juegos**. Primera activación entre plies **34 y 96**, mediana **58**. Con negras también mediana 58; 10 de las 17 primeras activaciones aún estaban 0–0.
- Control: se identifican **149 oportunidades hipotéticas** en 32 juegos, no activaciones reales. Negras: 91 oportunidades en 15 juegos.
- En la trayectoria de la variante, la fórmula añade nominalmente 0.181 s por activación de media (negras 0.185 s), manteniendo ese tablero y reloj. Es una diferencia algebraica de presupuesto; no un contrafactual del tiempo o jugada que habría usado el control.
- Las poblaciones activadas muestran tiempo 0.258→0.390 s y profundidad 4.993→5.200, pero son posiciones distintas. De las 185 activaciones, 28 devuelven una evaluación de magnitud terminal; eso se conoce después de buscar, no demuestra que antes se supiera que el tiempo era innecesario.

## Cómo se compone el −6 con negras

| Resultado del par | Juegos | Δ de puntos netos |
|---|---:|---:|
| Solo gana la variante | 3 | +8 |
| Solo gana el control | 2 | −7 |
| Ambos ganan | 7 | −5 |
| Ambos pierden | 8 | −2 |

Así pasa de 9 a 10 victorias, pero de +7 a +1 puntos netos. En las siete victorias compartidas, puntos rivales 3→8: explica cinco puntos perdidos en el balance, **sin identificar su causa**.

Ejemplos (puntos siempre propios–rival):

- **020**, 3–0→3–2: el piso **nunca** se activa en ninguna ejecución; primera divergencia MC en ply 3. **018**, 3–1→3–0, tampoco activa el piso y diverge en ply 1. Los cambios de puntos existen incluso sin aplicar la regla.
- **008**, 0–3→3–2: divergencia MC en ply 3; primera activación variante en 58 (`h9-h8`, prof. 5), oportunidad control en 42 (prof. 4). No son las mismas posiciones: no atribuir la victoria al nivel adicional.
- **032**, 3–0→2–3: divergencia MC en ply 3; primera activación variante en 96 (`c8-d7`, prof. 4), frente a oportunidad control en 78 (prof. 5). La variante recibe su primer punto rival en 97; el control ya había terminado en 82. No es evidencia de que la regla causara esa derrota.

Los 20 pares negros, jugadas y profundidades de cada activación, presupuestos y cronologías completas están en `/Users/josema/noche_salida/lab/tiempo_carreras/revision_pareada.json` y `revision_pareada.md`. Evidencia directa: [020 control](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_15-39-23/020_0_9_montecarlo_vs_iacasitegano.json) / [020 variante](../../.worktrees/tiempo-carreras-variante/resultados/2026-10-27_16-01-30/020_0_9_montecarlo_vs_iacasitegano.json); [032 control](../../.worktrees/tiempo-carreras-control/resultados/2026-10-27_15-39-23/032_0_15_montecarlo_vs_iacasitegano.json) / [032 variante](../../.worktrees/tiempo-carreras-variante/resultados/2026-10-27_16-01-30/032_0_15_montecarlo_vs_iacasitegano.json).

## Una hipótesis nueva: magnitud del ruido de medición

**Dos ejecuciones del control idéntico contra Montecarlo a reloj variarán típicamente al menos seis puntos netos por bloque de 40 partidas.** Propuesta A/A: tres semillas nuevas, cada una repetida dos veces con el mismo control, árbitro oficial y colores alternados, manteniendo las condiciones de carga. Son 240 partidas futuras; ninguna se ejecuta ahora ni utiliza las reservas del experimento rechazado.

**Métrica primaria única:** mediana de `abs(neto_control_A − neto_control_B)` en esos tres bloques pareados. Predicción prefijada: **≥6 puntos**; si es menor, la hipótesis de ruido de esa magnitud no se sostiene. Estudio exploratorio de precisión, no de fuerza.

Se conserva la decisión anterior: el piso no pasó su criterio de desarrollo. Esta revisión limita la explicación causal del −6; no rescata la variante, no reajusta su umbral ni confirma una mejora. No hay experimento en curso.
