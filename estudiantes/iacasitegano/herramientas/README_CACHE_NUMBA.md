# Caché Numba horneado para `iacasitegano`

El árbitro crea un contenedor nuevo por partida. Antes de `preparar`, el runner copia
el caché común del motor a `NUMBA_CACHE_DIR`; después monta el equipo como `/bot:ro`.
`strategy.preparar()` agrega a ese tmpfs los archivos de `data/numba_cache/`. Así el
código Numba del equipo carga sus firmas compiladas sin escribir en `data/`.

El caché es específico del entorno de la imagen `torneo-bot-base:local` (Linux,
arquitectura, Python, NumPy y Numba) y de las rutas `/bot/eval3.py` y
`/bot/busqueda_eval3.py`. No copies archivos de caché generados por Python/Numba del
host ni de otra arquitectura o imagen.

`data/numba_cache/manifest.json` guarda SHA-256 de `strategy.py`, `eval3.py`,
`busqueda_eval3.py` y `motor/nucleo.py`, además de versiones de Python, NumPy, Numba y
arquitectura. `preparar()` verifica esos datos antes de copiar.
Si el caché falta, está viejo o no corresponde al runtime, lo salta y deja que Numba
compile el código fuente actual. Ese respaldo protege la corrección si alguien olvida
regenerarlo; en ese caso se pierde la mejora de tiempo, no se reutiliza el caché viejo.

## Regeneración obligatoria

Regenera y vuelve a validar el caché después de cualquier cambio en `eval3.py`,
`busqueda_eval3.py`, `strategy.py`, `sistema/motor/nucleo.py`, las versiones de la
imagen base o las firmas que `busqueda_eval3.calentar()` compila. Desde la raíz del
repositorio, con Docker Desktop activo y la imagen real de la liga disponible:

```sh
./estudiantes/iacasitegano/herramientas/regenerar_cache_numba.sh
```

El script monta el código en `/bot`, usa `torneo-bot-base:local` con 1 CPU y 1024 MiB,
compila desde un directorio Numba vacío y deja archivos `.nbi/.nbc` de
`eval3`/`busqueda_eval3` más `manifest.json`. Reemplaza el directorio de caché de forma
reversible mientras instala el nuevo. Los archivos se incluyen en Git dentro de
`data/numba_cache/`.

En esta revisión de `integracion-tier1-2`, la búsqueda llama a
`eval3.evaluar_nb`; el nombre `evaluar_ligero_nb` del diagnóstico de laboratorio no
existe en esta revisión. El generador compila los dispatchers que realmente calienta
`busqueda_eval3.calentar()` en esta rama.

Después de regenerar, ejecuta la prueba de invalidación descrita en el cambio que
introduce una versión nueva de la caché y una partida oficial con Docker. Si la
versión del contenedor de liga cambia, reconstruye desde la imagen nueva antes de
medir: una caché incompatible solo debe causar recompilación, nunca cambiar la lógica.

Los kernels recursivos `_valor_numba` y `_quiescencia_numba` usan `@njit(cache=True)`
sin firma explícita para que Numba no los compile al importar `busqueda_eval3.py`: el
equipo no puede copiar su caché hasta `strategy.preparar()`. `busqueda_eval3.calentar()`
los compila o carga después de esa copia. No vuelvas a declararles una firma explícita
sin mover la copia antes de importar la estrategia en el runner.

## Verificación automatizada de `preparar()`

La prueba de regresión de una instancia fría verifica que importación + `preparar()`
terminen antes del límite de 10 s:

```sh
nice -n 19 python3 -B estudiantes/iacasitegano/herramientas/test_preparar_cache_docker.py
```

Después de regenerar el caché, desde la raíz ejecuta:

```sh
nice -n 19 python3 -B estudiantes/iacasitegano/herramientas/verificar_preparar_cache.py
```

Por defecto lanza 20 contenedores de prueba, en grupos de 7 concurrentes, cada uno con
0.5 CPU y 1024 MiB. El test monta el equipo exactamente en `/bot`, oculta el volumen
compartido del motor, verifica por el flujo oficial de `runner` y falla si alguna
preparación falla o si importación + `preparar()` llega a 10 s. Ajusta muestras con
`--repeticiones`, concurrencia con `--workers`, cuota con `--cpu` y el límite con
`--limite`. La salida incluye p50, p95 y máximo.
