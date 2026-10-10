import sys
from pathlib import Path
import numpy as np

ROOT = Path("traffic_project/tsc_framework").resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ablation_real import build_ablation_extractors
build_ablation_extractors()

from stable_baselines3 import PPO

model_off = PPO.load(str(ROOT / "outputs" / "ablation_real" / "models" / "coopsarg_gating_off_seed42.zip"), device="cpu")
model_on = PPO.load(str(ROOT / "outputs" / "ablation_real" / "models" / "coopsarg_gating_on_seed42.zip"), device="cpu")

print("model_off policy:", type(model_off.policy.features_extractor))
print("model_on policy:", type(model_on.policy.features_extractor))

# Test random observation
obs = np.random.uniform(0, 1, (1, 34)).astype(np.float32)
act_off, _ = model_off.predict(obs, deterministic=True)
act_on, _ = model_on.predict(obs, deterministic=True)
print(f"Random obs: act_off={act_off}, act_on={act_on}")

# Test 50 random observations: how often do actions differ?
diffs = 0
for _ in range(100):
    o = np.random.uniform(0, 1, (1, 34)).astype(np.float32)
    a_off, _ = model_off.predict(o, deterministic=True)
    a_on, _ = model_on.predict(o, deterministic=True)
    if a_off != a_on:
        diffs += 1
print(f"Out of 100 random observations, actions differ in {diffs} cases.")
