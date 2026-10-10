import pandas as pd
df = pd.read_csv("traffic_project/tsc_framework/outputs/ablation_real/results/ablation_real_results.csv")
print("Cities in ablation_real_results.csv:", df["city"].unique())
print("Variants:", df["variant"].unique())
print("Chaos levels:", df["chaos_level"].unique())
print("Total rows:", len(df))
print(df.groupby(["city", "variant", "chaos_level"])["gini_mean"].mean().unstack(level=1))
