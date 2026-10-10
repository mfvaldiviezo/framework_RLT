import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from src.core.tsc_env import TSCEnv
from stable_baselines3 import PPO

# ── Paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

MODELS_DIR = ROOT / "outputs" / "ablation_real" / "models"
RESULTS_DIR = ROOT / "outputs" / "ablation_real" / "results"
csv_path = RESULTS_DIR / "ablation_real_results.csv"

def main():
    if not csv_path.exists():
        print(f"[ERR] No se encontró el archivo CSV en {csv_path}")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    
    # Agrupar y contar por combinación
    counts = df.groupby(["variant", "city", "chaos_level"]).size().reset_index(name="count")
    
    # Encontrar combinaciones incompletas
    missing = counts[counts["count"] < 30]
    if missing.empty:
        print("[OK] ¡Todas las combinaciones tienen exactamente 30 episodios! Nada que hacer.")
        sys.exit(0)
        
    print(f"[INFO] Se encontraron {len(missing)} combinaciones con episodios faltantes:")
    for _, row in missing.iterrows():
        print(f"  - {row['variant']} en {row['city']}/{row['chaos_level']}: {row['count']}/30 episodios")
        
    new_results = []
    
    for _, row in missing.iterrows():
        name = row["variant"]
        city = row["city"]
        chaos = row["chaos_level"]
        
        # Encontrar qué índices de episodio faltan
        existing_eps = set(df[(df["variant"] == name) & (df["city"] == city) & (df["chaos_level"] == chaos)]["episode"].values)
        all_eps = set(range(30))
        missing_eps = sorted(list(all_eps - existing_eps))
        
        print(f"\n--> Completando {len(missing_eps)} episodios para {name} en {city}/{chaos} (Eps: {missing_eps})...")
        
        # Cargar modelo PPO
        model_path = MODELS_DIR / f"{name}_seed42.zip"
        if not model_path.exists():
            print(f"  [ERR] No se encontró el modelo en {model_path}. Saltando combinación.")
            continue
            
        try:
            model = PPO.load(str(model_path), device="cpu")
        except Exception as e:
            print(f"  [ERR] Error al cargar el modelo: {e}. Saltando.")
            continue
            
        # Rutas de red y sumocfg
        net_dir = ROOT / "sumo_configs" / "networks"
        net_files = list(net_dir.glob(f"{city.lower()}*.net.xml"))
        if not net_files:
            print(f"  [ERR] No se encontró .net.xml para {city}. Saltando.")
            continue
        net_path = net_files[0]
        
        sumocfg_path = ROOT / "outputs" / "ablation_real" / "sumocfg_eval" / f"{city}_{chaos}_{name}.sumocfg"
        
        # ID del semáforo principal
        import xml.etree.ElementTree as ET
        tls_id = "B1"
        try:
            tree = ET.parse(str(net_path))
            root_xml = tree.getroot()
            tls_counts = {}
            for conn in root_xml.findall("connection"):
                tl = conn.get("tl")
                if tl:
                    tls_counts[tl] = tls_counts.get(tl, 0) + 1
            if tls_counts:
                tls_id = max(tls_counts, key=tls_counts.get)
        except Exception:
            pass
            
        for ep in missing_eps:
            # Seed único y puerto seguro (usando offset de 52000 para evitar choques con ejecuciones previas)
            city_idx = ["Quito", "Barcelona"].index(city)
            chaos_idx = ["low", "mid", "mid_high", "high", "extreme"].index(chaos)
            variant_idx = ["hsarg_gating_on", "hsarg_gating_off", "coopsarg_gating_on", "coopsarg_gating_off"].index(name)
            
            comb_id = variant_idx * 300 + city_idx * 150 + chaos_idx * 30 + ep
            
            success = False
            for attempt in range(5):
                # Desplazar la semilla por un número no divisible por 500 (ej: 33) para cambiar de puerto TCP
                ep_seed = 52000 + comb_id + attempt * 33
                print(f"  [SIM] Corriendo episodio faltante {ep} (intento {attempt+1}, seed={ep_seed})...")
                
                env = None
                try:
                    env = TSCEnv(
                        sumocfg_path=str(sumocfg_path),
                        tls_id=tls_id,
                        use_gui=False,
                        max_steps=720,
                        seed=ep_seed,
                        enable_traci_chaos=(city == "Quito"),
                        probabilidad_caos=0.4 if city == "Quito" else 0.0,
                    )
                    
                    obs, _ = env.reset()
                    done = False
                    ep_delays = []
                    ep_queues = []
                    ep_ginis = []
                    n_steps = 0
                    
                    while not done and n_steps < 720:
                        action, _ = model.predict(obs, deterministic=True)
                        step_result = env.step(action)
                        if len(step_result) == 5:
                            obs, reward, terminated, truncated, info = step_result
                            done = terminated or truncated
                        else:
                            obs, reward, done, info = step_result
                        
                        if 'delay' in info:
                            ep_delays.append(info['delay'])
                        if 'total_queue' in info:
                            ep_queues.append(info['total_queue'])
                        if 'gini' in info:
                            ep_ginis.append(info['gini'])
                        
                        n_steps += 1
                    
                    delay_mean = np.mean(ep_delays) if ep_delays else 0.0
                    queue_mean = np.mean(ep_queues) if ep_queues else 0.0
                    gini_mean = np.mean(ep_ginis) if ep_ginis else 0.0
                    
                    new_results.append({
                        "variant": name,
                        "city": city,
                        "chaos_level": chaos,
                        "episode": ep,
                        "delay_mean": float(delay_mean),
                        "queue_mean": float(queue_mean),
                        "gini_mean": float(max(0, min(1, gini_mean))),
                        "n_steps": n_steps,
                    })
                    print(f"    [OK] Episodio {ep} completado exitosamente en el intento {attempt+1}.")
                    success = True
                    break  # Salir del bucle de intentos al tener éxito
                    
                except Exception as e:
                    print(f"    [WARN] Intento {attempt+1} falló: {e}")
                finally:
                    if env is not None:
                        try: env.close()
                        except: pass
                        try: env._safe_close_traci()
                        except: pass
                    try:
                        import traci
                        if hasattr(traci, '_connections'):
                            traci._connections.clear()
                    except:
                        pass
            
            if not success:
                print(f"  [ERR] No se pudo recuperar el episodio {ep} tras 5 intentos.")

    if new_results:
        # Combinar resultados y guardar
        new_df = pd.DataFrame(new_results)
        combined_df = pd.concat([df, new_df], ignore_index=True)
        # Ordenar para mantener consistencia
        combined_df = combined_df.sort_values(by=["variant", "city", "chaos_level", "episode"]).reset_index(drop=True)
        combined_df.to_csv(csv_path, index=False)
        print(f"\n[OK] Se añadieron con éxito {len(new_results)} episodios faltantes.")
        print(f"[OK] Nuevo total de registros en {csv_path.name}: {len(combined_df)} filas.")
    else:
        print("\n[WARN] No se pudo recuperar ningún episodio faltante.")

if __name__ == "__main__":
    main()
