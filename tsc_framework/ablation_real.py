"""
ablation_real.py — Estudio de Ablación MAD-Gating con SUMO REAL
================================================================
Entrena y evalúa variantes con/sin MAD-Gating usando SUMO + TraCI.

Requisitos:
    - stable-baselines3, torch, SUMO_HOME configurado
    - 12-24h de cómputo (GPU recomendada)

Uso:
    python ablation_real.py              # Pipeline completo
    python ablation_real.py --train-only # Solo entrenar
    python ablation_real.py --eval-only  # Solo evaluar (modelos ya entrenados)
"""

import argparse
import os
import sys
import json
import time
import warnings
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── Paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

OUTPUT_DIR = ROOT / "outputs" / "ablation_real"
MODELS_DIR = OUTPUT_DIR / "models"
RESULTS_DIR = OUTPUT_DIR / "results"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Constants ───────────────────────────────────────────────────────────────
TOTAL_TIMESTEPS = 500_000
N_ENVS = 4
N_EVAL_EPISODES = 30
SEEDS = [42]

CITIES_EVAL = ["Quito", "Barcelona"]
CHAOS_LEVELS = ["low", "mid", "mid_high", "high", "extreme"]


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 1: Construir variantes de ablación
# ═══════════════════════════════════════════════════════════════════════════════

def build_ablation_extractors():
    """
    Construye las 4 clases extractoras para el estudio de ablación.
    
    NO modifica sarg_policy.py — crea subclases en memoria.
    """
    import torch
    import torch.nn as nn
    from gymnasium import spaces
    from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
    
    # Importar los originales
    from src.rl_agent.sarg_policy import HSARGExtractor, CoopSARGExtractor
    
    # ── H-SARG con MAD-Gating (original) ─────────────────────────────────
    HSARG_ON = HSARGExtractor  # sin cambios
    
    # ── H-SARG SIN MAD-Gating ────────────────────────────────────────────
    class HSARG_OFF(HSARGExtractor):
        """H-SARG con gating deshabilitado (gates=1.0)."""
        def forward(self, observations):
            batch_size = observations.shape[0]
            queues = observations[:, 0:12]
            waits = observations[:, 12:24]
            nominal_features = observations[:, 24:34]
            nominal_latent = self.nominal_net(nominal_features)
            risk_grouped = torch.stack([queues, waits], dim=-1)
            risk_embed = self.carril_embed(risk_grouped)
            attn_output, attn_weights = self.self_attention(risk_embed, risk_embed, risk_embed)
            self.last_attention_weights = attn_weights.detach().cpu().numpy()
            # ABLACIÓN: pass-through
            gates = torch.ones(attn_output.shape[0], attn_output.shape[1], 1, device=attn_output.device)
            gated_risk = attn_output * gates
            gated_risk_flat = gated_risk.reshape(batch_size, -1)
            risk_latent = self.risk_reducer(gated_risk_flat)
            combined = torch.cat([nominal_latent, risk_latent], dim=-1)
            return self.fusion_net(combined)
    
    # ── Coop-SARG con MAD-Gating (original) ──────────────────────────────
    COOP_ON = CoopSARGExtractor  # sin cambios
    
    # ── Coop-SARG SIN MAD-Gating ─────────────────────────────────────────
    class COOP_OFF(CoopSARGExtractor):
        """Coop-SARG con gating + equity boost deshabilitados."""
        def forward(self, observations):
            batch_size = observations.shape[0]
            queues = observations[:, 0:12]
            waits = observations[:, 12:24]
            pressures = observations[:, 24:28]
            nominal_features = observations[:, 28:34]
            nominal_latent = self.nominal_net(nominal_features)
            max_q, _ = torch.max(queues, dim=-1, keepdim=True)
            resilience_scale = torch.exp(max_q / 10.0)
            pressures_resilient = pressures * resilience_scale
            lane_pressure = torch.repeat_interleave(pressures_resilient, repeats=3, dim=-1)
            risk_grouped = torch.stack([queues, waits, lane_pressure], dim=-1)
            risk_embed = self.carril_embed(risk_grouped)
            attn_output, attn_weights = self.self_attention(risk_embed, risk_embed, risk_embed)
            self.last_attention_weights = attn_weights.detach().cpu().numpy()
            # ABLACIÓN: pass-through gates + equity=1.0
            gates = torch.ones(attn_output.shape[0], attn_output.shape[1], 1, device=attn_output.device)
            self.last_cooperative_gates = gates.detach().cpu().numpy()
            equity_boost = torch.ones(batch_size, 12, device=attn_output.device)
            gated_risk = attn_output * (gates * equity_boost.unsqueeze(-1))
            gated_risk_flat = gated_risk.reshape(batch_size, -1)
            risk_latent = self.risk_reducer(gated_risk_flat)
            combined = torch.cat([nominal_latent, risk_latent], dim=-1)
            return self.fusion_net(combined)
    
    variants = {
        "hsarg_gating_on":  {"cls": HSARG_ON,  "label": "H-SARG (gating ON)",  "gating": True},
        "hsarg_gating_off": {"cls": HSARG_OFF, "label": "H-SARG (gating OFF)", "gating": False},
        "coopsarg_gating_on":  {"cls": COOP_ON,  "label": "Coop-SARG (gating ON)",  "gating": True},
        "coopsarg_gating_off": {"cls": COOP_OFF, "label": "Coop-SARG (gating OFF)", "gating": False},
    }
    
    return variants


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 2: Entrenamiento con SUMO + PPO
# ═══════════════════════════════════════════════════════════════════════════════

