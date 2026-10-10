# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-08
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Barcelona | ppo_coop_ideal | low | 30 | 117.3 | 31.7 | [109.5, 131.6] | 0.1703 | 0.0082 | 382.6 | 0.0% |
| Barcelona | ppo_coop_ideal | mid | 30 | 657.6 | 47.8 | [638.6, 669.7] | 0.2447 | 0.0108 | 1411.1 | 0.0% |
| Barcelona | ppo_coop_ideal | mid_high | 30 | 950.5 | 57.1 | [940.0, 970.2] | 0.2985 | 0.0201 | 2223.3 | 0.0% |
| Barcelona | ppo_coop_ideal | high | 30 | 2229.8 | 176.8 | [2205.2, 2304.5] | 0.4015 | 0.0194 | 5104.5 | 0.0% |
| Barcelona | ppo_coop_ideal | extreme | 30 | 3436.1 | 235.5 | [3332.5, 3530.5] | 0.4122 | 0.0106 | 6743.4 | 0.0% |
| Barcelona | ppo_coop_chaos | low | 30 | 113.0 | 24.3 | [109.2, 126.1] | 0.1658 | 0.0046 | 365.3 | 0.0% |
| Barcelona | ppo_coop_chaos | mid | 30 | 633.5 | 49.5 | [615.5, 644.1] | 0.2427 | 0.0154 | 1328.7 | 0.0% |
| Barcelona | ppo_coop_chaos | mid_high | 30 | 971.0 | 107.9 | [935.8, 1002.0] | 0.2968 | 0.0210 | 2275.8 | 0.0% |
| Barcelona | ppo_coop_chaos | high | 30 | 2215.0 | 138.2 | [2165.3, 2253.8] | 0.4004 | 0.0174 | 5183.8 | 0.0% |
| Barcelona | ppo_coop_chaos | extreme | 30 | 3398.6 | 180.6 | [3334.7, 3472.4] | 0.4191 | 0.0095 | 6688.8 | 0.0% |
| Barcelona | ppo_chaos | low | 30 | 156.6 | 27.3 | [151.8, 162.1] | 0.2322 | 0.0165 | 423.7 | 0.0% |
| Barcelona | ppo_chaos | mid | 30 | 743.4 | 64.6 | [713.5, 759.3] | 0.3100 | 0.0174 | 1519.1 | 0.0% |
| Barcelona | ppo_chaos | mid_high | 30 | 1114.7 | 148.6 | [1067.2, 1177.4] | 0.3553 | 0.0259 | 2677.1 | 0.0% |
| Barcelona | ppo_chaos | high | 30 | 2440.6 | 207.6 | [2329.7, 2502.8] | 0.4003 | 0.0173 | 5374.6 | 0.0% |
| Barcelona | ppo_chaos | extreme | 30 | 3432.3 | 278.0 | [3320.9, 3500.6] | 0.4145 | 0.0112 | 6409.1 | 0.0% |
| Barcelona | fixed_time_opt | low | 30 | 68.0 | 21.7 | [62.9, 76.9] | 0.1185 | 0.0134 | 311.5 | 0.0% |
| Barcelona | fixed_time_opt | mid | 30 | 637.6 | 81.5 | [610.7, 665.6] | 0.2320 | 0.0220 | 1432.3 | 0.0% |
| Barcelona | fixed_time_opt | mid_high | 30 | 1210.0 | 208.2 | [1138.1, 1290.4] | 0.3158 | 0.0453 | 3068.4 | 0.0% |
| Barcelona | fixed_time_opt | high | 30 | 2502.8 | 202.9 | [2419.0, 2554.1] | 0.3854 | 0.0152 | 5887.7 | 0.0% |
| Barcelona | fixed_time_opt | extreme | 30 | 3587.3 | 152.2 | [3533.3, 3617.6] | 0.3977 | 0.0099 | 6862.0 | 0.0% |
| Barcelona | random | low | 30 | 60.2 | 30.9 | [51.5, 70.9] | 0.1084 | 0.0186 | 285.8 | 0.0% |
| Barcelona | random | mid | 30 | 631.6 | 127.4 | [602.0, 691.4] | 0.2345 | 0.0167 | 1460.9 | 0.0% |
| Barcelona | random | mid_high | 30 | 1152.9 | 205.5 | [1044.7, 1205.8] | 0.3020 | 0.0245 | 2909.0 | 0.0% |
| Barcelona | random | high | 30 | 2251.7 | 115.4 | [2212.6, 2293.1] | 0.3790 | 0.0191 | 5068.4 | 0.0% |
| Barcelona | random | extreme | 30 | 3282.1 | 155.5 | [3238.7, 3347.1] | 0.4024 | 0.0128 | 6457.8 | 0.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Barcelona | ppo_coop_ideal | low | 4.92 | 2.156 |
| Barcelona | ppo_coop_ideal | mid | 11.92 | 5.222 |
| Barcelona | ppo_coop_ideal | mid_high | 14.71 | 6.446 |
| Barcelona | ppo_coop_ideal | high | 25.12 | 11.003 |
| Barcelona | ppo_coop_ideal | extreme | 32.50 | 14.238 |
| Barcelona | ppo_coop_chaos | low | 4.95 | 2.170 |
| Barcelona | ppo_coop_chaos | mid | 11.23 | 4.922 |
| Barcelona | ppo_coop_chaos | mid_high | 14.39 | 6.303 |
| Barcelona | ppo_coop_chaos | high | 24.61 | 10.782 |
| Barcelona | ppo_coop_chaos | extreme | 32.26 | 14.134 |
| Barcelona | ppo_chaos | low | 6.11 | 2.678 |
| Barcelona | ppo_chaos | mid | 12.88 | 5.641 |
| Barcelona | ppo_chaos | mid_high | 15.74 | 6.895 |
| Barcelona | ppo_chaos | high | 26.71 | 11.703 |
| Barcelona | ppo_chaos | extreme | 33.32 | 14.598 |
| Barcelona | fixed_time_opt | low | 2.99 | 1.308 |
| Barcelona | fixed_time_opt | mid | 9.23 | 4.044 |
| Barcelona | fixed_time_opt | mid_high | 14.51 | 6.358 |
| Barcelona | fixed_time_opt | high | 24.40 | 10.691 |
| Barcelona | fixed_time_opt | extreme | 32.76 | 14.353 |
| Barcelona | random | low | 2.57 | 1.126 |
| Barcelona | random | mid | 9.39 | 4.113 |
| Barcelona | random | mid_high | 14.02 | 6.142 |
| Barcelona | random | high | 23.02 | 10.084 |
| Barcelona | random | extreme | 30.94 | 13.556 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|
| Barcelona | low | Delay | 452.0 | 0.9823 | ns | -0.004 | negligible |
| Barcelona | low | Gini | 250.0 | 0.0032 | ** | 0.444 | medium |
| Barcelona | low | CVaR90 | 469.0 | 0.7845 | ns | -0.042 | negligible |
| Barcelona | mid | Delay | 337.0 | 0.0963 | ns | 0.251 | small |
| Barcelona | mid | Gini | 368.0 | 0.2282 | ns | 0.182 | small |
| Barcelona | mid | CVaR90 | 334.0 | 0.0877 | ns | 0.258 | small |
| Barcelona | mid_high | Delay | 459.0 | 0.9000 | ns | -0.020 | negligible |
| Barcelona | mid_high | Gini | 460.0 | 0.8883 | ns | -0.022 | negligible |
| Barcelona | mid_high | CVaR90 | 477.0 | 0.6952 | ns | -0.060 | negligible |
| Barcelona | high | Delay | 398.0 | 0.4464 | ns | 0.116 | small |
| Barcelona | high | Gini | 456.0 | 0.9352 | ns | -0.013 | negligible |
| Barcelona | high | CVaR90 | 501.0 | 0.4553 | ns | -0.113 | small |
| Barcelona | extreme | Delay | 428.0 | 0.7506 | ns | 0.049 | negligible |
| Barcelona | extreme | Gini | 626.0 | 0.0095 | ** | -0.391 | medium |
| Barcelona | extreme | CVaR90 | 400.0 | 0.4643 | ns | 0.111 | small |

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
| Barcelona | low | 118.3 | 0.0000 | *** |
| Barcelona | mid | 41.3 | 0.0000 | *** |
| Barcelona | mid_high | 80.4 | 0.0000 | *** |
| Barcelona | high | 45.1 | 0.0000 | *** |
| Barcelona | extreme | 38.5 | 0.0000 | *** |

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|
| Barcelona | low | ppo_coop_ideal | ppo_coop_chaos | 0.9823 | 1.0000 | ns |
| Barcelona | low | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | low | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Barcelona | low | fixed_time_opt | random | 0.1055 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_ideal | ppo_coop_chaos | 0.0963 | 0.9626 | ns |
| Barcelona | mid | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | mid | ppo_coop_ideal | fixed_time_opt | 0.2905 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_ideal | random | 0.5793 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | mid | ppo_coop_chaos | fixed_time_opt | 0.8187 | 1.0000 | ns |
| Barcelona | mid | ppo_coop_chaos | random | 0.6309 | 1.0000 | ns |
| Barcelona | mid | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | mid | ppo_chaos | random | 0.0000 | 0.0004 | *** |
| Barcelona | mid | fixed_time_opt | random | 0.6520 | 1.0000 | ns |
| Barcelona | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.9000 | 1.0000 | ns |
| Barcelona | mid_high | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | mid_high | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | mid_high | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| Barcelona | mid_high | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Barcelona | mid_high | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | mid_high | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Barcelona | mid_high | ppo_chaos | fixed_time_opt | 0.0029 | 0.0289 | * |
| Barcelona | mid_high | ppo_chaos | random | 0.6735 | 1.0000 | ns |
| Barcelona | mid_high | fixed_time_opt | random | 0.0303 | 0.3032 | ns |
| Barcelona | high | ppo_coop_ideal | ppo_coop_chaos | 0.4464 | 1.0000 | ns |
| Barcelona | high | ppo_coop_ideal | ppo_chaos | 0.0003 | 0.0034 | ** |
| Barcelona | high | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | high | ppo_coop_ideal | random | 0.5997 | 1.0000 | ns |
| Barcelona | high | ppo_coop_chaos | ppo_chaos | 0.0001 | 0.0010 | ** |
| Barcelona | high | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Barcelona | high | ppo_coop_chaos | random | 0.1580 | 1.0000 | ns |
| Barcelona | high | ppo_chaos | fixed_time_opt | 0.1188 | 1.0000 | ns |
| Barcelona | high | ppo_chaos | random | 0.0012 | 0.0117 | * |
| Barcelona | high | fixed_time_opt | random | 0.0000 | 0.0001 | *** |
| Barcelona | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.7506 | 1.0000 | ns |
| Barcelona | extreme | ppo_coop_ideal | ppo_chaos | 0.8073 | 1.0000 | ns |
| Barcelona | extreme | ppo_coop_ideal | fixed_time_opt | 0.0002 | 0.0020 | ** |
| Barcelona | extreme | ppo_coop_ideal | random | 0.0015 | 0.0152 | * |
| Barcelona | extreme | ppo_coop_chaos | ppo_chaos | 0.9587 | 1.0000 | ns |
| Barcelona | extreme | ppo_coop_chaos | fixed_time_opt | 0.0002 | 0.0016 | ** |
| Barcelona | extreme | ppo_coop_chaos | random | 0.0053 | 0.0532 | ns |
| Barcelona | extreme | ppo_chaos | fixed_time_opt | 0.0004 | 0.0045 | ** |
| Barcelona | extreme | ppo_chaos | random | 0.0076 | 0.0762 | ns |
| Barcelona | extreme | fixed_time_opt | random | 0.0000 | 0.0000 | *** |

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| Barcelona | ppo_coop_ideal | 0.980 | 0.0000 | *** |
| Barcelona | ppo_coop_chaos | 0.980 | 0.0000 | *** |
| Barcelona | ppo_chaos | 0.980 | 0.0000 | *** |
| Barcelona | fixed_time_opt | 0.980 | 0.0000 | *** |
| Barcelona | random | 0.980 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
