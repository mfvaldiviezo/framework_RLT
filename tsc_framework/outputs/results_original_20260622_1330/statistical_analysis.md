## [ANALISIS] Análisis Estadístico — Pruebas No-Paramétricas

> **Nota metodológica:** Dado que la distribución de los retrasos vehiculares no es normal (presencia de episodios catastróficos de gridlock), se aplican pruebas no-paramétricas robustas ante outliers: Mann-Whitney U (comparación por pares) y Kruskal-Wallis (comparación multi-grupo). El nivel de significancia es α = 0.05. El tamaño del efecto se mide mediante la correlación rank-biserial *r* (|r| < 0.3 = pequeño; 0.3–0.5 = medio; > 0.5 = grande).

---

### Comparaciones por Pares RL — delay\_mean y cvar\_95 (Mann-Whitney U)

*(Incluye modelos originales y variantes cooperativas)*

| Par de Modelos | Caos % | Métrica | U stat | p-value | Signif. | r (effect) | Magnitud | Mediana A | Mediana B |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| H-SARG Caótico vs Ideal | 0% | delay_mean | 415.0 | 0.6100 | ns | 0.078 | negligible | 588.5 | 592.8 |
| H-SARG Caótico vs Ideal | 15% | delay_mean | 493.0 | 0.5298 | ns | -0.096 | negligible | 573.8 | 589.6 |
| H-SARG Caótico vs Ideal | 30% | delay_mean | 462.0 | 0.8650 | ns | -0.027 | negligible | 589.6 | 577.3 |
| H-SARG Caótico vs Ideal | 50% | delay_mean | 504.0 | 0.4290 | ns | -0.120 | small | 614.0 | 573.6 |
| H-SARG Caótico vs Ideal | 0% | cvar_95 | 756.0 | 0.0000 | *** | -0.680 | large | 3224.3 | 1995.8 |
| H-SARG Caótico vs Ideal | 15% | cvar_95 | 248.0 | 0.0029 | ** | 0.449 | medium | 2329.7 | 3428.1 |
| H-SARG Caótico vs Ideal | 30% | cvar_95 | 49.0 | 0.0000 | *** | 0.891 | large | 1835.9 | 4561.1 |
| H-SARG Caótico vs Ideal | 50% | cvar_95 | 508.0 | 0.3953 | ns | -0.129 | small | 5056.9 | 4669.8 |
| Coop-Ideal vs Ideal | 0% | delay_mean | 205.0 | 0.0003 | *** | 0.544 | large | 384.9 | 592.8 |
| Coop-Ideal vs Ideal | 15% | delay_mean | 193.0 | 0.0001 | *** | 0.571 | large | 358.9 | 589.6 |
| Coop-Ideal vs Ideal | 30% | delay_mean | 151.0 | 0.0000 | *** | 0.664 | large | 311.1 | 577.3 |
| Coop-Ideal vs Ideal | 50% | delay_mean | 87.0 | 0.0000 | *** | 0.807 | large | 291.9 | 573.6 |
| Coop-Ideal vs Ideal | 0% | cvar_95 | 236.0 | 0.0016 | ** | 0.476 | medium | 1411.2 | 1995.8 |
| Coop-Ideal vs Ideal | 15% | cvar_95 | 120.0 | 0.0000 | *** | 0.733 | large | 1612.7 | 3428.1 |
| Coop-Ideal vs Ideal | 30% | cvar_95 | 87.0 | 0.0000 | *** | 0.807 | large | 1197.2 | 4561.1 |
| Coop-Ideal vs Ideal | 50% | cvar_95 | 117.0 | 0.0000 | *** | 0.740 | large | 2633.3 | 4669.8 |
| Coop-Caos vs Caótico | 0% | delay_mean | 462.0 | 0.8650 | ns | -0.027 | negligible | 597.6 | 588.5 |
| Coop-Caos vs Caótico | 15% | delay_mean | 373.0 | 0.2581 | ns | 0.171 | small | 550.3 | 573.8 |
| Coop-Caos vs Caótico | 30% | delay_mean | 517.0 | 0.3255 | ns | -0.149 | small | 683.5 | 589.6 |
| Coop-Caos vs Caótico | 50% | delay_mean | 495.0 | 0.5106 | ns | -0.100 | small | 698.9 | 614.0 |
| Coop-Caos vs Caótico | 0% | cvar_95 | 348.0 | 0.1335 | ns | 0.227 | small | 2841.2 | 3224.3 |
| Coop-Caos vs Caótico | 15% | cvar_95 | 349.0 | 0.1373 | ns | 0.224 | small | 2168.8 | 2329.7 |
| Coop-Caos vs Caótico | 30% | cvar_95 | 679.0 | 0.0007 | *** | -0.509 | large | 2891.9 | 1835.9 |
| Coop-Caos vs Caótico | 50% | cvar_95 | 221.0 | 0.0007 | *** | 0.509 | large | 3070.9 | 5056.9 |
| Coop-Caos vs Coop-Ideal | 0% | delay_mean | 678.0 | 0.0008 | *** | -0.507 | large | 597.6 | 384.9 |
| Coop-Caos vs Coop-Ideal | 15% | delay_mean | 709.0 | 0.0001 | *** | -0.576 | large | 550.3 | 358.9 |
| Coop-Caos vs Coop-Ideal | 30% | delay_mean | 752.0 | 0.0000 | *** | -0.671 | large | 683.5 | 311.1 |
| Coop-Caos vs Coop-Ideal | 50% | delay_mean | 827.0 | 0.0000 | *** | -0.838 | large | 698.9 | 291.9 |
| Coop-Caos vs Coop-Ideal | 0% | cvar_95 | 747.0 | 0.0000 | *** | -0.660 | large | 2841.2 | 1411.2 |
| Coop-Caos vs Coop-Ideal | 15% | cvar_95 | 642.0 | 0.0046 | ** | -0.427 | medium | 2168.8 | 1612.7 |
| Coop-Caos vs Coop-Ideal | 30% | cvar_95 | 763.0 | 0.0000 | *** | -0.696 | large | 2891.9 | 1197.2 |
| Coop-Caos vs Coop-Ideal | 50% | cvar_95 | 558.0 | 0.1120 | ns | -0.240 | small | 3070.9 | 2633.3 |