def train_one_variant(name: str, extractor_cls, seed: int, total_timesteps: int) -> Path:
    """Entrena UNA variante en Hangzhou 4x4 con PPO."""
    from stable_baselines3 import PPO
    from stable_baselines3.common.env_util import make_vec_env
    from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor
    from src.core.tsc_env import TSCEnv
    
    model_zip = MODELS_DIR / f"{name}_seed{seed}.zip"
    if model_zip.exists():
        print(f"  [OK] {name} seed={seed} ya existe. Saltando entrenamiento.")
        return model_zip
    
    print(f"  [TRAIN] Entrenando {name} seed={seed} ({total_timesteps:,} steps)...")
    t_start = time.time()
    
    policy_kwargs = {
        "features_extractor_class": extractor_cls,
        "features_extractor_kwargs": {"features_dim": 128},
        "net_arch": dict(pi=[64, 64], vf=[64, 64]),
    }
    
    # Crear sumocfg temporal con rutas absolutas (evita problemas de paths relativos)
    sumocfg_dir = OUTPUT_DIR / "sumocfg"
    sumocfg_dir.mkdir(parents=True, exist_ok=True)
    sumocfg_path = sumocfg_dir / "hangzhou_ablation.sumocfg"
    
    net_xml = ROOT / "sumo_configs" / "networks" / "hangzhou_4x4.net.xml"
    route_xml = ROOT / "sumo_configs" / "routes" / "hangzhou" / "hangzhou_minimal.rou.xml"
    
    sumocfg_path.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="{net_xml.as_posix()}"/>
        <route-files value="{route_xml.as_posix()}"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="3600"/>
    </time>
    <processing>
        <time-to-teleport value="300"/>
        <waiting-time-memory value="10000"/>
    </processing>
    <report>
        <no-warnings value="true"/>
    </report>
