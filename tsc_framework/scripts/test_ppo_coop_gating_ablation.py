import sys
from pathlib import Path
import numpy as np
import torch

ROOT = Path("traffic_project/tsc_framework").resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from stable_baselines3 import PPO

# Load the real main model
model_path = ROOT / "outputs" / "models" / "ppo_coop_chaos.zip"
model = PPO.load(str(model_path), device="cpu")

print("Loaded ppo_coop_chaos!")
extractor = model.policy.features_extractor
print("Extractor:", type(extractor))

# Test action distributions on 100 random observations: with gating vs without gating
diffs = 0
for i in range(100):
    o = np.random.uniform(0, 1, (1, 34)).astype(np.float32)
    t_o = torch.tensor(o)
    
    # 1. Normal predict (Gating ON)
    with torch.no_grad():
        dist_on = model.policy.get_distribution(t_o)
        act_on = dist_on.get_actions(deterministic=True).item()
        
    # 2. Monkey patch forward to disable equity boost (Gating OFF: equity_boost = 1.0)
    orig_forward = extractor.forward
    def forward_no_equity(observations):
        batch_size = observations.shape[0]
        queues = observations[:, 0:12]
        waits = observations[:, 12:24]
        pressures = observations[:, 24:28]
        nominal_features = observations[:, 28:34]
        nominal_latent = extractor.nominal_net(nominal_features)
        max_q, _ = torch.max(queues, dim=-1, keepdim=True)
        resilience_scale = torch.exp(max_q / 10.0)
        pressures_resilient = pressures * resilience_scale
        lane_pressure = torch.repeat_interleave(pressures_resilient, repeats=3, dim=-1)
        risk_grouped = torch.stack([queues, waits, lane_pressure], dim=-1)
        risk_embed = extractor.carril_embed(risk_grouped)
        attn_output, attn_weights = extractor.self_attention(risk_embed, risk_embed, risk_embed)
        gates = extractor.risk_gating(attn_output)
        
        # ABLATION: No equity boost! (equity_boost ≡ 1)
        equity_boost = torch.ones(batch_size, 12, device=attn_output.device)
        gated_risk = attn_output * (gates * equity_boost.unsqueeze(-1))
        gated_risk_flat = gated_risk.reshape(batch_size, -1)
        risk_latent = extractor.risk_reducer(gated_risk_flat)
        combined = torch.cat([nominal_latent, risk_latent], dim=-1)
        return extractor.fusion_net(combined)
        
    extractor.forward = forward_no_equity
    with torch.no_grad():
        dist_off = model.policy.get_distribution(t_o)
        act_off = dist_off.get_actions(deterministic=True).item()
    extractor.forward = orig_forward
    
    if act_on != act_off:
        diffs += 1

print(f"In ppo_coop_chaos, disabling equity boost changes the action in {diffs}/100 observations!")
