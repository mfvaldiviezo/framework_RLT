import pandas as pd
import numpy as np
from pathlib import Path

csv_path = Path("traffic_project/tsc_framework/data/quito_behavior/micro_behavior.csv")
if not csv_path.exists():
    csv_path = Path("traffic_project/tsc_framework/data/processed/micro_behavior.csv")

print("Checking:", csv_path)
df = pd.read_csv(csv_path, nrows=50)
print("Columns:", df.columns.tolist())
print(df.head())

# Read full summary
df_full = pd.read_csv(csv_path, usecols=["driver_id", "speed", "accel_magnitude", "jerk"])
print("\nDataset shape:", df_full.shape)
print("Drivers:", df_full["driver_id"].value_counts())
print("\nPercentiles of jerk across all data:")
print(df_full["jerk"].abs().quantile([0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]))

print("\nPercentiles of accel_magnitude across all data:")
print(df_full["accel_magnitude"].abs().quantile([0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]))
