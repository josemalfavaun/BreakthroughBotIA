---
tipo: experimento
estado: hipotesis-evaluada-sin-confirmar
fecha: 2026-10-27
baseline_commit: 85b2d55
---

# Baseline 40 — carreras, color y presupuesto

Lectura de los 40 JSON de [[resultados/2026-10-27_14-49-49/index.html]], semilla `20261031`. Se reconstruyó el tablero desde las jugadas y los combates registrados: legalidad, probabilidades y puntos finales coinciden en 40/40. Sin importar el motor, buscar posiciones ni ejecutar partidas. No hay contrafactual que permita identificar una jugada perdedora con certeza.

## Comparación observada

| Métrica propia | Blancas (20) | Negras (20) |
|---|---:|---:|
| Victorias–derrotas; puntos | 14–6; 48–31 | 7–13; 39–44 |
| Reloj medio / máximo por partida | 15.212 / 18.466 s | 14.525 / 17.561 s |
| Profundidad media (`info.prof`) | 4.929 | 4.723 |
| Sin evaluaciones de magnitud terminal (≥400) | 4.824 | 4.680 |
| Combates ganados / intentados; suma de probabilidades | 59/78; 45.45 esperados | 48/87; 49.05 esperados |
| Conversión al llegar primero a 2 puntos | 13/15 | 6/13 |

La profundidad excluye jugadas sin `info.prof` (libro, forzadas o victoria inmediata). Profundidades 12 en finales ya evaluados como perdidos inflan el promedio. En las primeras diez jugadas propias, profundidad 5.45/5.03 y tiempo medio 0.481/0.527 s (blancas/negras); en jugadas 21–30, 4.67/4.51 y 0.331/0.332 s. Las derrotas negras consumieron 13.763 s de media: no agotaron reloj.

**Aperturas:** blancas empieza `a2-a3` 20/20; `a2-a3,d2-e3,g2-f3,h2-g3` aparece 12/20 (9 victorias). Negras repite `b8-c7,e8-d7,f8-e7,g8-h7` 12/20 (5 victorias). Verificando las claves del libro contra el tablero reconstruido, se identifican 21 jugadas de libro blancas (20 primeras y una segunda) y ninguna negra. Esa cobertura asimétrica no prueba que el libro explique los resultados.

## Clasificación descriptiva de las 19 derrotas

| Trayectoria de puntos (categorías excluyentes) | Blancas | Negras |
|---|---:|---:|
| Tuvo ventaja y el rival remontó | 4 | 7 |
| Nunca tuvo ventaja y no llegó a 2–2 | 2 | 5 |
| Llegó a 2–2 sin haber tenido ventaja | 0 | 1 |

Marcadores finales: diez 2–3, cuatro 1–3 y cinco 0–3. Todas fueron por puntos; ninguna por bloqueo terminal (`sin_jugadas`), preparar, reloj, ilegal o excepción. Las 19 anotaciones rivales finales fueron sin combate. Esto describe carreras perdidas, no demuestra un error de apertura/evaluación/profundidad.

- [[resultados/2026-10-27_14-49-49/012_0_5_montecarlo_vs_iacasitegano.json|012]]: negras llega a 2–0 en ply 58; rival anota en 59, 61, 63, sin atacar. [[resultados/2026-10-27_14-49-49/026_0_12_montecarlo_vs_iacasitegano.json|026]] repite 2–0 en 82 y tres puntos rivales en 85, 87, 89.
- [[resultados/2026-10-27_14-49-49/036_0_17_montecarlo_vs_iacasitegano.json|036]]: 2–0 en 52, dos ataques propios fallidos al 50 % (56/58), derrota en 63. [[resultados/2026-10-27_14-49-49/008_0_3_montecarlo_vs_iacasitegano.json|008]] y [[resultados/2026-10-27_14-49-49/030_0_14_montecarlo_vs_iacasitegano.json|030]] pierden 0–3 con 0/3 y 0/4 combates propios ganados; Montecarlo no ataca. No confundir esos fallos del dado con elegir ataques desfavorables: solo 1/78 ataques blancos y 2/87 negros tenían p<0.5.

## Pares y cautela sobre el color

Hay 20 pares con misma `(semilla_maestra, pareja, juego)` y colores intercambiados: 3 ganados en ambos colores, 2 perdidos en ambos, 11 ganados solo con blancas y 4 solo con negras. Los dados se comparten **por color y número de ataque**, no por jugador ni ply ([[sistema/arbitro/azar]], [[sistema/cli/comandos]]); 115 valores del prefijo de combates coinciden exactamente entre partidas pareadas. Ejemplo: [[resultados/2026-10-27_14-49-49/001_0_0_iacasitegano_vs_montecarlo.json|001]] / [[resultados/2026-10-27_14-49-49/002_0_0_montecarlo_vs_iacasitegano.json|002]].

Sumando ambos bots, blancas ganó **107/146** combates frente a **83.95** esperados; negras **95/170** frente a **96.40**. Son residuos descriptivos, correlacionados por los pares: hay un fuerte confusor de dados favorable a blancas. La diferencia de color no identifica por sí sola un defecto de apertura.

## Una hipótesis falsable y cambio aislado

**El reparto basado solo en ataques asigna poco tiempo a carreras defensivas.** Propuesta: imponer `peso ≥ 1.0` cuando haya ≥2 peones rivales a ≤2 filas de su meta; conservar evaluación, libro, reserva, REPARTO y búsqueda. En seis de las siete derrotas negras tras llegar primero a 2 puntos se cumple esa amenaza al anotar el segundo: peso 0.50–0.62 y profundidad 4–5. Una ya mostraba valor terminal negativo entonces: el disparador debe actuar antes y no se supone que todas sean salvables.

**Predicción/métrica primaria:** mejorar en ≥6 puntos la diferencia total propia–Montecarlo frente al control pareado en 40 juegos (baseline +12; objetivo ≥+18). Diagnóstico secundario: mejorar la conversión negra al llegar primero a 2 puntos, hoy 6/13; ese subconjunto puede cambiar y no basta para aceptar. Exigir cero fallos técnicos y ninguna regresión de puntos con blancas.

**Protocolo propuesto:** árbitro oficial, control/candidato con mismas semillas y colores; 40 de desarrollo (`20261031`, ya vista), ampliar a 100 si es cerrado y confirmar con semillas reservadas no usadas para ajustar. Sin mejora repetida, rechazar. Estado: solo hipótesis; ninguna implementación o medición nueva.

**Seguimiento posterior:** [[Experimentos/2026-10-27-Tiempo-carreras]] evaluó la hipótesis con la semilla nueva `20261101`, sin reutilizar `20261031` como confirmación. Δ neto −6 en desarrollo: no se confirma ni se promueve. El análisis anterior permanece como origen de la hipótesis.
