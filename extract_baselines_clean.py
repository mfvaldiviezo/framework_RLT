import pandas as pd
import numpy as np
import re
from pathlib import Path

benchmark_dir = Path(r'c:\Proyecto_Tesis_Final_V1\traffic_project\benchmark_reports')
report_files = sorted(benchmark_dir.glob('marl_eval_*.txt'))

# ============================================================
# AUDIT: Check each report for anomalous values
# ============================================================
print("=" * 80)
print("AUDITORÍA DE CADA REPORTE — buscando anomalías")
print("=" * 80)

all_raw = []
for fpath in report_files:
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    timestamp = fpath.stem.replace('marl_eval_', '')
    
    table_pattern = re.findall(
        r'^\s*(\w+(?:\s+\w+)?)\s+(Ideal|LATAM Caótico)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([OK]|[FAIL])',
        content, re.MULTILINE
    )
    
    for match in table_pattern:
        algo, scenario, tput, q, gini, cvar, gini_f, t, ok = match
        all_raw.append({
            'timestamp': timestamp,
            'algorithm': algo.strip(),
            'scenario': scenario.strip(),
            'throughput': float(tput),
            'avg_queue': float(q),
            'gini_temp': float(gini),
            'cvar95': float(cvar),
            'gini_final': float(gini_f),
            'time_s': float(t),
            'ok': ok == '[OK]'
        })

df = pd.DataFrame(all_raw)

# Pivot to see all results
print("\n--- Throughput por reporte ---")
pivot = df.pivot_table(values='throughput', index=['algorithm','scenario'], columns='timestamp', aggfunc='first')
print(pivot.to_string())

print("\n--- Avg Queue por reporte ---")
pivot_q = df.pivot_table(values='avg_queue', index=['algorithm','scenario'], columns='timestamp', aggfunc='first')
print(pivot_q.to_string())

# ============================================================
# IDENTIFY ANOMALOUS REPORTS
# ============================================================
print("\n" + "=" * 80)
print("IDENTIFICACIÓN DE REPORTES ANÓMALOS")
print("=" * 80)

# Criteria: Fixed-Time Ideal throughput should be ~0.28-0.34
# If Fixed-Time LATAM throughput > 0.5, it's anomalous (wrong route file)
# If CoLight LATAM throughput > 0.5 AND queue < 20, it's anomalous
# If IPPO LATAM throughput > 0.3, anomalous (IPPO should be ~0.08-0.10)

anomalous_reports = set()

for ts in sorted(df['timestamp'].unique()):
    sub = df[df['timestamp'] == ts]
    issues = []
    
    # Check Fixed-Time LATAM
    ft_latam = sub[(sub['algorithm'] == 'FIXED') & (sub['scenario'] == 'LATAM Caótico')]
    if len(ft_latam) > 0:
        if ft_latam['throughput'].values[0] > 0.5:
            issues.append(f"FIXED LATAM tput={ft_latam['throughput'].values[0]:.3f} (>0.5, anomalo)")
        if ft_latam['avg_queue'].values[0] < 15:
            issues.append(f"FIXED LATAM queue={ft_latam['avg_queue'].values[0]:.1f} (<15, anomalo)")
    
    # Check CoLight LATAM
    cl_latam = sub[(sub['algorithm'] == 'CoLight') & (sub['scenario'] == 'LATAM Caótico')]
    if len(cl_latam) > 0:
        if cl_latam['throughput'].values[0] > 0.5:
            issues.append(f"CoLight LATAM tput={cl_latam['throughput'].values[0]:.3f} (>0.5, anomalo)")
    
    # Check IPPO — any extreme values?
    ippo = sub[sub['algorithm'] == 'IPPO']
    if len(ippo) > 0:
        if ippo['throughput'].max() > 0.3:
            issues.append(f"IPPO tput max={ippo['throughput'].max():.3f} (>0.3, anomalo)")
    
    # Check for N/D or zero throughput in Ideal (incomplete data)
    for algo in ['FIXED', 'CoLight', 'IPPO', 'MAXPRESSURE']:
        ideal = sub[(sub['algorithm'] == algo) & (sub['scenario'] == 'Ideal')]
        if len(ideal) > 0 and ideal['throughput'].values[0] < 0.001:
            issues.append(f"{algo} Ideal tput=0 (incompleto)")
    
    if issues:
        anomalous_reports.add(ts)
        print(f"  [ERROR] {ts}: {', '.join(issues)}")
    else:
        print(f"  [OK] {ts}: OK")

print(f"\nReportes anómalos: {len(anomalous_reports)}")
print(f"Reportes válidos: {len(df['timestamp'].unique()) - len(anomalous_reports)}")

# ============================================================
# RECALCULATE WITH CLEAN DATA ONLY
# ============================================================
df_clean = df[~df['timestamp'].isin(anomalous_reports) & df['ok']].copy()

print("\n" + "=" * 80)
print("TABLA FINAL (SOLO REPORTES VÁLIDOS)")
print("=" * 80)

print(f"Registros válidos usados: {len(df_clean)}")
print(f"Reportes usados: {sorted(df_clean['timestamp'].unique())}")
print()

# Aggregate
agg = df_clean.groupby(['algorithm', 'scenario']).agg(
    n_runs=('timestamp', 'count'),
    throughput_median=('throughput', 'median'),
    throughput_mean=('throughput', 'mean'),
    throughput_std=('throughput', 'std'),
    queue_median=('avg_queue', 'median'),
    gini_temp_median=('gini_temp', 'median'),
    cvar95_median=('cvar95', 'median'),
    gini_final_median=('gini_final', 'median'),
).round(4)

print(agg.to_string())
print()

