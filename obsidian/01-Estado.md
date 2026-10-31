---
tipo: estado
proyecto: BreakthroughBotIA
actualizado: 2026-10-30T14:21:18-06:00
confianza: procesos-fuentes-y-pruebas-verificados
---

# Estado para retomar

**Fase 5: S13 pasó la validación NUEVA y las comprobaciones funcionales Python/Numba. 64/64 episodios terminados; fuentes y principal intactos. Todavía no hay modelo nuevo aceptado. Test256 y UCT nuevo sin evaluación; examen reservado, controles técnicos específicos y partidas oficiales pendientes. Seguimiento finalizado y automatización eliminada. 7A/8A/8B.1/8B.2 técnicas terminadas; fases 5/7/8/9 globales abiertas.**

## Dónde y qué preservar

Principal: `/Users/josema/vs code/BreakthroughBotIA`, rama `integracion-tier1-2`, HEAD `85b2d55`. El cwd de este chat puede ser el worktree `fase5-adaptacion`: contieneN rechazado, **no es entrega ni se copian sus pesos al principal**. Sin commit, merge, push o promoción autorizados.

P búsqueda SHA `ceba365326e5ba8dd102218843f2b92744738d9c8a18db000f9edbc188832b7f`; NPZ `37678d0bd700c27a29d0084558158db1a65b01409dbf54828e89706441c2250b`. Fuentes del lote verificadas intactas; preservar cambios existentes. P sigue sin la corrección TT deA, pendiente de8.

**GRIS deshabilitado persistentemente por Jose.** No reactivarlo con los wrappers antiguos de pausa. Evidencia/recuperación: `resultados/medicion/gris_pausa_persistente_20261029/LEEME.md`.

## Corrida UCT de 14 horas preparada

En ejecución: [[Experimentos/2026-10-30-UCT14h]]. El último Job observado es `uct14h-6a3e0894`, con 8/8 pods `Running`. El controlador `estudiantes/iacasitegano/herramientas/fase5_uct14h_controller.py` orquesta UCT4096 exclusivamente, registra decisiones y, al completar 840 minutos, ejecuta ajuste/validación interna en una salida nueva. No sustituye pesos ni abre test o liga. Los resultados vivos permanecen ignorados por Git; al cierre se añadirá un resumen reproducible.

## Fase5 en curso

Fuente final: [[resultados/medicion/fase5_lote256_mac_20261029/RESULTADOS]], métricas primarias en`validacion/seleccion_replay/RESULTADO.json`, hashes en`AUDITORIA_CIERRE.json`.256/256episodios,4salidas0,replay sin errores,128grupos; fuentes/NPZ principal intactos. No procesos propios del lote pendientes según finalización/locks; confirmar estado antes de otra carga.

- Ajuste λ100centrado en activo, replay80/20, ejecutado según contrato.72train/24validación/32testUCT por grupos; purga registrada. CandidatoSHA`d5a28046e5790d47e406e3e0397fb717cf9eb2b305c2b8c54b18b10293a00c64` **rechazado**. No copiarlo al principal ni generar libro con sus pesos.
- Brier igual peso por grupo: validación0.14348033→0.13465573(mejora0.00882460); retención0.17400779→0.18057672(empeora0.00656894>máximo0.005). Logloss validación mejora, retención empeora. Cobertura/grupos/colores de validación pasan; retención falla. No es prueba de fuerza.
- TestUCTNOevaluado y sin EXAMEN/EXAMEN_ABIERTO; no abrirlo para investigar el rechazo. Sin entrenamiento extra automático ni rescates. El diagnóstico posterior y S13 están documentados más abajo; no rescatar el candidato amplio ni barrer parámetros para pasar las mismas puertas.
- Preparación funcional/protocolo deportivo de [[resultados/medicion/fase5_postseleccion_20261029/LEEME]] quedan condicionados a otro candidato apto. No ejecutar para este rechazo ni gastar20261211–16. Esas semillas permanecen reservadas; no se jugó U/Vnuevo.
- Reanudación de casa concluyó correctamente; supervisor terminó sin reinicio, no necesitó60minextra. Pausas/órdenes previas son históricas. Seguimiento de este lote terminado; automatización eliminada y confirmada por la app. No iniciar otra sesión por leer un estado anterior.

## Fases y coordinación

**0–4 y6cerradas;5,7,8,9abiertas.** [[07-Plan-definitivo]] conserva contratos. Fase2 certificada cerrada/rechazada:139checks,600pares/1200búsquedas, ratio0.982591>0.95, diferencia de valor0. [[resultados/medicion/cierre_fase2_20261029/CIERRE]]. No repetir. ParcheTT P→A no aplicado; conservar regresiones y validar integración8.

