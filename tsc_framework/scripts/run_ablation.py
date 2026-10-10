#!/usr/bin/env python3
"""
run_ablation.py — Estudio de Ablación de Comportamientos Imprudentes
====================================================================
Este script realiza el estudio de ablación sugerido en la revisión doctoral,
aislando los diferentes comportamientos de conducción caótica para identificar
cuál de ellos contribuye más a la transición de fase (gridlock).

Escenarios evaluados (en nivel de Caos 0.50):
A. Solo Exceso de Velocidad (Speeding)
B. Solo Tailgating (Reducción de distancia de seguridad)
C. Solo Bloqueo (Gridlock activo de intersecciones y microbuses)
D. Combinado (Todos los efectos simultáneos)
"""

import argparse
import csv
import sys
import os
import warnings
from pathlib import Path
from typing import Dict, List, Any

import numpy as np
import yaml

# Resolver Directorios
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

warnings.filterwarnings("ignore")

try:
    from stable_baselines3 import PPO
    from stable_baselines3.common.utils import set_random_seed
    from src.core.tsc_env import TSCEnv
except ImportError as e:
    raise ImportError(f"Error importando dependencias: {e}")

# Funciones de métricas
def cvar_95(losses: List[float]) -> float:
    if not losses: return 0.0
    arr = np.array(losses)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0: return 0.0
    q = np.quantile(arr, 0.95)
    tail = arr[arr >= q]
    return float(tail.mean()) if len(tail) > 0 else float(q)

def evaluate_ablation_mode(
    agent, 
    model_name: str,
    ablation_mode: str, 
    chaos_level: float, 
    n_episodes: int,
    sumocfg_path: str,
    delta_t: int,
    max_steps: int
) -> List[Dict[str, Any]]:
    
    # Configurar la variable de entorno que lee LatamChaosManager
    os.environ["LATAM_ABLATION_MODE"] = ablation_mode
    print(f"\n Iniciando Ablación: {ablation_mode.upper()} | Modelo: {model_name} | Episodios: {n_episodes}")
    
    episode_results = []
    
    for ep in range(n_episodes):
        env = TSCEnv(
            sumocfg_path=sumocfg_path,
            tls_id="B1",
            use_gui=False,
            delta_t=delta_t,
            max_steps=max_steps,
            seed=1000 + ep,
            enable_traci_chaos=True,
            probabilidad_caos=chaos_level
        )
        
        obs, _ = env.reset()
        done = False
        step_count = 0
        ep_delays = []
        ep_queues = []
        
        while not done and step_count < max_steps:
            action, _ = agent.predict(obs, deterministic=True)
            act_val = int(action) if hasattr(action, 'ndim') and action.ndim == 0 else int(action[0]) if hasattr(action, '__iter__') else int(action)
            obs, reward, terminated, truncated, info = env.step(act_val)
            
            ep_delays.append(info.get("delay", 0.0))
            ep_queues.append(info.get("total_queue", 0.0))
            
            done = terminated or truncated
            step_count += 1
            
        env.close()
        
        mean_delay = float(np.mean(ep_delays)) if ep_delays else 0.0
        cvar_val = cvar_95(ep_delays)
        
        res = {
            "model": model_name,
            "ablation_mode": ablation_mode,
            "episode": ep + 1,
            "delay_mean": mean_delay,
            "cvar_95": cvar_val
        }
        episode_results.append(res)
        print(f"    Ep {ep+1:2d} | Delay={mean_delay:.2f}s | CVaR={cvar_val:.2f}s")
        
    return episode_results

def main():
    parser = argparse.ArgumentParser(description="Estudio de Ablación de Caos")
    parser.add_argument("--model", type=str, default="ppo_chaos", help="Modelo a evaluar (ej: ppo_chaos o ppo_ideal)")
    parser.add_argument("--episodes", type=int, default=5, help="Episodios por escenario")
    parser.add_argument("--chaos", type=float, default=0.50, help="Nivel de caos fijo para el estrés")
    args = parser.parse_args()
    
    set_random_seed(999)
    
    # 1. Configuración de SUMO
    config_path = ROOT / "config" / "default_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
        
    end_time_sec = int(cfg.get("sumo", {}).get("end_time", 3600))
    delta_t = int(cfg.get("sumo", {}).get("step_length", 5))
    max_steps = end_time_sec // delta_t
    
    net_file = ROOT / "sumo_configs" / "networks" / "hangzhou_4x4.net.xml"
    route_file = ROOT / "sumo_configs" / "routes" / "hangzhou" / "hangzhou_dense.rou.xml"
    
    import tempfile
    sumocfg_path = os.path.join(tempfile.gettempdir(), "ablation.sumocfg")
    with open(sumocfg_path, "w", encoding="utf-8") as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="{net_file.resolve()}"/>
        <route-files value="{route_file.resolve()}"/>
    </input>
    <time><begin value="0"/><end value="{end_time_sec}"/></time>
    <processing><time-to-teleport value="-1"/></processing>
    <report><no-warnings value="true"/></report>
</configuration>''')
        
    # 2. Cargar el Modelo
    model_path = ROOT / "outputs" / "models" / f"{args.model}.zip"
    if not model_path.exists():
        print(f" Modelo no encontrado: {model_path}")
        sys.exit(1)
        
    print(f" Cargando modelo {args.model}...")
    agent = PPO.load(str(model_path), device="cpu")
    
    # 3. Ejecutar Ablación
    modes = ["speeding_only", "tailgating_only", "blocking_only", "combined"]
    all_results = []
    
    for mode in modes:
        res = evaluate_ablation_mode(
            agent=agent,
            model_name=args.model,
            ablation_mode=mode,
            chaos_level=args.chaos,
            n_episodes=args.episodes,
            sumocfg_path=sumocfg_path,
            delta_t=delta_t,
            max_steps=max_steps
        )
        all_results.extend(res)
        
    # 4. Guardar Resultados
    results_dir = ROOT / "outputs" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    out_file = results_dir / f"ablation_{args.model}.csv"
    
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)
        
    print(f"\n Análisis de Ablación completado. Resultados en: {out_file}")
    
    import pandas as pd
    df = pd.DataFrame(all_results)
    summary = df.groupby("ablation_mode").agg({
        "delay_mean": ["mean"],
        "cvar_95": ["mean"]
    }).reset_index()
    print("\n RESUMEN DE ABLACIÓN")
    print("="*60)
    print(summary.to_string())

if __name__ == "__main__":
    main()
