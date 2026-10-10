import os
import sys
import subprocess
import concurrent.futures
from threading import Lock

MAX_WORKERS = 3  # Seguro para 8 nucleos y 32GB RAM
MAX_RETRIES = 2

ALGOS = ["maxpressure", "idqn", "colight", "mplight"]
SCENARIOS = ["ideal", "latam"]

LOG_DIR = "logs_fase2"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print_lock = Lock()

def safe_print(msg):
    with print_lock:
        print(msg)
        sys.stdout.flush()

def run_experiment(algo, scenario):
    """
    Ejecuta un experimento individual. Retorna True si fue exitoso, False si falló luego de reintentos.
    """
    log_file = os.path.join(LOG_DIR, f"{algo}_{scenario}.log")
    
    cmd = [sys.executable, "..\\run_resco.py", "--algo", algo, "--scenario", scenario]
    
    for attempt in range(1, MAX_RETRIES + 1):
        safe_print(f" [INICIANDO] Algo: {algo.upper()} | Escenario: {scenario.upper()} (Intento {attempt}/{MAX_RETRIES})")
        
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["CUDA_VISIBLE_DEVICES"] = "" # Force CPU to avoid GTX 1050 sm_61 mismatch
            with open(log_file, "w", encoding="utf-8") as f:
                process = subprocess.run(
                    cmd, 
                    stdout=f, 
                    stderr=subprocess.STDOUT, 
                    text=True,
                    cwd=os.path.abspath("."), # Asegurar que corremos desde tsc_framework
                    env=env
                )
                
            if process.returncode == 0:
                safe_print(f" [ÉXITO] Algo: {algo.upper()} | Escenario: {scenario.upper()}")
                return True
            else:
                safe_print(f"️ [FALLO] Algo: {algo.upper()} | Escenario: {scenario.upper()} - Código: {process.returncode}")
                
        except Exception as e:
            safe_print(f" [ERROR FATAL] {algo.upper()} | {scenario.upper()}: {e}")
            
    safe_print(f" [ABORTADO] {algo.upper()} | {scenario.upper()} falló después de {MAX_RETRIES} intentos.")
    return False

def main():
    safe_print("="*80)
    safe_print(f" ORQUESTADOR MAESTRO DE EXPERIMENTOS SOTA (WORKERS={MAX_WORKERS})")
    safe_print("="*80)

    # Inyectar el caos primero
    safe_print("\n [1/3] Inyectando Caos LATAM en RESCO (scratch_inject.py)...")
    try:
        subprocess.run([sys.executable, "scratch_inject.py"], check=True)
        safe_print("️ Inyección completada exitosamente.\n")
    except Exception as e:
        safe_print(f" Fallo al inyectar el caos. Abortando orquestador. Error: {e}")
        return

    # Preparar tareas
    tasks = []
    for algo in ALGOS:
        for scen in SCENARIOS:
            tasks.append((algo, scen))
            
    safe_print(f" [2/3] Lanzando {len(tasks)} experimentos en PARALELO (Max simultáneos: {MAX_WORKERS})...")
    
    success_count = 0
    # Ejecutar en pool
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(run_experiment, algo, scen): (algo, scen) for algo, scen in tasks}
        
        for future in concurrent.futures.as_completed(futures):
            algo, scen = futures[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as exc:
                safe_print(f" Excepción procesando {algo}_{scen}: {exc}")

    safe_print("\n" + "="*80)
    safe_print(f" TAREAS COMPLETADAS: {success_count} / {len(tasks)} tuvieron éxito.")
    safe_print("="*80)

    if success_count > 0:
        safe_print("\n [3/3] Consolidando Resultados (compare_resco_results.py)...")
        subprocess.run([sys.executable, "compare_resco_results.py"])

if __name__ == "__main__":
    main()
