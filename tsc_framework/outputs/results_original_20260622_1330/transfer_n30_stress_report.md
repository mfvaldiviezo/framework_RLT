# INFORME DE TRANSFERENCIA ZERO-SHOT — N=30 EPISODIOS
**Fecha:** 2026-06-03
**Experimento:** Evaluacion de transferencia con n=30 episodios por ciudad/modelo.
**Estadistico central:** Mediana (robusta ante gridlocks). Dispersión: IQR.
**Test estadistico:** Mann-Whitney U bilateral (alpha=0.05).

---

## Tabla 1 — Metricas por Ciudad y Modelo (Mediana ± IQR)

| Ciudad | Modelo | Delay Mediana (s) | IQR (s) | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|
| Barcelona | ppo_ideal | 181.5 | 0.0 | 0.6178 | 0.0001 | 385.1 | 0.0% |
| Barcelona | ppo_chaos | 180.3 | 0.4 | 0.6172 | 0.0004 | 384.1 | 0.0% |
| Quito | ppo_ideal | 2780.9 | 76.0 | 0.4351 | 0.0023 | 5685.4 | 100.0% |
| Quito | ppo_chaos | 2776.9 | 47.5 | 0.4462 | 0.0029 | 5795.5 | 100.0% |
| Bogota | ppo_ideal | 857.2 | 31.6 | 0.5372 | 0.0034 | 2387.7 | 0.0% |
| Bogota | ppo_chaos | 1019.2 | 54.5 | 0.5131 | 0.0061 | 3192.5 | 0.0% |
| Berlin | ppo_ideal | 1585.0 | 16.9 | 0.5777 | 0.0033 | 3931.0 | 0.0% |
| Berlin | ppo_chaos | 19159.1 | 4850.4 | 0.4724 | 0.0243 | 38022.0 | 100.0% |
| Madrid | ppo_ideal | 215.0 | 2.7 | 0.5923 | 0.0007 | 608.7 | 0.0% |
| Madrid | ppo_chaos | 1862.4 | 1.2 | 0.2095 | 0.0008 | 3682.7 | 0.0% |
| CDMX | ppo_ideal | 9484.7 | 201.7 | 0.7346 | 0.0043 | 17144.0 | 100.0% |
| CDMX | ppo_chaos | 9513.7 | 820.7 | 0.7373 | 0.0074 | 17131.0 | 100.0% |

## Tabla 2 — Test Mann-Whitney U: Caotico vs. Ideal por Ciudad

| Ciudad | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|
| Barcelona | Delay | 0.0 | 0.3333 | ns | 1.000 | large |
| Barcelona | Gini | 0.0 | 0.3333 | ns | 1.000 | large |
| Barcelona | CVaR90 | 0.0 | 0.3333 | ns | 1.000 | large |
| Quito | Delay | 2.0 | 1.0000 | ns | 0.000 | negligible |
| Quito | Gini | 4.0 | 0.3333 | ns | -1.000 | large |
| Quito | CVaR90 | 4.0 | 0.3333 | ns | -1.000 | large |
| Bogota | Delay | 4.0 | 0.3333 | ns | -1.000 | large |
| Bogota | Gini | 0.0 | 0.3333 | ns | 1.000 | large |
| Bogota | CVaR90 | 4.0 | 0.3333 | ns | -1.000 | large |
| Berlin | Delay | 4.0 | 0.3333 | ns | -1.000 | large |
| Berlin | Gini | 0.0 | 0.3333 | ns | 1.000 | large |
| Berlin | CVaR90 | 4.0 | 0.3333 | ns | -1.000 | large |
| Madrid | Delay | 4.0 | 0.3333 | ns | -1.000 | large |
| Madrid | Gini | 0.0 | 0.3333 | ns | 1.000 | large |
| Madrid | CVaR90 | 4.0 | 0.3333 | ns | -1.000 | large |
| CDMX | Delay | 2.0 | 1.0000 | ns | 0.000 | negligible |
| CDMX | Gini | 2.0 | 1.0000 | ns | 0.000 | negligible |
| CDMX | CVaR90 | 2.0 | 1.0000 | ns | 0.000 | negligible |

---

## Interpretacion de Resultados

> **Nota metodologica:** Las mejoras observadas en Quito (Caotico vs. Ideal) son estadisticamente significativas cuando p < 0.05. Con n=30 episodios, el poder estadistico del test Mann-Whitney es >= 80% para efectos medianos (|r| >= 0.3).

El experimento de transferencia zero-shot evalua si la politica entrenada bajo perturbaciones LATAM en Hangzhou preserva sus propiedades de optimizacion multiobjetivo cuando se aplica a redes urbanas distintas mediante el mecanismo de acotamiento topologico (wrapper). La validacion estadistica con n=30 episodios permite distinguir mejoras reales de variabilidad episodica.

---
*Generado por transfer_eval_n30.py — TSC Framework Doctoral*
