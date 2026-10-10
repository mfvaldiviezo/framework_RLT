import pandas as pd
import numpy as np
from pathlib import Path

csv_path = Path("traffic_project/tsc_framework/data/quito_behavior/micro_behavior.csv")
df = pd.read_csv(csv_path, low_memory=False)

print(f"Total rows in micro_behavior.csv: {len(df):,}")
print(f"Drivers: {df['driver_id'].unique().tolist()}")

moving = df[df["speed"] > 5.0]
print(f"Moving rows (speed > 5): {len(moving):,}")

for driver in ["all", "furious", "alonso"]:
    sub = moving if driver == "all" else moving[moving["driver_id"] == driver]
    print(f"\n=================== DRIVER: {driver} (N={len(sub):,}) ===================")
    for col in ["speed", "accel_magnitude", "jerk"]:
        if col in sub.columns:
            s = sub[col].abs().dropna()
            p = np.percentile(s, [10, 25, 50, 75, 90, 95, 99])
            print(f"{col:15s} | Mean={s.mean():.4f} | Std={s.std():.4f} | P50={p[2]:.4f} | P90={p[4]:.4f} | P95={p[5]:.4f} | P99={p[6]:.4f}")

# Check raw preprocessed file timestamps
raw_pre = Path("traffic_project/tsc_framework/data/raw/polidriving/furious/20231226_150915/20231226_150915_pre.csv")
if raw_pre.exists():
    df_pre = pd.read_csv(raw_pre)
    print("\nRaw pre file columns:", df_pre.columns.tolist()[:10])
    print(f"Raw pre rows: {len(df_pre):,}")
    print("Raw pre speed percentiles:", np.percentile(df_pre['speed'].dropna(), [50, 90, 95, 99]))
    print("Raw pre acceleration percentiles:", np.percentile(df_pre['acceleration'].dropna(), [50, 90, 95, 99]))
