# Plan de trabajo para llevar `iacasitegano` hacia Tier 5

## Objetivo

Mejorar `estudiantes/iacasitegano/` hasta competir por la calificación 10. La calificación máxima se obtiene si el equipo termina por encima de Tier 5 en puntos de liga o queda entre los tres primeros equipos de alumnos. No se debe asumir que una técnica garantiza ese resultado: cada cambio se conserva solo después de medirlo en partidas completas.

## Estado inicial que debe quedar registrado

Antes de cambiar estrategia, guardar:

- `git status --short` y la revisión actual.
- Los pesos de `data/pesos.npy` y el contenido de `data/libro.json`.
- El protocolo, semillas, colores, rival, número de partidas y entorno.
- Victorias, derrotas, puntos anotados, errores, timeouts, reloj máximo y tiempo de `preparar`.

El informe existente documenta victorias contra `random`, pero el resultado contra `montecarlo` sigue siendo insuficiente y cambia según el protocolo. Las comparaciones anteriores no deben mezclarse: una búsqueda de profundidad fija offline no equivale a una partida completa con el reloj del árbitro.

## Reglas que no se pueden romper

- Leer antes de trabajar: `README.md`, `docs/reglas.md`, `docs/calificacion.md`, `docs/avanzado.md` y `estudiantes/iacasitegano/INFORME.md`.
- Cambiar solo `estudiantes/iacasitegano/` cuando el cambio sea para el participante.
- No modificar `sistema/`, el árbitro, el motor oficial, workflows, otros equipos ni documentos del curso para obtener ventaja.
- No usar redes neuronales ni librerías como `torch`, `tensorflow`, `keras`, `jax` u `onnxruntime`.
- No usar red, manipular dados, adivinar semillas, escribir fuera de `data/` durante una partida, persistir entre partidas ni ofuscar código.
- Respetar 30 s de reloj por partida, 10 s para preparación e importación, 1 núcleo, 1024 MB de memoria, 100 MB por carpeta y 50 MB por archivo.
- Mantener una jugada legal de respaldo y margen de reloj en todos los caminos de error.
- Usar `rtk` para los comandos de shell, según `/Users/josema/.codex/RTK.md`.

## Protocolo obligatorio de cada experimento

1. Formular una hipótesis falsable.
2. Definir qué métrica debería cambiar si la hipótesis es correcta.
3. Modificar una sola técnica o un conjunto inseparable de parámetros.
4. Ejecutar primero una tanda de desarrollo de 40 partidas.
5. Repetir con 100 partidas cuando el resultado sea estrecho o ruidoso.
6. Alternar colores y usar los mismos dados/semillas para comparar candidato y baseline.
7. Validar con semillas no usadas durante el desarrollo.
8. Medir partidas completas con el árbitro. `--sin-docker` solo sirve para explorar o depurar.
9. Registrar victorias, puntos, color, clock máximo, preparación, errores y timeouts.
10. Conservar el cambio únicamente si mejora de forma repetible y no causa regresiones.
11. Actualizar el informe si el cambio se acepta.

Comandos base:

```bash
rtk ./torneo jugar iacasitegano montecarlo --partidas 40 --semilla 2026 -v
rtk ./torneo jugar iacasitegano random --partidas 10 --semilla 2026
rtk ./torneo validar iacasitegano --entrega
rtk git diff --check
rtk python3 -m compileall -q estudiantes/iacasitegano
```

Para comparar pesos o versiones offline:

```bash
rtk python3 estudiantes/iacasitegano/herramientas/liga_interna.py \
  --partidas 40 --profundidad 4 \
  --checkpoint estudiantes/iacasitegano/data/pesos_checkpoint_profundidad4.npy
```

Esta liga interna sirve para explorar y comparar checkpoints. La decisión final debe confirmarse con `strategy.jugar()` y el árbitro oficial.

## Fase 0: hacer medible el baseline

### Hipótesis

Las derrotas no tienen todavía una clasificación suficientemente precisa para elegir la siguiente mejora.

### Trabajo

- Guardar automáticamente el resultado de cada partida y el reporte por jugada.
- Clasificar derrotas en carrera rival, ataque desfavorable, bloqueo, apertura, falta de profundidad, timeout, excepción o jugada ilegal.
- Separar resultados por Blancas y Negras.
- Registrar profundidad alcanzada, tiempo de búsqueda y cantidad de ataques por posición.
- Repetir suficientes partidas para que una sola tirada de dado no dicte la decisión.

### Criterio de salida

Existe una tabla de baseline con al menos 40 partidas contra `montecarlo`, ambos colores, semillas conocidas y un conjunto separado de validación.

## Fase 1: seguridad de ejecución y reloj

### Hipótesis

El bot puede perder fuerza práctica por dedicar demasiado tiempo a saltos de profundidad que no termina.

### Trabajo

- Medir el tiempo de `preparar` y la memoria bajo Docker.
- Medir percentil alto y máximo por jugada, no solo promedio.
- Conservar una jugada legal si queda poco reloj.
- Repartir más tiempo cuando haya amenaza de anotación, ataque múltiple o carrera irreversible.
- No empezar una profundidad nueva si el peor caso medido no cabe con margen.

### Criterio de salida

Cero derrotas por timeout, preparación, memoria, excepción o jugada ilegal en las tandas de validación.

