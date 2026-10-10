import sys
from pathlib import Path
ROOT = Path("traffic_project/tsc_framework").resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

# Also import ablation extractors so classes exist
from ablation_real import build_ablation_extractors
variants = build_ablation_extractors()

from stable_baselines3 import PPO
model_path = ROOT / "outputs" / "ablation_real" / "models" / "coopsarg_gating_off_seed42.zip"
m = PPO.load(str(model_path), device="cpu")
print("SUCCESSFULLY LOADED:", type(m), m.policy)
