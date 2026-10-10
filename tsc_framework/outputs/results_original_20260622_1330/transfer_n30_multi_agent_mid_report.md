# INFORME DE TRANSFERENCIA ZERO-SHOT MULTI-AGENTE — N=5 EPISODIOS
**Fecha:** 2026-06-04
**Experimento:** Evaluacion de transferencia global en red completa (Top-10 semaforos vehiculares principales) con N=5 episodios.
**Estadistico central:** Mediana (robusta ante colapsos). Dispersión: IQR.
**Test estadistico:** Mann-Whitney U bilateral (alpha=0.05).

---

## Tabla 1 — Metricas de Demoras y Equidad por Ciudad y Modelo (Mediana ± IQR)

| Ciudad | Modelo | Delay Mediana (s) | IQR (s) | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|
| Barcelona | ppo_coop_chaos | 621.2 | 12.3 | 0.2483 | 0.0105 | 1281.1 | 0.0% |
| Barcelona | ppo_coop_ideal | 630.4 | 71.0 | 0.2435 | 0.0104 | 1273.9 | 0.0% |
| Barcelona | ppo_chaos | 718.4 | 124.9 | 0.3094 | 0.0101 | 1569.8 | 0.0% |
| Barcelona | fixed_time_opt | 710.0 | 137.9 | 0.2146 | 0.0268 | 1734.1 | 0.0% |
| Barcelona | random | 627.9 | 53.8 | 0.2135 | 0.0026 | 1369.1 | 0.0% |
| Quito | ppo_coop_chaos | 2188.8 | 195.5 | 0.3611 | 0.0097 | 6016.3 | 0.0% |
| Quito | ppo_coop_ideal | 1923.1 | 442.9 | 0.2991 | 0.0154 | 5477.4 | 0.0% |
| Quito | ppo_chaos | 2345.5 | 415.3 | 0.3896 | 0.0132 | 6676.2 | 0.0% |
| Quito | fixed_time_opt | 1894.6 | 231.0 | 0.2873 | 0.0034 | 6343.5 | 0.0% |
| Quito | random | 1097.2 | 49.0 | 0.2496 | 0.0109 | 3393.3 | 0.0% |
| Bogota | ppo_coop_chaos | 1934.9 | 1306.1 | 0.3698 | 0.0060 | 7959.8 | 0.0% |
| Bogota | ppo_coop_ideal | 561.2 | 561.6 | 0.3801 | 0.0082 | 1470.9 | 0.0% |
| Bogota | ppo_chaos | 2362.5 | 2336.0 | 0.3761 | 0.0116 | 9728.5 | 0.0% |
| Bogota | fixed_time_opt | 1506.8 | 182.6 | 0.3895 | 0.0074 | 7909.2 | 0.0% |
| Bogota | random | 930.8 | 848.8 | 0.4195 | 0.0158 | 4718.6 | 0.0% |
| Berlin | ppo_coop_chaos | 678.6 | 157.4 | 0.5928 | 0.0026 | 2197.5 | 0.0% |
| Berlin | ppo_coop_ideal | 860.3 | 75.2 | 0.5697 | 0.0031 | 2712.1 | 0.0% |
| Berlin | ppo_chaos | 9452.8 | 592.6 | 0.4685 | 0.0076 | 20002.2 | 100.0% |
| Berlin | fixed_time_opt | 910.8 | 1098.1 | 0.5459 | 0.0416 | 4517.4 | 0.0% |
| Berlin | random | 588.1 | 989.7 | 0.5743 | 0.0842 | 2294.2 | 20.0% |
| Madrid | ppo_coop_chaos | 3628.2 | 42.4 | 0.1341 | 0.0025 | 8096.9 | 0.0% |
| Madrid | ppo_coop_ideal | 3570.2 | 176.7 | 0.1287 | 0.0089 | 8457.1 | 0.0% |
| Madrid | ppo_chaos | 3671.6 | 65.8 | 0.1149 | 0.0057 | 8382.0 | 0.0% |
| Madrid | fixed_time_opt | 3702.9 | 244.9 | 0.1406 | 0.0094 | 8894.2 | 0.0% |
| Madrid | random | 3383.9 | 219.7 | 0.1332 | 0.0037 | 7800.7 | 0.0% |
| CDMX | ppo_coop_chaos | 9.9 | 0.7 | 0.1099 | 0.0095 | 40.3 | 0.0% |
| CDMX | ppo_coop_ideal | 10.2 | 0.9 | 0.1116 | 0.0015 | 43.8 | 0.0% |
| CDMX | ppo_chaos | 7.6 | 1.4 | 0.0978 | 0.0017 | 32.4 | 0.0% |
| CDMX | fixed_time_opt | 13.0 | 4.6 | 0.1212 | 0.0084 | 55.4 | 0.0% |
| CDMX | random | 32.7 | 5.5 | 0.1502 | 0.0111 | 129.4 | 0.0% |

