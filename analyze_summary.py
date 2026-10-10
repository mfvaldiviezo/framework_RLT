import pandas as pd
import numpy as np

df = pd.read_csv(r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_summary.csv')

# Filter out noise: Unknown city, unknown model, fixed_time, chaos=unknown
clean = df[
    (df['city'] != 'Unknown') & 
    (df['model'] != 'unknown') & 
    (df['model'] != 'fixed_time') & 
    (df['chaos_level'] != 'unknown') &
    ~df['chaos_level'].isin(['0.0', '0.15', '0.3', '0.5'])
]

print("=" * 60)
print("DATASET LIMPIO (sin ruido)")
print("=" * 60)
print(f"Filas: {len(clean)}")
print(f"Modelos: {sorted(clean['model'].unique())}")
print(f"Chaos: {sorted(clean['chaos_level'].unique())}")
print(f"Esperado: 6 ciudades x 5 chaos x 6 modelos = 180")
print()

# CORRELATION BY CHAOS LEVEL
print("=" * 60)
print("GINI vs DELAY por CHAOS LEVEL (datos agregados)")
print("=" * 60)
for cl in sorted(clean['chaos_level'].unique()):
    sub = clean[clean['chaos_level'] == cl]
    c = sub['delay_median'].corr(sub['gini_median'])
    print(f"  {cl:>9s}: n={len(sub):2d}, corr={c:+.4f}, gini={sub['gini_median'].mean():.4f}, delay={sub['delay_median'].mean():.0f}, collapse={sub['collapse_rate'].mean():.1f}%")
print()

# CORRELATION BY MODEL
print("=" * 60)
print("GINI vs DELAY por MODELO (todos los chaos levels)")
print("=" * 60)
for m in sorted(clean['model'].unique()):
    sub = clean[clean['model'] == m]
    c = sub['delay_median'].corr(sub['gini_median'])
    print(f"  {m:>20s}: n={len(sub):2d}, corr={c:+.4f}, gini={sub['gini_median'].mean():.4f}, collapse_avg={sub['collapse_rate'].mean():.1f}%")
print()

# CORRELATION BY CITY x MODEL
print("=" * 60)
print("GINI vs DELAY: CIUDAD x MODELO (a traves de chaos levels)")
print("=" * 60)
for city in sorted(clean['city'].unique()):
    for model in sorted(clean['model'].unique()):
        sub = clean[(clean['city']==city) & (clean['model']==model)]
        if len(sub) >= 3:
            c = sub['delay_median'].corr(sub['gini_median'])
            print(f"  {city:>12s} x {model:>20s}: corr={c:+.4f}, gini_range={sub['gini_median'].min():.3f}-{sub['gini_median'].max():.3f}")

print()
# GINI vs COLLAPSE RATE
print("=" * 60)
print("GINI vs COLLAPSE RATE")
print("=" * 60)
corr_gc = clean['gini_median'].corr(clean['collapse_rate'])
print(f"Corr(gini, collapse_rate): {corr_gc:.4f}")
print()

# By collapse rate bins
clean['collapse_bin'] = pd.cut(clean['collapse_rate'], bins=[-1, 0.1, 50, 99, 101], labels=['0%','1-50%','51-99%','100%'])
print(clean.groupby('collapse_bin', observed=False)['gini_median'].describe())
print()

# The inverted-U question: does Gini drop at the highest delays?
print("=" * 60)
print("HAY UNA U INVERTIDA? (Gini en delays extremos)")
print("=" * 60)
clean['delay_bin'] = pd.qcut(clean['delay_median'], q=10, labels=False)
deciles = clean.groupby('delay_bin')['gini_median'].mean()
for i in range(len(deciles)):
    print(f"  Decil {i}: delay_medio={clean[clean['delay_bin']==i]['delay_median'].mean():.0f}, gini={deciles.iloc[i]:.4f}")

print()
# Best model by city
print("=" * 60)
print("MEJOR MODELO POR CIUDAD (menor delay mediano)")
print("=" * 60)
for city in sorted(clean['city'].unique()):
    print(f"\n  {city}:")
    city_data = clean[clean['city']==city]
    for cl in sorted(clean['chaos_level'].unique()):
        cl_data = city_data[city_data['chaos_level']==cl]
        if len(cl_data) > 0:
            best = cl_data.loc[cl_data['delay_median'].idxmin()]
            worst = cl_data.loc[cl_data['delay_median'].idxmax()]
            print(f"    {cl:>9s}: best={best['model']:>20s} (delay={best['delay_median']:.0f}, gini={best['gini_median']:.3f}) | worst={worst['model']:>20s} (delay={worst['delay_median']:.0f}, gini={worst['gini_median']:.3f})")
