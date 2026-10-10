import pandas as pd
from pathlib import Path

raw_dir = Path("traffic_project/tsc_framework/data/raw/polidriving")
csvs = list(raw_dir.rglob("*.csv"))
print(f"Total CSVs in raw polidriving: {len(csvs)}")

# Look for files belonging to 'furious' or similar
for c in csvs[:10]:
    print(c.relative_to(raw_dir))

# Check one furious file or one raw file
sample = [c for c in csvs if "furious" in str(c).lower()]
if sample:
    print("\nSample furious file:", sample[0])
    df = pd.read_csv(sample[0], nrows=20)
    print("Columns in furious:", df.columns.tolist())
    print(df.head())
else:
    print("No file with furious in path. Finding where furious driver comes from:")
    df_micro = pd.read_csv("traffic_project/tsc_framework/data/quito_behavior/micro_behavior.csv", nrows=1000)
    print(df_micro[df_micro["driver_id"] == "furious"][["driver_id", "source_file"]].head())