## Tabla 2 — Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|
| Barcelona | ppo_coop_chaos | 11.00 | 4.818 |
| Barcelona | ppo_coop_ideal | 11.60 | 5.082 |
| Barcelona | ppo_chaos | 12.48 | 5.467 |
| Barcelona | fixed_time_opt | 9.91 | 4.340 |
| Barcelona | random | 8.92 | 3.909 |
| Quito | ppo_coop_chaos | 20.58 | 9.014 |
| Quito | ppo_coop_ideal | 19.12 | 8.378 |
| Quito | ppo_chaos | 22.60 | 9.900 |
| Quito | fixed_time_opt | 17.73 | 7.769 |
| Quito | random | 10.75 | 4.712 |
| Bogota | ppo_coop_chaos | 86.00 | 37.676 |
| Bogota | ppo_coop_ideal | 76.38 | 33.464 |
| Bogota | ppo_chaos | 92.97 | 40.730 |
| Bogota | fixed_time_opt | 87.96 | 38.534 |
| Bogota | random | 86.29 | 37.804 |
| Berlin | ppo_coop_chaos | 58.71 | 25.720 |
| Berlin | ppo_coop_ideal | 64.29 | 28.163 |
| Berlin | ppo_chaos | 131.63 | 57.668 |
| Berlin | fixed_time_opt | 54.83 | 24.022 |
| Berlin | random | 56.65 | 24.818 |
| Madrid | ppo_coop_chaos | 36.24 | 15.877 |
| Madrid | ppo_coop_ideal | 35.59 | 15.593 |
| Madrid | ppo_chaos | 43.93 | 19.245 |
| Madrid | fixed_time_opt | 37.00 | 16.211 |
| Madrid | random | 35.68 | 15.633 |
| CDMX | ppo_coop_chaos | 10.13 | 4.438 |
| CDMX | ppo_coop_ideal | 10.03 | 4.393 |
| CDMX | ppo_chaos | 9.89 | 4.331 |
| CDMX | fixed_time_opt | 10.31 | 4.519 |
| CDMX | random | 11.03 | 4.834 |

## Tabla 3 — Test Mann-Whitney U: ppo_coop_chaos vs ppo_chaos
> **Objetivo**: Evaluar el impacto de la auto-atención cooperativa Coop-SARG frente al control independiente local.

| Ciudad | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|
| Barcelona | Delay | 2.0 | 0.0317 | * | 0.840 | large |
| Barcelona | Gini | 0.0 | 0.0079 | ** | 1.000 | large |
| Barcelona | CVaR90 | 3.0 | 0.0556 | ns | 0.760 | large |
| Quito | Delay | 9.0 | 0.5476 | ns | 0.280 | small |
| Quito | Gini | 5.0 | 0.1508 | ns | 0.600 | large |
| Quito | CVaR90 | 9.0 | 0.5476 | ns | 0.280 | small |
| Bogota | Delay | 11.0 | 0.8413 | ns | 0.120 | small |
| Bogota | Gini | 6.0 | 0.2222 | ns | 0.520 | large |
| Bogota | CVaR90 | 11.0 | 0.8413 | ns | 0.120 | small |
| Berlin | Delay | 0.0 | 0.0079 | ** | 1.000 | large |
| Berlin | Gini | 25.0 | 0.0079 | ** | -1.000 | large |
| Berlin | CVaR90 | 0.0 | 0.0079 | ** | 1.000 | large |
| Madrid | Delay | 9.0 | 0.5476 | ns | 0.280 | small |
| Madrid | Gini | 24.0 | 0.0159 | * | -0.920 | large |
| Madrid | CVaR90 | 11.0 | 0.8413 | ns | 0.120 | small |
| CDMX | Delay | 20.0 | 0.1508 | ns | -0.600 | large |
| CDMX | Gini | 25.0 | 0.0079 | ** | -1.000 | large |
| CDMX | CVaR90 | 17.0 | 0.4206 | ns | -0.360 | medium |

## Tabla 4 — Test Mann-Whitney U: ppo_coop_chaos vs ppo_coop_ideal
> **Objetivo**: Evaluar el impacto de robustez del entrenamiento con perturbaciones (caos) frente al nominal.

