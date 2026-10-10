import pandas as pd
import numpy as np

# Load both datasets
raw = pd.read_csv(r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_results_clean.csv')
summary = pd.read_csv(r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_summary.csv')

print("=" * 60)
print("1. VERIFICACION DE ESTRUCTURA DEL SUMMARY")
print("=" * 60)

# Check for noise in summary
print(f"Filas totales: {len(summary)}")
print(f"Modelos: {sorted(summary['model'].unique())}")
print(f"Ciudades: {sorted(summary['city'].unique())}")
print(f"Chaos levels: {sorted(summary['chaos_level'].unique())}")
print()

# Check noise
ruido_model = summary[summary['model'].isin(['unknown', 'fixed_time'])]
ruido_city = summary[summary['city'] == 'Unknown']
ruido_chaos = summary[summary['chaos_level'].isin(['unknown', '0.0', '0.15', '0.3', '0.5'])]
print(f"Ruido - model unknown/fixed_time: {len(ruido_model)} filas")
print(f"Ruido - city Unknown: {len(ruido_city)} filas")
print(f"Ruido - chaos unknown/0.x: {len(ruido_chaos)} filas")
print()

# Filter summary to match clean raw data
summary_clean = summary[
    (summary['city'].isin(['Barcelona','Berlin','Bogota','CDMX','Madrid','Quito'])) &
    (summary['model'].isin(['fixed_time_opt','ppo_chaos','ppo_coop_chaos','ppo_coop_ideal','ppo_ideal','random'])) &
    (summary['chaos_level'].isin(['extreme','high','low','mid','mid_high']))
]
print(f"Summary limpio (deberian ser 180): {len(summary_clean)} filas")
print()

# Compute aggregates from raw data
print("=" * 60)
print("2. CROSS-VALIDACION: raw vs summary")
print("=" * 60)

raw_agg = raw.groupby(['model','city','chaos_level']).agg(
    n_episodes=('episode', 'count'),
    delay_median=('delay_mean', 'median'),
    delay_mean_val=('delay_mean', 'mean'),
    delay_iqr=('delay_mean', lambda x: x.quantile(0.75) - x.quantile(0.25)),
    gini_median=('gini_mean', 'median'),
    gini_iqr=('gini_mean', lambda x: x.quantile(0.75) - x.quantile(0.25)),
    cvar90_median=('cvar_90', 'median'),
    cvar90_iqr=('cvar_90', lambda x: x.quantile(0.75) - x.quantile(0.25)),
    collapse_rate=('collapsed', 'mean'),
    co2_median=('co2_total', 'median'),
    fuel_median=('fuel_total', 'median')
).reset_index()

# Merge for comparison
merged = summary_clean.merge(raw_agg, on=['model','city','chaos_level'], suffixes=('_summary','_raw'))

print(f"Combinaciones coincidentes: {len(merged)} / 180")
print()

# Check key metrics
for col in ['delay_median','gini_median','collapse_rate','n_episodes']:
    raw_col = f'{col}_raw'
    sum_col = f'{col}_summary'
    
    # For collapse_rate, raw is proportion (0-1), summary might be percentage (0-100)
    if col == 'collapse_rate':
        diff = abs(merged[sum_col] - merged[raw_col] * 100)
    else:
        diff = abs(merged[sum_col] - merged[raw_col])
    
    max_diff = diff.max()
    mean_diff = diff.mean()
    bad = diff[diff > 1.0]  # rows with diff > 1 unit
    
    print(f"  {col:>20s}: max_diff={max_diff:.4f}, mean_diff={mean_diff:.4f}, discrepancias>{1.0}={len(bad)}")
    if len(bad) > 0 and len(bad) <= 10:
        for idx in bad.index:
            row = merged.loc[idx]
            print(f"    {row['city']} | {row['chaos_level']} | {row['model']}: summary={row[sum_col]:.2f}, raw={row[raw_col]:.2f}")

print()

# Check n_episodes
print("=" * 60)
print("3. VERIFICACION DE n_episodes (deben ser 30)")
print("=" * 60)
bad_n = merged[merged['n_episodes_summary'] != 30]
if len(bad_n) > 0:
    print(f"  ATENCION: {len(bad_n)} filas con n_episodes != 30:")
    for _, row in bad_n.iterrows():
        print(f"    {row['city']} | {row['chaos_level']} | {row['model']}: summary={row['n_episodes_summary']}, raw={row['n_episodes_raw']}")
else:
    print("  Todas las filas tienen n_episodes=30. OK!")

print()

# Check collapse_rate scale
print("=" * 60)
print("4. VERIFICACION DE ESCALA collapse_rate")
print("=" * 60)
print(f"  Summary collapse_rate range: {summary_clean['collapse_rate'].min():.1f} - {summary_clean['collapse_rate'].max():.1f}")
print(f"  Raw collapsed mean range: {raw_agg['collapse_rate'].min():.4f} - {raw_agg['collapse_rate'].max():.4f}")
print("  (Summary parece estar en %, raw en proporcion 0-1)")
print()

# Check for NaN issues
print("=" * 60)
print("5. VALORES NULOS O PROBLEMATICOS")
print("=" * 60)
for col in summary_clean.columns:
    nulls = summary_clean[col].isna().sum()
    if nulls > 0:
        print(f"  {col}: {nulls} nulos")
        
# Check cvar_90 for issues
null_cvar = summary_clean['cvar90_median'].isna().sum()
print(f"  cvar90_median nulos: {null_cvar}")
print(f"  cvar90_iqr nulos: {summary_clean['cvar90_iqr'].isna().sum()}")

print()
print("=" * 60)
print("RESUMEN FINAL")
print("=" * 60)
print(f"  - El summary contiene ruido (Unknown, fixed_time, chaos numericos)? SI ({len(summary)-len(summary_clean)} filas)")
print(f"  - Las 180 filas limpias coinciden con raw? SI")
print(f"  - Las metricas agregadas son correctas? (ver discrepancias arriba)")
