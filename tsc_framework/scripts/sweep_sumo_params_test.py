import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Run SUMO with different sigma and tau
from sumolib import checkBinary
import traci

NET_FILE = Path("traffic_project/tsc_framework/sumo_configs/networks/quito.net.xml")
ROU_FILE = Path("traffic_project/tsc_framework/sumo_configs/routes/quito.net_multi_agent_mid.rou.xml")

def test_sumo_params(sigma, tau, steps=300):
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
    
    speeds = {}
    accels = {}
    jerks = []
    accs = []
    
    for step in range(steps):
        traci.simulationStep()
        for v in traci.vehicle.getIDList():
            if v not in speeds:
                speeds[v] = []
                accels[v] = []
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
                a = speeds[v][-1] - speeds[v][-2]
                accels[v].append(a)
                if len(accels[v]) >= 2:
                    j = accels[v][-1] - accels[v][-2]
                    if spd > 1.39: # moving
                        jerks.append(abs(j))
                        accs.append(abs(a))
    traci.close()
    
    j_arr = np.array(jerks)
    a_arr = np.array(accs)
    return {
        "sigma": sigma,
        "tau": tau,
        "n": len(j_arr),
        "jerk_p50": np.percentile(j_arr, 50) if len(j_arr) > 0 else 0,
        "jerk_p90": np.percentile(j_arr, 90) if len(j_arr) > 0 else 0,
        "jerk_p95": np.percentile(j_arr, 95) if len(j_arr) > 0 else 0,
        "jerk_p99": np.percentile(j_arr, 99) if len(j_arr) > 0 else 0,
        "acc_p50": np.percentile(a_arr, 50) if len(a_arr) > 0 else 0,
        "acc_p90": np.percentile(a_arr, 90) if len(a_arr) > 0 else 0,
    }

configs = [
    (0.0, 1.4),
    (0.1, 1.4),
    (0.2, 1.4),
    (0.3, 1.0),
    (0.5, 0.8),
    (0.7, 0.6),
    (0.9, 0.5),
]

results = []
for s, t in configs:
    res = test_sumo_params(s, t, steps=250)
    print(f"sigma={s}, tau={t} -> jerk P50={res['jerk_p50']:.3f}, P90={res['jerk_p90']:.3f}, P95={res['jerk_p95']:.3f}, P99={res['jerk_p99']:.3f} | acc P50={res['acc_p50']:.3f}, P90={res['acc_p90']:.3f}")
    results.append(res)
