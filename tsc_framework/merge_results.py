"""
merge_results.py
================
Fusiona todos los archivos *_detailed.csv generados en outputs/results
en un único dataset maestro: master_results.csv

Características:
  - Detecta automáticamente todos los archivos *_detailed.csv
  - Desambigua y corrige columnas faltantes (si algún CSV antiguo no tiene city/model)
  - Elimina filas duplicadas (misma combinación model+city+chaos_level+episode+seed)
  - Añade columna 'source_file' para trazabilidad
  - Genera master_results.csv y master_summary.csv con estadísticas clave
  - Imprime un informe de calidad al final

Uso:
  python merge_results.py

Salida:
  outputs/results/master_results.csv      <- dataset maestro row-level
  outputs/results/master_summary.csv      <- medianas/IQR/colapso por grupo
  outputs/results/merge_report.txt        <- informe de calidad de la fusión
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

# ── Configuración ──────────────────────────────────────────────────────────────
RESULTS_DIR = Path(__file__).parent / "outputs" / "results"
MASTER_CSV   = RESULTS_DIR / "master_results.csv"
SUMMARY_CSV  = RESULTS_DIR / "master_summary.csv"
REPORT_TXT   = RESULTS_DIR / "merge_report.txt"

# Columnas canónicas esperadas en los _detailed.csv
CANONICAL_COLS = [
    "reward_total", "delay_mean", "queue_mean", "gini_mean",
    "cvar_90", "steps", "collapsed", "co2_total", "fuel_total",
    "model", "city", "chaos_level", "episode", "seed"
]

# Columnas que identifican unívocamente un episodio (para deduplicación)
DEDUP_KEYS = ["model", "city", "chaos_level", "episode", "seed"]

# Orden canónico de niveles de caos
CHAOS_ORDER = ["low", "mid", "mid_high", "high", "extreme"]

# ── Funciones auxiliares ───────────────────────────────────────────────────────

def load_detailed_csv(path: Path) -> pd.DataFrame:
    """Carga un _detailed.csv y normaliza sus columnas."""
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"  [WARN] No se pudo leer {path.name}: {e}")
        return pd.DataFrame()

    # Añadir columna de trazabilidad
    df["source_file"] = path.name

    # Normalizar nombres de columnas (strip + lowercase)
    df.columns = [c.strip().lower() for c in df.columns]

    # Si falta 'city' o 'model', intentar inferir del nombre de archivo
    stem = path.stem  # ej. transfer_n30_eur_detailed
    if "city" not in df.columns:
        df["city"] = _infer_city_from_filename(stem)
    if "model" not in df.columns:
        df["model"] = _infer_model_from_filename(stem)
    if "chaos_level" not in df.columns:
        df["chaos_level"] = _infer_chaos_from_filename(stem)

    # Asegurar que las columnas canónicas numéricas existen
    for col in ["reward_total", "delay_mean", "queue_mean", "gini_mean",
                "cvar_90", "steps", "collapsed", "co2_total", "fuel_total"]:
        if col not in df.columns:
            df[col] = np.nan

    for col in ["episode", "seed"]:
        if col not in df.columns:
            df[col] = np.nan

    return df


def _infer_city_from_filename(stem: str) -> str:
    stem_lower = stem.lower()
    mapping = {
        "berlin": "Berlin", "bcn": "Barcelona", "barcelona": "Barcelona",
        "madrid": "Madrid", "eur": "EUR_multi",
        "quito": "Quito", "bogota": "Bogota", "bogotá": "Bogota",
        "cdmx": "CDMX", "latam": "LATAM_multi",
    }
    for key, val in mapping.items():
        if key in stem_lower:
            return val
    return "Unknown"


def _infer_model_from_filename(stem: str) -> str:
    stem_lower = stem.lower()
    if "coop_ideal" in stem_lower:
        return "ppo_coop_ideal"
    if "coop_chaos" in stem_lower:
        return "ppo_coop_chaos"
    if "ppo_chaos" in stem_lower:
        return "ppo_chaos"
    if "ppo_ideal" in stem_lower:
        return "ppo_ideal"
    if "baseline" in stem_lower:
        return "baseline_multi"
    return "unknown"


def _infer_chaos_from_filename(stem: str) -> str:
    stem_lower = stem.lower()
    if "extreme" in stem_lower:
        return "extreme"
    if "mid_high" in stem_lower or "mid-high" in stem_lower:
        return "mid_high"
    if "high" in stem_lower:
        return "high"
    if "mid" in stem_lower:
        return "mid"
    if "low" in stem_lower:
        return "low"
    return "unknown"


def compute_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula estadísticas por grupo (model × city × chaos_level)."""
    group_cols = ["model", "city", "chaos_level"]

    def pct_collapse(x):
        return 100.0 * x.sum() / len(x)

    def iqr(x):
        return x.quantile(0.75) - x.quantile(0.25)

    agg = df.groupby(group_cols).agg(
        n_episodes      = ("episode",    "count"),
        delay_median    = ("delay_mean", "median"),
        delay_mean_val  = ("delay_mean", "mean"),
        delay_iqr       = ("delay_mean", iqr),
        gini_median     = ("gini_mean",  "median"),
        gini_iqr        = ("gini_mean",  iqr),
        cvar90_median   = ("cvar_90",    "median"),
        cvar90_iqr      = ("cvar_90",    iqr),
        collapse_rate   = ("collapsed",  pct_collapse),
        co2_median      = ("co2_total",  "median"),
        fuel_median     = ("fuel_total", "median"),
    ).reset_index()

    # Ordenar chaos_level canónicamente
    agg["chaos_order"] = agg["chaos_level"].apply(
        lambda x: CHAOS_ORDER.index(x) if x in CHAOS_ORDER else 99
    )
    agg = agg.sort_values(["model", "city", "chaos_order"]).drop(columns="chaos_order")

    return agg


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  MERGE RESULTS — Script de fusión de resultados de experimentos")
    print(f"  Directorio: {RESULTS_DIR}")
    print(f"  Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 1. Detectar todos los _detailed.csv
    detailed_files = sorted(RESULTS_DIR.glob("*_detailed.csv"))
    print(f"\n[1/5] Archivos *_detailed.csv detectados: {len(detailed_files)}")
    for f in detailed_files:
        size_kb = f.stat().st_size / 1024
        print(f"      {f.name:<60s} {size_kb:>7.1f} KB")

    if not detailed_files:
        print("\n[ERROR] No se encontraron archivos *_detailed.csv. Verifica el directorio.")
        sys.exit(1)

    # 2. Cargar y concatenar
    print(f"\n[2/5] Cargando y concatenando {len(detailed_files)} archivos...")
    frames = []
    load_errors = []
    for f in detailed_files:
        df = load_detailed_csv(f)
        if df.empty:
            load_errors.append(f.name)
            continue
        frames.append(df)
        print(f"      {f.name:<60s} {len(df):>6d} filas")

    master = pd.concat(frames, ignore_index=True)
    total_raw = len(master)
    print(f"\n      Total filas cargadas (raw): {total_raw:,}")

    # 3. Deduplicación
    print(f"\n[3/5] Deduplicando por {DEDUP_KEYS}...")
    before_dedup = len(master)
    master = master.sort_values("source_file")          # más reciente al final (sort alfab.)
    master = master.drop_duplicates(subset=DEDUP_KEYS, keep="last")
    after_dedup = len(master)
    n_dupes = before_dedup - after_dedup
    print(f"      Duplicados eliminados: {n_dupes:,}")
    print(f"      Filas únicas: {after_dedup:,}")

    # 4. Verificaciones de calidad
    print(f"\n[4/5] Verificaciones de calidad...")
    n_missing_model   = master["model"].isna().sum() + (master["model"] == "unknown").sum()
    n_missing_city    = master["city"].isna().sum() + (master["city"] == "Unknown").sum()
    n_missing_chaos   = master["chaos_level"].isna().sum() + (master["chaos_level"] == "unknown").sum()
    n_null_delay      = master["delay_mean"].isna().sum()
    n_collapsed       = int(master["collapsed"].sum())

    print(f"      Modelos desconocidos   : {n_missing_model}")
    print(f"      Ciudades desconocidas  : {n_missing_city}")
    print(f"      Caos desconocido       : {n_missing_chaos}")
    print(f"      delay_mean nulo        : {n_null_delay}")
    print(f"      Episodios colapsados   : {n_collapsed} / {after_dedup}")

    # Cobertura
    print("\n      Cobertura por modelo × ciudad × nivel de caos:")
    coverage = (
        master.groupby(["model", "city", "chaos_level"])
        .size()
        .reset_index(name="n_episodes")
    )
    coverage["chaos_order"] = coverage["chaos_level"].apply(
        lambda x: CHAOS_ORDER.index(x) if x in CHAOS_ORDER else 99
    )
    coverage = coverage.sort_values(["model", "city", "chaos_order"]).drop(columns="chaos_order")

    # Pivotar para visualización compacta
    pivot = coverage.pivot_table(
        index=["model", "city"],
        columns="chaos_level",
        values="n_episodes",
        aggfunc="sum",
        fill_value=0
    ).reindex(columns=[c for c in CHAOS_ORDER if c in coverage["chaos_level"].unique()], fill_value=0)
    print(pivot.to_string())

    # 5. Guardar
    print(f"\n[5/5] Guardando resultados...")

    # Reordenar columnas: canónicas primero + source_file al final
    ordered_cols = [c for c in CANONICAL_COLS if c in master.columns]
    extra_cols   = [c for c in master.columns if c not in ordered_cols and c != "source_file"]
    final_cols   = ordered_cols + extra_cols + ["source_file"]
    master = master[final_cols]

    master.to_csv(MASTER_CSV, index=False)
    print(f"      master_results.csv guardado  → {MASTER_CSV}")
    print(f"      Tamaño: {MASTER_CSV.stat().st_size / 1024:.1f} KB | {len(master):,} filas")

    summary = compute_summary(master)
    summary.to_csv(SUMMARY_CSV, index=False)
    print(f"      master_summary.csv guardado  → {SUMMARY_CSV}")
    print(f"      Grupos: {len(summary)}")

    # 6. Informe de texto
    report_lines = [
        f"MERGE REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 70,
        f"Archivos fusionados        : {len(detailed_files)}",
        f"Filas raw cargadas         : {total_raw:,}",
        f"Duplicados eliminados      : {n_dupes:,}",
        f"Filas únicas en master     : {after_dedup:,}",
        f"Episodios colapsados       : {n_collapsed}",
        f"Archivos con error de carga: {len(load_errors)}",
        "",
        "Archivos con error:",
    ] + [f"  - {e}" for e in load_errors] + [
        "",
        "Cobertura (model × city × chaos_level):",
        pivot.to_string(),
        "",
        "Resumen estadístico (primeras 30 filas):",
        summary.head(30).to_string(index=False),
    ]
    REPORT_TXT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"      merge_report.txt guardado    → {REPORT_TXT}")

    print("\n" + "=" * 70)
    print("   FUSIÓN COMPLETADA EXITOSAMENTE")
    print(f"  Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Vista rápida del summary
    print("\n  PREVIEW — master_summary.csv (primeras 20 filas):")
    print(summary.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
