import sys
from pathlib import Path
import numpy as np
import torch

ROOT = Path("traffic_project/tsc_framework").resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from stable_baselines3 import PPO
model = PPO.load(str(ROOT / "outputs" / "models" / "ppo_coop_chaos.zip"), device="cpu")

print("Action net bias:", model.policy.action_net.bias.detach().numpy())
print("Action net weight norm:", torch.norm(model.policy.action_net.weight).item())

for i in range(5):
    o = torch.tensor(np.random.uniform(0, 1, (1, 34)).astype(np.float32))
    dist = model.policy.get_distribution(o)
    print(f"Sample {i} action probs:", dist.distribution.probs.detach().numpy())
