import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# Paths
base_dir = r"c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework"
vol_det_path = os.path.join(base_dir, "outputs", "results_original_20260622_1330", "master_results_clean.csv")
beh_det_path = os.path.join(base_dir, "outputs", "results", "transfer_n30_multi_agent_latam_behavioral_detailed.csv")
figures_dir = os.path.join(base_dir, "outputs", "figures")
os.makedirs(figures_dir, exist_ok=True)

try:
    print("Cargando datos volumétricos...")
    df_vol = pd.read_csv(vol_det_path)
    print("Cargando datos conductuales...")
    df_beh = pd.read_csv(beh_det_path)
except Exception as e:
    print(f"Error al cargar archivos CSV: {e}")
    exit(1)

# Ensure required columns
df_vol['experiment'] = 'volumetric'
df_beh['experiment'] = 'behavioral'

# Combine for comparison
df_all = pd.concat([df_vol, df_beh], ignore_index=True)

# 1. Umbral de Bifurcación Física (Tasa de colapso)
print("Calculando métricas de bifurcación y Gini...")
collapse_rates = df_all.groupby(['experiment', 'city', 'chaos_level', 'model'])['collapsed'].mean().reset_index()
collapse_rates['collapsed_pct'] = collapse_rates['collapsed'] * 100

extreme_gini = df_all[df_all['chaos_level'] == 'extreme'].groupby(['experiment', 'city', 'model'])['gini_mean'].mean().reset_index()

# 2. Pruebas de Mann Whitney
print("Analizando tests estadísticos...")
quito_beh = df_beh[df_beh['city'] == 'Quito']
models = quito_beh['model'].unique()
quito_stats = []
if 'ppo_coop_chaos' in models and 'ppo_coop_ideal' in models:
    for chaos in quito_beh['chaos_level'].unique():
        a = quito_beh[(quito_beh['model'] == 'ppo_coop_chaos') & (quito_beh['chaos_level'] == chaos)]['delay_mean'].values
        b = quito_beh[(quito_beh['model'] == 'ppo_coop_ideal') & (quito_beh['chaos_level'] == chaos)]['delay_mean'].values
        if len(a) > 0 and len(b) > 0:
            stat, p = mannwhitneyu(a, b, alternative='two-sided')
            n1, n2 = len(a), len(b)
            r = 1.0 - (2.0 * stat) / (n1 * n2)
            quito_stats.append({'chaos_level': chaos, 'U': stat, 'p_value': p, 'r_effect': r, 'median_chaos': np.median(a), 'median_ideal': np.median(b)})

marginal_impact = []
for city in ['Barcelona', 'Quito', 'Madrid']:
    for chaos in ['low', 'extreme']:
        vol_delays = df_vol[(df_vol['city'] == city) & (df_vol['chaos_level'] == chaos)]['delay_mean'].values
        beh_delays = df_beh[(df_beh['city'] == city) & (df_beh['chaos_level'] == chaos)]['delay_mean'].values
        if len(vol_delays) > 0 and len(beh_delays) > 0:
            stat, p = mannwhitneyu(beh_delays, vol_delays, alternative='two-sided')
            marginal_impact.append({
                'city': city, 'chaos_level': chaos,
                'median_vol': np.median(vol_delays), 'median_beh': np.median(beh_delays),
                'p_value': p
            })

# Export text results
results_dict = {
    'collapse_rates': collapse_rates.to_dict(orient='records'),
    'extreme_gini': extreme_gini.to_dict(orient='records'),
    'quito_paradox': quito_stats,
    'marginal_impact': marginal_impact
}
results_path = os.path.join(base_dir, 'outputs', 'results', 'audit_stats_output.json')
with open(results_path, 'w') as f:
    json.dump(results_dict, f, indent=4)
print(f" Estadísticas guardadas en {results_path}")

# Visualizations
print("Generando visualizaciones...")

try:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_all[(df_all['chaos_level'] == 'extreme') & (df_all['experiment'] == 'behavioral')],
                    x='delay_mean', y='gini_mean', hue='city', style='model', s=100, alpha=0.7)
    plt.axvline(x=5000, color='r', linestyle='--', label='Umbral Bifurcación Físico')
    plt.title("Relación Delay-Gini en Nivel Extremo (Campaña Conductual)")
    plt.xlabel("Delay Promedio (s)")
    plt.ylabel("Índice de Gini (Desigualdad Espacial)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'scatter_delay_gini_extreme.png'), dpi=300)
    plt.close()
    
    heatmap_data = collapse_rates[collapse_rates['experiment'] == 'behavioral']
    if not heatmap_data.empty:
        pivot = heatmap_data.pivot_table(index='city', columns='chaos_level', values='collapsed_pct', aggfunc='mean')
        cols = ['low', 'mid', 'mid_high', 'high', 'extreme']
        cols = [c for c in cols if c in pivot.columns]
        pivot = pivot[cols]
        
        plt.figure(figsize=(8, 5))
        sns.heatmap(pivot, annot=True, cmap='Reds', fmt=".1f", vmin=0, vmax=100)
        plt.title("Tasa de Colapso Promedio (%) por Ciudad y Demanda\n(Campaña Conductual)")
        plt.ylabel("Ciudad")
        plt.xlabel("Nivel de Estrés (v/c)")
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'heatmap_collapse_rate.png'), dpi=300)
        plt.close()
    print(f" Visualizaciones guardadas en {figures_dir}")
except Exception as e:
    print(f"Error al generar gráficos: {e}")

print("¡Análisis completado exitosamente!")
