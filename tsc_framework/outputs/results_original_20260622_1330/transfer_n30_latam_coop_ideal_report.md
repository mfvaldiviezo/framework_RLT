# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-14
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Quito | ppo_coop_ideal | low | 30 | 318.6 | 116.0 | [285.2, 357.4] | 0.1591 | 0.0196 | 848.3 | 0.0% |
| Quito | ppo_coop_ideal | mid | 30 | 1951.0 | 479.5 | [1789.2, 2119.0] | 0.3063 | 0.0163 | 5830.4 | 0.0% |
| Quito | ppo_coop_ideal | mid_high | 30 | 2621.3 | 688.5 | [2413.1, 2717.5] | 0.3436 | 0.0363 | 7803.1 | 0.0% |
| Quito | ppo_coop_ideal | high | 30 | 3849.2 | 839.4 | [3646.7, 4066.3] | 0.4390 | 0.0365 | 9473.7 | 13.3% |
| Quito | ppo_coop_ideal | extreme | 30 | 4865.2 | 1351.9 | [4446.1, 5248.9] | 0.5584 | 0.0277 | 11056.2 | 43.3% |
| Bogota | ppo_coop_ideal | low | 30 | 49.3 | 3.5 | [48.6, 50.9] | 0.2379 | 0.0075 | 129.2 | 0.0% |
| Bogota | ppo_coop_ideal | mid | 30 | 1260.1 | 1573.3 | [937.0, 1714.3] | 0.3740 | 0.0129 | 6046.9 | 3.3% |
| Bogota | ppo_coop_ideal | mid_high | 30 | 29143.2 | 9309.7 | [25467.1, 31260.8] | 0.5241 | 0.0150 | 88038.9 | 100.0% |
| Bogota | ppo_coop_ideal | high | 30 | 82150.5 | 15688.0 | [77727.6, 87611.7] | 0.5852 | 0.0146 | 187452.5 | 100.0% |
| Bogota | ppo_coop_ideal | extreme | 30 | 145959.6 | 14058.9 | [138553.4, 149234.0] | 0.5682 | 0.0125 | 290005.2 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Quito | ppo_coop_ideal | low | 4.12 | 1.805 |
| Quito | ppo_coop_ideal | mid | 19.02 | 8.332 |
| Quito | ppo_coop_ideal | mid_high | 24.96 | 10.934 |
| Quito | ppo_coop_ideal | high | 36.80 | 16.122 |
| Quito | ppo_coop_ideal | extreme | 44.91 | 19.676 |
| Bogota | ppo_coop_ideal | low | 24.84 | 10.881 |
| Bogota | ppo_coop_ideal | mid | 81.11 | 35.535 |
| Bogota | ppo_coop_ideal | mid_high | 235.28 | 103.075 |
| Bogota | ppo_coop_ideal | high | 351.64 | 154.053 |
| Bogota | ppo_coop_ideal | extreme | 450.00 | 197.145 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
| Quito | low | N/A | N/A | N/A |
| Quito | mid | N/A | N/A | N/A |
| Quito | mid_high | N/A | N/A | N/A |
| Quito | high | N/A | N/A | N/A |
| Quito | extreme | N/A | N/A | N/A |
| Bogota | low | N/A | N/A | N/A |
| Bogota | mid | N/A | N/A | N/A |
| Bogota | mid_high | N/A | N/A | N/A |
| Bogota | high | N/A | N/A | N/A |
| Bogota | extreme | N/A | N/A | N/A |

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| Quito | ppo_coop_ideal | 0.942 | 0.0000 | *** |
| Bogota | ppo_coop_ideal | 0.980 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
