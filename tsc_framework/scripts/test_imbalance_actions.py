import sys
from pathlib import Path
import numpy as np
import torch

ROOT = Path("traffic_project/tsc_framework").resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ablation_real import build_ablation_extractors
build_ablation_extractors()

from stable_baselines3 import PPO

model_off = PPO.load(str(ROOT / "outputs" / "ablation_real" / "models" / "coopsarg_gating_off_seed42.zip"), device="cpu")
model_on = PPO.load(str(ROOT / "outputs" / "ablation_real" / "models" / "coopsarg_gating_on_seed42.zip"), device="cpu")

# Print action probabilities for an observation with extreme imbalance in waits
# carriles 0-11: queues, 12-23: waits
o = np.zeros((1, 34), dtype=np.float32)
# Lane 0 has 200s wait, others have 0
o[0, 12] = 200.0 / 300.0
# Lane 0 has 20 queue
o[0, 0] = 20.0 / 50.0

with torch.no_grad():
    t_o = torch.tensor(o)
    dist_off = model_off.policy.get_distribution(t_o)
    dist_on = model_on.policy.get_distribution(t_o)
    print("Action distribution OFF:", dist_off.distribution.probs.numpy())
    print("Action distribution ON :", dist_on.distribution.probs.numpy())
