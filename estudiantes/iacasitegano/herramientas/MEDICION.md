# Medición del campeón y protocolo de validación

## Arnés paralelo

`medir_liga.py` ejecuta tandas de `./torneo jugar iacasitegano montecarlo --sin-docker` en contenedores independientes de `torneo-base:local`. Cada proceso recibe una cuota de 1 CPU y directorios propios bajo `resultados/medicion/<tanda>/resultados/semilla_<n>`. El número máximo de workers es el total de CPU que informa Docker menos uno; en esta máquina son 9 workers para 10 CPU. Se fija a 1 el número de hilos de las bibliotecas numéricas y se da a cada contenedor un directorio temporal de caché Numba nuevo para evitar que una tanda herede cachés calientes de otra.

El arnés acepta `--equipo` y `--rival` (por defecto `iacasitegano` y `montecarlo`). Requiere un número par de partidas y un número par de partidas por trabajo, asigna una semilla distinta a cada trabajo y se niega a reutilizar la carpeta de salida. `--salida` puede apuntar fuera del repo: el directorio se monta como `/medicion` en cada contenedor. Guarda cada registro y la salida de cada invocación. Produce un `reporte.md` agregado con victorias y derrotas, Wilson 95% total y por color, puntos, reloj, motivos de final, timeouts, jugadas ilegales, excepciones, salidas y errores. Para el equipo medido, informa reloj por partida (media, p95 por rango más cercano y máximo) y profundidad media de los turnos con `info.prof`.

## Comprobación de reloj: serie frente a paralelo

Se repitieron las mismas 40 partidas y semillas (8300–8309), con 4 partidas por trabajo y caché Numba aislada en cada ejecución. La serie usó 1 worker; la tanda paralela, 9 workers. El máximo observado no aumentó en paralelo; ambas tandas acabaron sin timeout ni error. La variación del marcador confirma que estas corridas sirven para comprobar carga/reloj, no para comparar fuerza.

| Ejecución | Workers | Récord de iacasitegano | Wilson 95% | Reloj máximo | Duración | Timeouts / errores |
|---|---:|---:|---:|---:|---:|---:|
| Serie | 1 | 5–35 | 5.5%–26.1% | 1.227 s | 860.9 s | 0 / 0 |
| Paralelo | 9 | 8–32 | 10.5%–34.8% | 1.023 s | 180.3 s | 0 / 0 |

Informes detallados:

- `resultados/medicion/reloj_serie_controlado_20261024_200918/reporte.md`
- `resultados/medicion/reloj_paralelo_controlado_20261024_202342/reporte.md`

## Baseline del campeón

El baseline usa el bot actual `iacasitegano`, con el libro mixto ya promovido en `data/libro.json` (SHA-256 `00fd209f4ad9973d422e6370e9799c1dd3e3b48992518dcaa5d834680dc5f4c0`), contra `montecarlo`. Se ejecutaron 200 partidas: 10 trabajos de 20 partidas, semillas 5200–5209, hasta 9 workers simultáneos y una CPU por trabajo. El total fue de 40 victorias y 160 derrotas (20.0%; Wilson 95%: 15.0%–26.1%). El bot anotó 271 puntos; su reloj máximo fue 1.070 s. Por color: blancas 28–72, 146 puntos y 1.070 s de reloj máximo; negras 12–88, 125 puntos y 0.598 s. No hubo timeouts, otros motivos anormales, salidas no vacías de bots ni errores de ejecución/lectura. Duración total: 768.3 s (12 min 48.3 s).

Reporte agregado y duraciones por semilla: `resultados/medicion/baseline_campeon_200_20261024_202649/reporte.md`.

Con las métricas nuevas aplicadas a las trazas ya guardadas del mismo baseline: reloj medio por partida **0.408 s**, p95 **0.598 s**, máximo **1.070 s**; profundidad media **2.427** en 7,515 turnos con `info.prof`.

