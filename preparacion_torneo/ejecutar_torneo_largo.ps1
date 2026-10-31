param(
    [int]$Partidas = 200,
    [int]$Semilla = 20261030,
    [switch]$VerboseOutput
)

$ErrorActionPreference = 'Stop'
$raiz = (Resolve-Path (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '..\BreakthroughBotIA')).Path
$bash = 'C:\Program Files\Git\bin\bash.exe'
$torneo = Join-Path $raiz 'torneo'
$resultados = Join-Path $raiz 'resultados\torneo_largo'

if (-not (Test-Path -LiteralPath $bash)) {
    throw "No se encontró Git Bash en '$bash'."
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker CLI no está disponible. Instala y abre Docker Desktop antes de continuar.'
}

$dockerInfo = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    throw "Docker Desktop no está iniciado o no responde:`n$($dockerInfo -join "`n")"
}

New-Item -ItemType Directory -Force -Path $resultados | Out-Null
$marca = Get-Date -Format 'yyyyMMdd_HHmmss'
$log = Join-Path $resultados "partidas_${Partidas}_semilla_${Semilla}_$marca.log"
$detalle = if ($VerboseOutput) { '-v' } else { '' }
$raizBash = (& $bash -lc "cygpath -u '$raiz'").Trim()
$comando = "cd '$raizBash' && ./torneo jugar iacasitegano montecarlo --partidas $Partidas --semilla $Semilla $detalle"

Write-Host "Iniciando torneo: $Partidas partidas, semilla $Semilla"
Write-Host "Registro: $log"
& $bash -lc $comando 2>&1 | Tee-Object -FilePath $log
if ($LASTEXITCODE -ne 0) {
    throw "El torneo terminó con código $LASTEXITCODE. Revisa '$log'."
}
Write-Host "Torneo terminado correctamente."
