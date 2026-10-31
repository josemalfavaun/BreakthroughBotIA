---
tipo: experimento
estado: numba-validado-microbenchmark-exploratorio
fecha: 2026-10-27
baseline_commit: 85b2d55
---

# Reutilizar buffers entre jugadas hermanas

## Hipótesis falsable

El buscador reserva arrays de jugadas y copia tablero/puntos para cada alternativa y cada desenlace de un ataque. Reservar buffers una vez por invocación recursiva y restaurar su contenido entre hermanos podría reducir costo sin cambiar árbol, valores, decisiones o topes.

## Cambio aislado

- Worktree: `/Users/josema/.codex/worktrees/buffers-busqueda/BreakthroughBotIA`, HEAD separado desde `85b2d55`.
- Solo `_valor_numba` y `_mejor_jugada_numba` reutilizan cuatro arrays: orígenes/destinos hijos, tablero hijo y puntos hijos.
- Antes de cada jugada y antes del desenlace fallido, se restauran tablero y puntos desde el padre. Cada nivel tiene buffers propios; no se modifica la entrada ni se comparte espacio mutable entre niveles.
- Conserva TT, evaluación, orden, reloj, pesos y manejo de abortos del baseline. No incluye las otras correcciones/prototipos.

## Comprobación ejecutada

Arnés `herramientas/verificar_buffers_busqueda.py`, sin JIT, motor/eval3 reales, TT reducida a 1,024 entradas: **64 comparaciones**, profundidades 1–2, movimientos tranquilos/ataques/anotaciones, ambos turnos, sugerencia de raíz y topes 0/1/5/15. Cero diferencias en jugada, valor, nodos, aborto y raíces completadas; entradas intactas.

Cobertura: 32 completas, 32 abortadas; 8 abortadas con al menos dos alternativas de raíz completas. En un fixture fijo, las llamadas explícitas Python de NumPy fueron 66 `empty` en el original y 16 `empty` + 14 `empty_like` en el candidato. Este conteo no incluye `ndarray.copy`, no describe necesariamente las asignaciones optimizadas por LLVM y **no mide velocidad**.

Comando desde el worktree del candidato:

```sh
rtk '/Users/josema/vs code/BreakthroughBotIA/.venv/bin/python' -B estudiantes/iacasitegano/herramientas/verificar_buffers_busqueda.py --baseline '/Users/josema/vs code/BreakthroughBotIA/estudiantes/iacasitegano/busqueda_eval3.py'
```

## Protocolo antes de promover

**Tras cierre A/A:** pasó con Numba/imagen oficial/tabla normal: 96 casos hasta profundidad 3; el microbenchmark extendió a profundidad 4 y **128 casos**, sin diferencias. Cinco repeticiones ABBA/BAAB, cuatro fixtures, ratio mediano baseline/candidato **1.011176** (1.105% menos tiempo en ese panel). Ratios de medianas por fixture: 1.010375/1.004871/1.013236/0.994582. Ganancia pequeña y un fixture desfavorable; no se acepta una aceleración robusta ni fuerza. Logs `buffers-busqueda_numba.log` y `buffers-busqueda_microbench.log` en `/Users/josema/.codex/worktrees/tt-cotas-exactas/BreakthroughBotIA/resultados/medicion/tt_validacion_20261027/`. Prioridad baja frente a TT/utilidad; sin promoción.

Los modos `--jit` y `--benchmark` ya se ejecutaron como indica la actualización anterior. Sigue pendiente ampliar a posiciones reales en la base TT común, regenerar caché y validar la integración si el beneficio lo justifica. Fijar panel y criterio antes de otra medición; medir búsqueda completa, no solo asignaciones aisladas.

Primero resolver [[Experimentos/2026-10-27-TT-exactitud]]. Si esa corrección se acepta, trasladarla idénticamente al control y al candidato y congelar esa base antes de evaluar buffers. No combinar con hojas hasta medirlos separadamente. Una mejora de velocidad no se declara mejora de fuerza sin partidas oficiales, con victorias como métrica primaria.

Sin juegos nuevos, compilación Numba, entrenamiento, cambios al bot principal, commit o promoción.
