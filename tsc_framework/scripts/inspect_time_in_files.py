import pandas as pd
from pathlib import Path

p = Path("traffic_project/tsc_framework/data/raw/polidriving/furious/20231226_150915")
for name in ["2023-12-26 15-09-15.csv", "20231226_150915_col.csv", "20231226_150915_pre.csv", "20231226_150915_lab.csv"]:
    f = p / name
    if f.exists():
        df = pd.read_csv(f, nrows=10)
        print(f"\n--- {name} --- (rows: {len(pd.read_csv(f, usecols=[df.columns[0]]))})")
        print("Columns:", df.columns.tolist()[:6])
        if "time" in df.columns:
            print("Time col sample:", df["time"].head(3).tolist())
        if "observation_hour" in df.columns:
            print("observation_hour sample:", df["observation_hour"].head(3).tolist())
        if "acceleration" in df.columns:
            print("acceleration sample:", df["acceleration"].head(5).tolist())
