---
tipo: procedimiento
actualizado: 2026-10-29
estado: implementado-PC-pendiente
---

# Validación 5V y laboratorio PC

Jose autorizó implementar validación y preparar el escritorio. **Herramientas implementadas y probadas en Mac; escritorio aún sin conectar/probar. Fase 5 sigue abierta.** No se cambió el modelo activo ni se rescata N.

Fuente y evidencias: [[resultados/medicion/infra_pc_20261029/LEEME]]. Comandos completos: [[estudiantes/iacasitegano/herramientas/pc/LEEME_PC]]. Paquete actual: `resultados/medicion/infra_pc_20261029/laboratorio_pc_listo_20261029.tar`, SHA `a2b7602a8a15ff9d4af3797e0c9bac752eaf826fb36866c57f4c5f49b42e90fb`, 234 archivos verificados.

## Orden obligatorio

1. Diagnosticar Windows/WSL, instalar entorno CPU y reproducir activo. Pilotos de diez minutos con 2 y 4 trabajadores: elegir por rendimiento/RAM reales, no suponer aceleración.
2. Generar lote nuevo recuperable, cuatro familias, ambos colores; propuesta 4×64=256 episodios. Presupuesto 60/420/1440 minutos por sesión, mismas fuentes/salida/semillas para reanudar. No mezclar entrenamiento con medición oficial en el mismo host.
3. Verificar todos los episodios con replay independiente. Preparar train/validation/test por grupos completos; reservar UCT entero para test, otros grupos75/25 y purgar estados/espejos cruzados. Publicar proporciones reales: no prometer80/20 ni CV implementada.
4. Congelar datos, representación, entrenador, base y umbrales. Hipótesis nueva: logística λ100 centrada en activo con replay80%histórico/20%nuevo; entrenar solo con train/replay.
5. Seleccionar con Brier/logloss, mínimo de grupos y controles por color/fase; exigir retención histórica. Máximo dos candidatos. Datos históricos vistos no se llaman test independiente.
6. Abrir test una sola vez para el elegido que pase; no ajustar después. Si pasa, controles técnicos/costo y protocolo de partidas oficiales NUEVAS antes de aceptar. Fase9 permanece como examen final del candidato integrado.

Pruebas Mac: siete tests, cadena sintética completa, N archivado rechazado sin abrir test, cuatro procesos arrancados/parados y dos episodios reanudados con183 filas de replay correcto. Son pruebas de funcionamiento. No hay un entrenamiento nuevo aceptado ni evidencia de mejora deportiva en esta sesión.

## Kubernetes

Mac: kubectl1.37.2/kind0.33.0, clúster independiente1.37.0, cuatro tareas verificadas. Detenido y sin reinicio automático para liberar recursos; configuración privada en home, fuera del repositorio. La cola CPU del paquete no necesita Kubernetes, Docker ni GPU. Docker/árbitro se usarán después para partidas oficiales. Instrucciones y evidencias en la fuente anterior.

## Retomar

Seguir [[08-Escritorio-y-entrenamiento]] y LEEME_PC al conectar la PC. No ejecutar de nuevo N/U ni reservas20261102–04/11–14; confirmación cancelada19/20/21 permanece intacta. No reactivar GRIS con antiguos wrappers. Codex puede preparar cobertura de fase6 sin alterar el bot ni medir con otra carga pesada.

## Corrección y pruebas Linux posteriores — 29/oct

Vigente: [[resultados/medicion/fase5_mac_k8s_20261029/RESULTADOS]]. Nuevo paquete `laboratorio_pc_validado_linux_20261029_v2.tar`, SHA `7475911a4e9e84f1ee4256f97fd68607530244dd5e20065bd133a1faf5e66f86`,236entradas. Sustituye el paquete inicial enlazado arriba, que queda como historial.

Ahora también se purgan estados de validation/test presentes en replay o retención históricos y del entrenamiento nuevo presentes en retención. El contrato informa descartes. Ocho tests de validación y seis de modelos correctos en Linux; receta histórica completa exacta,8episodios funcionales/776filas y60históricos/6417filas con replay correcto. Un fallo de almacenamiento del arnés y su cancelación asociada se conservaron; reintentos2/3 correctos con mismos presupuestos. No usar las partidas funcionales para entrenar ni afirmar mejora de fuerza.

Piloto Mac separado con presupuestos de producción, dos trabajadores,2minutos por sesión; fuentes/progreso/resultados en la carpeta anterior. Revisar estado real antes de seguir. Kubernetes detenido tras exportar; Windows sigue pendiente, modelo activo intacto.

Piloto real Mac completado:16episodios/1495filas y replay correcto. Grupos3/3/2no alcanzan mínimos de5V; se inspeccionó como desarrollo y no se entrena con él. Profundidad real4/5/6/7=23/448/205/74; no profesor7universal. Calibración descriptiva en fuente, con2grupos por rival. `PILOTO_MAC_CIERRE.json` sustituye los estados intermedios; procesos terminados y Kubernetes detenido.