Fase6cerrada por rechazo de tablas/ampliación examinadas:890trazas,36,730raíces/35,094estados únicos,0errores; dominios pequeños/≤6peones sin cobertura,25carreras privadas ya con victoria segura inmediata. [[resultados/medicion/fase6_cobertura_20261029/CIERRE]]. Sin candidato ni mejora de fuerza. Hoja interna sin medir; no reabrir otro dominio sin hipótesis propia.

7A terminada: [[resultados/medicion/fase7A_aperturas_20261029/CIERRE_7A]]. Manifiesto, herramientas, protocolos y nota verificados por SHA;35 regresiones registradas.890trazas,470 apariciones potenciales de solo3claves/estados únicos, legales;455blancas/15negras. No es fuerza ni activación real histórica. Generador experimental listo;7Bespera modelo y ventana exclusiva. Riesgo reproducido: libro puede preceder victoria segura; ningún conflicto observado en las coincidencias actuales.

8A completada y revisada: [[resultados/medicion/fase8A_preintegracion_20261029/CIERRE_8A]]. Catálogo íntegro verificado; TT_A idéntica a A, dos controles negativos P reproducidos,0fallos corregidos,20llamadas de prioridad de libro; sin composición ni validación compilada/oficial. Principal intacto.

8B.1terminada/revisada: [[resultados/medicion/fase8B1_paquete_20261029/CIERRE_8B1]], catálogo60artefactos sin discrepancia. I0compuesto exacto,paquete8archivos/74599bytes,4fixtures y estático0errores/avisos, constructor reproducible. En ese hito estático no se habían aprobado JIT/humo/ABI/costo; el cierre técnico posterior 8B.2 se describe a continuación.

8B.2técnico completado/revisado: [[resultados/medicion/fase8B2_runtime_20261029/CIERRE_8B2]],169artefactos SHA sin discrepancias. I0con respaldo:Python/JIT/oráculo y LinuxARM64,3fríosmáx2.717s/142.54MiB; humo2y4técnicasrandomseparados,sin fallos. Tanda4máxpreparar3.032s/reloj14.375s/pico143.36MiB;20261221CONSUMIDA. Sin caché de participante necesaria, sin promoción/fuerza/fase8global cerrada. No certificar S13por estos resultados.

Ventana8B.2terminada21:11:23y comprobada sin procesos de cálculo ni contenedores propios/pesados antes de arrancarS13. [[resultados/medicion/fase5_validacion_S13_64_20261029/LIBERACION_8B2.json]].

Diagnóstico256: [[resultados/medicion/fase5_diagnostico_replay256_20261029/RESULTADOS]]. El amplio mejora replay pero falla82/126grupos retenidos; convergencia numérica correcta. Atribución descriptiva apunta patrones, sin demostrar causalidad.

Nueva S13: [[resultados/medicion/fase5_subespacio13_20261029/RESULTADOS]], protocolo previo, patrones congelados/13coeficientes libres,λ100/replay80/20,UNAejecución. SHAaba46e5595e442473ce5672abd5a6c3141e153761110e90600075b0e1300227d. Desarrollo visto mejora0.00214487Brier,retención+0.00032692; todo el filtro de desarrollo pasa, NOaceptación ni confirmación. Validación nueva completada; procedimiento: [[resultados/medicion/fase5_validacion_S13_64_20261029/LEEME]]. Semillas98–101millones+0..7auditadas en19worktrees INCLUYENDOignorados,12666archivos/321.8MB,0usosdetectados/0errores; referencias propias son propuestas/fixtures. Primera auditoría incompleta archivada y contrato recongelado ANTES de datos, sin cambiar muestra/modelo/puertas. Contrato finalSHA2ebabfced12603ad9c22e63c819a8f30d7143fd02a522702e59fd0c8ec38c343,24fuentes congeladas; no editar scripts/inputs.

Nuevo controlador pc/validar_s13_nuevo.py:4×16episodios,90minmáximos,sin reintento automático;24grupos MC/agresivo/carrera para validación,8UCTnuevos sin evaluar modelos. Purga contra cuatro conjuntos viejos vistos y entre familias, cobertura publicada antes de evaluar,flagUNAexposición. Cinco regresiones funcionales pasan, incluido canarioUCTno parseable y guardia de liberación. No se abrió test256 ni se reentrenaS13.

