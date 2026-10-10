import zipfile
import json
from pathlib import Path

p1 = Path("traffic_project/tsc_framework/outputs/models/ppo_coop_chaos.zip")
p2 = Path("traffic_project/tsc_framework/outputs/ablation_real/models/coopsarg_gating_off_seed42.zip")

print("Files in ppo_coop_chaos.zip:")
with zipfile.ZipFile(p1) as z:
    for name in z.namelist():
        print(" ", name, z.getinfo(name).file_size)

print("\nFiles in coopsarg_gating_off_seed42.zip:")
with zipfile.ZipFile(p2) as z:
    for name in z.namelist():
        print(" ", name, z.getinfo(name).file_size)
