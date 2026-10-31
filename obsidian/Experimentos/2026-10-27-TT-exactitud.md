---
tipo: experimento
estado: validacion-tecnica-compilada-pasada-sin-promover
fecha: 2026-10-27
baseline_commit: 85b2d55
---

# Exactitud de entradas de la tabla de transposiciones

## Hipótesis falsable

La condición `exacto = no hubo corte en este nodo` no es suficiente para guardar un resultado como exacto: con una ventana estrecha, los hijos pueden devolver cotas y el nodo padre terminar su ciclo sin hacer un corte propio. Reutilizar esa entrada con una ventana amplia puede cambiar el resultado.

## Evidencia reproducida

Se ejecutó `_valor_numba` con motor y eval3 reales, JIT desactivado, en una posición creada mediante `Estado.desde_dict`: blancas `a3,e4`, negras `b7,g6`, turno blancas, puntos 0–0, profundidad 2.

1. Consulta MAX con ventana `[419.7904604088274, 420.7904604088274]`: devuelve una cota de `210.20324999290867`.
2. Consulta con ventana amplia `[-GANANCIA,+GANANCIA]` y la misma tabla: el original devuelve ese mismo `210.203...` como exacto.
3. Consulta amplia con tabla limpia y referencia expectiminimax exhaustiva: `-1.3877787807814457e-17`, prácticamente cero.

Se reproduce también para la perspectiva contraria y una ventana negativa. El árbol artificial mínimo `MAX(MIN(4,0),MIN(3))` reproduce la misma clase de fallo (4 en caché frente a valor exacto 3), usando el cuerpo real de la función con auxiliares simuladas.

**Límite:** las ventanas se eligen deliberadamente para forzar el caso. Se demuestra un fallo del contrato de la función en una posición válida, no su frecuencia durante una partida ni que explique las derrotas del baseline. No hay resultados de fuerza del candidato.

## Cambio aislado

- Worktree adjunto: `/Users/josema/.codex/worktrees/tt-cotas-exactas/BreakthroughBotIA`, HEAD separado en `85b2d55`.
- `busqueda_eval3.py`: guardar `alfa_entrada/beta_entrada`; escribir un valor exacto solo si no hay corte local y `alfa_entrada < mejor < beta_entrada`. No se cambia cómo se consulta la tabla.
- Corrección conservadora: deja de guardar ciertos resultados; aún no añade tipos UPPER/LOWER ni ordenamiento. El prototipo de hojas está en otro worktree y no se combina aquí.

## Validación preliminar

Arnés `estudiantes/iacasitegano/herramientas/verificar_cotas_tt.py`, ambas perspectivas y cinco ventanas por perspectiva: **10 casos**, dos fallos reproducidos en el original y cero en el corregido. Las consultas amplias con tabla limpia coinciden con el oráculo exhaustivo. Se comprobó que búsquedas abortadas no escriban entradas. Tabla de 256 entradas para limitar memoria, con comparación de claves completas; no es medición de rendimiento.

Comando ligero ejecutado (sin compilación ni partidas):

```sh
rtk '/Users/josema/vs code/BreakthroughBotIA/.venv/bin/python' -B estudiantes/iacasitegano/herramientas/verificar_cotas_tt.py --baseline '/Users/josema/vs code/BreakthroughBotIA/estudiantes/iacasitegano/busqueda_eval3.py'
```

## Siguiente acción tras el A/A

**Avance con A/A cerrado:** se comprobó Docker sin contenedores activos y se ejecutó el arnés dentro de `torneo-bot-base:local`, 1 CPU/1024 MiB/sin red. Numba reproduce los dos fallos del baseline y el corregido pasa. Una segunda ejecución con `--jit --tt-bits 20 --extendido` (1,048,576 entradas) pasó **192 ventanas adicionales** y **15 raíces a profundidades 1–3** contra expectiminimax exhaustivo, además de los 10 casos originales. Incluye ataques, ambos turnos/objetivos, terminales, ausencia de jugadas, contrato de cotas y ausencia de mutación de entrada. Cero fallos del candidato. No mide frecuencia del bug en búsquedas habituales.

Se regeneró el caché únicamente de este worktree. `./torneo validar iacasitegano --entrega` pasó; avisos de carga dinámica en el entrenador y el arnés de pruebas, dentro de herramientas offline. Tres preparaciones frías en serie con 1 CPU: 3/3, máximo de importación+preparar **0.017623 s**. Logs en `resultados/medicion/tt_validacion_20261027/` del worktree TT.

Comprobación técnica completada, cuatro partidas con semilla `20261108`: **1–3, peones 8–10**; blancas 1–1/5–4, negras 0–2/3–6. Todas por puntos, salidas vacías, cero fallos técnicos; reloj propio máximo **16.655153 s**. Esta muestra no mide fuerza. JSON en `resultados/2026-10-27_22-47-44/` del worktree TT; resumen y protocolos en `resultados/medicion/tt_validacion_20261027/RESULTADOS.md`. No usar la semilla como confirmación reservada. Sigue sin integrar al principal o promover.

1. Ejecutar el mismo arnés con `--jit` en el entorno oficial; extender el diferencial a posiciones reales con ataques, terminales y transposiciones, a ventanas encontradas durante búsquedas desde la raíz y a distintos topes/abortos.
2. Estimar frecuencia del fallo en el buscador normal. Revisar además semántica Star1 antes de ampliar la TT a cotas LOWER/UPPER.
3. Regenerar caché, validar entrega y medir el costo de guardar menos entradas en ventana exclusiva.
4. Comparar fuerza bajo reloj oficial, victorias como métrica principal y peones anotados secundarios. No combinar con hojas hasta comprobar cada candidato por separado.

No se modificó el bot principal, no se usaron las semillas A/A ni las reservas y no hubo commit o promoción. Las pruebas compiladas y la integración técnica descritas arriba pasaron; quedan sin medir la frecuencia del fallo en las búsquedas normales y el costo/fuerza del cambio.
