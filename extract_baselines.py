import pandas as pd
import numpy as np
import json
import glob
import re
from pathlib import Path

# ============================================================
# EXTRACT BASELINE DATA FROM ALL BENCHMARK REPORTS
# ============================================================

benchmark_dir = Path(r'c:\Proyecto_Tesis_Final_V1\traffic_project\benchmark_reports')
report_files = sorted(benchmark_dir.glob('marl_eval_*.txt'))

print("=" * 80)
print("EXTRACCIÓN DE DATOS DE BENCHMARK REPORTS")
print("=" * 80)

all_results = []

for fpath in report_files:
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Extract run timestamp from filename
    timestamp = fpath.stem.replace('marl_eval_', '')
    
    # Parse the detailed results table
    # Pattern: ALGORITM    SCENARIO    Throughput  AvgQueue  Gini_temp  CVaR95  Gini_final  Time  OK
    table_pattern = re.findall(
        r'^\s*(\w+(?:\s+\w+)?)\s+(Ideal|LATAM Caótico)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([OK]|[FAIL])',
        content, re.MULTILINE
    )
    
    for match in table_pattern:
        algo, scenario, throughput, avg_queue, gini_temp, cvar95, gini_final, time_s, ok = match
        
        # Also try alternate pattern (some have Gini_final before time)
        all_results.append({
            'timestamp': timestamp,
            'algorithm': algo.strip(),
            'scenario': scenario.strip(),
            'throughput': float(throughput),
            'avg_queue': float(avg_queue),
            'gini_temp': float(gini_temp),
            'cvar95': float(cvar95),
            'gini_final': float(gini_final),
            'time_s': float(time_s),
            'ok': ok == '[OK]'
        })

df = pd.DataFrame(all_results)
print(f"Total registros extraídos: {len(df)}")
print(f"Algoritmos: {sorted(df['algorithm'].unique())}")
print(f"Escenarios: {sorted(df['scenario'].unique())}")
print()

# Filter to only valid (OK) runs
df_valid = df[df['ok']].copy()
print(f"Registros válidos (OK): {len(df_valid)}")

# Aggregate by algorithm and scenario (median across runs)
print("\n" + "=" * 80)
print("TABLA AGREGADA POR ALGORITMO Y ESCENARIO (mediana entre ejecuciones)")
print("=" * 80)

agg = df_valid.groupby(['algorithm', 'scenario']).agg(
    n_runs=('timestamp', 'count'),
    throughput_median=('throughput', 'median'),
    throughput_std=('throughput', 'std'),
    queue_median=('avg_queue', 'median'),
    gini_temp_median=('gini_temp', 'median'),
    cvar95_median=('cvar95', 'median'),
    gini_final_median=('gini_final', 'median'),
).round(4)

print(agg.to_string())
print()

# Compute degradation (LATAM vs Ideal)
print("\n" + "=" * 80)
print("DEGRADACIÓN BAJO CAOS (LATAM vs Ideal)")
print("=" * 80)

degradation = []
for algo in sorted(df_valid['algorithm'].unique()):
    ideal = df_valid[(df_valid['algorithm'] == algo) & (df_valid['scenario'] == 'Ideal')]
    latam = df_valid[(df_valid['algorithm'] == algo) & (df_valid['scenario'] == 'LATAM Caótico')]
    
    if len(ideal) > 0 and len(latam) > 0:
        t_ideal = ideal['throughput'].median()
        t_latam = latam['throughput'].median()
        g_ideal = ideal['gini_temp'].median()
        g_latam = latam['gini_temp'].median()
        c_ideal = ideal['cvar95'].median()
        c_latam = latam['cvar95'].median()
        q_ideal = ideal['avg_queue'].median()
        q_latam = latam['avg_queue'].median()
        
        degradation.append({
            'algorithm': algo,
            'throughput_ideal': t_ideal,
            'throughput_latam': t_latam,
            'delta_throughput_pct': ((t_latam - t_ideal) / abs(t_ideal) * 100) if t_ideal > 0.001 else float('nan'),
            'gini_ideal': g_ideal,
            'gini_latam': g_latam,
            'delta_gini_pct': ((g_latam - g_ideal) / abs(g_ideal) * 100) if g_ideal > 0.001 else float('nan'),
            'cvar95_ideal': c_ideal,
            'cvar95_latam': c_latam,
            'delta_cvar95_pct': ((c_latam - c_ideal) / abs(c_ideal) * 100) if c_ideal > 0.001 else float('nan'),
            'queue_ideal': q_ideal,
            'queue_latam': q_latam,
            'delta_queue_pct': ((q_latam - q_ideal) / abs(q_ideal) * 100) if q_ideal > 0.001 else float('nan'),
            'n_runs': len(ideal),
        })

deg_df = pd.DataFrame(degradation)
print(deg_df.to_string(index=False))

# ============================================================
# COMPARE WITH YOUR MODELS (from master_results_clean.csv)
# ============================================================

print("\n" + "=" * 80)
print("COMPARACIÓN: TUS MODELOS vs BASELINES (Hangzhou 4×4)")
print("=" * 80)
print("NOTA: Tus modelos se evaluaron en 6 ciudades con chaos levels semánticos.")
print("Los baselines SOLO en Hangzhou 4×4 con Ideal/LATAM Caótico.")
print("Comparación directa solo posible si hay datos de Hangzhou en tu dataset.")
print()

