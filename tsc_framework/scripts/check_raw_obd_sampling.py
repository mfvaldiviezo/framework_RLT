import pandas as pd
from pathlib import Path

raw_file = Path("traffic_project/tsc_framework/data/raw/polidriving/furious/20231226_150915/2023-12-26 15-09-15.csv")
df = pd.read_csv(raw_file, low_memory=False)

accel_col = "Vehicle acceleration (m/s²)"
accel_data = df[["time", accel_col]].dropna(subset=[accel_col]).copy()
print(f"Total rows with acceleration in raw OBD: {len(accel_data):,}")
print("First 10 rows:")
print(accel_data.head(10))

# Parse time to find delta t
accel_data["dt"] = pd.to_datetime(accel_data["time"], format="%H:%M:%S.%f", errors="coerce")
accel_data["time_diff_sec"] = accel_data["dt"].diff().dt.total_seconds()
print("\nDelta t statistics between consecutive acceleration readings:")
print(accel_data["time_diff_sec"].describe())
print("\nPercentiles of dt (seconds):", accel_data["time_diff_sec"].quantile([0.1, 0.25, 0.5, 0.75, 0.9, 0.99]))
