---
tipo: experimento
estado: 8B2-tecnico-I0-pasado-fase8-global-abierta
fecha: 2026-10-29
baseline_commit: 85b2d55e9713bd993d874cfa050c60827580c92a
---

# 8B.2 — controles técnicos reales de I0

I0 con respaldo seleccionado explícitamente solo para técnica. Búsqueda cc888a3c, estrategia 88ce9d47, NPZ 37678d0b, libro 00fd209f; no S13/U/modelo amplio ni promoción. Principal/informe/caché y 17 fuentes de 5 intactos.

Regresión original extendida Python/JIT pasa (10+192 ventanas, 15 raíces por pase, dos fallos P reproducidos y cero corregidos). Linux ARM64, imagen 79983872…, Python 3.12.16/NumPy 2.4.6/Numba 0.67.0. Tres fríos sin caché propia: máximo 2.717s y 142.54MiB cgroup; JIT real dentro de preparar. No hizo falta añadir caché Linux/Mac. Prioridad/forzada/legales/equivalencia TT y fallback por aborto real en ambos colores comprobados.

Validador oficial entrega con 2 humos separado, 0 errores/avisos. Cuatro técnicas random, 2 por color, semilla 20261221 ahora consumida, 4–0 sin fallos propios/timeout/ilegalidad. Máximos de tanda: preparar 3.032s, reloj 14.375s, pico 143.36MiB. No prueba fuerza ni finalista; fase 8 global sigue abierta.

[Certificado y traspaso](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8B2_runtime_20261029/CIERRE_8B2.md>) · [Métricas](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8B2_runtime_20261029/metricas.csv>) · [Paquete técnico](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8B2_runtime_20261029/paquete_exportado_01/participante.tar>) · [Ventana terminada](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8B2_runtime_20261029/VENTANA_TECNICA_TERMINADA.json>).

Primera ventana rechazada por Spotlight, posteriores comprobadas sin carga ajena pesada; ningún servicio/GRIS/clúster detenido. Solo contenedores propios, sin limpieza global. Instrumentación cgroup al adios fuera del reloj; fuentes cargadas/SHA/co_filename reales. Ventana técnica terminada; puede coordinarse validación independiente de S13 después, sin iniciarla desde aquí. Pendientes selección deportiva/integración/informe final/otros modelos/arquitecturas. No notas globales ni examen9.
