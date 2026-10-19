#!/usr/bin/env bash
# Huella (etiqueta `torneo.fuente`) del código que va dentro de cada imagen del torneo.
# La usan ./torneo (para saber si una imagen está al día) e imagen-base.yml (la pone como
# etiqueta al publicar), así ambos la calculan exactamente igual.
#
#   sistema/herramientas/huella.sh bot   # imagen de bots: sistema/ horneado (sin tests ni cachés)
#   sistema/herramientas/huella.sh cli   # imagen del CLI: Dockerfile y librerías (usa el
#                                        # sistema/ del repo montado, no el horneado)
#
# Se corre desde cualquier carpeta; imprime 16 caracteres hexadecimales.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

sha() {
    if command -v sha256sum >/dev/null 2>&1; then sha256sum; else shasum -a 256; fi | cut -c1-16
}

huella() { # <archivos...>: nombres y contenidos, en orden fijo
    {
        printf '%s\n' "$@"
        cat "$@"
    } | sha
}

case "${1:-}" in
bot)
    archivos=()
    while IFS= read -r archivo; do
        archivos+=("$archivo")
    done < <(find sistema -type f \
        -not -path '*/__pycache__/*' -not -path '*/.pytest_cache/*' -not -path '*/.ruff_cache/*' \
        -not -path 'sistema/tests/*' -not -path '*.egg-info/*' -not -name '*.py[co]' -not -name '.DS_Store' |
        LC_ALL=C sort)
    huella "${archivos[@]}"
    ;;
cli)
    huella sistema/Dockerfile sistema/requirements.txt sistema/constraints.txt
    ;;
*)
    echo "Uso: $0 bot|cli" >&2
    exit 2
    ;;
esac
