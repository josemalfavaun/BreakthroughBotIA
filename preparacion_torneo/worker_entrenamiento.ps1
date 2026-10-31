param([string]$Repo, [string]$Prep, [string]$Salida, [int]$Partidas, [int[]]$Semillas)
$ErrorActionPreference = 'Stop'
$out = '/torneo/' + ($Salida -replace '\\','/')
docker run --rm --cpus=1 --memory=1024m --network=none `
  -v "${Repo}:/torneo" -v "${Prep}:/prep" -w /torneo `
  -e NUMBA_CACHE_DIR=/tmp/numba torneo-base:local `
  python /prep/entrenar_candidato.py --partidas $Partidas --semillas $Semillas --salida $out
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
