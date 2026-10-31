param(
    [Parameter(Mandatory=$true)][string]$Repo,
    [Parameter(Mandatory=$true)][string]$SalidaRelativa,
    [Parameter(Mandatory=$true)][int]$Partidas,
    [Parameter(Mandatory=$true)][int]$Semilla
)

$ErrorActionPreference = 'Stop'
$compose = Join-Path $Repo 'docker-compose.yml'
$salida = Join-Path $Repo $SalidaRelativa
New-Item -ItemType Directory -Force -Path $salida | Out-Null
$env:TORNEO_RAIZ_HOST = $Repo
$env:TORNEO_HUSO = '-0600'
$containerOutput = '/torneo/' + ($SalidaRelativa -replace '\\','/')

docker compose --project-directory $Repo -f $compose run --rm -T `
    -w /torneo -e "TORNEO_RESULTADOS=$containerOutput" torneo `
    python -m cli jugar iacasitegano montecarlo --partidas $Partidas --semilla $Semilla -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
