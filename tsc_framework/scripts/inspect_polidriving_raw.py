import sys
from pathlib import Path
import pandas as pd

csv_path = Path("traffic_project/tsc_framework/data/quito_behavior/micro_behavior.csv")
print(f"File exists: {csv_path.exists()}")

df_head = pd.read_csv(csv_path, nrows=50)
print("\n--- COLUMNS ---")
print(df_head.columns.tolist())

print("\n--- SAMPLE ROWS ---")
for col in ["timestamp", "time", "speed", "accel", "acceleration", "jerk", "driver_id"]:
    if col in df_head.columns:
        print(f"Column '{col}' sample:\n{df_head[col].head(5)}\n")

# Check time difference between consecutive rows for same driver
df_full = pd.read_csv(csv_path, nrows=1000)
for time_col in ["timestamp", "time", "date"]:
    if time_col in df_full.columns:
        print(f"Found time col: {time_col}")
