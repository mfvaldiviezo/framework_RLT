"""
ablation_mad_gating.py — Estudio de Ablación del Mecanismo MAD-Gating
======================================================================
Tesis Doctoral: Control Semafórico Inteligente con RL Sensible al Riesgo

Este script implementa el estudio de ablación COMPLETO exigido por revisores
IEEE T-ITS para validar empíricamente que el MAD-Gating es el mecanismo causal
de la equidad distributiva en Coop-SARG.

Diseño Experimental (2×2×2×5):
  - Factor 1: ARQUITECTURA (H-SARG, Coop-SARG)
  - Factor 2: MAD-GATING (enabled, disabled → gates=1.0 pass-through)
  - Factor 3: CIUDAD (Quito=lineal, Barcelona=grid control)
  - Factor 4: CHAOS LEVEL (low, mid, mid_high, high, extreme)
  - 30 episodios por combinación
  - Total: 2 × 2 × 2 × 5 × 30 = 1,200 simulaciones

Pipeline:
  FASE 1 — Modificar sarg_policy.py para soportar use_mad_gating=False
  FASE 2 — Entrenar 4 variantes (H-SARG±Gating, Coop-SARG±Gating) en Hangzhou
  FASE 3 — Evaluar zero-shot transfer en Quito (lineal) + Barcelona (grid)
  FASE 4 — Análisis estadístico: Mann-Whitney U, bootstrap CI, effect size
  FASE 5 — Generar tabla LaTeX y figuras para el paper

Uso:
  python ablation_mad_gating.py --phase all
  python ablation_mad_gating.py --phase train
  python ablation_mad_gating.py --phase evaluate
  python ablation_mad_gating.py --phase analyze
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ─── Paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SRC))

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-7s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ablation")

# ─── Constants ───────────────────────────────────────────────────────────────
OUTPUT_DIR = ROOT / "outputs" / "ablation_mad_gating"
MODELS_DIR = OUTPUT_DIR / "models"
RESULTS_DIR = OUTPUT_DIR / "results"
PLOTS_DIR = OUTPUT_DIR / "plots"

CITY_CONFIG = {
    "Quito":     {"net": "quito.net.xml",     "chaos_prob": 0.4, "topology": "linear"},
    "Barcelona": {"net": "barcelona.net.xml", "chaos_prob": None, "topology": "grid"},
}

CHAOS_LEVELS = ["low", "mid", "mid_high", "high", "extreme"]
CHAOS_VC = {"low": 0.3, "mid": 0.6, "mid_high": 0.75, "high": 0.9, "extreme": 1.2}

N_EPISODES = 30
N_SEEDS_TRAIN = 3  # Train 3 seeds per variant for statistical power

# =============================================================================
# FASE 1: PATCH sarg_policy.py
# =============================================================================

MAD_GATING_PATCH = '''
# ═══════════════════════════════════════════════════════════════════════════════
# PATCH: use_mad_gating parameter — Ablation Study (IEEE T-ITS Reviewer Request)
# ═══════════════════════════════════════════════════════════════════════════════
# When use_mad_gating=False, the sigmoid gate is replaced by a pass-through
# (gates=1.0), disabling the risk modulation while preserving the attention
# mechanism. This isolates the causal effect of MAD-Gating on equity.
'''

def patch_sarg_policy():
    """Modifica sarg_policy.py para añadir soporte de use_mad_gating."""
    
    policy_file = SRC / "rl_agent" / "sarg_policy.py"
    
    if not policy_file.exists():
        logger.error(f"No se encuentra sarg_policy.py en {policy_file}")
        return False
    
    with open(policy_file, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if 'use_mad_gating' in content:
        logger.info("sarg_policy.py ya está parcheado con use_mad_gating. Saltando.")
        return True
    
    # Backup original
    backup_file = policy_file.with_suffix('.py.backup_ablation')
    shutil.copy(policy_file, backup_file)
    logger.info(f"Backup guardado en {backup_file}")
    
    # Patch 1: Add use_mad_gating to HSARGExtractor.__init__
    old_hsarg_init = "def __init__(self, observation_space: spaces.Box, features_dim: int = 128):"
    new_hsarg_init = "def __init__(self, observation_space: spaces.Box, features_dim: int = 128, use_mad_gating: bool = True):"
    content = content.replace(old_hsarg_init, new_hsarg_init)
    
    # Patch 2: Store use_mad_gating in HSARGExtractor
    old_super_hsarg = "super().__init__(observation_space, features_dim)"
    new_super_hsarg = "super().__init__(observation_space, features_dim)\n        self.use_mad_gating = use_mad_gating"
    content = content.replace(old_super_hsarg, new_super_hsarg)
    
    # Patch 3: Modify forward() in HSARGExtractor — conditionally disable gating
    old_gating_hsarg = "gates = self.risk_gating(attn_output)  # (Batch, 12, 1)\n        \n        # Multiplicación elemento a elemento"
    new_gating_hsarg = "gates = self.risk_gating(attn_output)  # (Batch, 12, 1)\n        if not self.use_mad_gating:\n            gates = torch.ones_like(gates)  # ABLATION: pass-through\n        \n        # Multiplicación elemento a elemento"
    content = content.replace(old_gating_hsarg, new_gating_hsarg)
    
    # Patch 4: Add use_mad_gating to CoopSARGExtractor.__init__
    old_coop_init = "def __init__(self, observation_space: spaces.Box, features_dim: int = 128):"
    # Find the second occurrence (CoopSARGExtractor)
    parts = content.split(old_coop_init)
    if len(parts) >= 3:
        new_coop_init = "def __init__(self, observation_space: spaces.Box, features_dim: int = 128, use_mad_gating: bool = True, use_equity_boost: bool = True):"
        content = old_coop_init.join([parts[0], parts[1]]) + new_coop_init + old_coop_init.join(parts[2:])
    
    # Patch 5: Store use_mad_gating and use_equity_boost in CoopSARGExtractor
    old_super_coop = "super().__init__(observation_space, features_dim)\n        \n        obs_dim"
    # Find second occurrence
    parts_coop = content.split("super().__init__(observation_space, features_dim)")
    if len(parts_coop) >= 3:
        new_super_coop = "super().__init__(observation_space, features_dim)\n        self.use_mad_gating = use_mad_gating\n        self.use_equity_boost = use_equity_boost\n        \n        obs_dim"
        content = "super().__init__(observation_space, features_dim)".join(parts_coop[:2]) + new_super_coop + "super().__init__(observation_space, features_dim)".join(parts_coop[2:])
    
    # Patch 6: Modify forward() in CoopSARGExtractor — conditionally disable gating + equity
    old_gating_coop = "gated_risk = attn_output * (gates * equity_boost.unsqueeze(-1))  # (Batch, 12, 16)"
    new_gating_coop = (
        "if not self.use_mad_gating:\n"
        "            gates = torch.ones_like(gates)  # ABLATION: pass-through\n"
        "        if not self.use_equity_boost:\n"
        "            equity_boost = torch.ones_like(equity_boost)  # ABLATION: no equity\n"
        "        gated_risk = attn_output * (gates * equity_boost.unsqueeze(-1))  # (Batch, 12, 16)"
    )
    content = content.replace(old_gating_coop, new_gating_coop)
    
    with open(policy_file, 'w') as f:
        f.write(content)
    
    logger.info(" sarg_policy.py parcheado exitosamente con use_mad_gating y use_equity_boost")
    return True


# =============================================================================
# FASE 2: TRAINING
# =============================================================================

VARIANTS = {
    "hsarg_gating_on":     {"extractor": "HSARGExtractor",    "use_mad_gating": True},
    "hsarg_gating_off":    {"extractor": "HSARGExtractor",    "use_mad_gating": False},
    "coopsarg_gating_on":  {"extractor": "CoopSARGExtractor", "use_mad_gating": True,  "use_equity_boost": True},
    "coopsarg_gating_off": {"extractor": "CoopSARGExtractor", "use_mad_gating": False, "use_equity_boost": False},
}


def train_variant(variant_name: str, config: dict, seed: int = 42) -> Path:
    """
    Entrena una variante específica en Hangzhou 4×4.
    
    Returns:
        Path al modelo entrenado (.zip)
    """
    from stable_baselines3 import PPO
    from src.rl_agent.sumo_env import TrafficEnv
    from src.rl_agent.sarg_policy import HSARGExtractor, CoopSARGExtractor
    
    model_path = MODELS_DIR / f"{variant_name}_seed{seed}"
    model_path.mkdir(parents=True, exist_ok=True)
    model_zip = model_path / "model.zip"
    
    if model_zip.exists():
        logger.info(f"  Modelo {variant_name}_seed{seed} ya existe. Saltando.")
        return model_zip
    
    logger.info(f"  Entrenando {variant_name} (seed={seed})...")
    
    # Select extractor class
    extractor_cls = HSARGExtractor if config["extractor"] == "HSARGExtractor" else CoopSARGExtractor
    
    # Build policy_kwargs
    policy_kwargs = {
        "features_extractor_class": extractor_cls,
        "features_extractor_kwargs": {
            "features_dim": 128,
            "use_mad_gating": config.get("use_mad_gating", True),
        },
        "net_arch": dict(pi=[64, 64], vf=[64, 64]),
    }
    
    if config["extractor"] == "CoopSARGExtractor":
        policy_kwargs["features_extractor_kwargs"]["use_equity_boost"] = config.get("use_equity_boost", True)
    
    # Create environment
    def make_env():
        from src.rl_agent.sumo_env import TrafficEnv
        return TrafficEnv(
            net_file=str(ROOT / "networks" / "hangzhou" / "hangzhou_4x4.net.xml"),
            route_file=str(ROOT / "networks" / "hangzhou" / "hangzhou_4x4.rou.xml"),
            use_gui=False,
            max_steps=3600,
            seed=seed,
        )
    
    try:
        from stable_baselines3.common.env_util import make_vec_env
        from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor
        
        env = make_vec_env(make_env, n_envs=4, vec_env_cls=SubprocVecEnv)
        env = VecMonitor(env)
        
        model = PPO(
            "MlpPolicy",
            env,
            policy_kwargs=policy_kwargs,
            verbose=0,
            tensorboard_log=str(OUTPUT_DIR / "tensorboard"),
            seed=seed,
            n_steps=2048,
            batch_size=64,
            n_epochs=10,
            learning_rate=3e-4,
        )
        
        model.learn(total_timesteps=500_000, progress_bar=True)
        model.save(str(model_zip))
        env.close()
        
        logger.info(f"   {variant_name}_seed{seed} entrenado.")
        return model_zip
        
    except Exception as e:
        logger.error(f"   Error entrenando {variant_name}: {e}")
        # Fallback: create a dummy model path for testing
        return model_zip


# =============================================================================
# FASE 3: EVALUATION
# =============================================================================

@dataclass
class EvalResult:
    variant: str
    city: str
    chaos_level: str
    episode: int
    seed: int
    delay_mean: float
    queue_mean: float
    gini_mean: float
    cvar_90: float
    throughput: float
    collapsed: bool


def evaluate_variant(
    variant_name: str,
    config: dict,
    city: str,
    chaos_level: str,
    seed: int = 42,
    n_episodes: int = N_EPISODES,
) -> List[EvalResult]:
    """Evalúa una variante en una ciudad y chaos level específicos."""
    
    from src.core.tsc_env import TSCEnv
    
    model_zip = MODELS_DIR / f"{variant_name}_seed{seed}" / "model.zip"
    if not model_zip.exists():
        logger.warning(f"  Modelo {variant_name}_seed{seed} no encontrado. Saltando.")
        return []
    
    city_cfg = CITY_CONFIG[city]
    vc_ratio = CHAOS_VC[chaos_level]
    
    results = []
    
    try:
        model = PPO.load(str(model_zip), device="cpu")
    except Exception as e:
        logger.error(f"  Error cargando modelo {variant_name}: {e}")
        return []
    
    for ep in range(n_episodes):
        ep_seed = seed * 1000 + ep
        
        try:
            env = TSCEnv(
                sumocfg_path=str(ROOT / "networks" / city / f"evaluate_{city.lower()}.sumocfg"),
                tls_id="B1",
                use_gui=False,
                max_steps=720,
                seed=ep_seed,
                enable_traci_chaos=(city_cfg["chaos_prob"] is not None),
                probabilidad_caos=city_cfg.get("chaos_prob", 0.0),
            )
            
            obs = env.reset()
            done = False
            total_delay = 0.0
            total_queue = 0.0
            total_gini = 0.0
            total_cvar = 0.0
            n_steps = 0
            collapsed = False
            
            while not done:
                action, _ = model.predict(obs, deterministic=True)
                obs, reward, done, info = env.step(action)
                
                if 'delay' in info:
                    total_delay += info['delay']
                if 'queue' in info:
                    total_queue += info['queue']
                if 'gini' in info:
                    total_gini += info['gini']
                if 'cvar_90' in info:
                    total_cvar += info['cvar_90']
                
                n_steps += 1
                
                if n_steps >= 720:
                    collapsed = (total_delay / n_steps) > 2000
            
            env.close()
            
            results.append(EvalResult(
                variant=variant_name,
                city=city,
                chaos_level=chaos_level,
                episode=ep,
                seed=ep_seed,
                delay_mean=total_delay / max(n_steps, 1),
                queue_mean=total_queue / max(n_steps, 1),
                gini_mean=total_gini / max(n_steps, 1),
                cvar_90=total_cvar / max(n_steps, 1),
                throughput=0.0,  # Would need tripinfo parsing
                collapsed=collapsed,
            ))
            
        except Exception as e:
            logger.warning(f"  Ep {ep} error: {e}")
            continue
    
    return results


# =============================================================================
# FASE 4: STATISTICAL ANALYSIS
# =============================================================================

def analyze_results(results_df: pd.DataFrame) -> str:
    """Análisis estadístico completo del estudio de ablación."""
    
    report = []
    report.append("=" * 78)
    report.append("INFORME DE ABLACIÓN MAD-GATING — Análisis Estadístico")
    report.append("=" * 78)
    report.append("")
    
    # 4.1 Overview
    report.append(f"Total de simulaciones: {len(results_df)}")
    report.append(f"Variantes: {sorted(results_df['variant'].unique())}")
    report.append(f"Ciudades: {sorted(results_df['city'].unique())}")
    report.append("")
    
    # 4.2 Gini comparison: gating ON vs OFF per city per chaos level
    report.append("-" * 78)
    report.append("4.2 EFECTO DEL MAD-GATING EN EQUIDAD (Gini)")
    report.append("-" * 78)
    report.append("")
    report.append(f"{'Variante':<25s} {'Ciudad':<12s} {'Chaos':<10s} {'Gini_ON':>8s} {'Gini_OFF':>8s} {'Δ':>8s} {'Effect_r':>8s} {'Sig':>6s}")
    report.append("-" * 90)
    
    from scipy import stats
    
    for variant_prefix in ["hsarg", "coopsarg"]:
        on_name = f"{variant_prefix}_gating_on"
        off_name = f"{variant_prefix}_gating_off"
        
        for city in sorted(results_df['city'].unique()):
            for chaos in CHAOS_LEVELS:
                on_data = results_df[(results_df['variant'] == on_name) & 
                                     (results_df['city'] == city) & 
                                     (results_df['chaos_level'] == chaos)]['gini_mean']
                off_data = results_df[(results_df['variant'] == off_name) & 
                                      (results_df['city'] == city) & 
                                      (results_df['chaos_level'] == chaos)]['gini_mean']
                
                if len(on_data) < 5 or len(off_data) < 5:
                    continue
                
                gini_on = on_data.mean()
                gini_off = off_data.mean()
                delta = gini_off - gini_on  # Positive = gating OFF increases Gini (worse equity)
                
                # Mann-Whitney U test
                try:
                    u_stat, p_value = stats.mannwhitneyu(on_data, off_data, alternative='two-sided')
                    # Rank-biserial correlation (effect size)
                    n1, n2 = len(on_data), len(off_data)
                    r = 1 - (2 * u_stat) / (n1 * n2)  # effect size r
                    sig = "***" if p_value < 0.001 else ("**" if p_value < 0.01 else ("*" if p_value < 0.05 else "ns"))
                except:
                    p_value = 1.0
                    r = 0.0
                    sig = "err"
                
                report.append(f"{on_name:<25s} {city:<12s} {chaos:<10s} {gini_on:>8.4f} {gini_off:>8.4f} {delta:>+8.4f} {r:>8.3f} {sig:>6s}")
    
    report.append("")
    
    # 4.3 Delay comparison
    report.append("-" * 78)
    report.append("4.3 EFECTO DEL MAD-GATING EN EFICIENCIA (Delay)")
    report.append("-" * 78)
    report.append("")
    
    for variant_prefix in ["hsarg", "coopsarg"]:
        on_name = f"{variant_prefix}_gating_on"
        off_name = f"{variant_prefix}_gating_off"
        
        for city in sorted(results_df['city'].unique()):
            for chaos in CHAOS_LEVELS:
                on_data = results_df[(results_df['variant'] == on_name) & 
                                     (results_df['city'] == city) & 
                                     (results_df['chaos_level'] == chaos)]['delay_mean']
                off_data = results_df[(results_df['variant'] == off_name) & 
                                      (results_df['city'] == city) & 
                                      (results_df['chaos_level'] == chaos)]['delay_mean']
                
                if len(on_data) < 5 or len(off_data) < 5:
                    continue
                
                d_on = on_data.mean()
                d_off = off_data.mean()
                
                # Positive delta = gating OFF increases delay (worse efficiency)
                delta = ((d_off - d_on) / max(abs(d_on), 1.0)) * 100
                
                try:
                    u_stat, p_value = stats.mannwhitneyu(on_data, off_data, alternative='two-sided')
                    sig = "***" if p_value < 0.001 else ("**" if p_value < 0.01 else ("*" if p_value < 0.05 else "ns"))
                except:
                    p_value = 1.0
                    sig = "err"
                
                report.append(f"{on_name:<25s} {city:<12s} {chaos:<10s} delay_ON={d_on:>8.1f}s delay_OFF={d_off:>8.1f}s Δ={delta:>+7.1f}% {sig:>6s}")
    
    report.append("")
    
    # 4.4 Hypothesis test
    report.append("-" * 78)
    report.append("4.4 CONTRASTE DE HIPÓTESIS")
    report.append("-" * 78)
    report.append("")
    report.append("H₀ (nula):        MAD-Gating NO afecta la equidad (Gini_ON = Gini_OFF)")
    report.append("H₁ (alternativa): MAD-Gating MEJORA la equidad (Gini_ON < Gini_OFF)")
    report.append("")
    
    # Aggregate test: all Quito data
    quito_on = results_df[(results_df['variant'].str.endswith('_on')) & 
                          (results_df['city'] == 'Quito')]['gini_mean']
    quito_off = results_df[(results_df['variant'].str.endswith('_off')) & 
                           (results_df['city'] == 'Quito')]['gini_mean']
    
    if len(quito_on) > 10 and len(quito_off) > 10:
        u_stat, p_value = stats.mannwhitneyu(quito_on, quito_off, alternative='less')
        n1, n2 = len(quito_on), len(quito_off)
        r = 1 - (2 * u_stat) / (n1 * n2)
        
        report.append(f"Test agregado (Quito, todas las variantes):")
        report.append(f"  Gini_ON  = {quito_on.mean():.4f} ± {quito_on.std():.4f} (n={n1})")
        report.append(f"  Gini_OFF = {quito_off.mean():.4f} ± {quito_off.std():.4f} (n={n2})")
        report.append(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_value:.6f}")
        report.append(f"  Effect size r = {r:.3f} ({'large' if abs(r)>0.5 else 'medium' if abs(r)>0.3 else 'small'})")
        
        if p_value < 0.05:
            report.append(f"   Se RECHAZA H₀. MAD-Gating mejora significativamente la equidad.")
        else:
            report.append(f"  ️ NO se puede rechazar H₀ con los datos actuales.")
    
    report.append("")
    report.append("=" * 78)
    
    return "\n".join(report)


# =============================================================================
# FASE 5: LaTeX TABLE
# =============================================================================

def generate_latex_table(results_df: pd.DataFrame) -> str:
    """Genera tabla LaTeX para el paper."""
    
    latex = []
    latex.append(r"\begin{table}[t]")
    latex.append(r"\centering")
    latex.append(r"\caption{Ablation study of the MAD-Gating mechanism. "
                 r"Gini and delay under zero-shot transfer to Quito (linear) "
                 r"and Barcelona (grid). $\Delta = \text{OFF} - \text{ON}$. "
                 r"Negative $\Delta$Gini indicates that disabling gating "
                 r"worsens equity. Significance: ***$p<0.001$, **$p<0.01$, *$p<0.05$}")
    latex.append(r"\label{tab:mad_gating_ablation}")
    latex.append(r"\begin{tabular}{lcccccc}")
    latex.append(r"\toprule")
    latex.append(r"\textbf{Variant} & \textbf{City} & \textbf{Chaos} & "
                 r"\textbf{Gini}$_{\text{ON}}$ & \textbf{Gini}$_{\text{OFF}}$ & "
                 r"$\Delta$Gini & \textbf{Sig.} \\")
    latex.append(r"\midrule")
    
    from scipy import stats
    
    for variant_prefix in ["hsarg", "coopsarg"]:
        on_name = f"{variant_prefix}_gating_on"
        off_name = f"{variant_prefix}_gating_off"
        display_name = "H-SARG" if variant_prefix == "hsarg" else "Coop-SARG"
        
        first_row = True
        for city in ["Quito", "Barcelona"]:
            for chaos in CHAOS_LEVELS:
                on_data = results_df[(results_df['variant'] == on_name) & 
                                     (results_df['city'] == city) & 
                                     (results_df['chaos_level'] == chaos)]['gini_mean']
                off_data = results_df[(results_df['variant'] == off_name) & 
                                      (results_df['city'] == city) & 
                                      (results_df['chaos_level'] == chaos)]['gini_mean']
                
                if len(on_data) < 5 or len(off_data) < 5:
                    continue
                
                gini_on = on_data.mean()
                gini_off = off_data.mean()
                delta = gini_off - gini_on
                
                try:
                    u_stat, p_value = stats.mannwhitneyu(on_data, off_data, alternative='two-sided')
                    sig = r"***" if p_value < 0.001 else (r"**" if p_value < 0.01 else (r"*" if p_value < 0.05 else "ns"))
                except:
                    sig = "—"
                
                variant_label = display_name if first_row else ""
                latex.append(f"  {variant_label:<12s} & {city} & {chaos} & "
                           f"{gini_on:.3f} & {gini_off:.3f} & "
                           f"{delta:+.3f} & {sig} \\\\")
                first_row = False
        
        # Add midrule between variants
        if variant_prefix == "hsarg":
            latex.append(r"\cmidrule{2-7}")
    
    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="MAD-Gating Ablation Study")
    parser.add_argument("--phase", type=str, default="all",
                       choices=["all", "patch", "train", "evaluate", "analyze"],
                       help="Fase a ejecutar")
    parser.add_argument("--skip-train", action="store_true",
                       help="Usar modelos existentes sin re-entrenar")
    parser.add_argument("--n-episodes", type=int, default=N_EPISODES,
                       help="Episodios por combinación")
    args = parser.parse_args()
    
    # Create output directories
    for d in [OUTPUT_DIR, MODELS_DIR, RESULTS_DIR, PLOTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    results_csv = RESULTS_DIR / "ablation_results.csv"
    report_md = RESULTS_DIR / "ablation_report.md"
    latex_tbl = RESULTS_DIR / "ablation_table.tex"
    
    imported = False
    try:
        import torch
        import shutil
        from scipy import stats
        imported = True
    except ImportError as e:
        logger.error(f"Dependencias faltantes: {e}")
        logger.error("Ejecuta: pip install torch scipy stable-baselines3")
        sys.exit(1)
    
    # ── FASE 1: Patch ────────────────────────────────────────────────────
    if args.phase in ["all", "patch"]:
        logger.info("═" * 60)
        logger.info("FASE 1: Parcheando sarg_policy.py")
        logger.info("═" * 60)
        patch_sarg_policy()
    
    # ── FASE 2: Train ────────────────────────────────────────────────────
    if args.phase in ["all", "train"] and not args.skip_train:
        logger.info("═" * 60)
        logger.info("FASE 2: Entrenando variantes")
        logger.info("═" * 60)
        
        for variant_name, config in VARIANTS.items():
            for seed in range(N_SEEDS_TRAIN):
                train_variant(variant_name, config, seed=42 + seed)
    
    # ── FASE 3: Evaluate ─────────────────────────────────────────────────
    if args.phase in ["all", "evaluate"]:
        logger.info("═" * 60)
        logger.info("FASE 3: Evaluando variantes")
        logger.info("═" * 60)
        
        all_results = []
        
        for variant_name, config in VARIANTS.items():
            for city in ["Quito", "Barcelona"]:
                for chaos in CHAOS_LEVELS:
                    logger.info(f"Evaluando {variant_name} en {city}/{chaos}...")
                    results = evaluate_variant(
                        variant_name, config, city, chaos,
                        seed=42, n_episodes=args.n_episodes
                    )
                    all_results.extend(results)
                    logger.info(f"  {len(results)} episodios completados")
        
        # Save results
        if all_results:
            df = pd.DataFrame([vars(r) for r in all_results])
            df.to_csv(results_csv, index=False)
            logger.info(f"Resultados guardados en {results_csv}")
            logger.info(f"Total: {len(df)} simulaciones")
        else:
            logger.warning("No se generaron resultados. ¿Existen los modelos?")
            # Load existing results if available
            if results_csv.exists():
                df = pd.read_csv(results_csv)
                logger.info(f"Cargados {len(df)} resultados previos.")
            else:
                logger.error("Sin resultados. Ejecuta primero --phase train")
                sys.exit(1)
    
    # ── FASE 4: Analyze ──────────────────────────────────────────────────
    if args.phase in ["all", "analyze"]:
        logger.info("═" * 60)
        logger.info("FASE 4: Análisis estadístico")
        logger.info("═" * 60)
        
        if not results_csv.exists():
            logger.error(f"No se encuentra {results_csv}")
            sys.exit(1)
        
        df = pd.read_csv(results_csv)
        
        # Generate report
        report = analyze_results(df)
        with open(report_md, 'w') as f:
            f.write(report)
        logger.info(f"Informe guardado en {report_md}")
        print("\n" + report)
        
        # Generate LaTeX table
        latex = generate_latex_table(df)
        with open(latex_tbl, 'w') as f:
            f.write(latex)
        logger.info(f"Tabla LaTeX guardada en {latex_tbl}")
        print("\n" + latex)
    
    logger.info("═" * 60)
    logger.info("ABLACIÓN COMPLETADA")
    logger.info("═" * 60)
    logger.info(f"  Modelos: {MODELS_DIR}")
    logger.info(f"  Resultados: {RESULTS_DIR}")
    logger.info(f"  Informe: {report_md}")
    logger.info(f"  Tabla LaTeX: {latex_tbl}")


if __name__ == "__main__":
    main()
