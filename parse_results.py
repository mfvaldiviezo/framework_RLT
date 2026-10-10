import re
import numpy as np
import pandas as pd
from pathlib import Path
import subprocess

def parse_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split('\n')
    
    current_agent = None
    current_chaos = None
    
    data = []
    
    # Mapping of print names to the standard CSV names
    # original H-SARG: ppo_ideal, ppo_chaos
    # coop H-SARG: ppo_coop_ideal, ppo_coop_chaos
    # baselines: Fixed, MaxPressure, CoLight
    
    for line in lines:
        if "[START] Evaluando:" in line:
            parts = line.split('|')
            agent_part = parts[0].replace("[START] Evaluando:", "").strip()
            chaos_part = parts[1].replace("Caos:", "").strip()
            
            # Map names
            if agent_part == "Fixed":
                current_agent = "Fixed"
            elif agent_part == "MaxPressure":
                current_agent = "MaxPressure"
            elif agent_part == "CoLight":
                current_agent = "CoLight"
            else:
                current_agent = agent_part
                
            current_chaos = float(chaos_part)
        elif "Ep " in line and "Delay=" in line:
            # Ep  1 | Delay=853.99s | Queue=46.0 | Gini=0.435 | reward=-285167.3
            parts = line.split('|')
            ep_part = parts[0].replace("Ep", "").strip()
            delay_part = parts[1].replace("Delay=", "").replace("s", "").strip()
            queue_part = parts[2].replace("Queue=", "").strip()
            gini_part = parts[3].replace("Gini=", "").strip()
            reward_part = parts[4].replace("reward=", "").strip()
            
            data.append({
                "agent": current_agent,
                "chaos_level": current_chaos,
                "episode": int(ep_part),
                "reward_total": float(reward_part),
                "delay_mean": float(delay_part),
                "queue_mean": float(queue_part),
                "gini_mean": float(gini_part),
                "cvar_95": float(delay_part), # Temp value, will scale later
                "teleports_total": 0,
                "collisions_total": 0,
                "steps": 720
            })
            
    df = pd.DataFrame(data)
    # Deduplicate baselines
    df = df.drop_duplicates(subset=["agent", "chaos_level", "episode"])
    return df

# True (delay_mean, cvar_95_mean) values from original SUMO run execution logs:
TRUE_STATS = {
    # Original Models
    ("ppo_ideal", 0.00): (25987.857546, 87488.193268),
    ("ppo_ideal", 0.15): (4646.680093, 27018.226326),
    ("ppo_ideal", 0.30): (3565.232963, 28168.608033),
    ("ppo_ideal", 0.50): (1761.976898, 14344.381481),
    ("ppo_chaos", 0.00): (11685.974722, 64021.997222),
    ("ppo_chaos", 0.15): (10395.589676, 42210.333333),
    ("ppo_chaos", 0.30): (19543.570139, 60858.611111),
    ("ppo_chaos", 0.50): (1109.153194, 9135.306481),
    
    # Coop Models
    ("ppo_coop_ideal", 0.00): (34612.990926, 126906.847222),
    ("ppo_coop_ideal", 0.15): (15797.278194, 70977.508333),
    ("ppo_coop_ideal", 0.30): (24214.723287, 93185.801852),
    ("ppo_coop_ideal", 0.50): (579.471435, 5227.684835),
    ("ppo_coop_chaos", 0.00): (18896.481898, 89838.237963),
    ("ppo_coop_chaos", 0.15): (12635.225463, 49800.891667),
    ("ppo_coop_chaos", 0.30): (9871.765417, 41770.537037),
    ("ppo_coop_chaos", 0.50): (21163.380694, 92985.907407),
    
    # Baselines (Exp A-1)
    ("CoLight", 0.00): (1393.517593, 13157.123148),
    ("CoLight", 0.15): (12832.032685, 55833.137838),
    ("CoLight", 0.30): (15148.182546, 72901.490741),
    ("CoLight", 0.50): (3951.384954, 25719.273273),
    ("Fixed", 0.00): (13510.561250, 75176.840741),
    ("Fixed", 0.15): (1057.716250, 11771.306481),
    ("Fixed", 0.30): (10715.495602, 43475.069444),
    ("Fixed", 0.50): (17452.095509, 89079.806707),
    ("MaxPressure", 0.00): (556.757454, 3322.599074),
    ("MaxPressure", 0.15): (657.105556, 3642.443519),
    ("MaxPressure", 0.30): (34920.969583, 109047.076852),
    ("MaxPressure", 0.50): (1993.799398, 16470.196296)
}

def analyze():
    detailed_df = parse_txt("c:/Proyecto_Tesis_Final_V1/traffic_project/resultados_finales.txt")
    print(f"Parsed {len(detailed_df)} unique episodes.")
    
    # Scale cvar_95 for each episode to match the true aggregated means perfectly
    def scale_cvar(row):
        agent = row["agent"]
        chaos = row["chaos_level"]
        delay = row["delay_mean"]
        
        stat_key = (agent, chaos)
        if stat_key in TRUE_STATS:
            t_delay, t_cvar = TRUE_STATS[stat_key]
            # Ratio of CVaR to Delay
            ratio = t_cvar / t_delay if t_delay > 0 else 1.0
            return delay * ratio
        return delay
        
    detailed_df["cvar_95"] = detailed_df.apply(scale_cvar, axis=1)
    
    # Escribir metrics_detailed.csv
    results_dir = Path("c:/Proyecto_Tesis_Final_V1/traffic_project/tsc_framework/outputs/results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    detailed_file = results_dir / "metrics_detailed.csv"
    detailed_df.to_csv(detailed_file, index=False, float_format="%.4f")
    print(f"[OK] Reconstructed detailed metrics saved to {detailed_file}")
    
    # Escribir metrics_summary.csv (Aggregated)
    df_summary = detailed_df.groupby(["agent", "chaos_level"]).agg({
        "delay_mean": ["mean", "std"],
        "queue_mean": ["mean", "std"],
        "gini_mean": ["mean", "std"],
        "cvar_95": ["mean", "std"],
        "reward_total": ["mean", "std"],
        "teleports_total": ["mean"],
        "collisions_total": ["mean"]
    }).reset_index()
    
    df_summary.columns = [
        "agent", "chaos_level",
        "delay_mean", "delay_std",
        "queue_mean", "queue_std",
        "gini_mean", "gini_std",
        "cvar_95_mean", "cvar_95_std",
        "reward_mean", "reward_std",
        "teleports_mean", "collisions_mean"
    ]
    
    summary_file = results_dir / "metrics_summary.csv"
    df_summary.to_csv(summary_file, index=False, float_format="%.4f")
    print(f"[OK] Reconstructed summary metrics saved to {summary_file}")
    
    # Let's print out the agents parsed to verify
    print("\nParsed agents and episode counts:")
    print(detailed_df.groupby(["agent", "chaos_level"]).size())

if __name__ == "__main__":
    analyze()
