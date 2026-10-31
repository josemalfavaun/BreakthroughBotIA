---
tipo: ejecucion-offline
fecha: 2026-10-29
estado: preparacion-pendiente-en-escritorio
---

# Escritorio: preparación y lotes offline

Equipo declarado: Windows, i5 aproximadamente octava generación, 16 GB RAM, RX 570. No hay conexión de este chat al escritorio. Esta guía prepara el trabajo de fase 5 de [[07-Plan-definitivo]]. No es un entrenamiento ya iniciado.

## Preparación inicial por Jose

1. Encender el escritorio, conectarlo a corriente/red y desactivar el reposo automático durante el lote. Apagar pantalla sí permite trabajar; suspender Windows detiene el cómputo.
2. Seguir [instrucciones oficiales del curso para Windows](https://github.com/raya-lucaria/ia_o26_torneo_adversarial/blob/main/docs/empezar.md#windows-wsl2): `wsl --install` desde PowerShell administrador, reiniciar si lo solicita y crear usuario Ubuntu; Docker Desktop con integración Ubuntu. Para instalar Docker/WSL manualmente, comprobar requisitos del Windows concreto antes de proceder.
3. Abrir Ubuntu y trabajar bajo `/home/<usuario>/`, siguiendo el curso; conectar VS Code mediante WSL. No lanzar torneo desde PowerShell/Git Bash.
4. Clonar el repositorio propio dentro de Ubuntu. La copia remota puede no incluir cambios locales: transportar después un **paquete explícito de trabajo** con herramientas/datos seleccionados y manifiesto SHA-256. No hacer push solo para mover archivos. No transferir `.git`, credenciales o caché Numba de macOS como dependencia del lote.
5. Ejecutar el diagnóstico/instalación del curso en ese clon; validar Python y dependencias del laboratorio. Registrar CPU/RAM/SO/arquitectura/versiones. Inicialmente NumPy, SciPy, Numba; scikit-learn solo en entorno offline si la tarea lo necesita. No instalar soporte GPU para el plan inicial.

Si Codex se abre en el escritorio, su tarea inicial será **preparar y verificar este entorno**, no ejecutar de inmediato todo el calendario. Este chat no puede controlar una máquina simplemente porque esté encendida; hace falta una sesión allí o acceso explícito configurado.

## Paquete vigente — validación Linux del 29 de octubre

Usar ahora `resultados/medicion/fase5_mac_k8s_20261029/laboratorio_pc_validado_linux_20261029_v2.tar`,16,947,200bytes/236entradas, SHA `7475911a4e9e84f1ee4256f97fd68607530244dd5e20065bd133a1faf5e66f86`. Incorpora purga de estados nuevos contra replay/retención históricos. Ocho tests correctos en Mac/Linux; receta completa reproducida exactamente en Linux ARM64. Guía en [[estudiantes/iacasitegano/herramientas/pc/LEEME_PC]]. Windows/x86 sigue pendiente de piloto. Evidencia: [[resultados/medicion/fase5_mac_k8s_20261029/RESULTADOS]].

## Paquete anterior — primera preparación del 29 de octubre

**Histórico; sustituido por el anterior.** `resultados/medicion/infra_pc_20261029/laboratorio_pc_listo_20261029.tar`:16,936,960 bytes, SHA `a2b7602a8a15ff9d4af3797e0c9bac752eaf826fb36866c57f4c5f49b42e90fb`,234 entradas verificadas. Incluye lanzador CPU recuperable de1–4 procesos, rivales reforzados, retención y train/validation/test. [[estudiantes/iacasitegano/herramientas/pc/LEEME_PC]] contiene las órdenes exactas de instalación/piloto/lote/validación; también está en la raíz del tar.

No hace falta clonar Git para ejecutar este paquete aislado; no contiene credenciales ni cachés de Mac. En Windows todavía hay que comprobar WSL y dependencias. Pruebas hechas en Mac: siete tests, cuatro procesos arrancados/parados, dos partidas generadas/reanudadas con replay correcto y cadena de validación sintética. [[Validacion-y-laboratorio-PC]] enlaza evidencias. Un lote nuevo no se declara completo mientras queden partidas pendientes.

## Paquetes históricos conservados en el Mac

- **Histórico, sustituido por el paquete anterior:** `resultados/medicion/fase5_20261028/laboratorio_fase5_sesion.tar`, 10,844,160 bytes; SHA-256 `803f45a4a30b684c3caf8de15f88e41716ec6369461940ef27e3fe2faee10a27`. Motor público sin modificar, herramientas propias, receta activa, fuentes del profesor U, histórico y 60 episodios nuevos verificados. Extracción en Mac: 217 archivos coinciden con manifiesto. La receta activa también se ejecutó desde la extracción limpia en Mac: máximo error de pesos 1.78e-15 (`portabilidad_mac/RESULTADO.json`). No probado todavía en Windows.
- **Solo entrenamiento NumPy:** `paquete_entrenamiento_cpu_v2.tar`, 5,632,000 bytes; SHA `bd79a7a2b1fed6fbedacb19f1e9c3cabb4b8b0f0c5f267c79725bc6045a58089`; incluye receta recuperada, antiguo prior e histórico. El v1 queda como artefacto histórico.
- No contienen `.git`, credenciales, entornos ni cachés Numba. Se extraen en carpeta nueva, sin sobrescribir el repositorio activo. El laboratorio completo lleva `LEEME.md` y `verificar_paquete.py` con comandos relativos.
- Los episodios ya soportan presupuesto en minutos, checkpoint por ply y reanudación automática por replay, sin un flag `--reanudar`. El contrato congela fuentes, semillas y presupuestos; una diferencia aborta en lugar de mezclar datos.
- Reanudar los 60 ya completos solo los verifica/omite: **no es un nuevo entrenamiento de siete horas**. Primero comprobar entorno y reproducir la receta activa. Un lote nuevo requiere otra salida, semillas privadas y protocolo propios antes de generar; no ampliar a ciegas el conjunto que produjo el candidato oficial congelado.
- El candidato N fue rechazado (6/80 frente a43/80 de U). No reemplazar pesos con resultados del escritorio ni ajustar N tras ver sus partidas. El lote nuevo tiene otra hipótesis prospectiva, prior activo y retención histórica.

Al volver al Mac: transportar salidas, verificar hashes/esquema, revisar métricas offline y ejecutar allí la comparación oficial de A/B bajo condiciones iguales. No comparar A en Mac y B en escritorio como prueba de fuerza controlada.

## Piloto y asignación de recursos

Seguir los pilotos vigentes de LEEME_PC: diez minutos con dos trabajadores y luego cuatro en otra salida/semillas. Medir producción total y RAM; elegir por rendimiento observado; 16 GB no implica que sea conveniente lanzar un trabajo por hilo. Limitar hilos internos BLAS/Numba para evitar sobresuscripción cuando haya procesos múltiples.

El lote de 1 h sirve para paneles, ajustes sobre datos existentes y pruebas del GA. El de 7 h para etiquetado o evaluación recuperable. El de 24 h usa la misma cola por etapas/checkpoints, no una orden sin límites. Calcular volumen por costo medido y dejar tiempo para guardar checkpoints.

Si el escritorio mide partidas oficiales, reservar ventana sin entrenamiento; cada bot sigue con 1 CPU/1024 MB/30 s/10 s. Si solo genera etiquetas offline puede aprovechar más núcleos. Mantener ambas cargas separadas por host o por horario.

## Herramientas externas y producto final

| Herramienta | Trabajo offline | Qué viaja a la liga |
|---|---|---|
| NumPy/SciPy | Ridge, logística, métricas y cálculo | Pesos/arrays y evaluación actual compatible. |
| scikit-learn | Referencia de regresión, árbol o profesor de interacciones | Pesos/tablas o árbol pequeño exportado y documentado; no dependencia obligatoria. |
| OpenSpiel como referencia | Verificar diseño MCTS con azar; adaptar nuestro juego | Solo implementación propia/adaptada permitida y citada, si supera pruebas. |
| GA en NumPy | Ajuste acotado de tres multiplicadores, historia recuperable | Tres números y pesos derivados, sin población ni optimizador. |
| Búsqueda de alto presupuesto | Etiquetas por acción, finales exactos y contraste | Modelo/tablas/libro legal y reproducible. |

Las reglas permiten herramientas neuronales offline, pero entrenar una red desde cero no es requisito del primer lote. Evaluar primero si un profesor de búsqueda ya mejora los datos. El informe final distingue herramientas usadas para generar datos y algoritmo que realmente juega.

## Primer trabajo verificable en Windows

Copiar el tar completo, verificar su SHA-256, extraerlo bajo `/home/<usuario>/` y ejecutar `python verificar_paquete.py`. Registrar versiones de Python/NumPy/Numba, CPU/RAM/arquitectura y luego el comando de reproducción del modelo activo que aparece en `LEEME.md`. Debe guardar arrays y tolerancias sin sustituir pesos. La compilación de Numba se hace localmente. Para este primer trabajo no se necesita Docker ni GPU; Docker es necesario para posteriores partidas oficiales. No se afirma que el escritorio esté conectado o trabajando hasta ver su salida.

## Plan actualizado de cuatro procesos — 29 de octubre

[[Experimentos/2026-10-29-Revision-oficial-validacion-y-PC4]] especifica4 generadores offline, shards/semillas distintos, un hilo BLAS/Numba por trabajador y prueba2→4 antes de7h/24h. El nuevo lanzador de cuatro procesos está implementado y su arranque/parada se probó en Mac; faltan piloto y ejecución de producción en Windows. El paquete histórico sirve de base y prueba de receta; reanudar60 completos no entrena nada más. Árbitro oficial asigna2 CPU por partida y reserva2: necesita10 visibles para4 paralelas; con6 permite2, con8 permite3. No forzar4 mediciones cronometradas con cuatro CLI separados. Preferencia:PC genera datos y Mac valida en serie. Preparar entorno oficial actual en copia controlada: el ./torneo local aún difiere del del curso en comandos instalar/diagnostico/actualizar.