Las semillas 6200–6204 (100 partidas en 5 trabajos de 20) quedan reservadas y no se usan para este baseline. Se destinan a validación final de cambios futuros; no deben mezclarse con las semillas de desarrollo 5200–5209.

## Uso

Desde la raíz del repositorio:

```sh
python3 estudiantes/iacasitegano/herramientas/medir_liga.py \
  --partidas 200 --por-trabajo 20 --semilla-inicio 5200 \
  --workers 9 --nombre baseline_campeon_200
```

Los reportes y registros de cada corrida se conservan en `resultados/medicion/` para permitir reproducir y auditar las agregaciones.

## Sensibilidad de profundidad y presupuesto de reloj

Barrida cancelada por cambio de plan. Factor 60 y factor 30 completaron 200 partidas cada uno contra `montecarlo`, con semillas 5200–5209, 9 workers y 1 CPU por trabajo. El baseline original fue 40–160 (20.0%; Wilson 95%: 15.0%–26.1%).

| Variante | Total (Wilson 95%) | Blancas (Wilson 95%) | Negras (Wilson 95%) | Reloj medio / p95 / máximo por partida | Prof. media | Timeouts / ilegales / excepciones | Finales | Errores ejecución/lectura | Duración |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| Factor 60, reserva 0.3 | 70–130; 35.0% (28.7%–41.8%) | 35–65 (26.4%–44.7%) | 35–65 (26.4%–44.7%) | 1.199 / 1.736 / 2.804 s | 3.410 | 0 / 0 / 0 | puntos 200 | 0; 819.7 s ([reporte](resultados/medicion/sens_iacasitegano_eval_f60_20261025_012556/reporte.md)) |
| Factor 30, reserva 0.3 | 88–112; 44.0% (37.3%–50.9%) | 41–59 (31.9%–50.8%) | 47–53 (37.5%–56.7%) | 2.835 / 4.457 / 5.953 s | 4.008 | 0 / 0 / 0 | puntos 200 | 0; 853.4 s ([reporte](resultados/medicion/sens_iacasitegano_eval_f30_20261025_012556/reporte.md)) |

Las dos tandas completas tuvieron cero timeouts, excepciones y jugadas ilegales. Factor 30 usó más reloj que factor 60 sin timeouts: 2.835 s de media por partida.

Factor 15 se canceló a petición del usuario cuando habían terminado solo las primeras 9 partidas: una con blancas por cada semilla 5200–5208. Hubo 4 victorias y 5 derrotas (44.4%; Wilson 95% descriptivo 18.9%–73.3%), media de reloj 4.208 s, p95/máximo 5.715 s, profundidad media 4.392 en 344 jugadas informadas, cero timeouts y nueve finales por puntos. Esas partidas son un parcial no balanceado y no cuentan como evaluación de 200. Los trabajos se detuvieron con exit 137 por la cancelación; los registros quedaron intactos en [reporte parcial](resultados/medicion/sens_iacasitegano_eval_f15_20261025_012556/reporte_parcial.md). La variante factor 30 con reserva 0.1 no se lanzó.

Las cuatro copias de la barrida se movieron a `/private/tmp/iacasitegano_variantes_parciales_20261025`; se retiraron sus patrones temporales de `.git/info/exclude`. Sus reportes, JSON y logs siguen bajo `resultados/medicion/`.

## Evaluación anytime: candidato de Claude Code

El baseline de reloj/profundidad que se puede recalcular desde los 200 JSON originales es: reloj medio 0.408 s, p95 0.598 s, máximo 1.070 s y profundidad media 2.427 en 7,515 jugadas con `info.prof`.

El arnés ya admite `--equipo`, `--rival`, `--partidas`, `--por-trabajo`, `--semilla-inicio`, `--workers` y `--nombre`. Cada informe incluye Wilson 95% total y por color, victorias por color, reloj medio/p95/máximo por partida, profundidad media, razones de finalización, timeouts, jugadas ilegales, excepciones, salidas y errores de ejecución. Cada contenedor tiene un límite de memoria de 1024 MiB; no se muestrea el pico. Un trabajo que exceda el límite sufrirá OOM y aparecerá con exit/error en el reporte, lo que permite confirmar que las corridas exitosas se mantuvieron bajo 1024 MiB.

