param(
    [int]$Horas = 17,
    [switch]$SaltarBaseline
)

$ErrorActionPreference = 'Stop'
$prep = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $prep '..\BreakthroughBotIA')).Path
$root = Join-Path $repo 'resultados\campana_17h'
$deadline = (Get-Date).AddHours($Horas)
$expected = 198
$log = Join-Path $root 'campana_17h.log'
Start-Transcript -Path $log -Append | Out-Null

try {
    if (-not $SaltarBaseline) {
        $baseline = Get-ChildItem $root -Directory -Filter 'baseline_montecarlo_*' |
            Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if (-not $baseline) { throw "No se encontro un baseline para continuar." }
        Write-Host "Esperando baseline: $($baseline.FullName)"
        while ((Get-Date) -lt $deadline) {
            $done = @(Get-ChildItem $baseline.FullName -Recurse -Filter '*_vs_*.json' -ErrorAction SilentlyContinue).Count
            Write-Host "Baseline: $done/$expected"
            if ($done -ge $expected) { break }
            Start-Sleep -Seconds 60
        }
    } else {
        Write-Host "Baseline omitido: iniciando campana fuerte inmediatamente."
    }

    $round = 1
    while ((Get-Date) -lt $deadline) {
        $roundName = 'round_{0:D2}' -f $round
        $roundDir = Join-Path $root $roundName
        New-Item -ItemType Directory -Force -Path $roundDir | Out-Null
        Write-Host "Iniciando $roundName"

        $trainers = @()
        for ($i = 0; $i -lt 3; $i++) {
            $name = 'candidate_{0:D2}' -f ($i + 1)
            $relativeOut = "resultados\campana_17h\$roundName\$name.npy"
            $seed0 = 300000 + ($round * 1000) + ($i * 10)
            $seeds = @($seed0, $seed0 + 1, $seed0 + 2)
            $stdout = Join-Path $roundDir "$name.train.log"
            $stderr = Join-Path $roundDir "$name.train.err.log"
            $args = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                (Join-Path $prep 'worker_entrenamiento.ps1'),
                '-Repo', $repo, '-Prep', $prep, '-Salida', $relativeOut,
                '-Partidas', 100, '-Semillas') + $seeds
            $trainers += Start-Process powershell -ArgumentList $args -WindowStyle Hidden `
                -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
        }
        $trainers | Wait-Process
        $trainingFailures = @($trainers | Where-Object { $_.ExitCode -ne 0 })
        if ($trainingFailures.Count -gt 0) {
            throw "Fallo de entrenamiento en $($trainingFailures.Count) worker(s); se detiene la campana para no crear rondas vacias."
        }

        $candidates = @(Get-ChildItem $roundDir -Filter 'candidate_*.npy')
        if ($candidates.Count -ne 3) {
            throw "Se esperaban 3 candidatos y se encontraron $($candidates.Count) en $roundDir."
        }
        $evaluators = @()
        foreach ($candidate in $candidates) {
            $name = $candidate.BaseName
            $relativeWeights = "resultados\campana_17h\$roundName\$name.npy"
            $relativeOut = "resultados\campana_17h\$roundName\$name.eval.json"
            $stdout = Join-Path $roundDir "$name.eval.log"
            $stderr = Join-Path $roundDir "$name.eval.err.log"
            $seed = 400000 + ($round * 100) + [int]($name -replace 'candidate_','')
            $args = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                (Join-Path $prep 'worker_evaluacion.ps1'),
                '-Repo', $repo, '-Prep', $prep, '-Pesos', $relativeWeights,
                '-Salida', $relativeOut, '-Partidas', 40, '-Semilla', $seed)
            $evaluators += Start-Process powershell -ArgumentList $args -WindowStyle Hidden `
                -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
        }
        $evaluators | Wait-Process
        $evaluationFailures = @($evaluators | Where-Object { $_.ExitCode -ne 0 })
        if ($evaluationFailures.Count -gt 0) {
            throw "Fallo de evaluacion en $($evaluationFailures.Count) worker(s); se detiene la campana."
        }
        $evaluationFiles = @(Get-ChildItem $roundDir -Filter 'candidate_*.eval.json')
        if ($evaluationFiles.Count -ne $candidates.Count) {
            throw "Se esperaban $($candidates.Count) evaluaciones y se encontraron $($evaluationFiles.Count) en $roundDir."
        }
        Write-Host "$roundName terminada"
        $round++
    }
} finally {
    Stop-Transcript | Out-Null
}
