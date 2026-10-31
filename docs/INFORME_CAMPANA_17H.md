# Informe de la campaña autónoma de 17 horas

Fecha de ejecución: 30–31 de octubre de 2026.

## Resultado operativo

- Se ejecutaron 5 rondas completas.
- Se generaron 15 candidatos válidos, con 3 workers Docker en paralelo por ronda.
- Cada candidato se evaluó en 40 partidas contra `montecarlo` y 40 contra `minimax2`.
- No se promocionaron pesos automáticamente; el campeón actual permanece intacto.
- La campaña se detuvo cuando Docker devolvió `read-only file system` en su base interna.

La versión anterior del controlador continuó creando carpetas vacías después del fallo. Esas carpetas no representan entrenamiento y no deben usarse como métricas.

## Mejor candidato observado

`resultados/campana_17h/round_04/candidate_01`

- Monte Carlo: 10–30 en 40 partidas.
- Minimax2: 39–1 en 40 partidas.

El resultado es prometedor contra `minimax2`, pero no demuestra una mejora concluyente contra Monte Carlo. Hace falta una validación final con más partidas, colores alternados, semillas nuevas y comparación directa contra los pesos campeones actuales.

## Mezcla usada

- 50% self-play.
- 20% Monte Carlo.
- 15% rival voraz.
- 15% minimax2.
- 0% random.

## Corrección incorporada

`preparacion_torneo/campana_17h.ps1` ahora falla rápido si un worker Docker devuelve un código distinto de cero, si no aparecen los 3 candidatos o si faltan evaluaciones. Así no vuelve a producir miles de rondas vacías después de un fallo del daemon.

## Siguiente paso

Reiniciar Docker Desktop, ejecutar una campaña corta de humo con el controlador corregido y después hacer la validación final del mejor candidato contra el campeón actual y Monte Carlo. No reemplazar `data/pesos.npy` hasta superar ese gate.
