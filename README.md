# TSC-Resilience: Probabilistic-Experimental Framework for Assessing Resilience of RL-based Traffic Signal Controllers under Non-Nominal Driving Behavior

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![SUMO](https://img.shields.io/badge/SUMO-1.20%2B-green.svg)](https://eclipse.dev/sumo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Verified-success.svg)]()

Official implementation and reproducibility repository for the research paper:
> **"A Probabilistic-Experimental Framework for Assessing Resilience of RL-based Traffic Signal Controllers under Non-Nominal Driving Behavior"**  
> *Marcelo Valdiviezo-Condolo, Miguel Ángel Salido Gregorio, and Christian Pérez.*  
> Universitat Politècnica de València (UPV) & Universidad Nacional de Loja (UNL).

---

## 1. Overview

Reinforcement Learning Traffic Signal Control (RL-TSC) benchmarks conventionally assume nominal, orderly driving behaviors. In real-world urban networks, non-nominal driving conditions (informal passenger stops, lane-splitting, sudden deceleration, and non-compliance) significantly degrade network throughput and induce spatial inequality.

This repository provides the complete experimental artifact, including:
- **Empirical Telemetry Ingestion & Copula Calibration:** Regular Vine Copulas (C-Vine and D-Vine) fitted to POLIDriving CAN-bus/OBD-II data.
- **Gymnasium-TraCI Simulation Environments:** Local and multi-agent network control integrated with SUMO.
- **Risk-Sensitive MARL Policies:** PPO, H-SARG, and Coop-SARG with CVaR-95 loss and spatial Gini penalty.
- **MAD-Gating Mechanism:** Attention gating that preserves spatial equity across asymmetric traffic flows.
- **Zero-Shot Cross-City Benchmarking:** Multi-network transfer across Barcelona, Quito, Madrid, Berlin, Bogota, and CDMX.
- **Baseline Benchmarks:** SOTA comparison against CoLight, IPPO, MaxPressure, and Fixed-Time on the Hangzhou 4x4 network.

---

## 2. Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/mfvaldiviezo/framework_RLT.git
cd framework_RLT/tsc_framework

# Create the Conda environment
conda env create -f environment.yml
conda activate tsc-env

# Install the framework
pip install -e .
```

### Configure SUMO Environment

- **Linux / macOS:**
  ```bash
  export SUMO_HOME="/usr/share/sumo"
  ```
- **Windows (PowerShell):**
  ```powershell
  $env:SUMO_HOME = "C:\Program Files\Eclipse\Sumo"
  ```

---

## 3. Paper Reproduction Commands

All reproduction commands should be executed from the `tsc_framework` directory:

```bash
cd tsc_framework

# 1. Fit Vine Copulas and synthesize stress scenarios
python src/probabilistic/vine_generator.py --mode production --samples 1000

# 2. Train Coop-SARG and H-SARG policies
python scripts/train.py --config config/default_config.yaml --timesteps 1000000

# 3. Run zero-shot transfer evaluation across 6 cities (N=30 episodes)
python scripts/transfer_eval_n30.py --episodes 30

# 4. Compare against SOTA baselines on Hangzhou 4x4
python compare_resco_results.py

# 5. Run causal ablation study on MAD-Gating and Equity Boost
python scripts/run_ablation.py --model ppo_coop_chaos --episodes 30

# 6. Execute statistical tests and regenerate paper figures
python scripts/statistical_analysis.py
python scripts/generate_plots.py
```

Generated publication plots are saved in `tsc_framework/outputs/figures/`.

---

## 4. Repository Structure

```
.
├── tsc_framework/              # Standalone Python framework package
│   ├── config/                 # YAML configuration files
│   ├── data/                   # Empirical and processed scenario datasets
│   ├── sumo_configs/           # Road networks (.net.xml) and route definitions
│   ├── src/                    # Core source code (probabilistic, RL, environment)
│   ├── scripts/                # Training, evaluation, and analysis scripts
│   ├── outputs/                # Pre-trained models, figures, and CSV logs
│   ├── environment.yml         # Conda environment definition
│   ├── setup.py                # Package installation script
│   └── README.md               # Detailed framework documentation
├── baselines/                  # Cloned external baselines (RESCO, CoordLight, pytsc)
├── benchmark_reports/          # Clean benchmark data tables and XAI reports
├── .gitignore                  # Git tracking exclusion rules
└── README.md                   # Repository overview
```

---

## 5. Pretrained Checkpoints

Verified checkpoints are located in `tsc_framework/outputs/models/`:
- `ppo_coop_chaos.zip`: Coop-SARG policy trained under behavioral stress.
- `ppo_coop_ideal.zip`: Policy trained under nominal conditions.

To verify model observation space and policy head consistency:
```bash
python tsc_framework/verify_models.py
```

---

## 6. Citation

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

Distributed under the MIT License.
