# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-08
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| CDMX | ppo_coop_ideal | low | 30 | 3.1 | 0.4 | [3.0, 3.2] | 0.0560 | 0.0032 | 14.5 | 0.0% |
| CDMX | ppo_coop_ideal | mid | 30 | 9.4 | 1.5 | [9.2, 10.3] | 0.1135 | 0.0064 | 39.0 | 0.0% |
| CDMX | ppo_coop_ideal | mid_high | 30 | 242.3 | 191.4 | [159.8, 302.3] | 0.1915 | 0.0056 | 1377.5 | 0.0% |
| CDMX | ppo_coop_ideal | high | 30 | 15031.6 | 5987.4 | [13930.8, 18289.6] | 0.3092 | 0.0093 | 37806.3 | 100.0% |
| CDMX | ppo_coop_ideal | extreme | 30 | 78716.7 | 27740.1 | [68646.0, 89994.9] | 0.4960 | 0.0337 | 178470.8 | 100.0% |
| CDMX | ppo_coop_chaos | low | 30 | 3.4 | 0.4 | [3.3, 3.5] | 0.0564 | 0.0032 | 16.4 | 0.0% |
| CDMX | ppo_coop_chaos | mid | 30 | 9.6 | 1.3 | [9.3, 10.3] | 0.1138 | 0.0047 | 37.4 | 0.0% |
| CDMX | ppo_coop_chaos | mid_high | 30 | 187.0 | 89.9 | [160.4, 227.6] | 0.1923 | 0.0073 | 1160.5 | 0.0% |
| CDMX | ppo_coop_chaos | high | 30 | 14802.3 | 7033.6 | [13764.8, 18027.8] | 0.3098 | 0.0129 | 34695.0 | 100.0% |
| CDMX | ppo_coop_chaos | extreme | 30 | 81096.6 | 29366.4 | [66174.9, 88210.5] | 0.4941 | 0.0220 | 175746.8 | 100.0% |
| CDMX | ppo_chaos | low | 30 | 2.5 | 0.3 | [2.4, 2.7] | 0.0497 | 0.0036 | 12.5 | 0.0% |
| CDMX | ppo_chaos | mid | 30 | 7.9 | 1.8 | [7.6, 9.0] | 0.1014 | 0.0050 | 33.7 | 0.0% |
| CDMX | ppo_chaos | mid_high | 30 | 191.7 | 143.6 | [147.2, 260.6] | 0.1784 | 0.0112 | 1152.9 | 0.0% |
| CDMX | ppo_chaos | high | 30 | 17612.7 | 9830.1 | [16256.7, 22057.9] | 0.2912 | 0.0098 | 43912.4 | 100.0% |
| CDMX | ppo_chaos | extreme | 30 | 75724.3 | 34553.3 | [64668.2, 86302.0] | 0.4917 | 0.0301 | 173193.1 | 100.0% |
| CDMX | fixed_time_opt | low | 30 | 4.8 | 0.6 | [4.6, 5.0] | 0.0620 | 0.0030 | 24.1 | 0.0% |
| CDMX | fixed_time_opt | mid | 30 | 13.1 | 2.1 | [12.2, 13.4] | 0.1213 | 0.0051 | 51.9 | 0.0% |
| CDMX | fixed_time_opt | mid_high | 30 | 201.5 | 206.2 | [176.6, 296.0] | 0.1993 | 0.0118 | 1214.8 | 0.0% |
| CDMX | fixed_time_opt | high | 30 | 16986.0 | 5065.7 | [15890.0, 18842.0] | 0.3153 | 0.0099 | 39403.8 | 100.0% |
| CDMX | fixed_time_opt | extreme | 30 | 74208.0 | 27963.4 | [62958.5, 86246.5] | 0.5096 | 0.0251 | 157776.5 | 100.0% |
| CDMX | random | low | 30 | 10.5 | 3.1 | [9.6, 11.3] | 0.0792 | 0.0064 | 53.8 | 0.0% |
| CDMX | random | mid | 30 | 29.1 | 6.2 | [27.6, 30.8] | 0.1524 | 0.0110 | 118.2 | 0.0% |
| CDMX | random | mid_high | 30 | 227.4 | 106.3 | [185.7, 277.0] | 0.2414 | 0.0086 | 1176.1 | 0.0% |
| CDMX | random | high | 30 | 17350.5 | 7653.4 | [15205.2, 18884.8] | 0.3528 | 0.0117 | 41121.1 | 100.0% |
| CDMX | random | extreme | 30 | 79953.3 | 20032.4 | [70392.7, 84447.0] | 0.5147 | 0.0275 | 169737.8 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| CDMX | ppo_coop_ideal | low | 4.83 | 2.117 |
| CDMX | ppo_coop_ideal | mid | 10.14 | 4.442 |
| CDMX | ppo_coop_ideal | mid_high | 20.39 | 8.932 |
| CDMX | ppo_coop_ideal | high | 131.38 | 57.556 |
| CDMX | ppo_coop_ideal | extreme | 284.58 | 124.674 |
| CDMX | ppo_coop_chaos | low | 4.83 | 2.117 |
| CDMX | ppo_coop_chaos | mid | 10.16 | 4.449 |
| CDMX | ppo_coop_chaos | mid_high | 19.97 | 8.748 |
| CDMX | ppo_coop_chaos | high | 126.83 | 55.566 |
| CDMX | ppo_coop_chaos | extreme | 277.45 | 121.552 |
| CDMX | ppo_chaos | low | 4.73 | 2.071 |
| CDMX | ppo_chaos | mid | 9.91 | 4.343 |
| CDMX | ppo_chaos | mid_high | 19.82 | 8.682 |
| CDMX | ppo_chaos | high | 131.53 | 57.625 |
| CDMX | ppo_chaos | extreme | 281.91 | 123.504 |
| CDMX | fixed_time_opt | low | 4.93 | 2.159 |
| CDMX | fixed_time_opt | mid | 10.38 | 4.545 |
| CDMX | fixed_time_opt | mid_high | 20.93 | 9.167 |
| CDMX | fixed_time_opt | high | 134.56 | 58.950 |
| CDMX | fixed_time_opt | extreme | 288.74 | 126.497 |
| CDMX | random | low | 5.18 | 2.268 |
| CDMX | random | mid | 11.10 | 4.865 |
| CDMX | random | mid_high | 22.59 | 9.897 |
| CDMX | random | high | 136.68 | 59.882 |
| CDMX | random | extreme | 284.64 | 124.699 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|
| CDMX | low | Delay | 693.0 | 0.0003 | *** | -0.540 | large |
| CDMX | low | Gini | 535.0 | 0.2116 | ns | -0.189 | small |
| CDMX | low | CVaR90 | 730.0 | 0.0000 | *** | -0.622 | large |
| CDMX | mid | Delay | 468.0 | 0.7958 | ns | -0.040 | negligible |
| CDMX | mid | Gini | 471.0 | 0.7618 | ns | -0.047 | negligible |
| CDMX | mid | CVaR90 | 417.0 | 0.6309 | ns | 0.073 | negligible |
| CDMX | mid_high | Delay | 359.0 | 0.1809 | ns | 0.202 | small |
| CDMX | mid_high | Gini | 484.0 | 0.6204 | ns | -0.076 | negligible |
| CDMX | mid_high | CVaR90 | 376.0 | 0.2772 | ns | 0.164 | small |
| CDMX | high | Delay | 422.0 | 0.6843 | ns | 0.062 | negligible |
| CDMX | high | Gini | 496.0 | 0.5011 | ns | -0.102 | small |
| CDMX | high | CVaR90 | 426.0 | 0.7283 | ns | 0.053 | negligible |
| CDMX | extreme | Delay | 451.0 | 0.9941 | ns | -0.002 | negligible |
| CDMX | extreme | Gini | 427.0 | 0.7394 | ns | 0.051 | negligible |
| CDMX | extreme | CVaR90 | 478.0 | 0.6843 | ns | -0.062 | negligible |

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
| CDMX | low | 135.4 | 0.0000 | *** |
| CDMX | mid | 105.1 | 0.0000 | *** |
| CDMX | mid_high | 3.7 | 0.4550 | ns |
| CDMX | high | 8.9 | 0.0630 | ns |
| CDMX | extreme | 1.0 | 0.9138 | ns |

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|
| CDMX | low | ppo_coop_ideal | ppo_coop_chaos | 0.0003 | 0.0034 | ** |
| CDMX | low | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | low | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | low | fixed_time_opt | random | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_ideal | ppo_coop_chaos | 0.7958 | 1.0000 | ns |
| CDMX | mid | ppo_coop_ideal | ppo_chaos | 0.0018 | 0.0177 | * |
| CDMX | mid | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_chaos | ppo_chaos | 0.0006 | 0.0056 | ** |
| CDMX | mid | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| CDMX | mid | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| CDMX | mid | fixed_time_opt | random | 0.0000 | 0.0000 | *** |
| CDMX | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.1809 | 1.0000 | ns |
| CDMX | mid_high | ppo_coop_ideal | ppo_chaos | 0.4035 | 1.0000 | ns |
| CDMX | mid_high | ppo_coop_ideal | fixed_time_opt | 0.7062 | 1.0000 | ns |
| CDMX | mid_high | ppo_coop_ideal | random | 0.8187 | 1.0000 | ns |
| CDMX | mid_high | ppo_coop_chaos | ppo_chaos | 0.8073 | 1.0000 | ns |
| CDMX | mid_high | ppo_coop_chaos | fixed_time_opt | 0.4733 | 1.0000 | ns |
| CDMX | mid_high | ppo_coop_chaos | random | 0.0468 | 0.4676 | ns |
| CDMX | mid_high | ppo_chaos | fixed_time_opt | 0.6843 | 1.0000 | ns |
| CDMX | mid_high | ppo_chaos | random | 0.2282 | 1.0000 | ns |
| CDMX | mid_high | fixed_time_opt | random | 0.5692 | 1.0000 | ns |
| CDMX | high | ppo_coop_ideal | ppo_coop_chaos | 0.6843 | 1.0000 | ns |
| CDMX | high | ppo_coop_ideal | ppo_chaos | 0.0303 | 0.3032 | ns |
| CDMX | high | ppo_coop_ideal | fixed_time_opt | 0.2170 | 1.0000 | ns |
| CDMX | high | ppo_coop_ideal | random | 0.2062 | 1.0000 | ns |
| CDMX | high | ppo_coop_chaos | ppo_chaos | 0.0099 | 0.0988 | ns |
| CDMX | high | ppo_coop_chaos | fixed_time_opt | 0.0905 | 0.9049 | ns |
| CDMX | high | ppo_coop_chaos | random | 0.0963 | 0.9626 | ns |
| CDMX | high | ppo_chaos | fixed_time_opt | 0.3183 | 1.0000 | ns |
| CDMX | high | ppo_chaos | random | 0.4204 | 1.0000 | ns |
| CDMX | high | fixed_time_opt | random | 0.9705 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.9941 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_ideal | ppo_chaos | 0.7283 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_ideal | fixed_time_opt | 0.5793 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_ideal | random | 0.9234 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_chaos | ppo_chaos | 0.5592 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_chaos | fixed_time_opt | 0.5201 | 1.0000 | ns |
| CDMX | extreme | ppo_coop_chaos | random | 0.9352 | 1.0000 | ns |
| CDMX | extreme | ppo_chaos | fixed_time_opt | 0.9234 | 1.0000 | ns |
| CDMX | extreme | ppo_chaos | random | 0.5592 | 1.0000 | ns |
| CDMX | extreme | fixed_time_opt | random | 0.3555 | 1.0000 | ns |

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| CDMX | ppo_coop_ideal | 0.980 | 0.0000 | *** |
| CDMX | ppo_coop_chaos | 0.980 | 0.0000 | *** |
| CDMX | ppo_chaos | 0.980 | 0.0000 | *** |
| CDMX | fixed_time_opt | 0.980 | 0.0000 | *** |
| CDMX | random | 0.980 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
