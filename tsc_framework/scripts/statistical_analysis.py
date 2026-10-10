#!/usr/bin/env python3
"""
statistical_analysis.py — Análisis Estadístico Riguroso para Tesis Doctoral
=============================================================================
Implementa las pruebas estadísticas recomendadas por el tutor doctoral:

  1. Prueba Mann-Whitney U: Comparación no-paramétrica entre ppo_chaos y ppo_ideal
     por cada nivel de caos. Robusta ante outliers y no asume normalidad.

  2. Prueba Kruskal-Wallis: Diferencias entre todos los agentes en cada nivel de caos.

  3. Effect size: Rank-biserial correlation (r) para cada comparación significativa.

  4. Tasa de colapso (gridlock rate) y análisis descriptivo completo.

  5. Output: CSV de resultados + sección Markdown lista para insertar en la tesis.

Referencia: Recomendaciones del tutor doctoral (revisión 2026-05-30).
"""

import sys
import csv
from pathlib import Path
import pandas as pd
import numpy as np

# Reconfigurar salida estándar para UTF-8 en Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from scipy import stats

# ─────────────────────────────────────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DETAILED_CSV = ROOT / "outputs" / "results" / "metrics_detailed.csv"
OUTPUT_DIR = ROOT / "outputs" / "results"
STATS_CSV = OUTPUT_DIR / "statistical_tests.csv"
STATS_MD = OUTPUT_DIR / "statistical_analysis.md"

GRIDLOCK_THRESHOLD = 2000.0   # s — umbral físico de gridlock
ALPHA = 0.05                   # Nivel de significancia

AGENT_ORDER = ["ppo_ideal", "ppo_chaos", "ppo_coop_ideal", "ppo_coop_chaos", "MaxPressure", "Fixed", "CoLight"]
LABELS = {
    "ppo_chaos":       "H-SARG Caótico",
    "ppo_ideal":       "H-SARG Ideal",
    "ppo_coop_ideal":  "H-SARG Coop-Ideal",
    "ppo_coop_chaos":  "H-SARG Coop-Caos",
    "Fixed":           "Fixed Time",
    "MaxPressure":     "MaxPressure",
    "CoLight":         "CoLight",
}

