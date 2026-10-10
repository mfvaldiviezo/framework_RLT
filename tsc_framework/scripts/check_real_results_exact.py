import pandas as pd

df = pd.read_csv("traffic_project/tsc_framework/outputs/ablation_real/results/ablation_real_results.csv")
print("Total rows:", len(df))
print("Columns:", df.columns.tolist())
print("\nVariants:", df["variant"].value_counts())
print("\nCities:", df["city"].value_counts())
print("\nChaos levels:", df["chaos_level"].value_counts())

print("\n--- GROUPBY (city, variant, chaos_level) Gini Mean ---")
grouped = df.groupby(["city", "chaos_level", "variant"])["gini_mean"].mean().unstack()
print(grouped)

print("\n--- COOP-SARG DELTA GINI (OFF - ON) ---")
if "coopsarg_gating_off" in grouped.columns and "coopsarg_gating_on" in grouped.columns:
    delta_coop = grouped["coopsarg_gating_off"] - grouped["coopsarg_gating_on"]
    print(delta_coop)

print("\n--- H-SARG DELTA GINI (OFF - ON) ---")
if "hsarg_gating_off" in grouped.columns and "hsarg_gating_on" in grouped.columns:
    delta_hsarg = grouped["hsarg_gating_off"] - grouped["hsarg_gating_on"]
    print(delta_hsarg)
