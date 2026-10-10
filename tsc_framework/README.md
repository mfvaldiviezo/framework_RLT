# TSC-Resilience: Probabilistic-Experimental Framework for Assessing Resilience of RL-based Traffic Signal Controllers under Non-Nominal Driving Behavior

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![SUMO](https://img.shields.io/badge/SUMO-1.20%2B-green.svg)](https://eclipse.dev/sumo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Verified-success.svg)]()

Official implementation and experimental reproduction package for the research paper:
> **"A Probabilistic-Experimental Framework for Assessing Resilience of RL-based Traffic Signal Controllers under Non-Nominal Driving Behavior"**  
> *Marcelo Valdiviezo-Condolo, Miguel Ángel Salido Gregorio, and Christian Pérez.*  
> Universitat Politècnica de València (UPV) & Universidad Nacional de Loja (UNL).

---

## 1. Overview

Conventional Reinforcement Learning Traffic Signal Controllers (RL-TSC) are predominantly trained and benchmarked under synthetic, nominal car-following regimes (such as standard Krauss models with strict lane discipline). However, urban traffic in developing regions and dense metropolitan areas frequently exhibits non-nominal, behavioral turbulence—including informal vehicle stopping, illegal turns, tailgating, and spatial lane-sharing.

This framework introduces a modular probabilistic-experimental pipeline to evaluate controller resilience, spatial equity, and tail-risk vulnerability under empirically grounded behavioral stress.

```
+-------------------------------------------------------------------------+
|                         TSC FRAMEWORK ARCHITECTURE                      |
+-------------------------------------------------------------------------+
|  [Data Pipeline]       Empirical CAN-bus/OBD-II Telemetry (POLIDriving) |
|         |                                                               |
|  [Probabilistic Core]  Regular Vine Copulas (C-Vine & D-Vine Trees)     |
|         |              Kendall's Tau & Tail Dependence Parameters       |
|         v                                                               |
|  [Scenario Generation] Extreme Marginal Stress Scenarios (.rou.xml)    |
|         |                                                               |
|  [Simulation Core]     SUMO + TraCI Local Traffic Light Controller      |
|         |              Dynamic Behavioral Perturbations                 |
|         v                                                               |
|  [MARL Agents]         PPO / H-SARG / Coop-SARG                         |
|                        Risk Gating (CVaR) + Spatial Equity (Gini)       |
|         v                                                               |
|  [Evaluation]          Zero-Shot Cross-City Transfer (6 Urban Networks) |
|                        Non-Parametric Inference (Mann-Whitney / KW)     |
+-------------------------------------------------------------------------+
```

---

## 2. Directory Structure

```
tsc_framework/
├── config/
│   └── default_config.yaml    # Simulation hyperparameters, seeds, and paths
├── data/
│   ├── raw/                   # Raw telemetric driving data and OSM sources
│   ├── processed/             # Marginal distributions and scenario parameters
│   └── quito_behavior/        # Empirical behavioral telemetry dataset
├── sumo_configs/
│   ├── networks/              # Validated SUMO networks (Berlin, Bogota, CDMX, Madrid, Hangzhou)
│   └── routes.rou.xml         # Base vehicular demand routes
├── src/
│   ├── core/                  # Gymnasium TraCI environment (tsc_env.py, latam_chaos_manager.py)
│   ├── data_pipeline/         # OBD-II ingestion and distribution fitting (process_data.py)
│   ├── probabilistic/         # Regular Vine Copula generator (vine_generator.py)
│   ├── rl_agent/              # SARG / Coop-SARG neural policies (sarg_policy.py)
│   └── sumo_configs/          # Network parsing and route generation utilities
├── scripts/
│   ├── train.py               # Policy training pipeline (PPO with CVaR and Gini)
│   ├── evaluate.py            # Single-intersection evaluation and stress testing
│   ├── transfer_eval_n30.py   # Multi-agent zero-shot cross-city transfer (N=30)
│   ├── run_ablation.py        # Causal ablation study on MAD-Gating and Equity Boost
│   ├── statistical_analysis.py# Non-parametric hypothesis testing (Mann-Whitney U, KW)
│   └── generate_plots.py      # Publication-grade figure generation
├── outputs/
│   ├── models/                # Pretrained model checkpoints (ppo_coop_chaos, ppo_coop_ideal)
│   ├── figures/               # Generated bifurcation plots, heatmaps, and tradeoffs
│   └── results/               # Detailed CSV episode logs and summary reports
├── environment.yml            # Conda environment specification
└── setup.py                   # Local package installer
```

---

## 3. Installation & Requirements

### System Prerequisites
- **Operating System:** Linux, macOS, or Windows
- **Eclipse SUMO:** Version >= 1.20.0 ([Installation Instructions](https://eclipse.dev/sumo/))
- **Python:** Version >= 3.10

### Setup Environment

1. Clone the repository and navigate to the framework directory:
```bash
git clone https://github.com/mfvaldiviezo/tesis-doctoral-final-v2.git
cd tesis-doctoral-final-v2/tsc_framework
```

2. Create and activate the reproducible Conda environment:
```bash
conda env create -f environment.yml
conda activate tsc-env
```

3. Install the package in editable mode:
```bash
pip install -e .
```

4. Configure the `SUMO_HOME` environment variable:
- **Linux/macOS:**
  ```bash
  export SUMO_HOME="/usr/share/sumo"  # Or your SUMO installation path
  ```
- **Windows (PowerShell):**
  ```powershell
  $env:SUMO_HOME = "C:\Program Files\Eclipse\Sumo"
  ```

---

## 4. Reproducing Paper Experiments

### Experiment 1: Vine Copula Fitting & Stress Scenario Generation
Fits regular C-Vine and D-Vine copulas to empirical OBD-II telemetry from POLIDriving and synthesizes joint tail-dependence stress scenarios:
```bash
python src/probabilistic/vine_generator.py --mode production --samples 1000
```

### Experiment 2: Training RL-TSC Agents (H-SARG and Coop-SARG)
Trains PPO agents equipped with Multi-Head Self-Attention (MHSA), Conditional Value-at-Risk (CVaR-95), and spatial Gini regularization:
```bash
python scripts/train.py --config config/default_config.yaml --timesteps 1000000
```

### Experiment 3: Zero-Shot Cross-City Transfer Evaluation (N=30 Episodes)
Evaluates pre-trained policies across 6 metropolitan networks (Barcelona, Quito, Madrid, Berlin, Bogota, CDMX) without fine-tuning:
```bash
python scripts/transfer_eval_n30.py --episodes 30 --render false
```

### Experiment 4: SOTA Baseline Benchmarking (Hangzhou 4x4)
Compares Coop-SARG against SOTA multi-agent and classic baselines (CoLight, IPPO, MaxPressure, Fixed-Time):
```bash
python compare_resco_results.py
```

### Experiment 5: Causal Ablation Study (MAD-Gating & Equity Boost)
Quantifies the isolated impact of the Mean Absolute Deviation gating mechanism and Equity Boost:
```bash
python scripts/run_ablation.py --model ppo_coop_chaos --episodes 30
```

### Experiment 6: Statistical Analysis & Paper Figures
Computes Mann-Whitney U tests, Kruskal-Wallis tests, Rank-Biserial effect sizes ($r$), and outputs publication-grade figures:
```bash
python scripts/statistical_analysis.py
python scripts/generate_plots.py
```
Output figures will be saved to `outputs/figures/`.

---

## 5. Verification & Model Checkpoints

Pretrained model weights reported in the paper are preserved in `outputs/models/`:
- `ppo_coop_chaos.zip`: Policy trained under behavioral stress scenarios.
- `ppo_coop_ideal.zip`: Policy trained under nominal car-following conditions.
- `best_model/best_model_chaos.zip`: Best checkpoint based on validation reward.

To verify the integrity and observation space alignment of all checkpointed models:
```bash
python verify_models.py
```

---

## 6. Citation

If you use this framework or experimental protocol in your research, please cite our paper:

```bibtex
@article{valdiviezo2026resilience,
  author={Valdiviezo-Condolo, Marcelo and Salido Gregorio, Miguel {\'A}ngel and P{\'e}rez, Christian},
  journal={IEEE Transactions on Intelligent Transportation Systems},
  title={A Probabilistic-Experimental Framework for Assessing Resilience of RL-based Traffic Signal Controllers under Non-Nominal Driving Behavior},
  year={2026},
  doi={10.1109/TITS.2026.XXXXXXX}
}
```

---

## 7. License

This project is licensed under the MIT License - see the `LICENSE` file for details.
