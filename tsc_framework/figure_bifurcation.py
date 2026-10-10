"""
figure_bifurcation.py — Figura 3 paneles para el artículo T-ITS
================================================================
Panel (a): Delay vs Saturation Level (log scale, CI 95% bootstrap)
Panel (b): Gini vs Saturation Level (linear scale, CI 95% bootstrap)
Panel (c): Gini vs Delay scatter (colored by chaos, sized by collapse rate)

Demuestra la "divergencia por saturación diferencial":
  - Gini AUMENTA con delay (r = +0.49)
  - Topología lineal (Quito) amplifica el efecto
  - El colapso NO iguala — exacerba la desigualdad

Uso:
  python figure_bifurcation.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "outputs" / "results"
FIGURES_DIR = ROOT / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ── Load clean data ──────────────────────────────────────────────────────────
df = pd.read_csv(RESULTS_DIR / "master_summary_clean.csv")

CHAOS_ORDER = ["low", "mid", "mid_high", "high", "extreme"]
CHAOS_LABELS = ["Low\n(0.3)", "Mid\n(0.6)", "Mid-High\n(0.75)", "High\n(0.9)", "Extreme\n(1.2)"]

CITY_COLORS = {
    "Barcelona": "#2166ac",   # Blue
    "Berlin":    "#4393c3",
    "Bogota":    "#f4a582",   # Orange-red
    "CDMX":      "#d6604d",
    "Madrid":    "#b2182b",
    "Quito":     "#67001f",   # Dark red (linear topology)
}

CITY_MARKERS = {
    "Barcelona": "o",
    "Berlin":    "s",
    "Bogota":    "D",
    "CDMX":      "^",
    "Madrid":    "v",
    "Quito":     "X",  # Special marker for linear topology
}

TOPOLOGY = {
    "Barcelona": "Grid",
    "Berlin":    "Grid",
    "Bogota":    "Mixed",
    "CDMX":      "Grid",
    "Madrid":    "Grid",
    "Quito":     "Linear",
}

# ── Bootstrap CI ─────────────────────────────────────────────────────────────

def bootstrap_ci95(data, n_bootstrap=1000):
    """95% CI via percentile bootstrap."""
    if len(data) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(42)
    medians = []
    arr = np.array(data)
    for _ in range(n_bootstrap):
        sample = rng.choice(arr, size=len(arr), replace=True)
        medians.append(np.median(sample))
    return np.percentile(medians, 2.5), np.percentile(medians, 97.5)


# ── Aggregate for panels (a) and (b) ────────────────────────────────────────
# For clean data: use raw episodes instead of summary medians
raw = pd.read_csv(RESULTS_DIR / "master_results_clean.csv")

# Build aggregated stats per city × chaos × model
agg_stats = []
for city in sorted(raw["city"].unique()):
    for chaos in CHAOS_ORDER:
        for model in ["ppo_coop_chaos", "ppo_coop_ideal", "fixed_time_opt"]:
            sub = raw[(raw["city"] == city) & 
                      (raw["chaos_level"] == chaos) & 
                      (raw["model"] == model)]
            if len(sub) >= 5:
                delay_lo, delay_hi = bootstrap_ci95(sub["delay_mean"].values)
                gini_lo, gini_hi = bootstrap_ci95(sub["gini_mean"].values)
                agg_stats.append({
                    "city": city,
                    "chaos_level": chaos,
                    "model": model,
                    "delay_median": sub["delay_mean"].median(),
                    "delay_ci_lo": delay_lo,
                    "delay_ci_hi": delay_hi,
                    "gini_median": sub["gini_mean"].median(),
                    "gini_ci_lo": gini_lo,
                    "gini_ci_hi": gini_hi,
                    "collapse_rate": sub["collapsed"].mean() * 100,
                    "n": len(sub),
                })

agg = pd.DataFrame(agg_stats)

# ── Global stats for panel (c) ───────────────────────────────────────────────
r_pearson = raw["delay_mean"].corr(raw["gini_mean"])
r_spearman = raw["delay_mean"].corr(raw["gini_mean"], method="spearman")

# Sample for scatter (avoid overcrowding)
scatter_data = raw.sample(n=min(2000, len(raw)), random_state=42).copy()
scatter_data["chaos_idx"] = scatter_data["chaos_level"].map(
    {c: i for i, c in enumerate(CHAOS_ORDER)}
)

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE
# ═══════════════════════════════════════════════════════════════════════════════

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 7,
    "figure.dpi": 150,
})

fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))
ax1, ax2, ax3 = axes

# ═══════════════════════════════════════════════════════════════════════════════
# PANEL (a): Delay vs Saturation Level
# ═══════════════════════════════════════════════════════════════════════════════

model_show = "ppo_coop_chaos"
for city in sorted(raw["city"].unique()):
    city_data = agg[(agg["city"] == city) & (agg["model"] == model_show)]
    city_data = city_data.sort_values("chaos_level", 
        key=lambda x: pd.Categorical(x, categories=CHAOS_ORDER, ordered=True))
    
    x = range(len(city_data))
    y = city_data["delay_median"].values
    y_lo = city_data["delay_ci_lo"].values
    y_hi = city_data["delay_ci_hi"].values
    
    ax1.errorbar(x, y, yerr=[y - y_lo, y_hi - y], 
                fmt=CITY_MARKERS[city], 
                color=CITY_COLORS[city],
                markersize=7, linewidth=1.5, capsize=3, capthick=1,
                label=f"{city} ({TOPOLOGY[city]})",
                markeredgewidth=0.5, markeredgecolor="white")

ax1.set_yscale("log")
ax1.set_ylabel("Median Delay (s)", fontweight="bold")
ax1.set_xlabel("Saturation Level ($v/c$)")
ax1.set_title("(a) Delay vs Saturation", fontweight="bold")
ax1.set_xticks(range(len(CHAOS_ORDER)))
ax1.set_xticklabels(CHAOS_LABELS, fontsize=7)
ax1.legend(loc="upper left", framealpha=0.85, ncol=2,
          handletextpad=0.5, columnspacing=0.8)
ax1.grid(True, alpha=0.25, linewidth=0.5)
ax1.set_ylim(5, 300000)

# Bifurcation threshold
ax1.axhline(y=2000, color="red", linestyle="--", linewidth=1.5, alpha=0.5)
ax1.annotate("Gridlock threshold\n(2,000s)", xy=(4.2, 2500), fontsize=7,
            color="red", alpha=0.7, ha="left", va="bottom")

# ═══════════════════════════════════════════════════════════════════════════════
# PANEL (b): Gini vs Saturation Level
# ═══════════════════════════════════════════════════════════════════════════════

for city in sorted(raw["city"].unique()):
    city_data = agg[(agg["city"] == city) & (agg["model"] == model_show)]
    city_data = city_data.sort_values("chaos_level",
        key=lambda x: pd.Categorical(x, categories=CHAOS_ORDER, ordered=True))
    
    x = range(len(city_data))
    y = city_data["gini_median"].values
    y_lo = city_data["gini_ci_lo"].values
    y_hi = city_data["gini_ci_hi"].values
    
    ax2.errorbar(x, y, yerr=[y - y_lo, y_hi - y],
                fmt=CITY_MARKERS[city],
                color=CITY_COLORS[city],
                markersize=7, linewidth=1.5, capsize=3, capthick=1,
                markeredgewidth=0.5, markeredgecolor="white")

ax2.set_ylabel("Gini Coefficient", fontweight="bold")
ax2.set_xlabel("Saturation Level ($v/c$)")
ax2.set_title("(b) Equity (Gini) vs Saturation", fontweight="bold")
ax2.set_xticks(range(len(CHAOS_ORDER)))
ax2.set_xticklabels(CHAOS_LABELS, fontsize=7)
ax2.grid(True, alpha=0.25, linewidth=0.5)
ax2.set_ylim(0, 0.75)

# Annotation: the key finding
ax2.annotate("Gini INCREASES\nwith saturation",
            xy=(3, 0.55), fontsize=8, fontweight="bold",
            color="#67001f", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

# ═══════════════════════════════════════════════════════════════════════════════
# PANEL (c): Gini vs Delay (scatter) — THE KEY FIGURE
# ═══════════════════════════════════════════════════════════════════════════════

chaos_colors = {
    "low":      "#0571b0",
    "mid":      "#92c5de",
    "mid_high": "#f7f7f7",
    "high":     "#f4a582",
    "extreme":  "#ca0020",
}

for chaos in CHAOS_ORDER:
    sub = scatter_data[scatter_data["chaos_level"] == chaos]
    ax3.scatter(sub["delay_mean"], sub["gini_mean"],
               c=chaos_colors[chaos], s=4, alpha=0.4,
               label=chaos.replace("_", " ").title(),
               edgecolors="none", rasterized=True)

ax3.set_xscale("log")
ax3.set_xlabel("Mean Delay (s)", fontweight="bold")
ax3.set_ylabel("Gini Coefficient", fontweight="bold")
ax3.set_title("(c) Gini vs Delay — All scenarios", fontweight="bold")
ax3.legend(loc="lower right", framealpha=0.85, markerscale=3,
          title="Chaos Level", title_fontsize=7)
ax3.grid(True, alpha=0.25, linewidth=0.5)
ax3.set_xlim(0.5, 300000)
ax3.set_ylim(0, 0.85)

# Correlation annotation
ax3.annotate(f"Pearson $r = {r_pearson:+.2f}$\nSpearman $\\rho = {r_spearman:+.2f}$\n$n = {len(raw):,}$",
            xy=(0.03, 0.97), xycoords="axes fraction",
            fontsize=8, ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.85))

# Arrow showing the "divergence" direction
ax3.annotate("", xy=(50000, 0.55), xytext=(500, 0.20),
            arrowprops=dict(arrowstyle="->", color="#ca0020", lw=2, alpha=0.6))
ax3.text(8000, 0.38, "Divergence by\ndifferential\nsaturation",
        fontsize=8, color="#ca0020", fontweight="bold", ha="center")

# ── Final layout ─────────────────────────────────────────────────────────────
plt.tight_layout(pad=1.5)

# Save
for fmt in ["pdf", "png"]:
    path = FIGURES_DIR / f"fig_bifurcation_gini_delay.{fmt}"
    fig.savefig(path, format=fmt, bbox_inches="tight", dpi=300)
    print(f"[OK] {path}")

print(f"""
{'='*70}
  FIGURA GENERADA — 3 paneles para artículo T-ITS
{'='*70}

Panel (a): Delay vs Saturation — muestra bifurcación en v/c ≥ 0.90
Panel (b): Gini vs Saturation   — Gini AUMENTA con saturación (NO baja)
Panel (c): Gini vs Delay        — Correlación positiva r={r_pearson:+.2f}
                                   Evidencia de "divergencia por saturación
                                   diferencial" — refuta hipótesis original

Datos: {len(raw):,} simulaciones SUMO (master_results_clean.csv)
       {len(raw['city'].unique())} ciudades × {len(CHAOS_ORDER)} chaos levels × 6 modelos
""")
