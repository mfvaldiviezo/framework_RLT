import pandas as pd
from pathlib import Path

csv_path = Path("traffic_project/tsc_framework/outputs/results_original_20260622_1330/master_results_clean.csv")
if csv_path.exists():
    df = pd.read_csv(csv_path, nrows=5)
    print("Columns in master_results_clean.csv:")
    print(df.columns.tolist())
    
    # Check TP or throughput columns
    tp_cols = [c for c in df.columns if "tp" in c.lower() or "through" in c.lower() or "flow" in c.lower()]
    print("TP/Throughput candidate columns:", tp_cols)
    if tp_cols:
        print(df[tp_cols].head())
