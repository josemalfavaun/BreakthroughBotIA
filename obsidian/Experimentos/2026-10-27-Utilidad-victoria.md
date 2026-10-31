---
tipo: experimento
estado: tt-comun-numba-validado-protocolo-fijado
fecha: 2026-10-27
baseline_commit: 85b2d55
---

# Utilidad esperada de victoria en nodos de azar

## Hipótesis falsable

Los pesos activos son logísticos. El entrenador IRLS calcula `p=sigmoid(Xw)` y la validación usa esa probabilidad; el buscador actual devuelve el logit crudo `Xw` en las hojas y asigna a terminales `±(cota_eval3+100)`, aproximadamente ±420.790 con este NPZ. Promediar logits y terminales de esa escala no equivale a maximizar la probabilidad de victoria estimada.

Hipótesis: transformar hojas con `tanh(logit/2) = 2*sigmoid(logit)-1` y terminales ±1 da unidades coherentes de utilidad y podría mejorar decisiones de riesgo. Mantener coeficientes y todas las familias. No es una mejora demostrada: calibración/política de entrenamiento y costo de tanh pueden hacer que el candidato juegue peor.

## Procedencia recuperada

- Carpeta propia de laboratorio: `/Users/josema/vs code/BreakthroughBotIA-claude/estudiantes/iacasitegano_eval3/`.
- `herramientas/lab/entrenar_eval3.py`, función `logistica`: IRLS con sigmoide.
- `herramientas/lab/logistica_resultado.py`: objetivo de resultados de partida y `sigmoide(X @ w)` para logloss.
- El NPZ de esa carpeta coincide por SHA-256 con el integrado: `37678d0bd700c27a29d0084558158db1a65b01409dbf54828e89706441c2250b`; contiene `pesos`, `crudo`, `modelo=ligero5_solo_puntos_patrones_filas_marcador`.
- Contexto: `/Users/josema/noche_salida/lab/eval3_ligero_estado.md`. Falta reconstruir y portar la receta completa de la ablación final y sus datos; localizar el entrenador no cierra la reproducibilidad de entrega.

## Cambio aislado

Worktree `/Users/josema/.codex/worktrees/utilidad-victoria/BreakthroughBotIA`, separado desde `85b2d55`. `_evaluar_numba` transforma el score de eval3; `GANANCIA=1`. `eval3.py`, NPZ, libro, reparto y búsqueda no cambian. `cota_eval3` queda como diagnóstico de logits, sin fijar terminales. La hipótesis es específica del modelo logístico activo; no extrapolarla a pesos ridge antiguos.

## Verificación preliminar

`herramientas/verificar_utilidad_victoria.py`, motor/eval3 reales con JIT apagado: 10 hojas acotadas (incluye logits extremos), 4 terminales y 8 raíces a profundidades 1–2 contra expectiminimax exhaustivo independiente con la nueva utilidad; cero diferencias. Se verifica antisimetría, terminales ±1 y jugada óptima del oráculo en fixtures con azar. No prueba calibración ni rendimiento.

Ejemplo algebraico, **no partida ni probabilidad real demostrada**: una opción con 50% de victoria terminal y 50% de hoja logit −2 obtiene 209.395 en la escala anterior, frente a 3 de una hoja alternativa logit +3. Bajo la interpretación logística, probabilidades estimadas 55.96% frente a 95.26%; el candidato prefiere la segunda. Ilustra una posible inversión por unidades de utilidad.

Diagnóstico adicional: se reconstruyeron las dos primeras trazas del baseline `20261031`; en 7 posiciones (plies 15/30/45/60 disponibles), ambos buscadores a profundidad 1 eligieron lo mismo. Esa muestra vista y pequeña no muestra una mejora ni permite estimar la frecuencia del efecto. Los puntos finales reconstruidos coinciden con los JSON.

## Protocolo pendiente

**2026-10-28, estado vigente:** candidato ya incorpora exactamente la corrección TT del control. AST de búsqueda/raíz idéntico salvo escala de utilidad. SHA de búsqueda B `83997dd323509bbfc2edd92de46a81a3770a6f1d5603daa730352ed56303277e`. Python y Numba oficial: 10 hojas, 4 terminales, 12 raíces hasta prof. 3 y 72 reutilizaciones de TT, cero diferencias. Caché B regenerado; validador aprobado con aviso de timeout en prueba reducida a 3 s. Tres arranques fríos en serie, 1 CPU/1024 MiB, 3/3 y máximo importación+preparar 0.372181 s. Memoria pico sin medir.

Protocolo vigente [[2026-10-28-Protocolo-utilidad-victoria]]: 4 partidas técnicas previas y 160 de desarrollo (80 por versión), aún sin ejecutar. Evidencia técnica y comandos en `/Users/josema/.codex/worktrees/utilidad-victoria/BreakthroughBotIA/resultados/medicion/utilidad_victoria_20261028/VALIDACION.md`. El listado de abajo describe la etapa anterior, concretada ahora por ese protocolo. Sin cambios al principal ni promoción.

**Tras cierre A/A:** `verificar_utilidad_victoria.py --jit` pasó en la imagen oficial, 1 CPU/1024 MiB: 10 hojas acotadas, 4 terminales y 8 raíces contra el oráculo independiente, cero diferencias. Log en `/Users/josema/.codex/worktrees/tt-cotas-exactas/BreakthroughBotIA/resultados/medicion/tt_validacion_20261027/utilidad-victoria_numba.log`. No hay benchmark integral, caché regenerado de este candidato ni partidas de fuerza. Antes de A/B hay que fijar la misma TT corregida en ambos lados.

1. Esperar A/A y resolver primero [[Experimentos/2026-10-27-TT-exactitud]]. La TT debe ser idéntica y correcta en control/candidato al probar esta hipótesis; no atribuir diferencias de exactitud a la escala.
2. Verificar Numba y oráculo a mayor profundidad, terminales, azar y saturación. Regenerar caché y revisar costo total dentro del buscador; tanh añade trabajo, mientras cotas ±1 pueden cambiar cuánto poda Star1.
3. Congelar control, parámetros y muestras antes de partidas. Métrica primaria: victorias/puntos de liga; peones anotados y conversión de ventajas secundarios. Elegir muestra y parada con la información A/A, sin reutilizar semillas de ajuste como validación.
4. Desarrollo y confirmación con árbitro/límites oficiales, ambos colores, más de un rival propio y Montecarlo. Sin mejora repetida y sin estabilidad técnica, rechazar. No reajustar una temperatura tras mirar el conjunto reservado.

El modo `--jit` se ejecutó después del A/A como se indica arriba. No hubo partidas de este candidato, entrenamiento, promociones o commits. No se cambiaron fuentes o pesos del checkout principal.