# Check if Hangzhou data exists in clean dataset
clean = pd.read_csv(r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_results_clean.csv')
print(f"Ciudades en master_results_clean: {sorted(clean['city'].unique())}")
print("Hangzhou NO está en el dataset limpio. La comparación es indirecta.")

# ============================================================
# GENERATE LATEX TABLE FOR PAPER
# ============================================================

print("\n" + "=" * 80)
print("TABLA LATEX PARA EL PAPER (Sección V.A)")
print("=" * 80)

print(r"""
\begin{table}[t]
\centering
\caption{Comparative evaluation of TSC controllers under nominal (Ideal) and 
  stress (LATAM Caótico) conditions on the Hangzhou $4\times4$ network. 
  Throughput in veh/s/intersection; $\Delta$ = relative change under chaos. 
  Best values in \textbf{bold}.}
\label{tab:baselines}
\begin{tabular}{lcccccc}
\toprule
\textbf{Controller} & \textbf{Throughput} & \textbf{Gini} & \textbf{CVaR$_{95}$} & 
  $\Delta$Throughput & $\Delta$Gini & $\Delta$CVaR$_{95}$ \\
 & (Ideal/LATAM) & (Ideal/LATAM) & (Ideal/LATAM) & (\%) & (\%) & (\%) \\
\midrule""")

for _, row in deg_df.iterrows():
    algo = row['algorithm']
    t_i = row['throughput_ideal']
    t_l = row['throughput_latam']
    g_i = row['gini_ideal']
    g_l = row['gini_latam']
    c_i = row['cvar95_ideal']
    c_l = row['cvar95_latam']
    dt = row['delta_throughput_pct']
    dg = row['delta_gini_pct']
    dc = row['delta_cvar95_pct']
    
    # Bold best values
    t_best_i = "\\textbf{" if t_i == deg_df['throughput_ideal'].max() else ""
    t_best_l = "\\textbf{" if t_l == deg_df['throughput_latam'].max() else ""
    g_best_i = "\\textbf{" if g_i == deg_df['gini_ideal'].min() else ""
    g_best_l = "\\textbf{" if g_l == deg_df['gini_latam'].min() else ""
    c_best_i = "\\textbf{" if c_i == deg_df['cvar95_ideal'].min() else ""
    c_best_l = "\\textbf{" if c_l == deg_df['cvar95_latam'].min() else ""
    
    t_i_end = "}" if t_best_i else ""
    t_l_end = "}" if t_best_l else ""
    g_i_end = "}" if g_best_i else ""
    g_l_end = "}" if g_best_l else ""
    c_i_end = "}" if c_best_i else ""
    c_l_end = "}" if c_best_l else ""
    
    # Resilience label
    if abs(dt) < 10 and abs(dc) < 10:
        resilience = 'High'
    elif abs(dt) < 25 and abs(dc) < 25:
        resilience = 'Medium'
    else:
        resilience = 'Low'
    
    print(f"  {algo:>15s} & {t_best_i}{t_i:.3f}{t_i_end}/{t_best_l}{t_l:.3f}{t_l_end} & "
          f"{g_best_i}{g_i:.3f}{g_i_end}/{g_best_l}{g_l:.3f}{g_l_end} & "
          f"{c_best_i}{c_i:.1f}{c_i_end}/{c_best_l}{c_l:.1f}{c_l_end} & "
          f"{dt:+.1f}\\% & {dg:+.1f}\\% & {dc:+.1f}\\% \\\\")

print(r"""\bottomrule
\end{tabular}
\end{table}
""")

# ============================================================
# KEY INSIGHTS FOR PAPER NARRATIVE
# ============================================================

print("=" * 80)
print("INSIGHTS CLAVE PARA LA NARRATIVA DEL PAPER")
print("=" * 80)

print("""
1. COLICHT (SOTA): 
   - Mejor throughput en ideal (0.35) pero Gini ALTÍSIMO (0.49) → sacrifica equidad
   - Bajo caos: colapso total de throughput (-81%), Gini MEJORA (-47%) → "equidad en la miseria"
   - No fue diseñado para equidad ni resiliencia

2. MAXPRESSURE:
   - PEOR throughput (0.07) — inaceptable para despliegue real
   - MEJOR equidad (Gini 0.32) y MEJOR resiliencia (ΔCVaR -0.1%)
   - Pero: throughput tan bajo que la "equidad" es irrelevante (todos igual de lentos)

3. FIXED-TIME:
   - Mejor throughput en ideal (0.32) pero PEOR Gini (0.52) → muy desigual
   - Colapso total bajo caos (-77% throughput)
   - Sin adaptabilidad

4. IPPO:
   - Throughput mediocre (0.10) pero equidad decente (Gini 0.34)
   - Resiliencia media-baja — no diseñado para estrés

5. TU MODELO (Coop-SARG / H-SARG):
   - [INSERTAR TUS DATOS AQUÍ]
   - Ventaja: CVaR + Attention + MAD-Gating → balance throughput-equidad-resiliencia
   - Zero-shot transfer a 6 ciudades con topologías diversas
""")

# ============================================================
# SAVE AGGREGATED DATA
# ============================================================
deg_df.to_csv(benchmark_dir / 'baseline_comparison_aggregated.csv', index=False)
print(f"\nDatos agregados guardados en: {benchmark_dir / 'baseline_comparison_aggregated.csv'}")
