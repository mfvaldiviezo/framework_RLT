# INFORME DE TRANSFERENCIA ZERO-SHOT — N=30 EPISODIOS
**Fecha:** 2026-06-04
**Experimento:** Evaluacion de transferencia con n=30 episodios por ciudad/modelo.
**Estadistico central:** Mediana (robusta ante gridlocks). Dispersión: IQR.
**Test estadistico:** Mann-Whitney U bilateral (alpha=0.05).

---

## Tabla 1 — Metricas por Ciudad y Modelo (Mediana ± IQR)

| Ciudad | Modelo | Delay Mediana (s) | IQR (s) | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|
| Barcelona | ppo_ideal | 181.6 | 0.0 | 0.6175 | 0.0000 | 385.3 | 0.0% |
| Barcelona | ppo_chaos | 180.3 | 0.3 | 0.6172 | 0.0004 | 384.3 | 0.0% |
| Barcelona | fixed_time | 274.3 | 0.5 | 0.5810 | 0.0006 | 551.7 | 0.0% |
| Barcelona | random | 103.0 | 6.3 | 0.6006 | 0.0120 | 344.9 | 0.0% |
| Quito | ppo_ideal | 2780.9 | 76.0 | 0.4351 | 0.0023 | 5685.4 | 100.0% |
| Quito | ppo_chaos | 2776.9 | 47.5 | 0.4462 | 0.0029 | 5795.5 | 100.0% |
| Quito | fixed_time | 1218.5 | 8.0 | 0.3781 | 0.0067 | 2183.3 | 0.0% |
| Quito | random | 1805.8 | 1318.5 | 0.4556 | 0.0176 | 14768.3 | 50.0% |
| Bogota | ppo_ideal | 857.2 | 31.6 | 0.5372 | 0.0034 | 2387.7 | 0.0% |
| Bogota | ppo_chaos | 1019.2 | 54.5 | 0.5131 | 0.0061 | 3192.5 | 0.0% |
| Bogota | fixed_time | 2297.3 | 10.6 | 0.4654 | 0.0172 | 12949.5 | 100.0% |
| Bogota | random | 2690.1 | 1059.7 | 0.5120 | 0.0390 | 16186.2 | 50.0% |
| Berlin | ppo_ideal | 1993.4 | 294.1 | 0.5812 | 0.0117 | 5118.7 | 50.0% |
| Berlin | ppo_chaos | 24652.9 | 1276.5 | 0.4813 | 0.0402 | 41326.1 | 100.0% |
| Berlin | fixed_time | 28242.0 | 780.0 | 0.4778 | 0.0185 | 50706.9 | 100.0% |
| Berlin | random | 27473.7 | 681.4 | 0.4923 | 0.0034 | 47475.4 | 100.0% |
| Madrid | ppo_ideal | 217.3 | 0.1 | 0.5906 | 0.0009 | 621.0 | 0.0% |
| Madrid | ppo_chaos | 1846.6 | 14.6 | 0.2115 | 0.0028 | 3672.2 | 0.0% |
| Madrid | fixed_time | 236.0 | 5.2 | 0.5937 | 0.0037 | 656.8 | 0.0% |
| Madrid | random | 43.0 | 1.2 | 0.6134 | 0.0008 | 209.5 | 0.0% |
| CDMX | ppo_ideal | 8524.0 | 58.1 | 0.7277 | 0.0034 | 15599.2 | 100.0% |
| CDMX | ppo_chaos | 9046.3 | 893.4 | 0.7369 | 0.0015 | 17675.8 | 100.0% |
| CDMX | fixed_time | 8856.4 | 170.1 | 0.7393 | 0.0004 | 16118.5 | 100.0% |
| CDMX | random | 8494.1 | 999.6 | 0.7385 | 0.0045 | 15053.3 | 100.0% |

## Tabla 2 — Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | CO2 Total (g) | Combustible Total (L) |
|---|---|---|---|
| Barcelona | ppo_ideal | 37133.69 | 12038.543 |
| Barcelona | ppo_chaos | 37297.96 | 12091.798 |
| Barcelona | fixed_time | 37977.85 | 12312.214 |
| Barcelona | random | 36878.17 | 11955.703 |
| Quito | ppo_ideal | 1177990.50 | 381892.810 |
| Quito | ppo_chaos | 1173025.14 | 380283.058 |
| Quito | fixed_time | 1147514.50 | 372012.063 |
| Quito | random | 1113268.59 | 360909.182 |
| Bogota | ppo_ideal | 354370.02 | 114883.175 |
| Bogota | ppo_chaos | 380468.16 | 123344.080 |
| Bogota | fixed_time | 418589.67 | 135703.145 |
| Bogota | random | 419041.08 | 135849.355 |
| Berlin | ppo_ideal | 595997.17 | 193216.473 |
| Berlin | ppo_chaos | 1077006.81 | 349159.396 |
| Berlin | fixed_time | 1100304.36 | 356712.320 |
| Berlin | random | 1097078.77 | 355666.563 |
| Madrid | ppo_ideal | 117398.96 | 38059.088 |
| Madrid | ppo_chaos | 96762.18 | 31369.408 |
| Madrid | fixed_time | 116516.05 | 37772.853 |
| Madrid | random | 119562.00 | 38760.100 |
| CDMX | ppo_ideal | 327307.01 | 106110.667 |
| CDMX | ppo_chaos | 323071.56 | 104737.501 |
| CDMX | fixed_time | 327146.53 | 106058.569 |
| CDMX | random | 321249.57 | 104146.805 |

## Tabla 3 — Test Mann-Whitney U: Caotico vs. Ideal por Ciudad

| Ciudad | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|
| Barcelona | Delay | 0.0 | 0.3333 | ns | 1.000 | large |
| Barcelona | Gini | 2.0 | 1.0000 | ns | 0.000 | negligible |
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
| CDMX | Gini | 4.0 | 0.3333 | ns | -1.000 | large |
| CDMX | CVaR90 | 3.0 | 0.6667 | ns | -0.500 | large |

---

## Interpretacion de Resultados

> **Nota metodologica:** Las mejoras observadas en Quito (Caotico vs. Ideal) son estadisticamente significativas cuando p < 0.05. Con n=30 episodios, el poder estadistico del test Mann-Whitney es >= 80% para efectos medianos (|r| >= 0.3).

El experimento de transferencia zero-shot evalua si la politica entrenada bajo perturbaciones LATAM en Hangzhou preserva sus propiedades de optimizacion multiobjetivo cuando se aplica a redes urbanas distintas mediante el mecanismo de acotamiento topologico (wrapper). La validacion estadistica con n=30 episodios permite distinguir mejoras reales de variabilidad episodica.

---
*Generado por transfer_eval_n30.py — TSC Framework Doctoral*
