---
tipo: protocolo
fecha: 2026-10-28
estado: completo-candidato-rechazado
---

# Modelo adaptado: validación técnica y fuerza pendiente

## Hipótesis y controles

¿Actualizar el modelo con resultados de rivales diversos, regularizando hacia el modelo activo, aumenta victorias con la misma búsqueda? La escala, TT, libro, reloj y heurísticas serán idénticos entre U y N.

- **U, control de aprendizaje:** `/Users/josema/.codex/worktrees/utilidad-victoria/BreakthroughBotIA`. Búsqueda utilidad/TT corregida SHA `83997dd323509bbfc2edd92de46a81a3770a6f1d5603daa730352ed56303277e`; NPZ original SHA `37678d0bd700c27a29d0084558158db1a65b01409dbf54828e89706441c2250b`.
- **N, modelo nuevo:** `/Users/josema/.codex/worktrees/fase5-adaptacion/BreakthroughBotIA`. Misma búsqueda SHA `83997dd323509bbfc2edd92de46a81a3770a6f1d5603daa730352ed56303277e`; NPZ SHA `ab1a599270424a40ff323dceb3aad3b2358a9ff87979f72db0721ad1fd5b3718`.
- **P, referencia desplegada:** principal `integracion-tier1-2`/`85b2d55`, búsqueda SHA `ceba365326e5ba8dd102218843f2b92744738d9c8a18db000f9edbc188832b7f`. No es el control directo de este experimento: difiere en TT y escala. Se requiere comparación final contra P antes de promoción.

U no fue promovido por el experimento anterior de utilidad (+7 frente a +8). Aquí sirve como control fijo para aislar el nuevo aprendizaje. No se amplía aquella serie, no se cambian sus criterios y no se gastan sus reservas. Ganar a U no demostraría por sí solo superar a P.

Entrenamiento registrado en `resultados/medicion/fase5_20261028/adaptacion_nueva/` del principal. Datos: 60 episodios privados, 6,417 posiciones, UCT reservado del ajuste; λ100 y reglas fijadas antes de entrenar. Selección: solo dos grupos; prueba UCT: nueve grupos. Son filtros offline limitados. Candidato congelado; sin simetría, GA, nuevos rasgos ni otra mezcla.

## Puerta técnica obligatoria

1. Comprobar trabajo ajeno y reservar CPU; no pausar aplicaciones sin autorización.
2. Confirmar las rutas/hashes, libro y tiempo idénticos. Guardar manifiestos de TODO el participante, rival, imágenes y montajes efectivos. Las etiquetas compartidas de Docker no bastan para identificar variante.
3. **Caché de N pendiente de regenerar/verificar:** la preparación copió U para preservar su fuente; no asumir que el caché anterior valida el modelo nuevo. Utilizar el procedimiento de caché existente, sin tocar U ni P. Registrar hashes finales antes del primer juego.
4. Contrastar las nuevas hojas con `tanh(dot(features, w)/2)`, terminales ±1 y raíces pequeñas contra oráculo independiente, con Numba y motor oficiales. Validar NPZ, finitud, banderas, legalidad y aborto.
5. Validador de entrega y tres preparaciones frías por variante, imagen oficial, 1 CPU/1024 MiB, importación+preparar <10 s. Si se reutiliza evidencia de U, comprobar identidad exacta y declarar origen. Medir memoria pico cuando se disponga de instrumentación; no inventar preparación por partida.
6. Cuatro partidas técnicas N–Montecarlo, ambos colores, semilla propuesta **20261118**, límites oficiales 30 s/10 s/1 CPU/1024 MiB. Un fallo propio detiene la serie y se conserva. No se usan para fuerza.

Antes de usar 20261116/17/18 verificar que no existan juegos anteriores con esas semillas; si están usadas, escoger y documentar reemplazos sin ver resultados. **No usar 20261102–04 ni 20261111–14.**

## Desarrollo fijo: 160 partidas

