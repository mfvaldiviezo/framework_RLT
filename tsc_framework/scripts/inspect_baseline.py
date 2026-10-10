import pandas as pd
from pathlib import Path

csv_path = Path("traffic_project/tsc_framework/outputs/results_original_20260622_1330/master_results_clean.csv")
df = pd.read_csv(csv_path)

coop = df[df["model"] == "ppo_coop_chaos"]
cities = ["Barcelona", "Madrid", "Berlin", "CDMX", "Bogota", "Quito"]
sats = ["low", "mid", "mid_high", "high", "extreme"]

print(f"Total rows for ppo_coop_chaos: {len(coop)}")

for c in cities:
    print(f"\n--- City: {c} ---")
    for s in sats:
        sub = coop[(coop["city"] == c) & (coop["chaos_level"] == s)]
        gini_m = sub["gini_mean"].mean()
        gini_s = sub["gini_mean"].std()
        delay_m = sub["delay_mean"].mean()
        queue_m = sub["queue_mean"].mean()
        print(f"  {s:8s} | Gini: {gini_m:.4f} ± {gini_s:.4f} | Delay: {delay_m:8.1f} s | Queue: {queue_m:5.1f} | N={len(sub)}")
