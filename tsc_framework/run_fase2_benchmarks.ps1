$algos = @("maxpressure", "idqn", "colight", "mplight")
$scenarios = @("ideal", "latam")

$log_dir = "logs_fase2"
if (-Not (Test-Path $log_dir)) {
    New-Item -ItemType Directory -Force -Path $log_dir | Out-Null
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Iniciando ejecución en lote: Fase 2 (Ideal vs LATAM)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Asegurar que el escenario latam está actualizado con el caos
Write-Host "`n[1/2] Generando caos LATAM fresco..." -ForegroundColor Yellow
python scratch_inject.py | Out-File "$log_dir\injection_log.txt"
Write-Host "Caos inyectado exitosamente." -ForegroundColor Green

# 2. Ejecutar todas las combinaciones
$total = $algos.Count * $scenarios.Count
$count = 1

foreach ($algo in $algos) {
    foreach ($scen in $scenarios) {
        Write-Host "`n[$count/$total] Ejecutando: ALGO=$algo | SCENARIO=$scen" -ForegroundColor Yellow
        $log_file = "$log_dir\${algo}_${scen}.log"
        
        Write-Host "  -> Guardando logs en $log_file" -ForegroundColor Gray
        
        # Ejecutar y capturar salida
        python ..\run_resco.py --algo $algo --scenario $scen *>&1 | Tee-Object -FilePath $log_file
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  -> [EXITO] Completado $algo con tráfico $scen" -ForegroundColor Green
        } else {
            Write-Host "  -> [ERROR] Falló $algo con tráfico $scen. Revisa el log." -ForegroundColor Red
        }
        $count++
    }
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "           TODAS LAS EJECUCIONES COMPLETADAS" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
