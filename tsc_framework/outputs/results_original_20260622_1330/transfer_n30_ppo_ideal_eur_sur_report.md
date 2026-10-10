# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-15
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Madrid | ppo_ideal | low | 30 | 4.1 | 0.5 | [4.0, 4.3] | 0.0492 | 0.0031 | 19.6 | 0.0% |
| Madrid | ppo_ideal | mid | 30 | 3615.2 | 303.9 | [3468.8, 3678.6] | 0.1388 | 0.0116 | 8382.5 | 0.0% |
| Madrid | ppo_ideal | mid_high | 30 | 5249.6 | 583.9 | [5037.7, 5441.0] | 0.1551 | 0.0094 | 11502.8 | 66.7% |
| Madrid | ppo_ideal | high | 30 | 9201.4 | 541.6 | [8967.3, 9291.5] | 0.1629 | 0.0139 | 17000.5 | 100.0% |
| Madrid | ppo_ideal | extreme | 30 | 10808.1 | 517.6 | [10653.1, 10971.0] | 0.1744 | 0.0185 | 18324.8 | 100.0% |
| Barcelona | ppo_ideal | low | 30 | 101.7 | 28.9 | [91.2, 114.0] | 0.1849 | 0.0115 | 372.8 | 0.0% |
| Barcelona | ppo_ideal | mid | 30 | 698.4 | 98.8 | [664.8, 723.9] | 0.2952 | 0.0206 | 1639.7 | 0.0% |
| Barcelona | ppo_ideal | mid_high | 30 | 1333.8 | 219.7 | [1234.8, 1382.4] | 0.3613 | 0.0128 | 3271.9 | 0.0% |
| Barcelona | ppo_ideal | high | 30 | 2542.2 | 186.7 | [2501.0, 2617.7] | 0.4120 | 0.0157 | 5794.1 | 0.0% |
| Barcelona | ppo_ideal | extreme | 30 | 3709.5 | 257.0 | [3665.2, 3797.5] | 0.4229 | 0.0095 | 7102.5 | 0.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Madrid | ppo_ideal | low | 5.72 | 2.504 |
| Madrid | ppo_ideal | mid | 35.75 | 15.663 |
| Madrid | ppo_ideal | mid_high | 50.70 | 22.213 |
| Madrid | ppo_ideal | high | 80.69 | 35.348 |
| Madrid | ppo_ideal | extreme | 91.00 | 39.869 |
| Barcelona | ppo_ideal | low | 4.76 | 2.085 |
| Barcelona | ppo_ideal | mid | 11.54 | 5.058 |
| Barcelona | ppo_ideal | mid_high | 16.65 | 7.295 |
| Barcelona | ppo_ideal | high | 26.37 | 11.552 |
| Barcelona | ppo_ideal | extreme | 34.60 | 15.157 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
| Madrid | low | N/A | N/A | N/A |
| Madrid | mid | N/A | N/A | N/A |
| Madrid | mid_high | N/A | N/A | N/A |
| Madrid | high | N/A | N/A | N/A |
| Madrid | extreme | N/A | N/A | N/A |
| Barcelona | low | N/A | N/A | N/A |
| Barcelona | mid | N/A | N/A | N/A |
| Barcelona | mid_high | N/A | N/A | N/A |
| Barcelona | high | N/A | N/A | N/A |
| Barcelona | extreme | N/A | N/A | N/A |

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| Madrid | ppo_ideal | 0.978 | 0.0000 | *** |
| Barcelona | ppo_ideal | 0.980 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
