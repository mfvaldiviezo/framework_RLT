# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-06
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Berlin | ppo_coop_ideal | low | 30 | 39.2 | 94.9 | [33.1, 89.0] | 0.3512 | 0.0210 | 172.8 | 0.0% |
| Berlin | ppo_coop_ideal | mid | 30 | 1057.5 | 594.8 | [912.4, 1256.6] | 0.5580 | 0.0268 | 3244.1 | 3.3% |
| Berlin | ppo_coop_ideal | mid_high | 30 | 4389.4 | 2276.9 | [3995.4, 5769.1] | 0.5010 | 0.0160 | 11329.3 | 43.3% |
| Berlin | ppo_coop_ideal | high | 30 | 20033.4 | 3278.2 | [18418.3, 20598.1] | 0.5064 | 0.0168 | 38844.9 | 100.0% |
| Berlin | ppo_coop_ideal | extreme | 30 | 26950.1 | 2589.5 | [26403.4, 27862.4] | 0.4916 | 0.0131 | 44525.5 | 100.0% |
| Berlin | ppo_coop_chaos | low | 30 | 30.8 | 2.4 | [29.6, 31.6] | 0.3442 | 0.0112 | 100.2 | 0.0% |
| Berlin | ppo_coop_chaos | mid | 30 | 1636.6 | 2909.4 | [785.9, 2693.3] | 0.5741 | 0.0288 | 8307.8 | 6.7% |
| Berlin | ppo_coop_chaos | mid_high | 30 | 7686.4 | 3846.5 | [6590.7, 9310.6] | 0.5261 | 0.0218 | 19495.6 | 96.7% |
| Berlin | ppo_coop_chaos | high | 30 | 18320.4 | 2562.6 | [17216.8, 19089.3] | 0.5501 | 0.0156 | 34349.5 | 100.0% |
| Berlin | ppo_coop_chaos | extreme | 30 | 25877.5 | 2472.5 | [24859.4, 26594.8] | 0.5396 | 0.0177 | 45064.5 | 100.0% |
| Berlin | ppo_chaos | low | 30 | 3453.3 | 262.9 | [3294.4, 3507.7] | 0.4782 | 0.0098 | 9375.8 | 0.0% |
| Berlin | ppo_chaos | mid | 30 | 9009.1 | 1386.0 | [8580.0, 9576.1] | 0.4715 | 0.0070 | 19199.6 | 100.0% |
| Berlin | ppo_chaos | mid_high | 30 | 17357.5 | 3909.4 | [16312.9, 19149.7] | 0.4456 | 0.0127 | 35748.3 | 100.0% |
| Berlin | ppo_chaos | high | 30 | 27613.9 | 3191.6 | [25668.8, 28144.6] | 0.4247 | 0.0094 | 46069.5 | 100.0% |
| Berlin | ppo_chaos | extreme | 30 | 33781.0 | 2639.5 | [32705.6, 34739.8] | 0.4097 | 0.0115 | 53657.3 | 100.0% |
| Berlin | fixed_time_opt | low | 30 | 83.8 | 23.6 | [80.3, 94.9] | 0.3720 | 0.0071 | 320.2 | 0.0% |
| Berlin | fixed_time_opt | mid | 30 | 477.4 | 138.7 | [448.6, 518.3] | 0.5576 | 0.0150 | 1604.8 | 0.0% |
| Berlin | fixed_time_opt | mid_high | 30 | 6591.4 | 4036.9 | [5079.6, 7751.4] | 0.4773 | 0.0431 | 17474.6 | 66.7% |
| Berlin | fixed_time_opt | high | 30 | 17522.9 | 6820.1 | [16557.3, 21099.4] | 0.5013 | 0.0383 | 36907.5 | 100.0% |
| Berlin | fixed_time_opt | extreme | 30 | 25513.3 | 4156.9 | [23100.0, 26567.7] | 0.5263 | 0.0208 | 44240.9 | 100.0% |
| Berlin | random | low | 30 | 225.1 | 62.2 | [213.4, 248.6] | 0.4153 | 0.0123 | 881.7 | 0.0% |
| Berlin | random | mid | 30 | 485.5 | 437.0 | [437.2, 571.1] | 0.5721 | 0.0361 | 1460.8 | 3.3% |
| Berlin | random | mid_high | 30 | 4738.9 | 3087.1 | [4251.7, 5961.1] | 0.4995 | 0.0578 | 14351.9 | 40.0% |
| Berlin | random | high | 30 | 16638.9 | 3332.7 | [14823.0, 17521.3] | 0.5433 | 0.0169 | 35137.5 | 100.0% |
| Berlin | random | extreme | 30 | 23460.0 | 3134.8 | [21930.4, 24767.5] | 0.5518 | 0.0184 | 40964.2 | 100.0% |
| Madrid | ppo_coop_ideal | low | 30 | 4.7 | 0.4 | [4.6, 4.9] | 0.0514 | 0.0034 | 20.3 | 0.0% |
| Madrid | ppo_coop_ideal | mid | 30 | 3605.0 | 347.7 | [3484.8, 3752.3] | 0.1348 | 0.0075 | 8498.0 | 0.0% |
| Madrid | ppo_coop_ideal | mid_high | 30 | 5018.6 | 205.0 | [4920.8, 5077.3] | 0.1358 | 0.0134 | 11007.5 | 53.3% |
| Madrid | ppo_coop_ideal | high | 30 | 9123.3 | 679.3 | [8980.9, 9434.5] | 0.1553 | 0.0175 | 17668.0 | 100.0% |
| Madrid | ppo_coop_ideal | extreme | 30 | 10748.4 | 437.8 | [10538.6, 10883.4] | 0.1622 | 0.0206 | 18199.9 | 100.0% |
| Madrid | ppo_coop_chaos | low | 30 | 4.4 | 0.4 | [4.3, 4.5] | 0.0500 | 0.0025 | 19.9 | 0.0% |
| Madrid | ppo_coop_chaos | mid | 30 | 3524.9 | 286.2 | [3415.8, 3608.6] | 0.1365 | 0.0094 | 8076.4 | 0.0% |
| Madrid | ppo_coop_chaos | mid_high | 30 | 5068.0 | 255.4 | [4982.8, 5130.0] | 0.1483 | 0.0058 | 11295.6 | 60.0% |
| Madrid | ppo_coop_chaos | high | 30 | 9088.7 | 493.3 | [8918.3, 9263.6] | 0.1614 | 0.0121 | 17315.2 | 100.0% |
| Madrid | ppo_coop_chaos | extreme | 30 | 10612.9 | 615.7 | [10479.5, 10804.3] | 0.1700 | 0.0136 | 18095.7 | 100.0% |
| Madrid | ppo_chaos | low | 30 | 1796.2 | 88.1 | [1782.0, 1830.9] | 0.1072 | 0.0078 | 4610.6 | 0.0% |
| Madrid | ppo_chaos | mid | 30 | 3646.8 | 226.7 | [3573.3, 3722.1] | 0.1131 | 0.0083 | 8370.7 | 0.0% |
| Madrid | ppo_chaos | mid_high | 30 | 4962.2 | 396.7 | [4846.1, 5076.6] | 0.1244 | 0.0065 | 10786.3 | 46.7% |
| Madrid | ppo_chaos | high | 30 | 8799.2 | 428.8 | [8668.2, 8923.3] | 0.1522 | 0.0133 | 17167.5 | 100.0% |
| Madrid | ppo_chaos | extreme | 30 | 10733.9 | 570.8 | [10577.8, 10948.8] | 0.1674 | 0.0195 | 18132.4 | 100.0% |
| Madrid | fixed_time_opt | low | 30 | 6.2 | 0.9 | [6.0, 6.6] | 0.0576 | 0.0034 | 29.0 | 0.0% |
| Madrid | fixed_time_opt | mid | 30 | 3586.4 | 277.1 | [3476.5, 3659.1] | 0.1394 | 0.0105 | 8409.5 | 0.0% |
| Madrid | fixed_time_opt | mid_high | 30 | 5217.3 | 454.1 | [4949.0, 5298.8] | 0.1559 | 0.0089 | 11398.8 | 63.3% |
| Madrid | fixed_time_opt | high | 30 | 9299.7 | 504.4 | [9114.9, 9490.3] | 0.1619 | 0.0161 | 18117.3 | 100.0% |
| Madrid | fixed_time_opt | extreme | 30 | 10688.4 | 420.9 | [10543.9, 10899.7] | 0.1763 | 0.0238 | 18135.6 | 100.0% |
| Madrid | random | low | 30 | 6.7 | 0.7 | [6.4, 6.9] | 0.0552 | 0.0045 | 29.3 | 0.0% |
| Madrid | random | mid | 30 | 3675.0 | 269.5 | [3625.8, 3732.5] | 0.1367 | 0.0110 | 8776.8 | 0.0% |
| Madrid | random | mid_high | 30 | 5096.8 | 364.6 | [5026.0, 5170.2] | 0.1388 | 0.0065 | 11635.7 | 73.3% |
| Madrid | random | high | 30 | 9040.1 | 427.0 | [8987.7, 9261.8] | 0.1563 | 0.0135 | 17591.2 | 100.0% |
| Madrid | random | extreme | 30 | 10959.2 | 925.9 | [10820.5, 11467.0] | 0.1681 | 0.0234 | 19091.5 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Berlin | ppo_coop_ideal | low | 15.23 | 6.670 |
| Berlin | ppo_coop_ideal | mid | 65.17 | 28.552 |
| Berlin | ppo_coop_ideal | mid_high | 117.06 | 51.283 |
| Berlin | ppo_coop_ideal | high | 266.87 | 116.917 |
| Berlin | ppo_coop_ideal | extreme | 324.81 | 142.301 |
| Berlin | ppo_coop_chaos | low | 14.89 | 6.523 |
| Berlin | ppo_coop_chaos | mid | 68.18 | 29.867 |
| Berlin | ppo_coop_chaos | mid_high | 148.34 | 64.987 |
| Berlin | ppo_coop_chaos | high | 258.07 | 113.059 |
| Berlin | ppo_coop_chaos | extreme | 323.38 | 141.674 |
| Berlin | ppo_chaos | low | 66.84 | 29.284 |
| Berlin | ppo_chaos | mid | 129.85 | 56.889 |
| Berlin | ppo_chaos | mid_high | 205.53 | 90.041 |
| Berlin | ppo_chaos | high | 284.02 | 124.428 |
| Berlin | ppo_chaos | extreme | 332.09 | 145.490 |
| Berlin | fixed_time_opt | low | 16.63 | 7.284 |
| Berlin | fixed_time_opt | mid | 48.08 | 21.065 |
| Berlin | fixed_time_opt | mid_high | 130.60 | 57.217 |
| Berlin | fixed_time_opt | high | 253.10 | 110.884 |
| Berlin | fixed_time_opt | extreme | 321.29 | 140.757 |
| Berlin | random | low | 23.41 | 10.255 |
| Berlin | random | mid | 60.34 | 26.433 |
| Berlin | random | mid_high | 127.52 | 55.868 |
| Berlin | random | high | 253.22 | 110.934 |
| Berlin | random | extreme | 318.17 | 139.388 |
| Madrid | ppo_coop_ideal | low | 6.08 | 2.664 |
| Madrid | ppo_coop_ideal | mid | 36.10 | 15.813 |
| Madrid | ppo_coop_ideal | mid_high | 51.91 | 22.741 |
| Madrid | ppo_coop_ideal | high | 80.22 | 35.144 |
| Madrid | ppo_coop_ideal | extreme | 90.56 | 39.673 |
| Madrid | ppo_coop_chaos | low | 5.92 | 2.592 |
| Madrid | ppo_coop_chaos | mid | 35.58 | 15.588 |
| Madrid | ppo_coop_chaos | mid_high | 50.69 | 22.208 |
| Madrid | ppo_coop_chaos | high | 80.82 | 35.406 |
| Madrid | ppo_coop_chaos | extreme | 90.73 | 39.748 |
| Madrid | ppo_chaos | low | 25.83 | 11.315 |
| Madrid | ppo_chaos | mid | 44.07 | 19.306 |
| Madrid | ppo_chaos | mid_high | 55.72 | 24.411 |
| Madrid | ppo_chaos | high | 78.84 | 34.538 |
| Madrid | ppo_chaos | extreme | 90.69 | 39.730 |
| Madrid | fixed_time_opt | low | 6.06 | 2.653 |
| Madrid | fixed_time_opt | mid | 36.11 | 15.819 |
| Madrid | fixed_time_opt | mid_high | 51.23 | 22.445 |
| Madrid | fixed_time_opt | high | 80.71 | 35.361 |
| Madrid | fixed_time_opt | extreme | 91.17 | 39.943 |
| Madrid | random | low | 6.46 | 2.829 |
| Madrid | random | mid | 37.01 | 16.214 |
| Madrid | random | mid_high | 52.65 | 23.067 |
| Madrid | random | high | 80.14 | 35.110 |
| Madrid | random | extreme | 90.76 | 39.763 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|
| Berlin | low | Delay | 169.0 | 0.0000 | *** | 0.624 | large |
| Berlin | low | Gini | 252.0 | 0.0035 | ** | 0.440 | medium |
| Berlin | low | CVaR90 | 118.0 | 0.0000 | *** | 0.738 | large |
| Berlin | mid | Delay | 528.0 | 0.2519 | ns | -0.173 | small |
| Berlin | mid | Gini | 623.0 | 0.0108 | * | -0.384 | medium |
| Berlin | mid | CVaR90 | 572.0 | 0.0724 | ns | -0.271 | small |
| Berlin | mid_high | Delay | 699.0 | 0.0002 | *** | -0.553 | large |
| Berlin | mid_high | Gini | 807.0 | 0.0000 | *** | -0.793 | large |
| Berlin | mid_high | CVaR90 | 672.0 | 0.0011 | ** | -0.493 | medium |
| Berlin | high | Delay | 269.0 | 0.0076 | ** | 0.402 | medium |
| Berlin | high | Gini | 843.0 | 0.0000 | *** | -0.873 | large |
| Berlin | high | CVaR90 | 203.0 | 0.0003 | *** | 0.549 | large |
| Berlin | extreme | Delay | 307.0 | 0.0351 | * | 0.318 | medium |
| Berlin | extreme | Gini | 889.0 | 0.0000 | *** | -0.976 | large |
| Berlin | extreme | CVaR90 | 402.0 | 0.4825 | ns | 0.107 | small |
| Madrid | low | Delay | 202.0 | 0.0003 | *** | 0.551 | large |
| Madrid | low | Gini | 342.0 | 0.1120 | ns | 0.240 | small |
| Madrid | low | CVaR90 | 372.5 | 0.2549 | ns | 0.172 | small |
| Madrid | mid | Delay | 341.0 | 0.1087 | ns | 0.242 | small |
| Madrid | mid | Gini | 560.0 | 0.1055 | ns | -0.244 | small |
| Madrid | mid | CVaR90 | 319.0 | 0.0537 | ns | 0.291 | small |
| Madrid | mid_high | Delay | 518.0 | 0.3183 | ns | -0.151 | small |
| Madrid | mid_high | Gini | 808.0 | 0.0000 | *** | -0.796 | large |
| Madrid | mid_high | CVaR90 | 597.0 | 0.0303 | * | -0.327 | medium |
| Madrid | high | Delay | 414.0 | 0.5997 | ns | 0.080 | negligible |
| Madrid | high | Gini | 574.0 | 0.0679 | ns | -0.276 | small |
| Madrid | high | CVaR90 | 342.0 | 0.1120 | ns | 0.240 | small |
| Madrid | extreme | Delay | 424.0 | 0.7062 | ns | 0.058 | negligible |
| Madrid | extreme | Gini | 593.0 | 0.0351 | * | -0.318 | medium |
| Madrid | extreme | CVaR90 | 386.0 | 0.3478 | ns | 0.142 | small |

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
| Berlin | low | 128.4 | 0.0000 | *** |
| Berlin | mid | 97.5 | 0.0000 | *** |
| Berlin | mid_high | 82.8 | 0.0000 | *** |
| Berlin | high | 80.1 | 0.0000 | *** |
| Berlin | extreme | 85.2 | 0.0000 | *** |
| Madrid | low | 129.6 | 0.0000 | *** |
| Madrid | mid | 11.1 | 0.0259 | * |
| Madrid | mid_high | 7.8 | 0.0982 | ns |
| Madrid | high | 24.9 | 0.0001 | *** |
| Madrid | extreme | 7.8 | 0.0987 | ns |

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|
| Berlin | low | ppo_coop_ideal | ppo_coop_chaos | 0.0000 | 0.0003 | *** |
| Berlin | low | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_ideal | fixed_time_opt | 0.0224 | 0.2236 | ns |
| Berlin | low | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | low | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | low | fixed_time_opt | random | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_ideal | ppo_coop_chaos | 0.2519 | 1.0000 | ns |
| Berlin | mid | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_ideal | random | 0.0002 | 0.0018 | ** |
| Berlin | mid | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_coop_chaos | random | 0.0000 | 0.0001 | *** |
| Berlin | mid | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | mid | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | mid | fixed_time_opt | random | 0.9117 | 1.0000 | ns |
| Berlin | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.0002 | 0.0024 | ** |
| Berlin | mid_high | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid_high | ppo_coop_ideal | fixed_time_opt | 0.1809 | 1.0000 | ns |
| Berlin | mid_high | ppo_coop_ideal | random | 0.9117 | 1.0000 | ns |
| Berlin | mid_high | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | mid_high | ppo_coop_chaos | fixed_time_opt | 0.0207 | 0.2068 | ns |
| Berlin | mid_high | ppo_coop_chaos | random | 0.0003 | 0.0030 | ** |
| Berlin | mid_high | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | mid_high | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | mid_high | fixed_time_opt | random | 0.1188 | 1.0000 | ns |
| Berlin | high | ppo_coop_ideal | ppo_coop_chaos | 0.0076 | 0.0762 | ns |
| Berlin | high | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | high | ppo_coop_ideal | fixed_time_opt | 0.1413 | 1.0000 | ns |
| Berlin | high | ppo_coop_ideal | random | 0.0000 | 0.0001 | *** |
| Berlin | high | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | high | ppo_coop_chaos | fixed_time_opt | 0.6952 | 1.0000 | ns |
| Berlin | high | ppo_coop_chaos | random | 0.0037 | 0.0367 | * |
| Berlin | high | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | high | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | high | fixed_time_opt | random | 0.0095 | 0.0947 | ns |
| Berlin | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.0351 | 0.3514 | ns |
| Berlin | extreme | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | extreme | ppo_coop_ideal | fixed_time_opt | 0.0076 | 0.0762 | ns |
| Berlin | extreme | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| Berlin | extreme | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Berlin | extreme | ppo_coop_chaos | fixed_time_opt | 0.2707 | 1.0000 | ns |
| Berlin | extreme | ppo_coop_chaos | random | 0.0003 | 0.0027 | ** |
| Berlin | extreme | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Berlin | extreme | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Berlin | extreme | fixed_time_opt | random | 0.0261 | 0.2608 | ns |
| Madrid | low | ppo_coop_ideal | ppo_coop_chaos | 0.0003 | 0.0025 | ** |
| Madrid | low | ppo_coop_ideal | ppo_chaos | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_ideal | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_ideal | random | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_chaos | ppo_chaos | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_coop_chaos | random | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_chaos | fixed_time_opt | 0.0000 | 0.0000 | *** |
| Madrid | low | ppo_chaos | random | 0.0000 | 0.0000 | *** |
| Madrid | low | fixed_time_opt | random | 0.0444 | 0.4435 | ns |
| Madrid | mid | ppo_coop_ideal | ppo_coop_chaos | 0.1087 | 1.0000 | ns |
| Madrid | mid | ppo_coop_ideal | ppo_chaos | 0.3112 | 1.0000 | ns |
| Madrid | mid | ppo_coop_ideal | fixed_time_opt | 0.6309 | 1.0000 | ns |
| Madrid | mid | ppo_coop_ideal | random | 0.3183 | 1.0000 | ns |
| Madrid | mid | ppo_coop_chaos | ppo_chaos | 0.0053 | 0.0532 | ns |
| Madrid | mid | ppo_coop_chaos | fixed_time_opt | 0.2398 | 1.0000 | ns |
| Madrid | mid | ppo_coop_chaos | random | 0.0056 | 0.0557 | ns |
| Madrid | mid | ppo_chaos | fixed_time_opt | 0.0933 | 0.9334 | ns |
| Madrid | mid | ppo_chaos | random | 0.8883 | 1.0000 | ns |
| Madrid | mid | fixed_time_opt | random | 0.0993 | 0.9926 | ns |
| Madrid | mid_high | ppo_coop_ideal | ppo_coop_chaos | 0.3183 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_ideal | ppo_chaos | 0.5997 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_ideal | fixed_time_opt | 0.0327 | 0.3265 | ns |
| Madrid | mid_high | ppo_coop_ideal | random | 0.0798 | 0.7978 | ns |
| Madrid | mid_high | ppo_coop_chaos | ppo_chaos | 0.3042 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_chaos | fixed_time_opt | 0.1335 | 1.0000 | ns |
| Madrid | mid_high | ppo_coop_chaos | random | 0.4204 | 1.0000 | ns |
| Madrid | mid_high | ppo_chaos | fixed_time_opt | 0.0635 | 0.6353 | ns |
| Madrid | mid_high | ppo_chaos | random | 0.0785 | 0.7851 | ns |
| Madrid | mid_high | fixed_time_opt | random | 0.6735 | 1.0000 | ns |
| Madrid | high | ppo_coop_ideal | ppo_coop_chaos | 0.5997 | 1.0000 | ns |
| Madrid | high | ppo_coop_ideal | ppo_chaos | 0.0004 | 0.0040 | ** |
| Madrid | high | ppo_coop_ideal | fixed_time_opt | 0.3403 | 1.0000 | ns |
| Madrid | high | ppo_coop_ideal | random | 0.3255 | 1.0000 | ns |
| Madrid | high | ppo_coop_chaos | ppo_chaos | 0.0012 | 0.0124 | * |
| Madrid | high | ppo_coop_chaos | fixed_time_opt | 0.1154 | 1.0000 | ns |
| Madrid | high | ppo_coop_chaos | random | 0.5793 | 1.0000 | ns |
| Madrid | high | ppo_chaos | fixed_time_opt | 0.0000 | 0.0001 | *** |
| Madrid | high | ppo_chaos | random | 0.0038 | 0.0385 | * |
| Madrid | high | fixed_time_opt | random | 0.0242 | 0.2416 | ns |
| Madrid | extreme | ppo_coop_ideal | ppo_coop_chaos | 0.7062 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_ideal | ppo_chaos | 0.6100 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_ideal | fixed_time_opt | 0.8883 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_ideal | random | 0.0184 | 0.1837 | ns |
| Madrid | extreme | ppo_coop_chaos | ppo_chaos | 0.3403 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_chaos | fixed_time_opt | 0.6414 | 1.0000 | ns |
| Madrid | extreme | ppo_coop_chaos | random | 0.0261 | 0.2608 | ns |
| Madrid | extreme | ppo_chaos | fixed_time_opt | 0.6735 | 1.0000 | ns |
| Madrid | extreme | ppo_chaos | random | 0.0635 | 0.6353 | ns |
| Madrid | extreme | fixed_time_opt | random | 0.0555 | 0.5555 | ns |

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| Berlin | ppo_coop_ideal | 0.972 | 0.0000 | *** |
| Berlin | ppo_coop_chaos | 0.977 | 0.0000 | *** |
| Berlin | ppo_chaos | 0.976 | 0.0000 | *** |
| Berlin | fixed_time_opt | 0.966 | 0.0000 | *** |
| Berlin | random | 0.974 | 0.0000 | *** |
| Madrid | ppo_coop_ideal | 0.976 | 0.0000 | *** |
| Madrid | ppo_coop_chaos | 0.979 | 0.0000 | *** |
| Madrid | ppo_chaos | 0.980 | 0.0000 | *** |
| Madrid | fixed_time_opt | 0.978 | 0.0000 | *** |
| Madrid | random | 0.980 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
