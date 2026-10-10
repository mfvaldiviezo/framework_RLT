"""
figure_bifurcation_v3.py — Layout corregido
============================================
CORRECCIONES aplicadas sobre v2:

  FIX 1: Leyenda de ciudades → fig.legend() encima de los 3 paneles (ncol=6)
          Eliminadas las dos legend() internas de ax1 que se solapaban.

  FIX 2: Leyenda de Policy  → ax1, esquina superior izquierda (zona vacía).
          Antes estaba en 'lower right' encima de las curvas densas.

  FIX 3: Anotación "Bifurcation v/c=0.90" → desplazada al margen superior
          con annotation_clip=False + flecha, en vez de flotar sobre curvas.

  FIX 4a: "Gini INCREASES" → movida a esquina superior derecha del panel (b),
           fuera del rango de datos x (usa xycoords='axes fraction').

  FIX 4b: "Quito Paradox"  → movida a zona inferior-izquierda del panel (b),
           región despejada con flecha curva hacia el punto de interés.

  FIX 5: fig.tight_layout(rect=[0,0,1,0.93]) para reservar espacio a la
          leyenda superior sin que se corte.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from pathlib import Path

ROOT        = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "outputs" / "results"
FIGURES_DIR = ROOT / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────
raw = pd.read_csv(RESULTS_DIR / "master_results_clean.csv")

CHAOS_ORDER = ["low", "mid", "mid_high", "high", "extreme"]
VC_VALUES   = [0.3, 0.6, 0.75, 0.9, 1.2]

# ── City styles ───────────────────────────────────────────────────────────────
CITY_STYLE = {
    "Barcelona": {"color": "#2166ac", "marker": "o", "topology": "Grid"},
    "Berlin":    {"color": "#762a83", "marker": "s", "topology": "Grid"},
    "Bogota":    {"color": "#1b7837", "marker": "D", "topology": "Mixed"},
    "CDMX":      {"color": "#d73027", "marker": "^", "topology": "Grid"},
    "Madrid":    {"color": "#fdae61", "marker": "v", "topology": "Grid"},
    "Quito":     {"color": "#000000", "marker": "*", "topology": "Linear"},
}

POLICY_STYLE = {
    "ppo_coop_ideal": {"ls": "-",  "lw": 1.5, "label": "Coop-Ideal", "fill": "full"},
    "ppo_coop_chaos": {"ls": "--", "lw": 1.5, "label": "Coop-Chaos", "fill": "none"},
}

# ── Bootstrap CI ──────────────────────────────────────────────────────────────
def bootstrap_ci95(data, n_bootstrap=1000):
    if len(data) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(42)
    arr = np.array(data)
    medians = [np.median(rng.choice(arr, size=len(arr), replace=True))
               for _ in range(n_bootstrap)]
    return np.percentile(medians, 2.5), np.percentile(medians, 97.5)

# ── Aggregate ─────────────────────────────────────────────────────────────────
agg_rows = []
for city in sorted(raw["city"].unique()):
    for chaos in CHAOS_ORDER:
        for model in ["ppo_coop_ideal", "ppo_coop_chaos"]:
            sub = raw[(raw["city"] == city) &
                      (raw["chaos_level"] == chaos) &
                      (raw["model"] == model)]
            if len(sub) >= 5:
                d_lo, d_hi = bootstrap_ci95(sub["delay_mean"].values)
                g_lo, g_hi = bootstrap_ci95(sub["gini_mean"].values)
                agg_rows.append({
                    "city": city, "chaos_level": chaos, "model": model,
                    "v_c":          VC_VALUES[CHAOS_ORDER.index(chaos)],
                    "delay_median": sub["delay_mean"].median(),
                    "delay_lo": d_lo, "delay_hi": d_hi,
                    "gini_median":  sub["gini_mean"].median(),
                    "gini_lo": g_lo, "gini_hi": g_hi,
                    "collapse":     sub["collapsed"].mean() * 100,
                })
agg = pd.DataFrame(agg_rows)

# ── Scatter for panel (c) ─────────────────────────────────────────────────────
scatter    = raw.sample(n=min(2000, len(raw)), random_state=42).copy()
r_pearson  = raw["delay_mean"].corr(raw["gini_mean"])
r_spearman = raw["delay_mean"].corr(raw["gini_mean"], method="spearman")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURA
# ══════════════════════════════════════════════════════════════════════════════
plt.rcParams.update({
    "font.family":     "serif",
    "font.size":       16,
    "axes.titlesize":  18,
    "axes.labelsize":  16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 13,
    "figure.dpi":      150,
})

fig, axes = plt.subplots(1, 3, figsize=(21, 7))
ax1, ax2, ax3 = axes

# ══════════════════════════════════════════════════════════════════════════════
# PANEL (a): Delay vs Saturation
# ══════════════════════════════════════════════════════════════════════════════
for city in sorted(raw["city"].unique()):
    style = CITY_STYLE[city]
    for model, pstyle in POLICY_STYLE.items():
        cdata = agg[(agg["city"] == city) & (agg["model"] == model)].sort_values("v_c")
        if len(cdata) == 0:
            continue
        x = cdata["v_c"].values
        y = cdata["delay_median"].values
        x_off = x + (-0.015 if model == "ppo_coop_ideal" else 0.015)

        mk = style["marker"]
        if pstyle["fill"] == "none":
            ax1.plot(x_off, y, marker=mk, linestyle=pstyle["ls"],
                     linewidth=pstyle["lw"], color=style["color"],
                     markersize=12, markerfacecolor="white",
                     markeredgewidth=1.2, markeredgecolor=style["color"], alpha=0.85)
        else:
            ax1.plot(x_off, y, marker=mk, linestyle=pstyle["ls"],
                     linewidth=pstyle["lw"], color=style["color"],
                     markersize=12, markerfacecolor=style["color"],
                     markeredgewidth=0.5, markeredgecolor="white", alpha=0.85)

        if model == "ppo_coop_chaos":
            ax1.fill_between(x, cdata["delay_lo"].values,
                             cdata["delay_hi"].values,
                             color=style["color"], alpha=0.08)

ax1.set_yscale("log")
ax1.set_ylabel("Median Delay (s)", fontweight="bold")
ax1.set_xlabel("Saturation Level ($v/c$)")
ax1.set_title("(a) Delay vs Saturation", fontweight="bold")
ax1.set_xticks(VC_VALUES)
ax1.set_xticklabels([f"{v:.2f}" for v in VC_VALUES])
ax1.grid(True, alpha=0.2, linewidth=0.5)
ax1.set_ylim(1, 800_000)   # ampliado para dar espacio a la anotación superior

# Línea de bifurcación
ax1.axvline(x=0.90, color="red", linestyle="--", linewidth=2.5, alpha=0.5, zorder=1)

# FIX 3 — anotación "Bifurcation" en el margen SUPERIOR con flecha descendente
ax1.annotate(
    "Bifurcation\n$v/c = 0.90$",
    xy=(0.90, 700_000),
    xytext=(0.65, 500_000),
    xycoords="data",
    textcoords="data",
    fontsize=13,
    fontstyle="italic",
    color="#333333",
    ha="center",
    va="top",
    arrowprops=dict(
        arrowstyle="-|>",
        color="#555555",
        lw=1.1,
        alpha=0.75,
        connectionstyle="arc3,rad=0.0",
    ),
    bbox=dict(boxstyle="round,pad=0.3", facecolor="#fffde7",
              edgecolor="#aaaaaa", alpha=0.93, lw=0.7),
    annotation_clip=False,
    zorder=10,
)

# Línea de referencia gridlock
ax1.axhline(y=2000, color="gray", linestyle=":", linewidth=1, alpha=0.4)

# FIX 2 — Policy legend en esquina SUPERIOR IZQUIERDA (zona vacía en panel a)
policy_handles = [
    Line2D([0], [0], color="black", linestyle="-",  linewidth=2.5, label="Coop-Ideal"),
    Line2D([0], [0], color="black", linestyle="--", linewidth=2.5, label="Coop-Chaos"),
]
ax1.legend(
    handles=policy_handles,
    loc="upper left",
    framealpha=0.88,
    fontsize=13,
    title="Policy",
    title_fontsize=14,
    handlelength=1.8,
    borderpad=0.5,
)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL (b): Gini vs Saturation
# ══════════════════════════════════════════════════════════════════════════════
for city in sorted(raw["city"].unique()):
    style = CITY_STYLE[city]
    for model, pstyle in POLICY_STYLE.items():
        cdata = agg[(agg["city"] == city) & (agg["model"] == model)].sort_values("v_c")
        if len(cdata) == 0:
            continue
        x     = cdata["v_c"].values
        y     = cdata["gini_median"].values
        x_off = x + (-0.015 if model == "ppo_coop_ideal" else 0.015)

        mk = style["marker"]
        if pstyle["fill"] == "none":
            ax2.plot(x_off, y, marker=mk, linestyle=pstyle["ls"],
                     linewidth=pstyle["lw"], color=style["color"],
                     markersize=12, markerfacecolor="white",
                     markeredgewidth=1.2, markeredgecolor=style["color"], alpha=0.85)
        else:
            ax2.plot(x_off, y, marker=mk, linestyle=pstyle["ls"],
                     linewidth=pstyle["lw"], color=style["color"],
                     markersize=12, markerfacecolor=style["color"],
                     markeredgewidth=0.5, markeredgecolor="white", alpha=0.85)

        if model == "ppo_coop_chaos":
            ax2.fill_between(x, cdata["gini_lo"].values,
                             cdata["gini_hi"].values,
                             color=style["color"], alpha=0.08)

ax2.set_ylabel("Gini Coefficient", fontweight="bold")
ax2.set_xlabel("Saturation Level ($v/c$)")
ax2.set_title("(b) Equity (Gini) vs Saturation", fontweight="bold")
ax2.set_xticks(VC_VALUES)
ax2.set_xticklabels([f"{v:.2f}" for v in VC_VALUES])
ax2.grid(True, alpha=0.2, linewidth=0.5)
ax2.set_ylim(0, 0.82)   # ampliado de 0.72 → 0.82 para dar espacio a anotación

# Línea de bifurcación
ax2.axvline(x=0.90, color="red", linestyle="--", linewidth=2.5, alpha=0.5, zorder=1)

# FIX 4b — "Quito Paradox" → zona INFERIOR IZQUIERDA (despejada)
#           con flecha curva apuntando hacia el punto del paradox en Quito
quito_chaos = agg[(agg["city"] == "Quito") &
                  (agg["model"] == "ppo_coop_chaos") &
                  (agg["v_c"] == 0.9)]
arrow_y = float(quito_chaos["gini_median"].values[0]) if len(quito_chaos) else 0.50

ax2.annotate(
    "Quito Paradox:\nChaos policy\nworsens equity",
    xy=(0.90, arrow_y),          # punta: punto v/c=0.90 de Quito-chaos
    xytext=(0.37, 0.70),         # texto: zona superior izquierda vacía
    xycoords="data",
    textcoords="data",
    fontsize=13,
    fontstyle="italic",
    color="#333333",
    ha="left",
    va="bottom",
    arrowprops=dict(
        arrowstyle="-|>",
        color="#555555",
        lw=1.1,
        alpha=0.75,
        connectionstyle="arc3,rad=-0.25",
    ),
    bbox=dict(boxstyle="round,pad=0.3", facecolor="#fffde7",
              edgecolor="#aaaaaa", alpha=0.93, lw=0.7),
    zorder=10,
)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL (c): Gini vs Delay scatter
# ══════════════════════════════════════════════════════════════════════════════
chaos_colors = {
    "low":      "#0571b0",
    "mid":      "#92c5de",
    "mid_high": "#d9d9d9",
    "high":     "#f4a582",
    "extreme":  "#ca0020",
}

for chaos in CHAOS_ORDER:
    sub = scatter[scatter["chaos_level"] == chaos]
    ax3.scatter(sub["delay_mean"], sub["gini_mean"],
                c=chaos_colors[chaos], s=12, alpha=0.50,
                label=chaos.replace("_", " ").title(),
                edgecolors="white", linewidth=0.2, rasterized=True)

ax3.set_xscale("log")
ax3.set_xlabel("Mean Delay (s)", fontweight="bold")
ax3.set_ylabel("Gini Coefficient", fontweight="bold")
ax3.set_title(
    "(c) Spatial Inequality Amplification:\n"
    "Gini vs Delay Across All Cities and Chaos Levels",
    fontweight="bold",
)
ax3.legend(loc="upper left", framealpha=0.85, markerscale=5,
           title="Chaos Level", title_fontsize=15,
           bbox_to_anchor=(0.02, 0.98),
           bbox_transform=ax3.transAxes)
ax3.grid(True, alpha=0.2, linewidth=0.5)
ax3.set_xlim(0.5, 250_000)
ax3.set_ylim(0, 0.82)



# Línea de gridlock
ax3.axvline(x=2000, color="red", linestyle="--", linewidth=2.5, alpha=0.4)



# Flecha de divergencia — desde zona baja-izquierda hacia alta-derecha
ax3.annotate(
    "",
    xy=(80_000, 0.62),
    xytext=(600, 0.12),
    arrowprops=dict(arrowstyle="-|>", color="#555555",
                    lw=1.1, alpha=0.75),
)
# Etiqueta "Divergence" en la parte SUPERIOR DERECHA
ax3.text(0.98, 0.90,
         "Divergence by\ndifferential\nsaturation",
         transform=ax3.transAxes,
         fontsize=13, fontstyle="italic", color="#333333",
         ha="right", va="top",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="#fffde7",
                   edgecolor="#aaaaaa", alpha=0.93, lw=0.7))

# ══════════════════════════════════════════════════════════════════════════════
# FIX 1 — Leyenda de ciudades: fig.legend() ENCIMA de los 3 paneles
#          (una sola fila horizontal, fuera de cualquier axes)
# ══════════════════════════════════════════════════════════════════════════════
city_handles = [
    Line2D([0], [0],
           marker=CITY_STYLE[city]["marker"],
           color=CITY_STYLE[city]["color"],
           markersize=11,
           linewidth=0,
           label=f"{city} ({CITY_STYLE[city]['topology']})",
           markerfacecolor=CITY_STYLE[city]["color"],
           markeredgewidth=0.5,
           markeredgecolor="white")
    for city in sorted(raw["city"].unique())
]

fig.legend(
    handles=city_handles,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.00),   # justo encima del área de plots
    ncol=6,                        # todas las ciudades en una fila
    fontsize=13,
    framealpha=0.90,
    edgecolor="gray",
    columnspacing=0.8,
    handlelength=1.0,
    handletextpad=0.4,
    borderpad=0.5,
)

# FIX 5 — tight_layout con rect reservando espacio para la leyenda superior
fig.tight_layout(rect=[0, 0, 1, 0.93])

# ── Guardar ───────────────────────────────────────────────────────────────────
for fmt in ["pdf", "png"]:
    path = FIGURES_DIR / f"fig_bifurcation_v4.{fmt}"
    fig.savefig(path, format=fmt, bbox_inches="tight", dpi=300)
    print(f"[OK] {path}")