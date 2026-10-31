---
tipo: experimento
estado: numba-validado-microbenchmark-exploratorio
fecha: 2026-10-27
baseline_commit: 85b2d55
---

# Hojas sin generación duplicada

## Hipótesis falsable

Con `QUIESCENCIA_MAX = 0`, `_valor_numba` comprueba puntos y ausencia de jugadas antes de llegar a profundidad cero. Después llama a `_quiescencia_numba`, que repite esas comprobaciones y genera las mismas jugadas antes de devolver la evaluación estática. Eliminar esa repetición podría reducir costo por nodo manteniendo el valor y la elección a profundidad fija.

## Cambio aislado

- Prototipo: `/Users/josema/.codex/worktrees/hojas-sin-duplicado/BreakthroughBotIA` (HEAD separado en `85b2d55`, adjunto a este chat).
- Archivo: `estudiantes/iacasitegano/busqueda_eval3.py`, cinco líneas añadidas.
- En profundidad cero y quiescencia apagada, retornar `_evaluar_numba` después de las comprobaciones existentes. Con quiescencia activa se conserva el camino anterior.
- No se modificó el bot del checkout principal ni los worktrees A/A. No se compiló Numba, regeneró caché o ejecutaron partidas.

## Comprobación preliminar

Se compararon los cuerpos Python de las funciones originales y modificadas, extraídos con AST y sin importar Numba/motor: 1,152 combinaciones de color/objetivo, puntos terminales/no terminales, cantidad de jugadas, evaluación y aborto. Cero diferencias en retorno/contador. Dos llamadas a `generar` en una hoja no terminal original frente a una en el prototipo interpretado. Sintaxis y `git diff --check` correctos.

Esta comprobación usa funciones auxiliares simuladas; no sustituye el diferencial con posiciones reales ni prueba una aceleración del código compilado. LLVM podría optimizar parte del camino original. El prototipo permanece sin aceptar, sin commit.

## Protocolo pendiente antes de medir

**Tras cierre A/A:** el arnés pasó con Numba en la imagen oficial, 1 CPU/1024 MiB: 96 hojas/terminales/abortos y 12 raíces de profundidades 1–3, cero diferencias. Microbenchmark previamente fijado con cuatro fixtures a profundidad 3, cinco repeticiones ABBA/BAAB: ratio mediano baseline/candidato **1.019199** (1.884% menos tiempo en este panel). Por fixture, ratios de medianas 1.094826/1.016392/1.030220/1.004874. Tiempos pequeños y panel limitado: no se acepta como aceleración integral ni fuerza. Logs `hojas-sin-duplicado_numba.log` y `hojas-sin-duplicado_microbench.log` en `/Users/josema/.codex/worktrees/tt-cotas-exactas/BreakthroughBotIA/resultados/medicion/tt_validacion_20261027/`. Pendientes panel real y base común corregida; sin promoción.

**Avance posterior:** arnés preparado en `herramientas/verificar_hojas_sin_duplicado.py` dentro del worktree del candidato. Pasaron **96 comprobaciones con motor y eval3 reales y JIT desactivado**, incluyendo terminales, ausencia de jugadas, ambos objetivos, ventanas estrechas, aborto e inmutabilidad de entrada. Se mantienen las limitaciones de compilación/rendimiento indicadas arriba. Admite `--jit --profundidad 3` para el diferencial de raíces y `--benchmark` para tiempos ABBA después de calentar; esos modos no se ejecutaron durante el A/A. Una entrada accidental `dal` en la línea del prototipo rompía la sintaxis: se conservó copia en `/tmp/busqueda_eval3-antes-corregir-dal.py` y se corrigieron solo esos caracteres.

La auditoría de TT dio un caso reproducible con motor real y una corrección en **otro** worktree: [[Experimentos/2026-10-27-TT-exactitud]]. Priorizar su validación de corrección antes de atribuir mejoras de fuerza a optimizaciones.

Siguiente fase después del microbenchmark descrito arriba: fijar un panel de posiciones reales y criterio de velocidad, repetir el diferencial en la base TT común y regenerar el caché si se decide medir la estrategia completa. Solo una aceleración repetible justifica después partidas bajo el árbitro y límites oficiales; no definir el criterio de fuerza retrospectivamente.

Para fuerza, priorizar porcentaje de victorias/puntos de liga; peones anotados y su diferencial son métricas secundarias. `docs/calificacion.md` asigna 1 punto por victoria; los peones son desempate. El criterio anterior del experimento de carreras se mantiene histórico, sin rescatar su variante.

## Siguientes oportunidades distintas

1. Auditar la clasificación de entradas de la TT: terminar el ciclo local sin corte no demuestra por sí solo que un valor heredado de una búsqueda con ventana estrecha sea exacto. Primero buscar un contraejemplo diferencial reproducible; no cambiar la TT por intuición.
2. Estudiar una jugada sugerida por la TT antes de otras, sin el costoso cálculo táctico de prioridad para todas las jugadas que ya se rechazó. Tratarlo como experimento independiente.
3. Recuperar el entrenador eval3 y preparar aprendizaje sobre elecciones de jugadas/carreras, según el defecto que confirmen los diagnósticos. No iniciar entrenamiento durante el A/A.

Tier 5 no está disponible en el repositorio: `docs/calificacion.md` dice que aparece el día de la liga y su código no se publica. Las comparaciones locales deben cubrir Montecarlo y nuestros propios campeones/estilos distintos; no equivalen a medir Tier 5.
