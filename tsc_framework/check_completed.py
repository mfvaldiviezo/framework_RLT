import pandas as pd
import glob
import os

files = glob.glob('outputs/results/transfer_n30*detailed.csv')
print(f"Archivos encontrados: {files}")

if not files:
    print("No se encontraron archivos.")
    exit()

df = pd.concat([pd.read_csv(f) for f in files])

grouped = df.groupby(['city', 'model', 'chaos_level']).size().reset_index(name='count')
print(grouped.to_string())

# Calculate missing
all_cities = ["Barcelona", "Quito", "Bogota", "Berlin", "Madrid", "CDMX"]
all_models = ["ppo_coop_ideal", "ppo_coop_chaos", "ppo_chaos", "fixed_time_opt", "random"] 
# Did the user say ppo_ideal? The script doesn't have it by default. 
all_chaos = ["low", "mid", "mid_high", "high", "extreme"]

print("\n--- COMBINACIONES FALTANTES ---")
for c in all_cities:
    for m in all_models:
        for ch in all_chaos:
            mask = (grouped['city'] == c) & (grouped['model'] == m) & (grouped['chaos_level'] == ch)
            if mask.sum() == 0 or grouped[mask]['count'].iloc[0] < 30:
                count = grouped[mask]['count'].iloc[0] if mask.sum() > 0 else 0
                print(f"Falta: {c} | {m} | {ch} (Tiene {count}/30)")
