# agregar_ciudad.ps1
# Descarga OSM, convierte a red SUMO y genera rutas para una nueva ciudad
# Uso: .\agregar_ciudad.ps1 -Ciudad "bogota" -Lat 4.6097 -Lon -74.0817
#
# Ciudades LATAM sugeridas:
#   Bogota:    -Lat 4.6097  -Lon -74.0817
#   Lima:      -Lat -12.0464 -Lon -77.0428
#   Santiago:  -Lat -33.4489 -Lon -70.6693
#   CDMX:      -Lat 19.4326  -Lon -99.1332
#   Guayaquil: -Lat -2.1710  -Lon -79.9224
#
# Ciudades Europa sugeridas:
#   Madrid:    -Lat 40.4168  -Lon -3.7038
#   Berlin:    -Lat 52.5200  -Lon 13.4050
#   Amsterdam: -Lat 52.3676  -Lon 4.9041
#   Lisboa:    -Lat 38.7169  -Lon -9.1395

param(
    [Parameter(Mandatory=$true)]
    [string]$Ciudad,

    [Parameter(Mandatory=$true)]
    [float]$Lat,

    [Parameter(Mandatory=$true)]
    [float]$Lon,

    [float]$RadioGrados = 0.012,   # ~1.3 km radio, ajusta segun densidad
    [float]$FrecuenciaVeh = 1.8,   # segundos entre vehiculos (1.2=denso, 3.0=fluido)
    [switch]$LateralResolucion      # activar para LATAM (motos, buses)
)

$ErrorActionPreference = "Stop"

# Detectar SUMO_HOME
if ($env:SUMO_HOME) {
    $SUMO_HOME = $env:SUMO_HOME
} elseif (Test-Path "C:\Program Files (x86)\Eclipse\Sumo") {
    $SUMO_HOME = "C:\Program Files (x86)\Eclipse\Sumo"
} elseif (Test-Path "C:\Program Files\Eclipse\Sumo") {
    $SUMO_HOME = "C:\Program Files\Eclipse\Sumo"
} else {
    Write-Error "SUMO_HOME no encontrado. Instala SUMO o configura la variable de entorno."
    exit 1
}

$BASE = "c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework"
$REDES = "$BASE\sumo_configs\networks"
$RUTAS = "$BASE\sumo_configs\routes"
$OSM_DIR = "$BASE\sumo_configs"
$LOGS_DIR = "c:\Proyecto_Tesis_Final_V1\traffic_project\logs"

# Crear directorios si no existen
New-Item -ItemType Directory -Force -Path $REDES | Out-Null
New-Item -ItemType Directory -Force -Path $RUTAS | Out-Null
New-Item -ItemType Directory -Force -Path $LOGS_DIR | Out-Null

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AGREGANDO CIUDAD: $($Ciudad.ToUpper())" -ForegroundColor Cyan
Write-Host "  Coordenadas: $Lat, $Lon  |  Radio: ${RadioGrados} grados" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# ── PASO 1: Descargar OSM via Overpass API ─────────────────────────────────
$osmFile = "$OSM_DIR\$Ciudad.osm"
$netFile = "$REDES\$Ciudad.net.xml"
$routeFile = "$RUTAS\${Ciudad}_routes.rou.xml"

if (Test-Path $osmFile) {
    Write-Host "[PASO 1] Archivo OSM ya existe. Omitiendo descarga." -ForegroundColor Yellow
} else {
    Write-Host "[PASO 1] Descargando mapa OSM desde Overpass API..." -ForegroundColor Yellow

    $minLon = [math]::Round($Lon - $RadioGrados, 6)
    $minLat = [math]::Round($Lat - $RadioGrados, 6)
    $maxLon = [math]::Round($Lon + $RadioGrados, 6)
    $maxLat = [math]::Round($Lat + $RadioGrados, 6)

    $bbox = "${minLon},${minLat},${maxLon},${maxLat}"
    $url = "https://overpass-api.de/api/map?bbox=$bbox"

    Write-Host "  URL: $url" -ForegroundColor Gray
    Write-Host "  Descargando... (puede tardar 30-90 segundos)" -ForegroundColor Gray

    try {
        Invoke-WebRequest -Uri $url -OutFile $osmFile -TimeoutSec 120
        $sizeMB = [math]::Round((Get-Item $osmFile).Length / 1MB, 2)
        Write-Host "  OSM descargado: $osmFile ($sizeMB MB)" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR en Overpass API. Intenta manualmente en https://overpass-turbo.eu/" -ForegroundColor Red
        Write-Host "  Guarda el archivo como: $osmFile" -ForegroundColor Red
        exit 1
    }
}

