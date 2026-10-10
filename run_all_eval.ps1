# run_all_eval.ps1 - Suite de Evaluacion Doctoral (v3 - sin duplicacion de baselines)
$ErrorActionPreference = "Continue"

$env:GIT_CONFIG_NOSYSTEM  = 1
$env:GIT_CONFIG_GLOBAL    = 'NUL'
$env:GIT_CONFIG_SYSTEM    = 'NUL'
$env:PYTHONIOENCODING     = 'utf-8'

$TS_INICIO = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  SUITE DOCTORAL DE EVALUACION UNIFICADA v3" -ForegroundColor Cyan
Write-Host "  Modelos: ppo_ideal | ppo_chaos | ppo_coop_ideal | ppo_coop_chaos" -ForegroundColor Cyan
Write-Host "  Baselines: fixed | maxpressure | colight  (corrida unica)" -ForegroundColor Cyan
Write-Host "  Inicio: $TS_INICIO" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$PYTHON = "baselines\pytsc\venv_pytsc\Scripts\python.exe"
$EVAL   = "tsc_framework/scripts/run_evaluation.py"
$TRANS  = "tsc_framework/scripts/transfer_eval.py"
$PLOTS  = "tsc_framework/scripts/generate_plots.py"
$STATS  = "tsc_framework/scripts/statistical_analysis.py"
$REPORT = "tsc_framework/scripts/generate_thesis_report.py"

# --- Experimento A: Robustez - LOS 4 MODELOS + BASELINES en una sola corrida ---
# (Baselines se ejecutan una sola vez, resultado va a metrics_summary.csv unificado)
Write-Host ""
Write-Host " [1/4] Exp A: Robustez Hangzhou - 4 modelos + baselines (30 eps, 4 niveles caos)..." -ForegroundColor Yellow
& $PYTHON $EVAL `
    --network hangzhou `
    --models ppo_ideal ppo_chaos ppo_coop_ideal ppo_coop_chaos `
    --baselines fixed maxpressure colight `
    --chaos-levels 0.0 0.15 0.30 0.50 `
    --episodes 30 `
    --output metrics_summary.csv

if ($LASTEXITCODE -ne 0) {
    Write-Host " [ERROR] Experimento A fallo. Abortando suite." -ForegroundColor Red
    exit 1
}

# --- Experimento B: Transferencia Zero-Shot (Barcelona + Quito) ---
Write-Host ""
Write-Host " [2/4] Exp B: Transferencia Zero-Shot - los 4 modelos (Barcelona + Quito)..." -ForegroundColor Yellow
& $PYTHON $TRANS

if ($LASTEXITCODE -ne 0) {
    Write-Host " [ERROR] Experimento B fallo. Abortando suite." -ForegroundColor Red
    exit 1
}

# --- Generacion de Figuras Cientificas ---
Write-Host ""
Write-Host " [3/4] Figuras: 300 DPI con Medianas + IQR..." -ForegroundColor Yellow
& $PYTHON $PLOTS
if ($LASTEXITCODE -ne 0) {
    Write-Host " [ADVERTENCIA] Error al generar graficos. Continuando..." -ForegroundColor DarkYellow
}

# --- Analisis Estadistico ---
Write-Host ""
Write-Host " [3.5/4] Stats: Mann-Whitney U, Kruskal-Wallis, Effect Sizes..." -ForegroundColor Yellow
& $PYTHON $STATS
if ($LASTEXITCODE -ne 0) {
    Write-Host " [ADVERTENCIA] Error en analisis estadistico. Continuando..." -ForegroundColor DarkYellow
}

# --- Reporte Final Doctoral ---
Write-Host ""
Write-Host " [4/4] Reporte: Consolidando INFORME_FINAL_ROBUSTEZ.md..." -ForegroundColor Yellow
& $PYTHON $REPORT
if ($LASTEXITCODE -ne 0) {
    Write-Host " [ADVERTENCIA] Error al consolidar reporte." -ForegroundColor DarkYellow
}

# --- Resumen Final ---
$TS_FIN = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  SUITE COMPLETADA - $TS_FIN" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Resultados en: tsc_framework/outputs/results/" -ForegroundColor Green
Write-Host "    metrics_summary.csv    => Exp A (7 agentes x 4 niveles x 30 eps)" -ForegroundColor Green
Write-Host "    metrics_detailed.csv   => Registros por episodio" -ForegroundColor Green
Write-Host "    transfer_report.md     => Exp B (Zero-Shot Barcelona + Quito)" -ForegroundColor Green
Write-Host "    INFORME_FINAL_ROBUSTEZ.md => Reporte doctoral consolidado" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
