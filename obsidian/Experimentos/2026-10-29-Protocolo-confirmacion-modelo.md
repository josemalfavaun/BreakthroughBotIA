---
tipo: protocolo-condicional
fecha_redaccion: 2026-10-28T23:53:55.638687-06:00
estado: no-ejecutado-condicion-de-entrada-incumplida
---

# Confirmación del modelo adaptado contra el principal

Se fija durante el primer bloque U del desarrollo de fase 5, antes de jugar el primer bloque de desarrollo N. No modifica ni amplía la serie U/N. Solo se ejecuta si N supera todos los criterios prefijados de `2026-10-28-Protocolo-modelo-adaptado`. Si falla, este protocolo no se ejecuta y sus semillas permanecen sin usar. Es trabajo autorizado de validación de fase 5; no implica commit, integración ni promoción automática.

## Pregunta y versiones

¿La combinación N, con pesos nuevos, TT corregida y utilidad acotada, supera al participante P que sigue desplegado? Esta comparación evalúa el paquete completo, no atribuye por sí sola el efecto al modelo. El experimento anterior U/N aísla el aprendizaje.

- P: principal en `integracion-tier1-2`/`85b2d55`, búsqueda SHA `ceba365326e5ba8dd102218843f2b92744738d9c8a18db000f9edbc188832b7f`, modelo `37678d0bd700c27a29d0084558158db1a65b01409dbf54828e89706441c2250b`.
- N: `/Users/josema/.codex/worktrees/fase5-adaptacion/BreakthroughBotIA`, búsqueda `83997dd323509bbfc2edd92de46a81a3770a6f1d5603daa730352ed56303277e`, modelo `ab1a599270424a40ff323dceb3aad3b2358a9ff87979f72db0721ad1fd5b3718`.
- Rival: Montecarlo oficial idéntico al del desarrollo, fuente y motor congelados. No cambiar libro, reloj, features, pesos ni caches entre bloques; cache técnico compatible sí puede regenerarse antes del manifiesto inicial.

## Puerta técnica y ejecución

Comprobar que 20261119/20/21 no se han usado en juegos; guardar resultado del escaneo y detener ante conflicto, sin reemplazar silenciosamente. No usar 20261102–04 ni 20261111–14. Congelar participantes completos, rival, sistema, límites e IDs de imágenes, con archivos de respaldo. Fuente P verificada antes de arrancar: el principal puede tener herramientas/documentos locales, pero las fuentes de juego y pesos deben coincidir con el control especificado.

Tres preparaciones frías nuevas y validador de entrega por versión. Cuatro técnicas N seed20261121, fuera de fuerza; cero fallos propios para seguir. Fuente/caché de N y oráculo oficial ya validados: registrar su identidad y procedencia, no presentarlos como prueba nueva de fuerza. Preparar <10 s, reloj 30 s, 1 CPU, 1024 MiB, red desactivada y montaje solo lectura. Registrar consumo medido si se dispone; memoria límite no equivale a pico medido.

Serie fija de desarrollo independiente/confirmación: **160 partidas, 80 por versión**, orden:

| Orden | Versión | Semilla | Partidas |
|---|---|---:|---:|
| 1 | P | 20261119 | 40 |
| 2 | N | 20261119 | 40 |
| 3 | N | 20261120 | 40 |
| 4 | P | 20261120 | 40 |

Cada bloque contiene 20 por color. Un solo árbitro concurrente, sin entrenamiento ni carga pesada externa en el host. GRIS solo puede pausarse temporalmente con la autorización ya dada y debe restaurarse al terminar o ante interrupción; cualquier pausa se registra. Si vuelve a usarse después de la primera serie, registrar una pausa nueva y comprobar identidad. La autorización no se extiende a otras aplicaciones.

Conservar cualquier bloque interrumpido por infraestructura y repetirlo entero solo tras documentar el motivo externo. Los fallos propios cuentan. No parar por ventaja ni ampliar por resultado estrecho; no elegir otra lambda, temperatura o genoma tras ver esta serie.

## Decisión fijada

Primaria: victorias. Pasa esta confirmación si N suma ≥8 victorias más que P sobre 80 por versión, N >40/80, ninguna semilla con diferencia negativa y cero fallos propios observados, con límites/identidad comprobados. Es un filtro práctico de selección, no significancia estadística. Publicar ambos colores/semillas, razones, puntos secundarios, relojes y arranques, además de incertidumbre por grupos. No compensar con peones un filtro fallido en victorias.

Si falla, no promover N, conservar P y cerrar esta adaptación sin rescatarla con más ajustes sobre las mismas reservas. Si pasa, N queda como finalista confirmado frente a P **para este rival y entorno**, sujeto a integración/entrega y examen de generalización de fases 8/9. El estudio de otras familias sigue obligatorio en el examen final; este resultado no demuestra ganar a MCTS fuertes, redes ni Tier 5. El libro de fase 7 se estudia después de elegir el modelo; modificarlo exige nuevos hashes y pruebas.

Evidencia prevista: `resultados/medicion/fase5_confirmacion_20261029/`. El ejecutor/analizador se prepararán únicamente si pasa U/N. No se han ejecutado estas semillas al redactar.

## Condición de entrada incumplida — 29 de octubre

N terminó desarrollo 6/80, 3/40 por semilla; U ya obtuvo 19/40 en la primera, y queda su último bloque. La condición de no retroceder por semilla ya es imposible. Este protocolo **no se ejecuta**; 20261119/20/21 permanecen sin uso en esta sesión. No se ajusta el modelo para rescatarlo. El informe definitivo del desarrollo se publica tras completar sus 160 partidas.
