# INFORME DE TRANSFERENCIA ZERO-SHOT — N=30 EPISODIOS
**Fecha:** 2026-06-04
**Experimento:** Evaluacion de transferencia con n=30 episodios por ciudad/modelo.
**Estadistico central:** Mediana (robusta ante gridlocks). Dispersión: IQR.
**Test estadistico:** Mann-Whitney U bilateral (alpha=0.05).

---

## Tabla 1 — Metricas por Ciudad y Modelo (Mediana ± IQR)

| Ciudad | Modelo | Delay Mediana (s) | IQR (s) | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|
| Barcelona | random | 108.7 | 0.0 | 0.5862 | 0.0000 | 356.8 | 0.0% |
| Quito | random | 471.9 | 0.0 | 0.4390 | 0.0000 | 1698.2 | 0.0% |
| Bogota | random | 797.4 | 0.0 | 0.5778 | 0.0000 | 4587.8 | 0.0% |
| Berlin | random | 27987.3 | 0.0 | 0.4626 | 0.0000 | 50915.7 | 100.0% |
| Madrid | random | 51.6 | 0.0 | 0.5789 | 0.0000 | 259.4 | 0.0% |
| CDMX | random | 8476.5 | 0.0 | 0.7511 | 0.0000 | 14109.3 | 100.0% |

## Tabla 2 — Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|
| Barcelona | random | 37.27 | 16.328 |
| Quito | random | 1106.58 | 484.784 |
| Bogota | random | 370.07 | 162.127 |
| Berlin | random | 1114.17 | 488.118 |
| Madrid | random | 118.42 | 51.878 |
| CDMX | random | 314.89 | 137.955 |

## Tabla 3 — Test Mann-Whitney U: Caotico vs. Ideal por Ciudad

| Ciudad | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|

---

## Interpretacion de Resultados

> **Nota metodologica:** Las mejoras observadas en Quito (Caotico vs. Ideal) son estadisticamente significativas cuando p < 0.05. Con n=30 episodios, el poder estadistico del test Mann-Whitney es >= 80% para efectos medianos (|r| >= 0.3).

El experimento de transferencia zero-shot evalua si la politica entrenada bajo perturbaciones LATAM en Hangzhou preserva sus propiedades de optimizacion multiobjetivo cuando se aplica a redes urbanas distintas mediante el mecanismo de acotamiento topologico (wrapper). La validacion estadistica con n=30 episodios permite distinguir mejoras reales de variabilidad episodica.

---
*Generado por transfer_eval_n30.py — TSC Framework Doctoral*