</configuration>""")
    
    # Matar procesos SUMO zombies que bloquean puertos
    import subprocess as sp
    try:
        sp.run(["taskkill", "/F", "/IM", "sumo.exe"], capture_output=True, timeout=5)
        sp.run(["taskkill", "/F", "/IM", "sumo-gui.exe"], capture_output=True, timeout=5)
        time.sleep(2)
    except Exception:
        pass
    
    # Wrapper que reintenta si hay conflicto de puerto SUMO
    class RobustTSCEnv(TSCEnv):
        def reset(self, **kwargs):
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    return super().reset(**kwargs)
                except RuntimeError as e:
                    if "Address already in use" in str(e) and attempt < max_retries - 1:
                        wait = 2 * (attempt + 1)
                        print(f"    [WARN] Conflicto de puerto SUMO, reintentando en {wait}s...")
                        time.sleep(wait)
                        # Cambiar puerto para el siguiente intento
                        self._traci_port = 8813 + ((self.seed_val + attempt * 100) % 500)
                    else:
                        raise
    
    sumocfg_path_str = str(sumocfg_path)
    
    def make_env(rank=0):
        return RobustTSCEnv(
            sumocfg_path=sumocfg_path_str,
            tls_id="B1",
            use_gui=False,
            max_steps=720,
            seed=seed + rank,
        )
    
    env = make_vec_env(make_env, n_envs=1, seed=seed)
    env = VecMonitor(env)
    
    # Checkpoint: guardar cada 50k steps para no perder progreso
    checkpoint_dir = MODELS_DIR / f"{name}_seed{seed}_checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    from stable_baselines3.common.callbacks import CheckpointCallback
    checkpoint_callback = CheckpointCallback(
        save_freq=10_000 // (1),  # cada ~8 min con CPU
        save_path=str(checkpoint_dir),
        name_prefix=f"{name}_seed{seed}",
        save_replay_buffer=False,
        save_vecnormalize=False,
    )
    
    # Si hay un checkpoint previo, cargarlo para continuar
    existing_checkpoints = sorted(checkpoint_dir.glob(f"{name}_seed{seed}*_steps.zip"))
    if existing_checkpoints:
        latest = existing_checkpoints[-1]
        steps_done = int(latest.stem.split("_")[-2])
        print(f"    [RESUME] Cargando checkpoint {latest.name} ({steps_done:,} steps previos)")
        model = PPO.load(str(latest), env=env, device="cpu")
        remaining = total_timesteps - steps_done
    else:
        model = PPO(
            "MlpPolicy", env,
            policy_kwargs=policy_kwargs,
            verbose=0,
            seed=seed,
            device="cpu",
            n_steps=512, batch_size=64, n_epochs=10,
            learning_rate=3e-4,
            tensorboard_log=str(OUTPUT_DIR / "tensorboard"),
        )
        remaining = total_timesteps
    
    model.learn(total_timesteps=remaining, progress_bar=True, callback=checkpoint_callback)
    model.save(str(model_zip))
    env.close()
    
    # Limpiar conexiones TraCI residuales antes del siguiente entrenamiento
    try:
        import traci
        traci.close()
    except Exception:
        pass
    time.sleep(3)  # Esperar que SO libere recursos de red
    
    elapsed = (time.time() - t_start) / 60
    print(f"  [OK] {name} seed={seed}: {elapsed:.1f} min")
    return model_zip


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 3: Evaluación zero-shot transfer
# ═══════════════════════════════════════════════════════════════════════════════

def evaluate_variant(name: str, city: str, chaos: str, model_path: Path) -> List[dict]:
    """
    Evalúa una variante en una ciudad/chaos específicos usando SUMO.
    Genera rutas y sumocfg dinámicamente como transfer_eval_n30_robust.py.
    """
    from src.core.tsc_env import TSCEnv
    from stable_baselines3 import PPO
    import tempfile
    import subprocess as sp
    
    print(f"  [EVAL] Evaluando {name} en {city}/{chaos}...")
    
    # Cargar modelo
    try:
        model = PPO.load(str(model_path), device="cpu")
    except Exception as e:
        print(f"    [ERR] Error cargando modelo: {e}")
        return []
    
    # Encontrar archivo de red
    net_dir = ROOT / "sumo_configs" / "networks"
    net_files = list(net_dir.glob(f"{city.lower()}*.net.xml"))
    if not net_files:
        print(f"    [ERR] No se encontró .net.xml para {city} en {net_dir}")
        return []
    
    net_path = net_files[0]
    
    # Generar rutas con randomTrips.py
    routes_dir = OUTPUT_DIR / "routes" / city.lower()
    routes_dir.mkdir(parents=True, exist_ok=True)
    route_path = routes_dir / f"{chaos}.rou.xml"
    
    sumo_home = os.environ.get("SUMO_HOME", r"C:\Program Files (x86)\Eclipse\Sumo")
    random_trips = os.path.join(sumo_home, "tools", "randomTrips.py")
    
    # v/c ratio -> period for randomTrips
    vc_map = {"low": "10.0", "mid": "5.0", "mid_high": "3.5", "high": "2.0", "extreme": "1.0"}
    period = vc_map.get(chaos, "2.0")
    
    if not route_path.exists():
        try:
            sp.run([
                sys.executable, random_trips,
                "-n", str(net_path.resolve()),
                "-o", str(route_path.resolve()),
                "-e", "3600",
                "-p", period,
                "--validate"
            ], check=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL, timeout=120)
        except Exception as e:
            print(f"    [WARN] randomTrips.py falló: {e}. Usando ruta mínima.")
            # Fallback: create minimal route file
            route_path.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<routes>
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5.0" minGap="2.0" maxSpeed="16.67"/>
    <flow id="f0" type="car" begin="0" end="3600" period="{period}" from="A0B0" to="B0C0"/>
    <flow id="f1" type="car" begin="0" end="3600" period="{period}" from="B0C0" to="C0D0"/>
</routes>""")
    
    # Descubrir el ID del semáforo principal para esta ciudad
    import xml.etree.ElementTree as ET
    tls_id = "B1"  # fallback
    try:
        tree = ET.parse(str(net_path))
        root = tree.getroot()
        # Buscar el primer tlLogic en el archivo adicional o en la red
        tls_counts = {}
        for conn in root.findall("connection"):
            tl = conn.get("tl")
            if tl:
                tls_counts[tl] = tls_counts.get(tl, 0) + 1
        if tls_counts:
            tls_id = max(tls_counts, key=tls_counts.get)
        else:
            # Buscar en la red directamente
            for tl_elem in root.findall("tlLogic"):
                tid = tl_elem.get("id")
                if tid:
                    tls_id = tid
                    break
        print(f"    TLS detectado: {tls_id} ({len(tls_counts)} conexiones)")
    except Exception:
        pass
    
    # Generar sumocfg temporal
    sumocfg_dir = OUTPUT_DIR / "sumocfg_eval"
    sumocfg_dir.mkdir(parents=True, exist_ok=True)
    sumocfg_path = sumocfg_dir / f"{city}_{chaos}_{name}.sumocfg"
    sumocfg_path.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="{net_path.resolve().as_posix()}"/>
        <route-files value="{route_path.resolve().as_posix()}"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="3600"/>
    </time>
    <processing>
        <time-to-teleport value="300"/>
        <waiting-time-memory value="10000"/>
    </processing>
    <report>
        <no-warnings value="true"/>
    </report>
