#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)"
EQUIPO="$ROOT/estudiantes/iacasitegano"
DATOS="$EQUIPO/data"
CACHE="$DATOS/numba_cache"
TMP_BUILD="$(mktemp -d "$DATOS/.numba-cache-build.XXXXXX")"
SALIDA="$TMP_BUILD/cache"
NUEVO="$DATOS/.numba_cache.new.$$"
ANTERIOR="$DATOS/.numba_cache.old.$$"

limpiar() {
    if [ -d "$ANTERIOR" ] && [ ! -d "$CACHE" ]; then
        mv "$ANTERIOR" "$CACHE"
    fi
    rm -rf "$TMP_BUILD" "$NUEVO"
}
trap limpiar EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -m 777 "$SALIDA"
chmod 755 "$TMP_BUILD"
docker run --rm --cpus=1 --memory=1024m --memory-swap=1024m --network=none \
    -v "$EQUIPO:/bot:ro" \
    -v "$SALIDA:/tmp/numba:rw" \
    --entrypoint python torneo-bot-base:local \
    /bot/herramientas/cache_numba_build.py

test -n "$(find "$SALIDA" -type f \( -name '*.nbi' -o -name '*.nbc' \) -print -quit)"
rm -rf "$NUEVO"
mkdir "$NUEVO"
cp -R "$SALIDA/." "$NUEVO/"
if [ -d "$CACHE" ]; then
    mv "$CACHE" "$ANTERIOR"
fi
if mv "$NUEVO" "$CACHE"; then
    rm -rf "$ANTERIOR"
else
    if [ -d "$ANTERIOR" ]; then mv "$ANTERIOR" "$CACHE"; fi
    exit 1
fi
printf 'Caché Numba actualizado en %s\n' "$CACHE"