**Leyenda:** *** p < 0.001 | ** p < 0.01 | * p < 0.05 | ns = no significativo

---

### Diferencias entre Todos los Controladores (Kruskal-Wallis)

| Caos % | H stat | p-value | Signif. | Interpretación |
|:---:|:---:|:---:|:---:|:---|
| 0% | 63.354 | 0.0000 | *** | Diferencias significativas entre controladores |
| 15% | 68.244 | 0.0000 | *** | Diferencias significativas entre controladores |
| 30% | 70.418 | 0.0000 | *** | Diferencias significativas entre controladores |
| 50% | 103.886 | 0.0000 | *** | Diferencias significativas entre controladores |

---

### Tabla de Tasa de Colapso de Red — 4 Modelos RL

*(Umbral de gridlock: Delay > 2000 s por episodio)*

| Controlador | Caos % | Tasa Colapso (%) | Mediana Delay (s) | IQR (s) | CVaR₉₅ (s) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **H-SARG Ideal** | 0% | **6.7%** | 592.8 s | 232.7 s | 381152.2 s |
| **H-SARG Ideal** | 15% | **3.3%** | 589.6 s | 296.9 s | 61685.1 s |
| **H-SARG Ideal** | 30% | **10.0%** | 577.3 s | 180.8 s | 43198.3 s |
| **H-SARG Ideal** | 50% | **3.3%** | 573.6 s | 404.3 s | 17891.3 s |
| **H-SARG Caótico** | 0% | **10.0%** | 588.5 s | 244.1 s | 156324.7 s |
| **H-SARG Caótico** | 15% | **3.3%** | 573.8 s | 244.7 s | 147564.8 s |
| **H-SARG Caótico** | 30% | **3.3%** | 589.6 s | 223.7 s | 284590.2 s |
| **H-SARG Caótico** | 50% | **3.3%** | 614.0 s | 232.8 s | 7533.1 s |
| **H-SARG Coop-Ideal** | 0% | **13.3%** | 384.9 s | 299.2 s | 454896.5 s |
| **H-SARG Coop-Ideal** | 15% | **6.7%** | 358.9 s | 199.3 s | 232030.8 s |
| **H-SARG Coop-Ideal** | 30% | **10.0%** | 311.1 s | 189.8 s | 354428.7 s |
| **H-SARG Coop-Ideal** | 50% | **3.3%** | 291.9 s | 109.3 s | 4666.6 s |
| **H-SARG Coop-Caos** | 0% | **13.3%** | 597.6 s | 176.5 s | 221485.6 s |
| **H-SARG Coop-Caos** | 15% | **6.7%** | 550.3 s | 247.4 s | 181828.4 s |
| **H-SARG Coop-Caos** | 30% | **6.7%** | 683.5 s | 340.9 s | 138510.2 s |
| **H-SARG Coop-Caos** | 50% | **16.7%** | 698.9 s | 475.1 s | 240420.4 s |

