import sys
from pathlib import Path
import numpy as np
import torch

ROOT = Path("traffic_project/tsc_framework").resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from stable_baselines3 import PPO

model = PPO.load(str(ROOT / "outputs" / "models" / "ppo_coop_chaos.zip"), device="cpu")
extractor = model.policy.features_extractor

# Check fusion_net weights:
# combined has 80 dimensions: nominal_latent is 0:16, risk_latent is 16:80
W_fusion = extractor.fusion_net[0].weight.detach().numpy() # shape (128, 80)
print("Fusion net input dim:", W_fusion.shape)
w_nominal_norm = np.linalg.norm(W_fusion[:, :16])
w_risk_norm = np.linalg.norm(W_fusion[:, 16:])
print(f"Norm of nominal branch weights: {w_nominal_norm:.4f}")
print(f"Norm of risk branch weights: {w_risk_norm:.4f}")

# Check what happens to logits when risk branch is zeroed out vs normal:
o = torch.tensor(np.random.uniform(0, 1, (10, 34)).astype(np.float32))
dist_norm = model.policy.get_distribution(o)
logits_norm = dist_norm.distribution.logits.detach().numpy()

# Zero out risk branch
orig_forward = extractor.forward
def forward_zero_risk(observations):
    nominal_features = observations[:, 28:34]
    nominal_latent = extractor.nominal_net(nominal_features)
    risk_latent = torch.zeros(observations.shape[0], 64, device=observations.device)
    combined = torch.cat([nominal_latent, risk_latent], dim=-1)
    return extractor.fusion_net(combined)

extractor.forward = forward_zero_risk
dist_zero = model.policy.get_distribution(o)
logits_zero = dist_zero.distribution.logits.detach().numpy()
extractor.forward = orig_forward

print("\nLogits Normal vs Zero-Risk (sample 0):")
print("  Normal   :", logits_norm[0])
print("  Zero-risk:", logits_zero[0])
print("  Action Normal   :", np.argmax(logits_norm, axis=-1))
print("  Action Zero-risk:", np.argmax(logits_zero, axis=-1))
print("  Matches:", np.sum(np.argmax(logits_norm, axis=-1) == np.argmax(logits_zero, axis=-1)), "/ 10")
