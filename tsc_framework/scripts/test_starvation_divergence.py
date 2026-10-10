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

# Create 50 realistic traffic scenarios with acute starvation:
# One approach (3 lanes) has severe wait (300s, w=1.0) and queues (40 veh, q=0.8)
# Other approaches have low wait (10s, w=0.03) and medium queue (5 veh, q=0.1)
diffs = 0
for starved_lane_group in [0, 3, 6, 9]:
    for phase in range(4):
        for age in [10, 30, 60, 90]:
            o = np.zeros((1, 34), dtype=np.float32)
            # Normal traffic on all lanes
            o[0, 0:12] = 0.1 # queues
            o[0, 12:24] = 0.05 # waits
            o[0, 24:28] = 0.2 # pressures
            
            # Starvation on specific lane group
            o[0, starved_lane_group:starved_lane_group+3] = 0.8
            o[0, 12+starved_lane_group:12+starved_lane_group+3] = 0.95
            o[0, 24 + (starved_lane_group//3)] = 0.9 # high downstream pressure
            
            # Phase
            o[0, 28 + phase] = 1.0
            o[0, 32] = age / 120.0
            o[0, 33] = min(1.0, age / 120.0)
            
            t_o = torch.tensor(o)
            
            # 1. Normal predict (Gating ON)
            with torch.no_grad():
                dist_on = model.policy.get_distribution(t_o)
                act_on = dist_on.get_actions(deterministic=True).item()
                
            # 2. Gating OFF: gated_risk = attn_output (pass-through)
            orig_forward = extractor.forward
            def forward_no_gating(observations):
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
                
                # Pass through
                gated_risk = attn_output
                gated_risk_flat = gated_risk.reshape(batch_size, -1)
                risk_latent = extractor.risk_reducer(gated_risk_flat)
                combined = torch.cat([nominal_latent, risk_latent], dim=-1)
                return extractor.fusion_net(combined)
                
            extractor.forward = forward_no_gating
            with torch.no_grad():
                dist_off = model.policy.get_distribution(t_o)
                act_off = dist_off.get_actions(deterministic=True).item()
            extractor.forward = orig_forward
            
            if act_on != act_off:
                diffs += 1
                print(f"Group {starved_lane_group}, Phase {phase}, Age {age}: Gating ON -> act {act_on}, Gating OFF -> act {act_off}")

print(f"\nTotal action divergence under starvation states: {diffs} / 64 scenarios!")
