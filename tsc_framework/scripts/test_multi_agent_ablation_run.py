import time
import sys
from pathlib import Path

ROOT = Path("traffic_project/tsc_framework").resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

# Load build_ablation_extractors so classes exist
from ablation_real import build_ablation_extractors
build_ablation_extractors()

from stable_baselines3 import PPO
from transfer_eval_n30_robust import run_multi_agent_episode, CITY_CONFIGS

# Load models
model_off = PPO.load(str(ROOT / "outputs" / "ablation_real" / "models" / "coopsarg_gating_off_seed42.zip"), device="cpu")
model_on = PPO.load(str(ROOT / "outputs" / "ablation_real" / "models" / "coopsarg_gating_on_seed42.zip"), device="cpu")

# Choose Quito
net_path = ROOT / "sumo_configs" / "networks" / "quito.net.xml"
route_path = ROOT / "sumo_configs" / "routes" / "quito.net_multi_agent_extreme.rou.xml"

# Build temp sumocfg
sumocfg_path = ROOT / "outputs" / "ablation_real" / "sumocfg" / "test_eval_quito.sumocfg"
sumocfg_path.parent.mkdir(parents=True, exist_ok=True)
with open(sumocfg_path, "w", encoding="utf-8") as f:
    f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="{net_path}"/>
        <route-files value="{route_path}"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="1000"/>
    </time>
    <processing>
        <time-to-teleport value="-1"/>
        <waiting-time-memory value="1000"/>
    </processing>
</configuration>''')

print("Running 1 episode with Gating OFF on Quito (extreme)...")
t0 = time.time()
res_off = run_multi_agent_episode(model=model_off, sumocfg=str(sumocfg_path), steps_limit=150, seed=42)
t_off = time.time() - t0
print(f"Gating OFF finished in {t_off:.2f}s:")
print(f"  Delay: {res_off['delay_mean']:.2f}, Gini: {res_off['gini_mean']:.4f}, Queue: {res_off['queue_mean']:.2f}")

print("\nRunning 1 episode with Gating ON on Quito (extreme)...")
t0 = time.time()
res_on = run_multi_agent_episode(model=model_on, sumocfg=str(sumocfg_path), steps_limit=150, seed=42)
t_on = time.time() - t0
print(f"Gating ON finished in {t_on:.2f}s:")
print(f"  Delay: {res_on['delay_mean']:.2f}, Gini: {res_on['gini_mean']:.4f}, Queue: {res_on['queue_mean']:.2f}")
print(f"  DELTA GINI (OFF - ON): {res_off['gini_mean'] - res_on['gini_mean']:+.4f}")
