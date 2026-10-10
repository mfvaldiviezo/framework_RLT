import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sumolib import checkBinary
import traci

NET_FILE = Path("traffic_project/tsc_framework/sumo_configs/networks/quito.net.xml")
ROU_FILE = Path("traffic_project/tsc_framework/sumo_configs/routes/quito.net_multi_agent_mid.rou.xml")

def test_step_length(step_len=0.1, total_sim_time=200):
    cmd = [
        checkBinary("sumo"),
        "-n", str(NET_FILE),
        "-r", str(ROU_FILE),
        "--step-length", str(step_len),
        "--no-warnings", "true",
        "--seed", "42",
        "--begin", "0",
        "--end", str(total_sim_time)
    ]
    traci.start(cmd)
    
    speeds = {}
    accels = {}
    jerks = []
    
    steps = int(total_sim_time / step_len)
    for s in range(steps):
        traci.simulationStep()
        for v in traci.vehicle.getIDList():
            if v not in speeds:
                speeds[v] = []
                accels[v] = []
            try:
                spd = traci.vehicle.getSpeed(v)
            except:
                continue
            speeds[v].append(spd)
            if len(speeds[v]) >= 2:
                a = (speeds[v][-1] - speeds[v][-2]) / step_len
                accels[v].append(a)
                if len(accels[v]) >= 2:
                    j = (accels[v][-1] - accels[v][-2]) / step_len
                    if spd > 1.39:
                        jerks.append(abs(j))
    traci.close()
    
    j_arr = np.array(jerks)
    print(f"\n--- Step length: {step_len} s (N={len(j_arr)}) ---")
    for q in [0.5, 0.9, 0.95, 0.99]:
        print(f"  P{int(q*100)}: {np.percentile(j_arr, q*100):.3f}")

test_step_length(0.2, total_sim_time=100)
