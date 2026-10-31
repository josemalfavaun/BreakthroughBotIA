param(
    [int]$Workers = 3,
    [int]$PartidasPorWorker = 40,
    [int]$SemillaInicial = 20261030
)

$ErrorActionPreference = 'Stop'
$prep = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $prep '..\BreakthroughBotIA')).Path
$worker = Join-Path $prep 'worker_partidas.ps1'
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$base = "resultados\campana_17h\baseline_montecarlo_$stamp"
$hostBase = Join-Path $repo $base
New-Item -ItemType Directory -Force -Path $hostBase | Out-Null

$procesos = @()
for ($i = 0; $i -lt $Workers; $i++) {
    $seed = $SemillaInicial + $i
    $rel = "$base\worker_$('{0:D2}' -f ($i + 1))_semilla_$seed"
    $log = Join-Path $hostBase "worker_$('{0:D2}' -f ($i + 1)).log"
    $err = Join-Path $hostBase "worker_$('{0:D2}' -f ($i + 1)).err.log"
    $args = @('-NoProfile','-ExecutionPolicy','Bypass','-File',$worker,
        '-Repo',$repo,'-SalidaRelativa',$rel,'-Partidas',$PartidasPorWorker,'-Semilla',$seed)
    $procesos += Start-Process -FilePath 'powershell.exe' -ArgumentList $args `
        -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError $err -PassThru
}

@{
    started = (Get-Date).ToString('o')
    repo = $repo
    workers = $Workers
    partidas_por_worker = $PartidasPorWorker
    partidas_totales = $Workers * $PartidasPorWorker
    semillas = @($SemillaInicial..($SemillaInicial + $Workers - 1))
    pids = @($procesos.Id)
    salida = $hostBase
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $hostBase 'LANZAMIENTO.json') -Encoding UTF8

Write-Host "Baseline lanzado en $Workers workers: $($Workers * $PartidasPorWorker) partidas."
Write-Host "PID: $($procesos.Id -join ', ')"
Write-Host "Resultados: $hostBase"