El candidato se copió a `estudiantes/iacasitegano_anytime/` y se agregó a `.git/info/exclude`. `diff -r` confirmó que su `data/` es idéntico al de `iacasitegano`; para igualar los cuatro archivos de pesos históricos que faltaban en la copia se copiaron esos archivos desde la carpeta real, sin modificarla. En el código de ejecución, `busqueda_numba.py` agrega el contador/tope de nodos, aborto y descarte de profundidades incompletas, con `FRACCION_TOPE=0.8`, `TOPE_MINIMO=20000` y `TOPE_PRIMERA_PROFUNDIDAD=2000000`. `strategy.py` solo añade `nodos` y `abortos` a `reportar()`. `equipo.toml` cambia el nombre para la carpeta. La copia de Claude no incluye `INFORME.md`, `fase2_limpia_supervisor.py` ni `herramientas/`; son diferencias de documentación/soporte, no módulos usados por `strategy.py`.

La corrida de desarrollo (200 partidas, semillas 7300–7309), la validación reservada (100, semillas 6200–6204) y la tanda adicional (100, semillas 7500–7504) se ejecutan en serie. Ninguna comparte CPUs con otra medición.

### Corridas del candidato anytime

Tandas secuenciales, sin otras mediciones concurrentes; cada una usa 9 workers con cuota de 1 CPU y límite de 1024 MiB por contenedor.

- **desarrollo:** 200/200 partidas; 109–91, 54.5%, Wilson 95% 47.6%–61.3%. Blancas 59–41 — 59.0% — 49.2%–68.1%; negras 50–50 — 50.0% — 40.4%–59.6%. Reloj medio/p95/máximo 14.449 s/16.912 s/17.981 s; profundidad media 4.382. Finales `{"puntos": 200}` (puntos: 200); timeouts 0 (bot 0), jugadas ilegales 0, excepciones 0, errores de ejecución/lectura 0; exit 0, 1357.1s. [Reporte](resultados/medicion/anytime_200_20261025_015907/reporte.md)
- **validación:** 100/100 partidas; 46–54, 46.0%, Wilson 95% 36.6%–55.7%. Blancas 21–29 — 42.0% — 29.4%–55.8%; negras 25–25 — 50.0% — 36.6%–63.4%. Reloj medio/p95/máximo 14.556 s/16.842 s/17.686 s; profundidad media 4.530. Finales `{"puntos": 100}` (puntos: 100); timeouts 0 (bot 0), jugadas ilegales 0, excepciones 0, errores de ejecución/lectura 0; exit 0, 695.7s. [Reporte](resultados/medicion/anytime_validacion_20261025_022145/reporte.md)
- **adicional:** 100/100 partidas; 44–56, 44.0%, Wilson 95% 34.7%–53.8%. Blancas 23–27 — 46.0% — 33.0%–59.6%; negras 21–29 — 42.0% — 29.4%–55.8%. Reloj medio/p95/máximo 14.669 s/16.598 s/17.860 s; profundidad media 4.528. Finales `{"puntos": 100}` (puntos: 100); timeouts 0 (bot 0), jugadas ilegales 0, excepciones 0, errores de ejecución/lectura 0; exit 0, 698.1s. [Reporte](resultados/medicion/anytime_extra_20261025_023322/reporte.md)
- Estado: cola terminada.

Sumando las tres tandas con semillas disjuntas: **199–201/400 (49.75%; Wilson 95%: 44.9%–54.6%)**; Blancas 103–97, Negras 96–104. Los 400 juegos terminaron por puntos; cero timeouts, jugadas ilegales y excepciones. Reloj medio/p95/máximo 14.531/16.842/17.981 s; profundidad media 4.456.
