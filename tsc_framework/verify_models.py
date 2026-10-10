"""
verify_models.py
================
Verificación forense de los modelos PPO entrenados.

Responde las preguntas críticas del tribunal doctoral:
  1. ¿Qué observation_space tiene cada modelo? (shape = 34 → compatible con H-SARG)
  2. ¿Qué features_extractor usa? (HSARGExtractor / CoopSARGExtractor / MlpExtractor)
  3. ¿Qué policy_kwargs se usaron? (arquitectura del actor-crítico)
  4. ¿Cuántos parámetros tiene cada red?

Genera una tabla de auditoría imprimible y un JSON para el Apéndice de la tesis.

Uso:
    python verify_models.py

Requiere:
    stable-baselines3, torch  (pip install stable-baselines3 torch)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ── Rutas ───────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).resolve().parent
MODELS_DIR  = ROOT / "outputs" / "models"
OUTPUT_JSON = ROOT / "outputs" / "model_audit.json"

# ── Importaciones con manejo de errores ─────────────────────────────────────
try:
    from stable_baselines3 import PPO
except ImportError:
    print("[ERROR] stable-baselines3 no encontrado.")
    print("        Activa el entorno: venv_pytsc\\Scripts\\activate")
    sys.exit(1)

try:
    import torch
    TORCH_OK = True
except ImportError:
    TORCH_OK = False


# ── Helpers ──────────────────────────────────────────────────────────────────

def count_parameters(model_sb3) -> int:
    """Cuenta el total de parámetros entrenables de la red."""
    try:
        return sum(p.numel() for p in model_sb3.policy.parameters() if p.requires_grad)
    except Exception:
        return -1


def get_net_arch(model_sb3) -> str:
    """Devuelve la arquitectura pi/vf como string legible."""
    try:
        pk = model_sb3.policy.net_arch
        return str(pk)
    except Exception:
        try:
            # SB3 ≥ 1.7 guarda la arch en policy.mlp_extractor
            pi = [l.out_features for l in model_sb3.policy.mlp_extractor.policy_net]
            vf = [l.out_features for l in model_sb3.policy.mlp_extractor.value_net]
            return f"pi={pi}, vf={vf}"
        except Exception:
            return "N/A"


def get_extractor_info(model_sb3) -> dict:
    """Extrae nombre de clase, features_dim y parámetros del extractor."""
    fe = model_sb3.policy.features_extractor
    cls_name = type(fe).__name__

    # features_dim es el tamaño del vector de salida del extractor
    features_dim = getattr(fe, "features_dim", "N/A")

    # Para H-SARG / Coop-SARG: último tamaño de capa de fusión
    if hasattr(fe, "fusion"):
        try:
            # El último Linear de la capa de fusión determina features_dim
            for layer in reversed(list(fe.fusion)):
                if hasattr(layer, "out_features"):
                    features_dim = layer.out_features
                    break
        except Exception:
            pass

    # Parámetros del extractor
    try:
        extractor_params = sum(p.numel() for p in fe.parameters() if p.requires_grad)
    except Exception:
        extractor_params = -1

    return {
        "class":          cls_name,
        "features_dim":   features_dim,
        "params":         extractor_params,
    }


def diagnose_compatibility(obs_shape: tuple, extractor_cls: str) -> str:
    """
    Determina la coherencia entre el observation_space del modelo
    y lo que espera HSARGExtractor / LocalTLSManager.get_state().
    """
    expected_shape = (34,)
    compatible_extractors = {"HSARGExtractor", "CoopSARGExtractor"}

    if obs_shape == expected_shape and extractor_cls in compatible_extractors:
        return " COHERENTE — obs=(34,) + extractor correcto"
    elif obs_shape == expected_shape and extractor_cls not in compatible_extractors:
        return (
            f"️  ATENCIÓN — obs=(34,) pero extractor={extractor_cls}. "
            "El modelo usa MlpPolicy estándar sobre un vector de 34D. "
            "Compatible con LocalTLSManager.get_state() pero sin MHSA ni gating."
        )
    elif obs_shape != expected_shape and extractor_cls in compatible_extractors:
        return (
            f" INCOHERENTE — obs={obs_shape} pero extractor={extractor_cls}. "
            f"HSARGExtractor espera obs=(34,). El modelo fue entrenado con "
            f"un entorno diferente (¿SumoRLEnv con n_lanes≠10?)."
        )
    else:
        return (
            f"️  MIXTO — obs={obs_shape}, extractor={extractor_cls}. "
            "Verificar manualmente cuál entorno generó este modelo."
        )


# ── Pipeline principal ────────────────────────────────────────────────────────

def audit_models() -> list[dict]:
    """Carga cada modelo .zip y extrae su información forense."""

    zip_files = sorted(MODELS_DIR.glob("*.zip"))
    if not zip_files:
        print(f"[ERROR] No se encontraron archivos .zip en {MODELS_DIR}")
        sys.exit(1)

    results = []

    print("\n" + "═" * 80)
    print("  AUDITORÍA FORENSE DE MODELOS PPO — Tesis Doctoral")
    print("═" * 80)

    for zip_path in zip_files:
        print(f"\n{'─' * 60}")
        print(f"  Modelo: {zip_path.name}")
        print(f"{'─' * 60}")

        try:
            model = PPO.load(str(zip_path), device="cpu")
        except Exception as exc:
            print(f"  [ERROR] No se pudo cargar: {exc}")
            results.append({"model": zip_path.name, "error": str(exc)})
            continue

        # ── Observation / Action space ────────────────────────────────────
        obs_space   = model.observation_space
        act_space   = model.action_space
        obs_shape   = tuple(obs_space.shape)
        obs_low     = float(obs_space.low.min())
        obs_high    = float(obs_space.high.max())

        print(f"  observation_space : Box{obs_shape}  low={obs_low:.1f}  high={obs_high:.1f}")
        print(f"  action_space      : Discrete({act_space.n})")

        # ── Features extractor ───────────────────────────────────────────
        ext_info = get_extractor_info(model)
        print(f"  features_extractor: {ext_info['class']}")
        print(f"    └─ features_dim : {ext_info['features_dim']}")
        print(f"    └─ params       : {ext_info['params']:,}" if isinstance(ext_info['params'], int) and ext_info['params'] >= 0 else f"    └─ params: N/A")

        # ── Arquitectura actor-crítico ────────────────────────────────────
        net_arch = get_net_arch(model)
        print(f"  net_arch          : {net_arch}")

        # ── Hiperparámetros de entrenamiento ─────────────────────────────
        lr = model.learning_rate
        gamma = model.gamma
        n_steps = model.n_steps
        batch_size = model.batch_size
        print(f"  lr={lr}  γ={gamma}  n_steps={n_steps}  batch={batch_size}")

        # ── Total de parámetros ───────────────────────────────────────────
        total_params = count_parameters(model)
        print(f"  Total parámetros  : {total_params:,}" if total_params >= 0 else "  Total parámetros: N/A")

        # ── Diagnóstico de coherencia ─────────────────────────────────────
        diagnosis = diagnose_compatibility(obs_shape, ext_info["class"])
        print(f"\n  DIAGNÓSTICO: {diagnosis}")

        # ── Atención H-SARG (si aplica) ───────────────────────────────────
        fe = model.policy.features_extractor
        if hasattr(fe, "last_attention_weights"):
            print("  XAI              :  last_attention_weights disponible (MHSA)")
        if hasattr(fe, "risk_gate"):
            print("  Gating           :  Sigmoid Risk Gate presente")
        if hasattr(fe, "equity_boost"):
            print("  Equity Boost     :  Gini-equity modulation presente (Coop)")

        # ── Guardar resultado ────────────────────────────────────────────
        record = {
            "model":             zip_path.stem,
            "file_size_mb":      round(zip_path.stat().st_size / 1_048_576, 2),
            "obs_shape":         list(obs_shape),
            "obs_low":           obs_low,
            "obs_high":          obs_high,
            "n_actions":         int(act_space.n),
            "features_extractor": ext_info["class"],
            "features_dim":      ext_info["features_dim"],
            "extractor_params":  ext_info["params"],
            "net_arch":          net_arch,
            "total_params":      total_params,
            "learning_rate":     str(lr),
            "gamma":             gamma,
            "n_steps":           n_steps,
            "batch_size":        batch_size,
            "diagnosis":         diagnosis,
        }
        results.append(record)

    return results


def print_summary_table(results: list[dict]) -> None:
    """Imprime una tabla resumen compacta al final."""
    print("\n\n" + "═" * 80)
    print("  TABLA RESUMEN — Para incluir en el Apéndice de la Tesis")
    print("═" * 80)
    header = f"{'Modelo':<22} {'obs_shape':<12} {'Extractor':<24} {'Params':>10} {'Diagnóstico'}"
    print(header)
    print("─" * 80)

    for r in results:
        if "error" in r:
            print(f"  {r['model']:<20} ERROR: {r['error']}")
            continue
        obs = str(r["obs_shape"])
        ext = r["features_extractor"]
        params = f"{r['total_params']:,}" if isinstance(r["total_params"], int) and r["total_params"] >= 0 else "N/A"
        # Extraer solo el emoji del diagnóstico
        diag_short = r["diagnosis"].split("—")[0].strip()
        print(f"  {r['model']:<20} {obs:<12} {ext:<24} {params:>10}  {diag_short}")


def save_json(results: list[dict]) -> None:
    """Guarda los resultados completos como JSON para el Apéndice."""
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    print(f"\n  JSON guardado en: {OUTPUT_JSON}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"  Python  : {sys.version.split()[0]}")
    if TORCH_OK:
        print(f"  PyTorch : {torch.__version__}")
    try:
        import stable_baselines3 as sb3
        print(f"  SB3     : {sb3.__version__}")
    except Exception:
        pass
    print(f"  Modelos : {MODELS_DIR}")

    results = audit_models()
    print_summary_table(results)
    save_json(results)

    print("\n" + "═" * 80)
    # Diagnóstico rápido de coherencia global
    coherent   = sum(1 for r in results if "" in r.get("diagnosis", ""))
    warning    = sum(1 for r in results if "️"  in r.get("diagnosis", ""))
    critical   = sum(1 for r in results if "" in r.get("diagnosis", ""))
    print(f"  RESULTADO GLOBAL: {coherent}  coherentes | {warning} ️ atención | {critical}  críticos")
    if critical > 0:
        print("   Hay modelos con incoherencia crítica. Revisar antes de la defensa.")
    elif warning > 0:
        print("  ️  Hay modelos que requieren verificación adicional.")
    else:
        print("   Todos los modelos son coherentes con el entorno de evaluación.")
    print("═" * 80 + "\n")
