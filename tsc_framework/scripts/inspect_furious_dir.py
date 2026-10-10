from pathlib import Path
import pandas as pd

p = Path("traffic_project/tsc_framework/data/raw/polidriving/furious/20231226_150915")
for f in p.glob("*"):
    print(f.name, f.stat().st_size)
    if f.suffix == ".csv":
        df = pd.read_csv(f, nrows=5)
        print("   Cols:", df.columns.tolist()[:8])
