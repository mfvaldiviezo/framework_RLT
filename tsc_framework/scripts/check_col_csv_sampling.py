import pandas as pd
from pathlib import Path

p = Path("traffic_project/tsc_framework/data/raw/polidriving/furious/20231226_150915/20231226_150915_col.csv")
df = pd.read_csv(p)
t = pd.to_datetime(df["time"], format="%H:%M:%S", errors="coerce")
dt = t.diff().dt.total_seconds()
print("Time differences in 20231226_150915_col.csv:")
print(dt.describe())
print("Value counts of dt:")
print(dt.value_counts().head(10))

print("\nAcceleration in col.csv:")
print(df["acceleration"].describe())
print("Quantiles of abs(acceleration):")
print(df["acceleration"].abs().quantile([0.5, 0.9, 0.95, 0.99]))

# Check how acceleration is calculated in col.csv or how jerk behaves if calculated from col.csv
df["jerk"] = df["acceleration"].diff() / dt
print("\nJerk calculated as diff(acceleration)/dt in col.csv:")
print(df["jerk"].abs().describe())
print("Quantiles of abs(jerk):")
print(df["jerk"].abs().quantile([0.5, 0.9, 0.95, 0.99]))