**Validación nueva S13 finalizada el 30/oct a las 04:26:18; auditada 2026-10-30T14:21:18-06:00.** [[resultados/medicion/fase5_validacion_S13_64_20261029/RESULTADOS]]:64/64episodios,4salidas0,sin interrupción.4512filas/24gruposMC-agresivo-carrera después de purgar225filas;8gruposUCTnuevos reservados sin evaluar. Brier con igual peso por grupo0.13163538→0.12574267(mejora0.00589271>mínimo0.002);logloss0.40312045→0.39003946. Blancas0.13395562→0.12795232,negras0.12925341→0.12347201; cobertura y todas las puertas pasan. Inicio empeora ligeramente+0.00039721; no retocar modelo con esta información.

Comprobaciones funcionales posteriores SOLO en48estados del piloto histórico visto:288comparacionesPython+288Numba correctas, error logit5.33e-15/utilidad4.44e-16. NPZS13aba46e55yU83997dd3fijos, salidas nuevas funcional_python.json/funcional_numba.json. AUDITORIA_CIERRE.json verifica24fuentesactuales+17del256,contrato/datos/modelo/64paresporSHA y principal intacto. La generación conservó90minmonotónicos y fue demorada por suspensiones de tapa ya documentadas; sin ampliación ni reinicio. Procesos de generación terminados; no reiniciar el flujo. Seguimiento `validar-s13-despu-s-de-controles-t-cnicos` eliminado con confirmación de la app al concluir; sin alertas pendientes.

**Próximo paso5:** fijar un protocolo de examen reservado para S13 sin usarlo para ajuste, después controles técnicos del candidato concreto y comparación deportiva oficial prefijada. NOtest256/UCTnuevoabierto, NOliga ni promoción ejecutadas. Este seguimiento autorizaba validación y equivalencia funcional solamente. I0certificado8B.2lleva otros pesos y no certificaS13. Fase5sigue abierta.

Diagnóstico5B adicional: [[resultados/medicion/fase5_cotas_tacticas_20261029/RESULTADOS]]. Oráculo racional independiente del modelo,8tardíos ya vistos, horizonte3y desconocidos[-1,1];0dominancias demostradas,3observadas óptimas por valor1,5sin resolver. Cinco regresiones correctas. No prueba ausencia de errores ni usa test nuevo; modelo/receta en curso intactos.

## Evidencia previa que no se reabre

- N rechazado:6/80 frente aU43/80 contraMC; cero fallos propios observados. U es utilidad/TTcorregida, noP. [[resultados/medicion/fase5_oficial_20261028/RESULTADOS]]. No reentrenarN para rescatarlo.
- Receta activa reproducida, histórico77038auditado; ridge/GA/simetría con decisiones de rechazo, profesor contrafactual antiguo sin cobertura suficiente. [[Experimentos/2026-10-28-Fase5-datos-modelos]]. Diagnóstico de transferencia: [[Experimentos/2026-10-29-Diagnostico-transferencia-y-proximo-ajuste]].
- Piloto real16episodios/1495filas,8grupos, replay correcto; partición3/3/2insuficiente, ya inspeccionado como desarrollo. No usarlo como examen. Prof7solo74/750decisiones. [[resultados/medicion/fase5_mac_k8s_20261029/RESULTADOS]].
- P contra random20–0,10por color; no demuestra superarMC/tiers. `resultados/medicion/random_principal_20261029/RESULTADOS.md`; semilla20261201ya usada.
- No tocar reservas20261102–04/11–14; confirmaciónN cancelada19/20/21 sin ejecutar. Semilla20261221consumida por4técnicasI0el29/oct; no reutilizar.

## Docker y escritorio

Integrado Docker Desktop activo,kind1nodo1.31.1,Ready,4tareasSucceeded. Contexto `docker-desktop`; cliente compatible privado `$HOME/.kube/bin/kubectl-desktop`. Clúster externo anterior detenido/conservado. [[resultados/medicion/docker_integrado_20261029/LEEME]]. Exportar antes de operaciones que borren recursos; no reactivarGRIS.

Windows no conectado/probado. Paquete base236entradas en `resultados/medicion/fase5_mac_k8s_20261029/laboratorio_pc_validado_linux_20261029_v2.tar`, SHA `7475911a4e9e84f1ee4256f97fd68607530244dd5e20065bd133a1faf5e66f86`. [[08-Escritorio-y-entrenamiento]]. Los nuevos controladores son del flujoMac/principal; no presuponer que el paquete anterior los incluye.

Detalle anterior archivado: [[Archivo/2026-10-29-Estado-antes-continuacion-automatica]]. Leer solo si hace falta.