---

### Análisis de Equidad Condicional — Gini en Régimen Nominal vs Gridlock

*(Valida H3/RQ4: el Índice de Gini colapsa durante episodios de gridlock, demostrando que las métricas de equidad son estables solo en condiciones nominales)*

| Controlador | Caos % | Gini Nominal (delay<2000s) | Gini Gridlock (delay>2000s) | Episodios Gridlock |
|:---|:---:|:---:|:---:|:---:|
| H-SARG Ideal | 0% | 0.451 | 0.226 | 2 |
| H-SARG Ideal | 15% | 0.459 | 0.321 | 1 |
| H-SARG Ideal | 30% | 0.462 | 0.442 | 3 |
| H-SARG Ideal | 50% | 0.475 | 0.407 | 1 |
| H-SARG Caótico | 0% | 0.454 | 0.344 | 3 |
| H-SARG Caótico | 15% | 0.452 | 0.267 | 1 |
| H-SARG Caótico | 30% | 0.465 | 0.150 | 1 |
| H-SARG Caótico | 50% | 0.465 | 0.410 | 1 |
| H-SARG Coop-Ideal | 0% | 0.503 | 0.266 | 4 |
| H-SARG Coop-Ideal | 15% | 0.506 | 0.275 | 2 |
| H-SARG Coop-Ideal | 30% | 0.504 | 0.236 | 3 |
| H-SARG Coop-Ideal | 50% | 0.518 | 0.537 | 1 |
| H-SARG Coop-Caos | 0% | 0.455 | 0.333 | 4 |
| H-SARG Coop-Caos | 15% | 0.465 | 0.313 | 2 |
| H-SARG Coop-Caos | 30% | 0.454 | 0.332 | 2 |
| H-SARG Coop-Caos | 50% | 0.461 | 0.373 | 5 |
| MaxPressure | 0% | 0.465 | — | 0 |
| MaxPressure | 15% | 0.457 | — | 0 |
| MaxPressure | 30% | 0.454 | 0.181 | 2 |
| MaxPressure | 50% | 0.478 | 0.426 | 1 |
| Fixed Time | 0% | 0.483 | 0.404 | 4 |
| Fixed Time | 15% | 0.484 | 0.425 | 2 |
| Fixed Time | 30% | 0.498 | 0.229 | 1 |
| Fixed Time | 50% | 0.493 | 0.313 | 3 |
| CoLight | 0% | 0.496 | 0.354 | 1 |
| CoLight | 15% | 0.504 | 0.353 | 3 |
| CoLight | 30% | 0.503 | 0.346 | 3 |
| CoLight | 50% | 0.496 | 0.355 | 1 |

---
*Análisis generado automáticamente por `statistical_analysis.py` — TSC Framework Doctoral.*
