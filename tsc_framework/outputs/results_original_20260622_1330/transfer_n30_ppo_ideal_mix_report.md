# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-15
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Berlin | ppo_ideal | low | 30 | 21.7 | 1.5 | [21.4, 22.4] | 0.3278 | 0.0076 | 67.3 | 0.0% |
| Berlin | ppo_ideal | mid | 30 | 400.1 | 84.8 | [371.0, 425.2] | 0.5779 | 0.0170 | 1123.6 | 0.0% |
| Berlin | ppo_ideal | mid_high | 30 | 6848.2 | 3670.4 | [5772.6, 8597.1] | 0.5232 | 0.0247 | 16453.9 | 86.7% |
| Berlin | ppo_ideal | high | 30 | 17185.6 | 2263.2 | [16438.4, 17996.1] | 0.5503 | 0.0124 | 32727.0 | 100.0% |
| Berlin | ppo_ideal | extreme | 30 | 26918.3 | 2849.4 | [25918.4, 27527.0] | 0.5444 | 0.0101 | 44929.2 | 100.0% |
| CDMX | ppo_ideal | low | 30 | 3.2 | 0.5 | [3.1, 3.3] | 0.0587 | 0.0034 | 14.8 | 0.0% |
| CDMX | ppo_ideal | mid | 30 | 9.4 | 2.4 | [8.8, 10.1] | 0.1151 | 0.0043 | 37.9 | 0.0% |
| CDMX | ppo_ideal | mid_high | 30 | 149.9 | 120.8 | [117.9, 199.1] | 0.1931 | 0.0073 | 933.1 | 0.0% |
| CDMX | ppo_ideal | high | 30 | 15870.5 | 5397.0 | [13925.1, 18040.6] | 0.3134 | 0.0092 | 37515.4 | 100.0% |
| CDMX | ppo_ideal | extreme | 30 | 75833.4 | 27375.7 | [67658.9, 87779.1] | 0.4966 | 0.0245 | 163653.9 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Berlin | ppo_ideal | low | 14.17 | 6.209 |
| Berlin | ppo_ideal | mid | 51.39 | 22.512 |
| Berlin | ppo_ideal | mid_high | 140.07 | 61.363 |
| Berlin | ppo_ideal | high | 257.66 | 112.882 |
| Berlin | ppo_ideal | extreme | 324.39 | 142.115 |
| CDMX | ppo_ideal | low | 4.87 | 2.134 |
| CDMX | ppo_ideal | mid | 10.13 | 4.438 |
| CDMX | ppo_ideal | mid_high | 19.65 | 8.606 |
| CDMX | ppo_ideal | high | 129.49 | 56.729 |
| CDMX | ppo_ideal | extreme | 284.21 | 124.512 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
| Berlin | low | N/A | N/A | N/A |
| Berlin | mid | N/A | N/A | N/A |
| Berlin | mid_high | N/A | N/A | N/A |
| Berlin | high | N/A | N/A | N/A |
| Berlin | extreme | N/A | N/A | N/A |
| CDMX | low | N/A | N/A | N/A |
| CDMX | mid | N/A | N/A | N/A |
| CDMX | mid_high | N/A | N/A | N/A |
| CDMX | high | N/A | N/A | N/A |
| CDMX | extreme | N/A | N/A | N/A |

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| Berlin | ppo_ideal | 0.980 | 0.0000 | *** |
| CDMX | ppo_ideal | 0.980 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
