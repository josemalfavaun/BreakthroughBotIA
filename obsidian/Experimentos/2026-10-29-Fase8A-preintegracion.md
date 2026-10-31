---
tipo: experimento
estado: preparacion-8A-completa-integracion-8B-pendiente
fecha: 2026-10-29
baseline_commit: 85b2d55e9713bd993d874cfa050c60827580c92a
---

# Fase 8A — correcciones independientes en copias

8A preparada, fase 8 abierta. Principal/runtime/caché intactos; no selección de modelo ni mejora deportiva declarada.

- Copia TT_A: parche original SHA 38591003…, fuente idéntica byte a byte a A cc888a3c. P reproduce los dos errores originales ±210.20324999290867 frente a oráculo≈0. Copia corregida pasa 10 ventanas originales, 6 fronteras/interiores, 4 abortos y 6 terminales sin TT/poda en el oráculo. Suite extendida/JIT pendiente.
- Copia PRIORIDAD_LIBRO: solo mueve victoria garantizada antes del libro legal; conserva búsqueda P. 20 llamadas verificadas en ambos colores, con ataque/fracaso, victoria no segura, libro legal/ilegal, fallback simulado y forzada. Globals restaurados, sin preparar/calentar.
- Rutas absolutas/SHA/co_filename reales guardados; 17 fuentes congeladas de 5 y 30 archivos de caché principal verificados antes/después. Sin test nuevo, N, liga, benchmark, JIT, generación masiva, commits o promoción. Las fases 2/6 no se reabren; 7B sigue pendiente.

[Certificado y traspaso](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8A_preintegracion_20261029/CIERRE_8A.md>) · [TT](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8A_preintegracion_20261029/TT_FUNCIONAL.json>) · [Libro](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8A_preintegracion_20261029/LIBRO_FUNCIONAL.json>) · [Checklist 8B y comandos pendientes](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8A_preintegracion_20261029/CHECKLIST_8B.md>) · [Reproducción](</Users/josema/vs code/BreakthroughBotIA/resultados/medicion/fase8A_preintegracion_20261029/LEEME.md>).

8B: recibir decisión real de 5, revisar composición (no aplicar TT dos veces si buscador ya corregido), conservar U/V de 5 con mismas fuentes/libro, validar Linux/ABI/caché/frío/seguridad/costo/tamaño y protocolo contra P/control corregido en ventana exclusiva. No integrar desde este encargo ni editar notas globales.