# ── PASO 2: Convertir OSM a red SUMO ──────────────────────────────────────
if (Test-Path $netFile) {
    Write-Host "[PASO 2] Red SUMO ya existe. Omitiendo conversion." -ForegroundColor Yellow
} else {
    Write-Host "[PASO 2] Convirtiendo OSM a red SUMO con netconvert..." -ForegroundColor Yellow

    $netconvertArgs = @(
        "--osm-files", $osmFile,
        "--output-file", $netFile,
        "--geometry.remove",
        "--roundabouts.guess",
        "--ramps.guess",
        "--junctions.join",
        "--junctions.join-dist", "20",
        "--tls.guess-signals",
        "--tls.discard-simple",
        "--tls.join",
        "--tls.default-type", "actuated",
        "--keep-edges.by-vclass", "passenger",
        "--remove-edges.isolated",
        "--no-turnarounds",
        "--no-internal-links", "false",
        "--type-files", "$SUMO_HOME\data\typemap\osmNetconvert.typ.xml"
    )

    $logFile = "$LOGS_DIR\netconvert_$Ciudad.log"
    netconvert @netconvertArgs 2>&1 | Tee-Object -FilePath $logFile

    if (Test-Path $netFile) {
        $sizeMB = [math]::Round((Get-Item $netFile).Length / 1MB, 2)
        Write-Host "  Red generada: $netFile ($sizeMB MB)" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: netconvert fallo. Revisa: $logFile" -ForegroundColor Red
        exit 1
    }
}

# ── PASO 3: Verificar semaforos en la red ─────────────────────────────────
Write-Host "[PASO 3] Verificando semaforos en la red..." -ForegroundColor Yellow

$tlsCount = python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('$($netFile.Replace('\', '/'))')
root = tree.getroot()
tls_list = [(tl.get('id'), tl.get('type')) for tl in root.findall('tlLogic')]
print(len(tls_list))
for tid, ttype in tls_list[:5]:
    print(f'  {tid} ({ttype})')
"

Write-Host "  Resultado:" -ForegroundColor Gray
Write-Host $tlsCount -ForegroundColor Cyan

$numTLS = ($tlsCount -split "`n")[0].Trim()
if ([int]$numTLS -eq 0) {
    Write-Host "  ADVERTENCIA: No se detectaron semaforos." -ForegroundColor Red
    Write-Host "  Intenta agregar --tls.guess al comando de netconvert." -ForegroundColor Red
    Write-Host "  Editando netconvert y reintentando con --tls.guess..." -ForegroundColor Yellow
    Remove-Item $netFile -Force

    $netconvertArgs += @("--tls.guess")
    netconvert @netconvertArgs 2>&1 | Tee-Object -FilePath "$LOGS_DIR\netconvert_${Ciudad}_retry.log"
}

# ── PASO 4: Generar rutas vehiculares ─────────────────────────────────────
if (Test-Path $routeFile) {
    Write-Host "[PASO 4] Archivo de rutas ya existe. Omitiendo generacion." -ForegroundColor Yellow
} else {
    Write-Host "[PASO 4] Generando rutas vehiculares con randomTrips.py..." -ForegroundColor Yellow
    Write-Host "  Frecuencia: 1 vehiculo cada $FrecuenciaVeh segundos" -ForegroundColor Gray

    $randomTripsPath = "$SUMO_HOME\tools\randomTrips.py"

    if (-not (Test-Path $randomTripsPath)) {
        Write-Error "randomTrips.py no encontrado en: $randomTripsPath"
        exit 1
    }

    python $randomTripsPath `
        -n $netFile `
        -o $routeFile `
        -e 3600 `
        -p $FrecuenciaVeh `
        --validate `
        --fringe-factor 5 `
        --min-distance 150 `
        --trip-attributes "departLane=`"best`" departSpeed=`"max`""

    if (Test-Path $routeFile) {
        $sizeKB = [math]::Round((Get-Item $routeFile).Length / 1KB, 1)
        Write-Host "  Rutas generadas: $routeFile ($sizeKB KB)" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: randomTrips.py fallo. Intenta reducir --min-distance." -ForegroundColor Red
        exit 1
    }
}

# ── PASO 5: Generar codigo de integracion ─────────────────────────────────
Write-Host "[PASO 5] Generando fragmento de codigo para transfer_eval_n30.py..." -ForegroundColor Yellow

$lateralResCode = if ($LateralResolucion) { "0.4   # LATAM: motos y buses informales" } else { "None  # Europa: sin resolucion lateral" }

$codeSnippet = @"

    # ── NUEVA CIUDAD: $($Ciudad.ToUpper()) ────────────────────────────
    ${Ciudad}_net = ROOT / "sumo_configs/networks/${Ciudad}.net.xml"
    ${Ciudad}_route = generate_junction_traffic(${Ciudad}_net, args.steps)

    res_${Ciudad} = evaluate_transfer_n_episodes(
        model=model, model_name=model_name, city="$($Ciudad.Substring(0,1).ToUpper())$($Ciudad.Substring(1))",
        net_path=${Ciudad}_net, route_path=${Ciudad}_route,
        n_episodes=args.episodes, steps_limit=args.steps,
        lateral_res=$lateralResCode
    )
    all_results.extend(res_${Ciudad})
    # ── FIN NUEVA CIUDAD ──────────────────────────────────────────────
"@

Write-Host ""
Write-Host "Agrega este fragmento en transfer_eval_n30.py dentro del bucle de evaluacion:" -ForegroundColor Cyan
Write-Host $codeSnippet -ForegroundColor White

# ── Resumen final ──────────────────────────────────────────────────────────
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  CIUDAD LISTA: $($Ciudad.ToUpper())" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Red SUMO:    $netFile" -ForegroundColor White
Write-Host "  Rutas:       $routeFile" -ForegroundColor White
Write-Host ""
Write-Host "  Para evaluar, ejecuta:" -ForegroundColor Yellow
Write-Host "  python tsc_framework\scripts\transfer_eval_n30.py --episodes 30" -ForegroundColor Cyan
Write-Host ""
