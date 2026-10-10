import time
import subprocess
import sys
from pathlib import Path

# Run 1 episode of Quito with transfer_eval_n30_robust.py
t0 = time.time()
cmd = [
    r"C:\Users\mfval\anaconda3\envs\tsc-env\python.exe",
    "traffic_project/tsc_framework/transfer_eval_n30_robust.py",
    "--models", "ppo_coop_chaos",
    "--cities", "Quito",
    "--chaos-levels", "high",
    "--episodes", "1",
    "--steps", "200",
    "--mode", "multi_agent",
    "--prefix", "test_speed"
]
print("Running command:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
elapsed = time.time() - t0
print(f"Elapsed: {elapsed:.2f} seconds")
print("Return code:", res.returncode)
print("STDOUT tail:")
print("\n".join(res.stdout.splitlines()[-10:]))
if res.stderr:
    print("STDERR tail:")
    print("\n".join(res.stderr.splitlines()[-10:]))