# Degradation
degradation = []
for algo in sorted(df_clean['algorithm'].unique()):
    ideal = df_clean[(df_clean['algorithm'] == algo) & (df_clean['scenario'] == 'Ideal')]
    latam = df_clean[(df_clean['algorithm'] == algo) & (df_clean['scenario'] == 'LATAM Caótico')]
    
    if len(ideal) > 0 and len(latam) > 0:
        t_i, t_l = ideal['throughput'].median(), latam['throughput'].median()
        g_i, g_l = ideal['gini_temp'].median(), latam['gini_temp'].median()
        c_i, c_l = ideal['cvar95'].median(), latam['cvar95'].median()
        q_i, q_l = ideal['avg_queue'].median(), latam['avg_queue'].median()
        
        degradation.append({
            'algorithm': algo,
            't_ideal': t_i, 't_latam': t_l,
            'dt_pct': ((t_l - t_i) / abs(t_i) * 100) if t_i > 0.001 else float('nan'),
            'g_ideal': g_i, 'g_latam': g_l,
            'dg_pct': ((g_l - g_i) / abs(g_i) * 100) if g_i > 0.001 else float('nan'),
            'c_ideal': c_i, 'c_latam': c_l,
            'dc_pct': ((c_l - c_i) / abs(c_i) * 100) if c_i > 0.001 else float('nan'),
            'q_ideal': q_i, 'q_latam': q_l,
            'dq_pct': ((q_l - q_i) / abs(q_i) * 100) if q_i > 0.001 else float('nan'),
            'n_runs': len(ideal),
        })

deg_df = pd.DataFrame(degradation)
print("DEGRADACIÓN (mediana entre ejecuciones válidas):")
print(deg_df.to_string(index=False))

# ============================================================
# FINAL LATEX TABLE
# ============================================================
print("\n" + "=" * 80)
print("TABLA LATEX FINAL")
print("=" * 80)

# Compute min/max for bolding
t_best_i = deg_df['t_ideal'].max()
t_best_l = deg_df['t_latam'].max()
g_best_i = deg_df['g_ideal'].min()
g_best_l = deg_df['g_latam'].min()
c_best_i = deg_df['c_ideal'].min()
c_best_l = deg_df['c_latam'].min()

print(r"""
\begin{table}[t]
\centering
\caption{Comparative evaluation of TSC controllers under nominal (Ideal) and 
  adversarial stress (LATAM Caótico) on Hangzhou $4\times4$. 
  $\Delta$ = relative change under chaos. Best values in \textbf{bold}.
  Results aggregated over """ + f"{len(df_clean['timestamp'].unique())}" + r""" consistent runs.}
\label{tab:baselines}
\begin{tabular}{lccccccc}
\toprule
\textbf{Controller} & \textbf{Throughput} & \textbf{Gini} & \textbf{CVaR$_{95}$} & \textbf{Queue} & 
  $\Delta$Tput & $\Delta$Gini & $\Delta$CVaR \\
 & (Ideal/LATAM) & (Ideal/LATAM) & (Ideal/LATAM) & (Ideal/LATAM) & (\%) & (\%) & (\%) \\
\midrule""")

for _, row in deg_df.iterrows():
    algo = row['algorithm']
    
    def bold(val, best, fmt):
        s = f"{val:{fmt}}"
        return f"\\textbf{{{s}}}" if abs(val - best) < 0.001 else s
    
    t_i_s = bold(row['t_ideal'], t_best_i, '.3f')
    t_l_s = bold(row['t_latam'], t_best_l, '.3f')
    g_i_s = bold(row['g_ideal'], g_best_i, '.3f')
    g_l_s = bold(row['g_latam'], g_best_l, '.3f')
    c_i_s = bold(row['c_ideal'], c_best_i, '.1f')
    c_l_s = bold(row['c_latam'], c_best_l, '.1f')
    
    print(f"  {algo:>15s} & {t_i_s}/{t_l_s} & {g_i_s}/{g_l_s} & {c_i_s}/{c_l_s} & "
          f"{row['q_ideal']:.1f}/{row['q_latam']:.1f} & "
          f"{row['dt_pct']:+.1f}\\% & {row['dg_pct']:+.1f}\\% & {row['dc_pct']:+.1f}\\% \\\\")

print(r"""\bottomrule
\end{tabular}
\end{table}
""")

# ============================================================
# NARRATIVE SUMMARY
# ============================================================
print("=" * 80)
print("NARRATIVA PARA EL PAPER (basada en datos limpios)")
print("=" * 80)

for _, row in deg_df.iterrows():
    algo = row['algorithm']
    dt = row['dt_pct']
    dg = row['dg_pct']
    dc = row['dc_pct']
    
    # Resilience rating
    if abs(dt) < 15 and abs(dc) < 5:
        res = 'Alta'
    elif abs(dt) < 40 and abs(dc) < 10:
        res = 'Media'
    else:
        res = 'Baja'
    
    print(f"\n  {algo}:")
    print(f"    Throughput: {row['t_ideal']:.3f} → {row['t_latam']:.3f} ({dt:+.1f}%)")
    print(f"    Gini:       {row['g_ideal']:.3f} → {row['g_latam']:.3f} ({dg:+.1f}%)")
    print(f"    CVaR95:     {row['c_ideal']:.1f} → {row['c_latam']:.1f} ({dc:+.1f}%)")
    print(f"    Resiliencia: {res}")

# Save
deg_df.to_csv(benchmark_dir / 'baseline_comparison_clean.csv', index=False)
print(f"\n[OK] Datos limpios guardados en: {benchmark_dir / 'baseline_comparison_clean.csv'}")