</configuration>""")
    
    results = []
    
    for ep in range(N_EVAL_EPISODES):
        # Mapear de forma determinista para evitar conflictos y asegurar reproducibilidad
        city_idx = ["Quito", "Barcelona"].index(city)
        chaos_idx = ["low", "mid", "mid_high", "high", "extreme"].index(chaos)
        variant_idx = ["hsarg_gating_on", "hsarg_gating_off", "coopsarg_gating_on", "coopsarg_gating_off"].index(name)
        
        comb_id = variant_idx * 300 + city_idx * 150 + chaos_idx * 30 + ep
        ep_seed = 42000 + comb_id
        
        env = None
        try:
            env = TSCEnv(
                sumocfg_path=str(sumocfg_path),
                tls_id=tls_id,
                use_gui=False,
                max_steps=720,
                seed=ep_seed,
                enable_traci_chaos=(city == "Quito"),
                probabilidad_caos=0.4 if city == "Quito" else 0.0,
            )
            
            obs, _ = env.reset()
            done = False
            ep_delays = []
            ep_queues = []
            ep_ginis = []
            n_steps = 0
            
            while not done and n_steps < 720:
                action, _ = model.predict(obs, deterministic=True)
                step_result = env.step(action)
                if len(step_result) == 5:
                    obs, reward, terminated, truncated, info = step_result
                    done = terminated or truncated
                else:
                    obs, reward, done, info = step_result
                
                if 'delay' in info:
                    ep_delays.append(info['delay'])
                if 'total_queue' in info:
                    ep_queues.append(info['total_queue'])
                if 'gini' in info:
                    ep_ginis.append(info['gini'])
                
                n_steps += 1
            
            delay_mean = np.mean(ep_delays) if ep_delays else 0.0
            queue_mean = np.mean(ep_queues) if ep_queues else 0.0
            gini_mean = np.mean(ep_ginis) if ep_ginis else 0.0
            
            results.append({
                "variant": name,
                "city": city,
                "chaos_level": chaos,
                "episode": ep,
                "delay_mean": float(delay_mean),
                "queue_mean": float(queue_mean),
                "gini_mean": float(max(0, min(1, gini_mean))),
                "n_steps": n_steps,
            })
            
        except Exception as e:
            print(f"    [WARN] Ep {ep} error: {e}")
            continue
        finally:
            if env is not None:
                try:
                    env.close()
                except:
                    pass
                try:
                    env._safe_close_traci()
                except:
                    pass
            # Limpiar conexiones de TraCI residuales para evitar "Connection 'default' is already active"
            try:
                import traci
                if hasattr(traci, '_connections'):
                    traci._connections.clear()
            except:
                pass
    
    print(f"    [OK] {len(results)}/{N_EVAL_EPISODES} episodios completados")
    return results


def eval_task(args):
    name, city, chaos, model_path = args
    return evaluate_variant(name, city, chaos, model_path)


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 4: Análisis estadístico
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_results(df: pd.DataFrame) -> str:
    """Genera informe estadístico con datos REALES de SUMO."""
    from scipy import stats
    
    lines = []
    L = lines.append
    
    L("=" * 78)
    L("  ESTUDIO DE ABLACIÓN MAD-GATING — RESULTADOS REALES (SUMO)")
    L("=" * 78)
    L("")
    L(f"Total simulaciones SUMO: {len(df):,}")
    L(f"Variantes: {sorted(df['variant'].unique())}")
    L(f"Ciudades: {sorted(df['city'].unique())}")
    L("")
    
    # ── Gini comparison ──────────────────────────────────────────────────
    L("-" * 78)
    L("EFECTO DEL MAD-GATING EN EQUIDAD (Gini)")
    L("-" * 78)
    L(f"{'Variante':<22s} {'Ciudad':<10s} {'Chaos':<9s} {'Gini_ON':>8s} {'Gini_OFF':>8s} {'Δ':>8s} {'p':>8s} {'Sig':>5s}")
    L("-" * 82)
    
    for vp in ["hsarg", "coopsarg"]:
        on = f"{vp}_gating_on"
        off = f"{vp}_gating_off"
        for city in sorted(df['city'].unique()):
            for chaos in CHAOS_LEVELS:
                on_d = df[(df['variant']==on)&(df['city']==city)&(df['chaos_level']==chaos)]['gini_mean']
                off_d = df[(df['variant']==off)&(df['city']==city)&(df['chaos_level']==chaos)]['gini_mean']
                if len(on_d) < 5 or len(off_d) < 5:
                    continue
                try:
                    u, p = stats.mannwhitneyu(on_d, off_d, alternative='less')
                    sig = "***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "ns"
                except:
                    p, sig = 1.0, "err"
                L(f"{on:<22s} {city:<10s} {chaos:<9s} {on_d.mean():>8.4f} {off_d.mean():>8.4f} {off_d.mean()-on_d.mean():>+8.4f} {p:>8.4f} {sig:>5s}")
    
    L("")
    
    # ── Aggregate test ───────────────────────────────────────────────────
    L("-" * 78)
    L("TEST AGREGADO (Quito)")
    L("-" * 78)
    quito_on = df[(df['variant'].str.endswith('_on'))&(df['city']=='Quito')]['gini_mean']
    quito_off = df[(df['variant'].str.endswith('_off'))&(df['city']=='Quito')]['gini_mean']
    if len(quito_on) > 10 and len(quito_off) > 10:
        u, p = stats.mannwhitneyu(quito_on, quito_off, alternative='less')
        n1, n2 = len(quito_on), len(quito_off)
        r = 1 - (2*u)/(n1*n2)
        L(f"  Gini(gating=ON)  = {quito_on.mean():.4f} ± {quito_on.std():.4f}")
        L(f"  Gini(gating=OFF) = {quito_off.mean():.4f} ± {quito_off.std():.4f}")
        L(f"  Δ = {quito_off.mean()-quito_on.mean():+.4f}")
        L(f"  Mann-Whitney U = {u:.1f}, p = {p:.6f}, r = {r:.3f}")
        L(f"  {'[OK] H1 aceptada' if p < 0.05 else '[WARN] No significativo'}")
    
    L("")
    L("=" * 78)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="MAD-Gating Ablation con SUMO REAL")
    parser.add_argument("--train-only", action="store_true", help="Solo entrenar variantes")
    parser.add_argument("--eval-only", action="store_true", help="Solo evaluar (modelos ya entrenados)")
    parser.add_argument("--analyze-only", action="store_true", help="Solo analizar resultados existentes")
    parser.add_argument("--seed", type=int, default=42, help="Semilla base")
    parser.add_argument("--timesteps", type=int, default=TOTAL_TIMESTEPS)
    args = parser.parse_args()
    
    timesteps = args.timesteps
    do_train = not args.eval_only and not args.analyze_only
    do_eval = not args.train_only and not args.analyze_only
    
    print("=" * 78)
    print("  ABLACIÓN MAD-GATING — SUMO REAL")
    print("=" * 78)
    print(f"  Timesteps: {timesteps:,}")
    print(f"  Seeds: {SEEDS}")
    print(f"  Episodios eval: {N_EVAL_EPISODES}")
    print(f"  Ciudades eval: {CITIES_EVAL}")
    print()
    
    # ── Build variants ───────────────────────────────────────────────────
    print("[1] Construyendo variantes de ablación...")
    try:
        variants = build_ablation_extractors()
        for name, cfg in variants.items():
            print(f"    {name:<25s} -> {cfg['label']}")
        print(f"    [OK] {len(variants)} variantes listas")
    except ImportError as e:
        print(f"    [ERR] Error: {e}")
        print("    Asegúrate de estar en el entorno (tsc-env) con:")
        print("    conda activate tsc-env")
        sys.exit(1)
    print()
    
    # ── Train ────────────────────────────────────────────────────────────
    if do_train:
        print(f"[2] Entrenando {len(variants)} variantes × {len(SEEDS)} seeds...")
        print(f"    [TIME]  Estimado: {len(variants)*len(SEEDS)*timesteps/500000*2:.0f}-{len(variants)*len(SEEDS)*timesteps/500000*4:.0f}h con GPU")
        
        for name, cfg in variants.items():
            for seed in SEEDS:
                train_one_variant(name, cfg["cls"], seed, timesteps)
        print()
    
    # ── Evaluate ─────────────────────────────────────────────────────────
    if do_eval:
        print(f"[3] Evaluando zero-shot transfer en paralelo...")
        all_results = []
        
        tasks = []
        for name, cfg in variants.items():
            for seed in SEEDS:
                model_path = MODELS_DIR / f"{name}_seed{seed}.zip"
                if not model_path.exists():
                    print(f"    [WARN]  Modelo {name}_seed{seed} no encontrado. Saltando.")
                    continue
                
                for city in CITIES_EVAL:
                    for chaos in CHAOS_LEVELS:
                        tasks.append((name, city, chaos, model_path))
                        
        if tasks:
            from concurrent.futures import ProcessPoolExecutor, as_completed
            import os
            
            # Limitar a máximo 3 workers para evitar sobrecarga del sistema de red (sockets) y de CPU en Windows
            max_workers = min(3, max(1, os.cpu_count() - 1))
            print(f"    [PARALLEL] Iniciando ProcessPoolExecutor con {max_workers} workers para {len(tasks)} combinaciones...")
            
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(eval_task, t): t for t in tasks}
                
                completed = 0
                for future in as_completed(futures):
                    name, city, chaos, _ = futures[future]
                    try:
                        results = future.result()
                        all_results.extend(results)
                        completed += 1
                        print(f"    [PROGRESS] {completed}/{len(tasks)} combinaciones completadas ({name} en {city}/{chaos})")
                    except Exception as e:
                        print(f"    [ERR] Error evaluando {name} en {city}/{chaos}: {e}")
        
        if all_results:
            df = pd.DataFrame(all_results)
            csv_path = RESULTS_DIR / "ablation_real_results.csv"
            df.to_csv(csv_path, index=False)
            print(f"\n    [OK] {len(df):,} simulaciones -> {csv_path}")
            
            # ── Analyze ──────────────────────────────────────────────────
            print(f"\n[4] Análisis estadístico...")
            report = analyze_results(df)
            report_path = RESULTS_DIR / "ablation_real_report.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(report)
            print(f"\n    [OK] Informe -> {report_path}")
        else:
            print("    [ERR] No se generaron resultados. Verifica que los modelos existen.")
            sys.exit(1)
            
    if args.analyze_only:
        csv_path = RESULTS_DIR / "ablation_real_results.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            print(f"\n[4] Análisis estadístico (cargado de {csv_path})...")
            report = analyze_results(df)
            report_path = RESULTS_DIR / "ablation_real_report.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(report)
            print(f"\n    [OK] Informe -> {report_path}")
        else:
            print(f"    [ERR] No se encontró {csv_path} para analizar.")
            sys.exit(1)
    
    print("\n" + "=" * 78)
    print("  ABLACIÓN COMPLETADA")
    print("=" * 78)


if __name__ == "__main__":
    main()
