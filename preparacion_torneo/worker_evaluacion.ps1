param([string]$Repo, [string]$Prep, [string]$Pesos, [string]$Salida, [int]$Partidas, [int]$Semilla)
$ErrorActionPreference = 'Stop'
$weights = '/torneo/' + ($Pesos -replace '\\','/')
$out = '/torneo/' + ($Salida -replace '\\','/')
docker run --rm --cpus=1 --memory=1024m --network=none `
  -v "${Repo}:/torneo" -v "${Prep}:/prep" -w /torneo torneo-base:local `
  python /prep/evaluar_candidato.py --pesos $weights --salida $out --partidas $Partidas --semilla $Semilla
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