| Orden | Variante | Semilla propuesta | Partidas |
|---|---|---:|---:|
| 1 | U | 20261116 | 40 |
| 2 | N | 20261116 | 40 |
| 3 | N | 20261117 | 40 |
| 4 | U | 20261117 | 40 |

Comando desde cada worktree: `rtk env TORNEO_SIMULTANEAS=1 ./torneo jugar iacasitegano montecarlo --partidas 40 --semilla SEMILLA -v`.

Primaria: victorias. Pasa desarrollo si N obtiene ≥8 victorias adicionales sobre 80 por versión, N >40/80, ninguna semilla con diferencia negativa y cero fallos propios. Filtro práctico fijado ahora; no es significancia estadística. Reportar color/semilla, puntos secundarios, motivos, importación/preparación, reloj y memoria medida. No rescatar con peones un fallo en victorias.

Sin entrenamiento/carga pesada concurrente, sin parada por ventaja ni ampliación por resultado estrecho. Interrupción externa conserva bloque excluido y lo repite completo, con motivo previo; fallos del bot cuentan. Si Jose debe cerrar la laptop, guardar progreso y detener antes de otro bloque. No atravesar reposo ni duplicar JSON.

## Confirmación y decisión

Reservas propuestas **20261119/20**, sin ejecutar: primero verificar historial y fijar por escrito un protocolo independiente de confirmación, rivales adicionales y comparación con P. No promover ni aceptar un porcentaje aislado. Si no pasa desarrollo, conservar base y cerrar esta versión; no retocar λ ni modelo con las reservas.

Estado al preparar esta nota: **cero partidas oficiales nuevas**, caché/Numba/preparaciones/validator de N pendientes. Sin commit, merge, push ni promoción.

## Ejecución iniciada — 2026-10-28 23:15

Caché N regenerado: 30 archivos/1,211,696 bytes. Oráculo Numba oficial: 10 hojas, 4 terminales, 12 raíces, 72 reutilizaciones de TT, cero diferencias. Ambas versiones pasan entrega y tres arranques fríos; N máximo 0.062996625 s. Evidencia nueva, sin reutilizar arranques de U. Las advertencias del validador son sobre importación dinámica en herramientas offline; deben revisarse al empaquetar la entrega.

Ejecutor único de este chat: `resultados/medicion/fase5_oficial_20261028/ejecutar.py`. A en el ejecutor significa U; B significa N. `manifiesto.json` congela participantes completos/rival/sistema/imágenes y `comprobacion_semillas.json` confirma cero conflictos. `progreso.json` es la autoridad del avance; `analizar.py` recalcula solo bloques completos desde JSON canónicos y verifica sus hashes. Las frases iniciales sobre caché o pruebas pendientes son el protocolo prospectivo conservado.

## Confirmación condicional fijada antes de jugar el primer desarrollo N

Ver [[2026-10-29-Protocolo-confirmacion-modelo]]. Solo si N pasa U/N: comparación independiente P/N, 80 por versión, seeds20261119/20, cuatro técnicas21; mismo filtro práctico, sin ampliación ni ajustes. Al redactar, el control U seguía en su primer bloque y N no había empezado desarrollo. Las reservas antiguas permanecen intactas. No ejecutado todavía.

## Cierre — 29 de octubre 01:00

U43/80 y N6/80; diferencias N−U por semilla −16/−21. No pasa.164 válidas (160 desarrollo+4 técnicas), cero fallos propios;23 excluidas por interferencia externa conservadas.328 inspecciones de contenedores, fuentes/pesos congelados sin cambios y principal intacto. GRIS restaurado. La confirmación condicionada no se ejecuta. `VERIFICACION_FINAL.json`, `RESPALDO_VERIFICADO.json` y `RESULTADOS.md` en la carpeta oficial nueva documentan el cierre. [[2026-10-29-Diagnostico-transferencia-y-proximo-ajuste]].