## Fase 2: ordenamiento de jugadas

### Hipótesis

Examinar primero jugadas críticas aumenta la poda y permite buscar más profundo sin aumentar el reloj.

### Orden candidato

1. Victoria inmediata sin importar el dado.
2. Jugadas que anotan si ganan el ataque.
3. Ataques con mayor probabilidad de ganar.
4. Jugadas que bloquean una anotación rival.
5. Jugadas que crean una carrera pasada o aumentan apoyo.
6. Jugada ganadora de la iteración anterior.
7. Jugadas tranquilas restantes.

### Verificación

- Comparar valores contra búsqueda exhaustiva en posiciones pequeñas.
- Medir nodos o tiempo por profundidad.
- Medir partidas completas contra `montecarlo`.
- Rechazar si gana profundidad pero reduce victorias o provoca timeouts.

## Fase 3: Star2 y poda en nodos de azar

### Hipótesis

Los bounds de Star1 son correctos pero demasiado amplios; Star2 puede reducir ramas sin cambiar valores.

### Trabajo

- Implementar Star2 en una copia experimental.
- Comparar contra expectiminimax exhaustivo en posiciones generadas aleatoriamente y finales pequeños.
- Verificar tanto ataques favorables como desfavorables y ambos colores.
- Medir colisiones y efectividad de la tabla de transposición.

### Criterio de salida

Los valores coinciden con la referencia y la versión nueva gana partidas completas o alcanza más profundidad sin perder estabilidad de reloj.

## Fase 4: búsqueda híbrida

### Hipótesis

Expectiminimax ve bien las tácticas cercanas, pero una evaluación estática no ve carreras largas; rollouts completos pueden cubrir ese horizonte.

### Diseño candidato

- Usar expectiminimax para posiciones tácticas, amenazas inmediatas y finales pequeños.
- Usar rollouts numba para posiciones tranquilas o como desempate entre las mejores jugadas.
- Comparar cada jugada con varias semillas de simulación, sin usar los dados reales de la partida.
- Hacer que el número de simulaciones dependa del tiempo restante y dejar reserva.
- Mantener una política de rollout razonable: priorizar avance seguro, apoyo, ataques con buena probabilidad y defensa de carreras.

### Criterio de salida

La versión híbrida mejora victorias o puntos contra `montecarlo` en semillas de desarrollo y de validación, sin elevar el reloj máximo ni producir decisiones inestables.

## Fase 5: evaluación orientada a acciones

### Problema actual

`herramientas/entrenar.py` guarda features de la posición y etiqueta cada una con el resultado final de la partida. Eso aprende correlaciones de estado, pero no mide directamente qué jugada era mejor desde esa posición.

### Hipótesis

Aprender preferencias entre acciones desde la misma posición dará una evaluación más útil para elegir jugadas.

### Trabajo

- Generar posiciones variadas mediante self-play, partidas contra `random`, `montecarlo` y políticas débiles alteradas.
- Desde cada posición, evaluar varias jugadas con semillas repetidas y registrar valor esperado, varianza y resultado.
- Ajustar pesos con regresión sobre diferencias entre acciones, no solo sobre resultado final.
- Mantener un conjunto de validación separado por semillas y posiciones.
- Comparar los pesos nuevos contra el checkpoint actual antes de reemplazar `data/pesos.npy`.

### Restricción

Todo lo que se ejecute en la liga debe seguir siendo un modelo no neuronal, legible y permitido por el reglamento.

## Fase 6: finales exactos

### Hipótesis

En posiciones con pocos peones, una tabla o solver exacto puede eliminar errores de carrera que una búsqueda limitada todavía comete.

### Trabajo

- Empezar con límites pequeños de material.
- Incluir en la clave tablero, turno y puntos.
- Resolver terminales de victoria, bloqueo y ataques con sus probabilidades.
- Guardar solo datos precomputados auditables dentro de los límites de tamaño.
- Comparar contra búsqueda exhaustiva y el motor oficial.

### Criterio de salida

El solver coincide con la referencia y mejora partidas donde la causa de derrota es una carrera o final mal evaluado.

## Fase 7: libro de apertura

- Regenerar el libro después de estabilizar búsqueda y pesos.
- No fijar una apertura solo porque gana en self-play.
- Validar contra `random`, `montecarlo` y posiciones de apertura alteradas.
- Mantener únicamente entradas legales, claras y con ventaja repetible.

## Gate de aceptación

Una mejora se acepta solo si cumple todo lo siguiente:

- Pasa compilación y `git diff --check`.
- Pasa las pruebas diferenciales relevantes.
- No tiene imports prohibidos ni datos que parezcan código oculto.
- No pierde por timeout, preparación, memoria, excepción o jugada ilegal.
- Mejora partidas completas contra el baseline con ambos colores.
- Mantiene la mejora en semillas de validación no vistas.
- Se puede explicar en `INFORME.md` y regenerar sus datos.

## Entrega final

Antes de preparar el PR:

```bash
rtk ./torneo validar iacasitegano --entrega
rtk git diff --check
rtk python3 -m compileall -q estudiantes/iacasitegano
rtk git status --short
```

El PR debe modificar únicamente `estudiantes/iacasitegano/`. `CLAUDE.local.md`, este plan y cualquier configuración local de Claude/Codex deben quedar fuera del PR de entrega salvo que el profesor confirme que se permiten.
