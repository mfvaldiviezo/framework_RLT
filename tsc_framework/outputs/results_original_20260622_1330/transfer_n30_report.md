# INFORME DE TRANSFERENCIA ZERO-SHOT — N=30 EPISODIOS
**Fecha:** 2026-06-03
**Experimento:** Evaluacion de transferencia con n=30 episodios por ciudad/modelo.
**Estadistico central:** Mediana (robusta ante gridlocks). Dispersión: IQR.
**Test estadistico:** Mann-Whitney U bilateral (alpha=0.05).

---

## Tabla 1 — Metricas por Ciudad y Modelo (Mediana ± IQR)

| Ciudad | Modelo | Delay Mediana (s) | IQR (s) | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|
| Barcelona | ppo_ideal | 4.3 | 1.7 | 0.0428 | 0.0047 | 4.3 | 0.0% |
| Barcelona | ppo_chaos | 0.3 | 0.7 | 0.0127 | 0.0040 | 0.3 | 0.0% |
| Quito | ppo_ideal | 11.4 | 1.9 | 0.2054 | 0.0216 | 90.3 | 0.0% |
| Quito | ppo_chaos | 30.9 | 4.8 | 0.2048 | 0.0275 | 234.2 | 0.0% |
| Bogota | ppo_ideal | 22.1 | 2.7 | 0.5873 | 0.0213 | 113.2 | 0.0% |
| Bogota | ppo_chaos | 22.5 | 5.0 | 0.5765 | 0.0250 | 117.3 | 0.0% |
| Berlin | ppo_ideal | 16.6 | 1.5 | 0.6839 | 0.0146 | 60.9 | 0.0% |
| Berlin | ppo_chaos | 5.8 | 1.8 | 0.4675 | 0.0363 | 33.8 | 0.0% |
| Madrid | ppo_ideal | 9.5 | 1.3 | 0.1752 | 0.0127 | 65.3 | 0.0% |
| Madrid | ppo_chaos | 4972.2 | 870.8 | 0.1279 | 0.0329 | 13761.2 | 100.0% |
| CDMX | ppo_ideal | 0.3 | 0.1 | 0.0675 | 0.0121 | 0.3 | 0.0% |
| CDMX | ppo_chaos | 0.3 | 0.1 | 0.0633 | 0.0127 | 0.3 | 0.0% |

## Tabla 2 — Test Mann-Whitney U: Caotico vs. Ideal por Ciudad

| Ciudad | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|
| Barcelona | Delay | 148.0 | 0.0000 | *** | 0.671 | large |
| Barcelona | Gini | 139.0 | 0.0000 | *** | 0.691 | large |
| Barcelona | CVaR90 | 148.0 | 0.0000 | *** | 0.671 | large |
| Quito | Delay | 899.0 | 0.0000 | *** | -0.998 | large |
| Quito | Gini | 508.0 | 0.3953 | ns | -0.129 | small |
| Quito | CVaR90 | 900.0 | 0.0000 | *** | -1.000 | large |
| Bogota | Delay | 532.0 | 0.2282 | ns | -0.182 | small |
| Bogota | Gini | 358.0 | 0.1761 | ns | 0.204 | small |
| Bogota | CVaR90 | 547.0 | 0.1537 | ns | -0.216 | small |
| Berlin | Delay | 0.0 | 0.0000 | *** | 1.000 | large |
| Berlin | Gini | 0.0 | 0.0000 | *** | 1.000 | large |
| Berlin | CVaR90 | 0.0 | 0.0000 | *** | 1.000 | large |
| Madrid | Delay | 900.0 | 0.0000 | *** | -1.000 | large |
| Madrid | Gini | 21.0 | 0.0000 | *** | 0.953 | large |
| Madrid | CVaR90 | 900.0 | 0.0000 | *** | -1.000 | large |
| CDMX | Delay | 234.0 | 0.0014 | ** | 0.480 | medium |
| CDMX | Gini | 383.0 | 0.3255 | ns | 0.149 | small |
| CDMX | CVaR90 | 234.0 | 0.0014 | ** | 0.480 | medium |

---

## Interpretacion de Resultados

> **Nota metodologica:** Las mejoras observadas en Quito (Caotico vs. Ideal) son estadisticamente significativas cuando p < 0.05. Con n=30 episodios, el poder estadistico del test Mann-Whitney es >= 80% para efectos medianos (|r| >= 0.3).

El experimento de transferencia zero-shot evalua si la politica entrenada bajo perturbaciones LATAM en Hangzhou preserva sus propiedades de optimizacion multiobjetivo cuando se aplica a redes urbanas distintas mediante el mecanismo de acotamiento topologico (wrapper). La validacion estadistica con n=30 episodios permite distinguir mejoras reales de variabilidad episodica.

---
*Generado por transfer_eval_n30.py — TSC Framework Doctoral*
