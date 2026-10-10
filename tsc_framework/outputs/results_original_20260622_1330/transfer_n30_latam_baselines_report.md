# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-16
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Quito | fixed_time_opt | low | 30 | 286.6 | 226.4 | [213.4, 311.0] | 0.0984 | 0.0428 | 1170.8 | 0.0% |
| Quito | fixed_time_opt | mid | 30 | 1849.7 | 414.6 | [1708.9, 1949.3] | 0.2859 | 0.0202 | 5849.9 | 0.0% |
| Quito | fixed_time_opt | mid_high | 30 | 2493.1 | 478.7 | [2374.8, 2656.1] | 0.3327 | 0.0287 | 6879.3 | 0.0% |
| Quito | fixed_time_opt | high | 30 | 3963.4 | 953.6 | [3719.1, 4158.1] | 0.4283 | 0.0259 | 10078.1 | 10.0% |
| Quito | fixed_time_opt | extreme | 30 | 5100.7 | 1769.4 | [4731.4, 5665.1] | 0.5348 | 0.0307 | 12218.5 | 60.0% |
| Quito | random | low | 30 | 160.2 | 150.4 | [132.7, 218.6] | 0.0876 | 0.0224 | 811.1 | 0.0% |
| Quito | random | mid | 30 | 1761.0 | 865.4 | [1453.3, 1924.5] | 0.2786 | 0.0407 | 5071.0 | 0.0% |
| Quito | random | mid_high | 30 | 2605.0 | 569.1 | [2471.8, 2737.7] | 0.3458 | 0.0519 | 7764.3 | 0.0% |
| Quito | random | high | 30 | 4058.4 | 1004.8 | [3723.0, 4449.2] | 0.4256 | 0.0259 | 11840.2 | 10.0% |
| Quito | random | extreme | 30 | 5988.8 | 1383.5 | [5471.4, 6527.2] | 0.5337 | 0.0174 | 13671.9 | 90.0% |
| Bogota | fixed_time_opt | low | 30 | 73.0 | 6.5 | [70.9, 75.7] | 0.2630 | 0.0065 | 175.1 | 0.0% |
| Bogota | fixed_time_opt | mid | 30 | 1480.9 | 929.5 | [1041.4, 1709.5] | 0.3910 | 0.0084 | 6910.9 | 3.3% |
| Bogota | fixed_time_opt | mid_high | 30 | 25818.5 | 13765.4 | [19587.2, 30368.3] | 0.5151 | 0.0198 | 86003.4 | 100.0% |
| Bogota | fixed_time_opt | high | 30 | 78760.3 | 9282.2 | [75935.0, 81253.0] | 0.5848 | 0.0152 | 180228.5 | 100.0% |
| Bogota | fixed_time_opt | extreme | 30 | 132300.1 | 16835.3 | [129724.1, 139035.4] | 0.5613 | 0.0201 | 268550.8 | 100.0% |
| Bogota | random | low | 30 | 123.7 | 29.6 | [112.3, 135.1] | 0.2906 | 0.0072 | 378.5 | 0.0% |
| Bogota | random | mid | 30 | 1149.3 | 1628.6 | [863.7, 1608.2] | 0.4108 | 0.0143 | 6555.4 | 3.3% |
| Bogota | random | mid_high | 30 | 23280.9 | 8137.9 | [21006.1, 25827.0] | 0.5334 | 0.0237 | 79965.1 | 100.0% |
| Bogota | random | high | 30 | 86567.8 | 17721.3 | [78402.8, 91272.5] | 0.5974 | 0.0133 | 198336.8 | 100.0% |
| Bogota | random | extreme | 30 | 145799.0 | 22847.3 | [135764.8, 153715.9] | 0.5730 | 0.0122 | 296765.6 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Quito | fixed_time_opt | low | 3.55 | 1.554 |
| Quito | fixed_time_opt | mid | 17.55 | 7.689 |
| Quito | fixed_time_opt | mid_high | 23.95 | 10.493 |
| Quito | fixed_time_opt | high | 37.28 | 16.330 |
| Quito | fixed_time_opt | extreme | 46.70 | 20.458 |
| Quito | random | low | 2.55 | 1.119 |
| Quito | random | mid | 16.89 | 7.400 |
| Quito | random | mid_high | 24.68 | 10.814 |
| Quito | random | high | 36.89 | 16.161 |
| Quito | random | extreme | 48.92 | 21.434 |
| Bogota | fixed_time_opt | low | 26.07 | 11.421 |
| Bogota | fixed_time_opt | mid | 82.68 | 36.221 |
| Bogota | fixed_time_opt | mid_high | 224.51 | 98.358 |
| Bogota | fixed_time_opt | high | 355.00 | 155.527 |
| Bogota | fixed_time_opt | extreme | 455.67 | 199.629 |
| Bogota | random | low | 27.65 | 12.114 |
| Bogota | random | mid | 87.09 | 38.156 |
| Bogota | random | mid_high | 233.51 | 102.298 |
| Bogota | random | high | 358.33 | 156.984 |
| Bogota | random | extreme | 451.20 | 197.669 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
| Quito | low | 602.0 | 0.0251 | * |
| Quito | mid | 563.0 | 0.0963 | ns |
| Quito | mid_high | 389.0 | 0.3711 | ns |
| Quito | high | 421.0 | 0.6735 | ns |
| Quito | extreme | 279.0 | 0.0117 | * |
| Bogota | low | 201.0 | 0.0002 | *** |
| Bogota | mid | 486.0 | 0.5997 | ns |
| Bogota | mid_high | 494.0 | 0.5201 | ns |
| Bogota | high | 313.0 | 0.0436 | * |
| Bogota | extreme | 314.0 | 0.0451 | * |

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|
| Quito | low | fixed_time_opt | random | 0.0251 | 0.0251 | * |
| Quito | mid | fixed_time_opt | random | 0.0963 | 0.0963 | ns |
| Quito | mid_high | fixed_time_opt | random | 0.3711 | 0.3711 | ns |
| Quito | high | fixed_time_opt | random | 0.6735 | 0.6735 | ns |
| Quito | extreme | fixed_time_opt | random | 0.0117 | 0.0117 | * |
| Bogota | low | fixed_time_opt | random | 0.0002 | 0.0002 | *** |
| Bogota | mid | fixed_time_opt | random | 0.5997 | 0.5997 | ns |
| Bogota | mid_high | fixed_time_opt | random | 0.5201 | 0.5201 | ns |
| Bogota | high | fixed_time_opt | random | 0.0436 | 0.0436 | * |
| Bogota | extreme | fixed_time_opt | random | 0.0451 | 0.0451 | * |

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| Quito | fixed_time_opt | 0.949 | 0.0000 | *** |
| Quito | random | 0.966 | 0.0000 | *** |
| Bogota | fixed_time_opt | 0.979 | 0.0000 | *** |
| Bogota | random | 0.979 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