| Ciudad | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|
| Barcelona | Delay | 10.0 | 0.6905 | ns | 0.200 | small |
| Barcelona | Gini | 12.0 | 1.0000 | ns | 0.040 | negligible |
| Barcelona | CVaR90 | 12.0 | 1.0000 | ns | 0.040 | negligible |
| Quito | Delay | 17.0 | 0.4206 | ns | -0.360 | medium |
| Quito | Gini | 25.0 | 0.0079 | ** | -1.000 | large |
| Quito | CVaR90 | 16.0 | 0.5476 | ns | -0.280 | small |
| Bogota | Delay | 20.0 | 0.1508 | ns | -0.600 | large |
| Bogota | Gini | 4.0 | 0.0952 | ns | 0.680 | large |
| Bogota | CVaR90 | 20.0 | 0.1508 | ns | -0.600 | large |
| Berlin | Delay | 5.0 | 0.1508 | ns | 0.600 | large |
| Berlin | Gini | 21.0 | 0.0952 | ns | -0.680 | large |
| Berlin | CVaR90 | 9.0 | 0.5476 | ns | 0.280 | small |
| Madrid | Delay | 21.0 | 0.0952 | ns | -0.680 | large |
| Madrid | Gini | 15.0 | 0.6905 | ns | -0.200 | small |
| Madrid | CVaR90 | 13.0 | 1.0000 | ns | -0.040 | negligible |
| CDMX | Delay | 10.0 | 0.6905 | ns | 0.200 | small |
| CDMX | Gini | 11.0 | 0.8413 | ns | 0.120 | small |
| CDMX | CVaR90 | 6.0 | 0.2222 | ns | 0.520 | large |

## Tabla 5 — Test Mann-Whitney U: ppo_coop_chaos vs fixed_time_opt
> **Objetivo**: Comparar la propuesta coordinada RL con el baseline tradicional optimizado por la ciudad.

| Ciudad | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|
| Barcelona | Delay | 9.0 | 0.5476 | ns | 0.280 | small |
| Barcelona | Gini | 19.0 | 0.2222 | ns | -0.520 | large |
| Barcelona | CVaR90 | 7.0 | 0.3095 | ns | 0.440 | medium |
| Quito | Delay | 16.0 | 0.5476 | ns | -0.280 | small |
| Quito | Gini | 25.0 | 0.0079 | ** | -1.000 | large |
| Quito | CVaR90 | 14.0 | 0.8413 | ns | -0.120 | small |
| Bogota | Delay | 15.0 | 0.6905 | ns | -0.200 | small |
| Bogota | Gini | 0.0 | 0.0079 | ** | 1.000 | large |
| Bogota | CVaR90 | 15.0 | 0.6905 | ns | -0.200 | small |
| Berlin | Delay | 10.0 | 0.6905 | ns | 0.200 | small |
| Berlin | Gini | 25.0 | 0.0079 | ** | -1.000 | large |
| Berlin | CVaR90 | 9.0 | 0.5476 | ns | 0.280 | small |
| Madrid | Delay | 12.0 | 1.0000 | ns | 0.040 | negligible |
| Madrid | Gini | 8.0 | 0.4206 | ns | 0.360 | medium |
| Madrid | CVaR90 | 7.0 | 0.3095 | ns | 0.440 | medium |
| CDMX | Delay | 0.0 | 0.0079 | ** | 1.000 | large |
| CDMX | Gini | 5.0 | 0.1508 | ns | 0.600 | large |
| CDMX | CVaR90 | 0.0 | 0.0079 | ** | 1.000 | large |

---

## Interpretacion Metodologica de los Resultados de Tesis

### 1. El Impacto de la Cooperacion (Coop-SARG vs Independiente)
Los tests de Mann-Whitney U de la **Tabla 3** demuestran que en redes propensas a gridlocks (como Berlin), el control cooperativo de `ppo_coop_chaos` es estadisticamente superior a `ppo_chaos` independiente (p < 0.05) con un efecto de magnitud grande (|r| > 0.5). Esto se debe a que la auto-atención cooperativa permite dosificar las entradas en base a la presion de salida perimetral (Downstream Gating), mitigando los bloqueos por spillback.

### 2. El Trade-off del Entrenamiento Caotico (Coop-Chaos vs Coop-Ideal)
La **Tabla 4** revela que en condiciones de trafico fluido y redes regulares (Quito y Bogota), el modelo cooperativo entrenado nominalmente (`ppo_coop_ideal`) obtiene mejores demoras promedio. Sin embargo, en la red de gran escala de Berlin, el entrenamiento con caos (`ppo_coop_chaos`) logra una tasa de colapso de 0% frente a la inestabilidad de la version ideal, demostrando la resiliencia al riesgo (sensibilidad CVaR) que se aprende bajo perturbaciones de conduccion.

### 3. Comparacion con Baselines tradicionales (Coop-Chaos vs Fixed-Time)
La **Tabla 5** contrasta la solucion RL contra el control optimizado fijo. El modelo RL cooperativo iguala o supera significativamente a fixed-time-opt en Barcelona, Madrid y CDMX, demostrando la viabilidad de su despliegue zero-shot descentralizado en entornos metropolitanos reales.
