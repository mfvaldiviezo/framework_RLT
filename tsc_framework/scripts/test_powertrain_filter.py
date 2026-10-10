import numpy as np
import pandas as pd
from pathlib import Path
from sumolib import checkBinary
import traci

NET_FILE = Path("traffic_project/tsc_framework/sumo_configs/networks/quito.net.xml")
ROU_FILE = Path("traffic_project/tsc_framework/sumo_configs/routes/quito.net_multi_agent_mid.rou.xml")

# Load empirical furious jerk
df_emp = pd.read_csv("traffic_project/tsc_framework/data/quito_behavior/micro_behavior.csv")
furious = df_emp[(df_emp["driver_id"] == "furious") & (df_emp["speed"] > 5.0)]
emp_jerk = furious["jerk"].abs().dropna().values
print("Empirical Furious Jerk percentiles:")
for q in [0.5, 0.9, 0.95, 0.99]:
    print(f"  P{int(q*100)}: {np.percentile(emp_jerk, q*100):.3f}")

# Test with moving average filter on SUMO trajectory (filter window: 2s or EMA alpha=0.5)
def test_smoothing(alpha=0.5, sigma=0.5, tau=0.8, steps=250):
    cmd = [
        checkBinary("sumo"),
        "-n", str(NET_FILE),
        "-r", str(ROU_FILE),
        "--no-warnings", "true",
        "--seed", "42",
        "--begin", "0",
        "--end", str(steps)
    ]
    traci.start(cmd)
    raw_jerks = []
    smoothed_jerks = []
    
    speeds = {}
    smooth_accs = {}
    
    for s in range(steps):
        traci.simulationStep()
        for v in traci.vehicle.getIDList():
            if v not in speeds:
                speeds[v] = []
                smooth_accs[v] = []
                try:
                    traci.vehicle.setTau(v, tau)
                    traci.vehicle.setImperfection(v, sigma)
                except:
                    pass
            try:
                spd = traci.vehicle.getSpeed(v)
            except:
                continue
            speeds[v].append(spd)
            if len(speeds[v]) >= 2:
                a_raw = speeds[v][-1] - speeds[v][-2]
                # EMA smoothing for acceleration (representing engine/powertrain inertia)
                if len(smooth_accs[v]) == 0:
                    a_smooth = a_raw
                else:
                    a_smooth = alpha * a_raw + (1 - alpha) * smooth_accs[v][-1]
                smooth_accs[v].append(a_smooth)
                
                if len(smooth_accs[v]) >= 2:
                    j_raw = a_raw - (speeds[v][-2] - speeds[v][-3]) if len(speeds[v]) >= 3 else 0
                    j_smooth = smooth_accs[v][-1] - smooth_accs[v][-2]
                    if spd > 1.39:
                        raw_jerks.append(abs(j_raw))
                        smoothed_jerks.append(abs(j_smooth))
    traci.close()
    
    rj = np.array(raw_jerks)
    sj = np.array(smoothed_jerks)
    print(f"\nSmoothing alpha={alpha}, sigma={sigma}, tau={tau}:")
    print(f"  Raw Jerk: P50={np.percentile(rj, 50):.3f}, P90={np.percentile(rj, 90):.3f}, P95={np.percentile(rj, 95):.3f}")
    print(f"  Smoothed Jerk: P50={np.percentile(sj, 50):.3f}, P90={np.percentile(sj, 90):.3f}, P95={np.percentile(sj, 95):.3f}")

test_smoothing(alpha=0.3, sigma=0.5, tau=0.8)
test_smoothing(alpha=0.2, sigma=0.3, tau=1.0)
