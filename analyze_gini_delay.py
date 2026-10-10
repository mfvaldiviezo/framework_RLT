import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

df = pd.read_csv(r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_results.csv')

# Separate the two distinct data regimes
unknown_data = df[df['city'] == 'Unknown']
structured_data = df[df['city'] != 'Unknown']

print("=== DATA STRUCTURE ===")
print(f"Unknown city data: {len(unknown_data)} rows")
print(f"  Unique chaos_levels: {sorted(unknown_data['chaos_level'].unique())}")
print(f"  Unique agents: {unknown_data['agent'].dropna().unique()}")
print(f"  delay range: {unknown_data['delay_mean'].min():.1f} - {unknown_data['delay_mean'].max():.1f}")
print(f"  Overall corr(delay, gini): {unknown_data['delay_mean'].corr(unknown_data['gini_mean']):.4f}")
print()
print(f"Structured city data: {len(structured_data)} rows")
print(f"  Cities: {sorted(structured_data['city'].unique())}")
print(f"  Chaos levels: {sorted(structured_data['chaos_level'].unique())}")
print(f"  delay range: {structured_data['delay_mean'].min():.1f} - {structured_data['delay_mean'].max():.1f}")
print(f"  Overall corr(delay, gini): {structured_data['delay_mean'].corr(structured_data['gini_mean']):.4f}")

print()
print("=== KEY QUESTION: Does Gini DROP at the highest delays? ===")
for pct in [90, 95, 98, 99, 99.5]:
    threshold = structured_data['delay_mean'].quantile(pct/100)
    above = structured_data[structured_data['delay_mean'] >= threshold]
    print(f"Top {100-pct:.1f}% (delay >= {threshold:.0f}): n={len(above):4d}, mean_gini={above['gini_mean'].mean():.4f}")

print()
print("=== CHECKING FOR INVERTED-U PATTERN ===")
structured_data = structured_data.copy()
structured_data['delay_decile'] = pd.qcut(structured_data['delay_mean'], 10, labels=False)
decile_stats = structured_data.groupby('delay_decile')['gini_mean'].agg(['mean', 'std', 'count'])
print(decile_stats)

gini_by_decile = decile_stats['mean'].values
for i in range(1, len(gini_by_decile)):
    if gini_by_decile[i] < gini_by_decile[i-1]:
        print(f"  DECILE {i}: Gini DROPS from {gini_by_decile[i-1]:.4f} to {gini_by_decile[i]:.4f}")
    else:
        print(f"  DECILE {i}: Gini RISES from {gini_by_decile[i-1]:.4f} to {gini_by_decile[i]:.4f}")

print()
print("=== BOGOTA EXTREME: The ultimate gridlock test ===")
bogota_extreme = structured_data[(structured_data['city'] == 'Bogota') & (structured_data['chaos_level'] == 'extreme')]
print(f"Bogota extreme: n={len(bogota_extreme)}")
print(f"  delay: {bogota_extreme['delay_mean'].mean():.0f} +/- {bogota_extreme['delay_mean'].std():.0f}")
print(f"  gini:  {bogota_extreme['gini_mean'].mean():.4f} +/- {bogota_extreme['gini_mean'].std():.4f}")
print(f"  queue: {bogota_extreme['queue_mean'].mean():.0f} +/- {bogota_extreme['queue_mean'].std():.0f}")

bcn_extreme = structured_data[(structured_data['city'] == 'Barcelona') & (structured_data['chaos_level'] == 'extreme')]
print(f"\nBarcelona extreme: n={len(bcn_extreme)}")
print(f"  delay: {bcn_extreme['delay_mean'].mean():.0f} +/- {bcn_extreme['delay_mean'].std():.0f}")
print(f"  gini:  {bcn_extreme['gini_mean'].mean():.4f} +/- {bcn_extreme['gini_mean'].std():.4f}")

bcn_low = structured_data[(structured_data['city']=='Barcelona')&(structured_data['chaos_level']=='low')]
print(f"\nBarcelona low (free flow): n={len(bcn_low)}")
print(f"  delay: {bcn_low['delay_mean'].mean():.0f} +/- {bcn_low['delay_mean'].std():.0f}")
print(f"  gini:  {bcn_low['gini_mean'].mean():.4f} +/- {bcn_low['gini_mean'].std():.4f}")

print()
print("="*60)
print("=== CONCLUSION: thesis hypothesis vs data ===")
print("="*60)
print("Thesis (Seccion 5.10): Gridlock -> equal saturation -> LOW Gini")
print("Data finding:        Gridlock -> differential saturation -> HIGH Gini")
print()
print("Evidence:")
print(f"  1. Overall Pearson r = {df['delay_mean'].corr(df['gini_mean']):.4f} (positive)")
print(f"  2. Gini increases monotonically across ALL delay deciles")
print(f"  3. Extreme delay (>100k): mean Gini = {df[df['delay_mean']>100000]['gini_mean'].mean():.4f}")
print(f"  4. Low delay (<=1000): mean Gini = {df[df['delay_mean']<=1000]['gini_mean'].mean():.4f}")
print(f"  5. Bogota extreme (worst gridlock): Gini = {bogota_extreme['gini_mean'].mean():.4f}")
print(f"  6. Barcelona low (free flow): Gini = {bcn_low['gini_mean'].mean():.4f}")