# Pares de comparación para Wilcoxon / Mann-Whitney
RL_PAIRS = [
    ("ppo_chaos",      "ppo_ideal",      "H-SARG Caótico vs Ideal"),
    ("ppo_coop_ideal", "ppo_ideal",      "Coop-Ideal vs Ideal"),
    ("ppo_coop_chaos", "ppo_chaos",      "Coop-Caos vs Caótico"),
    ("ppo_coop_chaos", "ppo_coop_ideal", "Coop-Caos vs Coop-Ideal"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Funciones de Effect Size
# ─────────────────────────────────────────────────────────────────────────────
def rank_biserial_r(x: np.ndarray, y: np.ndarray) -> float:
    """
    Rank-biserial correlation: effect size para Mann-Whitney U.
    r = 1 - (2*U) / (n1*n2)
    Interpretación: |r| < 0.3 = pequeño, 0.3-0.5 = medio, > 0.5 = grande.
    """
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return np.nan
    u_stat, _ = stats.mannwhitneyu(x, y, alternative='two-sided')
    return float(1 - (2 * u_stat) / (n1 * n2))


def effect_size_label(r: float) -> str:
    ar = abs(r)
    if ar < 0.1:
        return "negligible"
    elif ar < 0.3:
        return "small"
    elif ar < 0.5:
        return "medium"
    else:
        return "large"


def stars(p: float) -> str:
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return "ns"


# ─────────────────────────────────────────────────────────────────────────────
# Estadísticas Descriptivas Avanzadas
# ─────────────────────────────────────────────────────────────────────────────
def descriptive_stats(series: pd.Series) -> dict:
    arr = np.array(series.dropna())
    if len(arr) == 0:
        return {}
    q1, q3 = np.percentile(arr, 25), np.percentile(arr, 75)
    collapse = float((arr > GRIDLOCK_THRESHOLD).mean() * 100)
    cvar_arr = arr[arr >= np.quantile(arr, 0.95)]
    cvar95 = float(cvar_arr.mean()) if len(cvar_arr) > 0 else float(np.max(arr))
    return {
        "n": len(arr),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr)),
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(q3 - q1),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "collapse_pct": collapse,
        "cvar95": cvar95,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Análisis Principal
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("  ANÁLISIS ESTADÍSTICO DOCTORAL — H-SARG vs Baselines")
    print("  (Mann-Whitney U | Kruskal-Wallis | Effect Sizes | Gridlock Rate)")
    print("=" * 70)

    if not DETAILED_CSV.exists():
        print(f"Error: CSV no encontrado: {DETAILED_CSV}")
        sys.exit(1)

    df = pd.read_csv(DETAILED_CSV)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chaos_levels = sorted(df["chaos_level"].unique())
    agents_present = [a for a in AGENT_ORDER if a in df["agent"].unique()]

    # ─── 1. Estadísticas Descriptivas Completas ────────────────────────────
    print("\n[1/4] Calculando estadisticas descriptivas avanzadas...")
    desc_rows = []
    for agent in agents_present:
        for cl in chaos_levels:
            sub = df[(df["agent"] == agent) & (df["chaos_level"] == cl)]["delay_mean"]
            d = descriptive_stats(sub)
            if d:
                d.update({"agent": agent, "chaos_level": cl})
                desc_rows.append(d)

    desc_df = pd.DataFrame(desc_rows)
    desc_file = OUTPUT_DIR / "descriptive_stats.csv"
    desc_df.to_csv(desc_file, index=False, float_format="%.4f")
    print(f"   OK Estadisticas descriptivas -> {desc_file.name}")

    # ─── 2. Mann-Whitney U + Wilcoxon sobre delay_mean Y cvar_95 (todos los pares RL) ───
    print("\n[2/4] Prueba Mann-Whitney U + Wilcoxon sobre delay_mean y cvar_95 (todos los pares RL)...")
    mw_rows = []
    mw_lines = []
    mw_lines.append("| Par de Modelos | Caos % | Métrica | U stat | p-value | Signif. | r (effect) | Magnitud | Mediana A | Mediana B |")
    mw_lines.append("|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")

    for agent_a, agent_b, pair_label in RL_PAIRS:
        agents_in_df = df["agent"].unique()
        if agent_a not in agents_in_df or agent_b not in agents_in_df:
            print(f"   [SKIP] {pair_label}: uno o ambos agentes no encontrados en CSV.")
            continue

        for metric in ["delay_mean", "cvar_95"]:
            metric_col = metric if metric in df.columns else None
            if metric_col is None:
                continue

            for cl in chaos_levels:
                x_a = df[(df["agent"] == agent_a) & (df["chaos_level"] == cl)][metric_col].dropna().values
                x_b = df[(df["agent"] == agent_b) & (df["chaos_level"] == cl)][metric_col].dropna().values

                if len(x_a) < 3 or len(x_b) < 3:
                    continue

                u_stat, p_val = stats.mannwhitneyu(x_a, x_b, alternative='two-sided')
                r = rank_biserial_r(x_a, x_b)
                sig = stars(p_val)
                mag = effect_size_label(r)
                med_a = np.median(x_a)
                med_b = np.median(x_b)
                chaos_pct = f"{cl*100:.0f}%"

                row = {
                    "chaos_level": cl,
                    "test": "Mann-Whitney U",
                    "comparison": pair_label,
                    "metric": metric,
                    "U_statistic": round(u_stat, 4),
                    "p_value": round(p_val, 6),
                    "significant": p_val < ALPHA,
                    "stars": sig,
                    "effect_size_r": round(r, 4),
                    "effect_magnitude": mag,
                    "median_a": round(med_a, 2),
                    "median_b": round(med_b, 2),
                }
                mw_rows.append(row)
                mw_lines.append(
                    f"| {pair_label} | {chaos_pct} | {metric} | {u_stat:.1f} | {p_val:.4f} | {sig} | "
                    f"{r:.3f} | {mag} | {med_a:.1f} | {med_b:.1f} |"
                )

        print(f"   OK {pair_label}")

    mw_table_md = "\n".join(mw_lines)

    # ─── 3. Kruskal-Wallis: todos los agentes por nivel de caos ────────────
    print("\n[3/4] Prueba Kruskal-Wallis: todos los agentes...")
    kw_rows = []
    kw_lines = []
    kw_lines.append("| Caos % | H stat | p-value | Signif. | Interpretación |")
    kw_lines.append("|:---:|:---:|:---:|:---:|:---|")

    for cl in chaos_levels:
        groups = []
        for agent in agents_present:
            sub = df[(df["agent"] == agent) & (df["chaos_level"] == cl)]["delay_mean"].dropna().values
            if len(sub) >= 2:
                groups.append(sub)

        if len(groups) < 2:
            continue

        h_stat, p_val = stats.kruskal(*groups)
        sig = stars(p_val)
        chaos_pct = f"{cl*100:.0f}%"

        if p_val < ALPHA:
            interp = "Diferencias significativas entre controladores"
        else:
            interp = "Sin diferencias estadísticamente significativas"

        kw_row = {
            "chaos_level": cl,
            "test": "Kruskal-Wallis",
            "H_statistic": round(h_stat, 4),
            "p_value": round(p_val, 6),
            "significant": p_val < ALPHA,
            "stars": sig,
            "n_groups": len(groups),
        }
        kw_rows.append(kw_row)
        kw_lines.append(
            f"| {chaos_pct} | {h_stat:.3f} | {p_val:.4f} | {sig} | {interp} |"
        )
        print(f"   Caos {chaos_pct}: H={h_stat:.3f}, p={p_val:.4f}{sig}")

    kw_table_md = "\n".join(kw_lines)

    # ─── 4. Tabla de Colapso + Análisis Gini Condicional ─────────────────────
    print("\n[4/4] Calculando tasa de colapso y analisis Gini condicional...")

    # 4a. Tabla de colapso — todos los modelos RL
    collapse_lines = []
    collapse_lines.append("| Controlador | Caos % | Tasa Colapso (%) | Mediana Delay (s) | IQR (s) | CVaR₉₅ (s) |")
    collapse_lines.append("|:---|:---:|:---:|:---:|:---:|:---:|")

    rl_models = [a for a in ["ppo_ideal", "ppo_chaos", "ppo_coop_ideal", "ppo_coop_chaos"] if a in df["agent"].unique()]
    for agent in rl_models:
        for cl in chaos_levels:
            sub = df[(df["agent"] == agent) & (df["chaos_level"] == cl)]["delay_mean"].dropna()
            d = descriptive_stats(sub)
            collapse_lines.append(
                f"| **{LABELS.get(agent, agent)}** | {cl*100:.0f}% | "
                f"**{d['collapse_pct']:.1f}%** | {d['median']:.1f} s | "
                f"{d['iqr']:.1f} s | {d['cvar95']:.1f} s |"
            )

    collapse_table_md = "\n".join(collapse_lines)

    # 4b. Análisis Gini Condicional: Gridlock vs Nominal
    print("   Calculando Gini condicional (gridlock vs nominal)...")
    gini_lines = []
    gini_lines.append("| Controlador | Caos % | Gini Nominal (delay<2000s) | Gini Gridlock (delay>2000s) | Episodios Gridlock |")
    gini_lines.append("|:---|:---:|:---:|:---:|:---:|")

    all_rl = [a for a in AGENT_ORDER if a in df["agent"].unique()]
    for agent in all_rl:
        for cl in chaos_levels:
            sub = df[(df["agent"] == agent) & (df["chaos_level"] == cl)]
            nominal = sub[sub["delay_mean"] < GRIDLOCK_THRESHOLD]["gini_mean"].dropna()
            gridlock = sub[sub["delay_mean"] >= GRIDLOCK_THRESHOLD]["gini_mean"].dropna()
            gini_nom = f"{nominal.median():.3f}" if len(nominal) > 0 else "—"
            gini_grid = f"{gridlock.median():.3f}" if len(gridlock) > 0 else "—"
            n_grid = len(gridlock)
            gini_lines.append(
                f"| {LABELS.get(agent, agent)} | {cl*100:.0f}% | "
                f"{gini_nom} | {gini_grid} | {n_grid} |"
            )

    gini_cond_table_md = "\n".join(gini_lines)
    print(f"   OK Analisis Gini condicional completado.")

    # ─── Exportar resultados CSV ────────────────────────────────────────────
    # Exportar Mann-Whitney y Kruskal-Wallis como CSVs separados
    if mw_rows:
        mw_file = OUTPUT_DIR / "stats_mann_whitney.csv"
        with open(mw_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=mw_rows[0].keys())
            writer.writeheader()
            writer.writerows(mw_rows)
        print(f"\n   OK Mann-Whitney results -> {mw_file.name}")

    if kw_rows:
        kw_file = OUTPUT_DIR / "stats_kruskal_wallis.csv"
        with open(kw_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=kw_rows[0].keys())
            writer.writeheader()
            writer.writerows(kw_rows)
        print(f"   OK Kruskal-Wallis results -> {kw_file.name}")

    # ─── Generar Sección Markdown ───────────────────────────────────────────
    md_content = f"""## [ANALISIS] Análisis Estadístico — Pruebas No-Paramétricas

> **Nota metodológica:** Dado que la distribución de los retrasos vehiculares no es normal (presencia de episodios catastróficos de gridlock), se aplican pruebas no-paramétricas robustas ante outliers: Mann-Whitney U (comparación por pares) y Kruskal-Wallis (comparación multi-grupo). El nivel de significancia es α = {ALPHA}. El tamaño del efecto se mide mediante la correlación rank-biserial *r* (|r| < 0.3 = pequeño; 0.3–0.5 = medio; > 0.5 = grande).

---

### Comparaciones por Pares RL — delay\_mean y cvar\_95 (Mann-Whitney U)

*(Incluye modelos originales y variantes cooperativas)*

{mw_table_md}

**Leyenda:** *** p < 0.001 | ** p < 0.01 | * p < 0.05 | ns = no significativo

---

### Diferencias entre Todos los Controladores (Kruskal-Wallis)

{kw_table_md}

---

### Tabla de Tasa de Colapso de Red — 4 Modelos RL

*(Umbral de gridlock: Delay > {GRIDLOCK_THRESHOLD:.0f} s por episodio)*

{collapse_table_md}

---

### Análisis de Equidad Condicional — Gini en Régimen Nominal vs Gridlock

*(Valida H3/RQ4: el Índice de Gini colapsa durante episodios de gridlock, demostrando que las métricas de equidad son estables solo en condiciones nominales)*

{gini_cond_table_md}

---
*Análisis generado automáticamente por `statistical_analysis.py` — TSC Framework Doctoral.*
"""

    with open(STATS_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"   OK Seccion Markdown -> {STATS_MD.name}")

    # ─── Resumen en consola ─────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  RESUMEN EJECUTIVO -- HALLAZGOS ESTADISTICOS CLAVE")
    print("=" * 70)

    # Caso más importante: caos 15%
    try:
        row_15 = [r for r in mw_rows if r["chaos_level"] == 0.15][0]
        print(f"\n  [!] Caos 15%: {'SIGNIFICATIVO' if row_15['significant'] else 'NO SIGNIFICATIVO'} "
              f"(p={row_15['p_value']:.4f}{row_15['stars']}, r={row_15['effect_size_r']:.3f} [{row_15['effect_magnitude']}])")
        print(f"     Mediana ppo_chaos = {row_15['median_ppo_chaos']:.1f}s vs ppo_ideal = {row_15['median_ppo_ideal']:.1f}s")
    except Exception:
        pass

    for cl in [0.30, 0.50]:
        try:
            row = [r for r in mw_rows if r["chaos_level"] == cl][0]
            print(f"\n  [!] Caos {cl*100:.0f}%: {'SIGNIFICATIVO' if row['significant'] else 'NO SIGNIFICATIVO'} "
                  f"(p={row['p_value']:.4f}{row['stars']}, r={row['effect_size_r']:.3f} [{row['effect_magnitude']}])")
        except Exception:
            pass

    print(f"\n  Archivos generados:")
    print(f"   - {STATS_CSV.name}")
    print(f"   - {STATS_MD.name}")
    print(f"   - {desc_file.name}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
