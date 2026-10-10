# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-14
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Quito | ppo_chaos | low | 30 | 363.6 | 136.2 | [293.8, 389.3] | 0.1843 | 0.0332 | 1038.7 | 0.0% |
| Quito | ppo_chaos | mid | 30 | 2194.6 | 459.5 | [2035.6, 2353.2] | 0.4070 | 0.0382 | 6511.5 | 0.0% |
| Quito | ppo_chaos | mid_high | 30 | 3266.6 | 540.1 | [2969.6, 3384.4] | 0.4423 | 0.0247 | 8577.0 | 0.0% |
| Quito | ppo_chaos | high | 30 | 4247.8 | 1068.9 | [4026.4, 4673.2] | 0.5161 | 0.0321 | 9915.7 | 26.7% |
| Quito | ppo_chaos | extreme | 30 | 5738.2 | 1891.7 | [5311.9, 6644.7] | 0.5972 | 0.0233 | 14439.8 | 83.3% |
| Bogota | ppo_chaos | low | 30 | 43.6 | 2.7 | [42.7, 45.0] | 0.2345 | 0.0044 | 108.8 | 0.0% |
| Bogota | ppo_chaos | mid | 30 | 2184.1 | 1738.4 | [1267.6, 2458.9] | 0.3803 | 0.0118 | 8489.3 | 0.0% |
| Bogota | ppo_chaos | mid_high | 30 | 35010.4 | 9786.4 | [30325.8, 38286.5] | 0.5242 | 0.0199 | 104517.1 | 100.0% |
| Bogota | ppo_chaos | high | 30 | 85089.2 | 12387.5 | [81764.9, 87667.8] | 0.5913 | 0.0131 | 196898.4 | 100.0% |
| Bogota | ppo_chaos | extreme | 30 | 145653.8 | 17649.1 | [139326.7, 153715.2] | 0.5720 | 0.0130 | 291047.5 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Quito | ppo_chaos | low | 4.57 | 2.003 |
| Quito | ppo_chaos | mid | 22.01 | 9.642 |
| Quito | ppo_chaos | mid_high | 30.01 | 13.149 |
| Quito | ppo_chaos | high | 40.72 | 17.839 |
| Quito | ppo_chaos | extreme | 52.47 | 22.986 |
| Bogota | ppo_chaos | low | 24.76 | 10.849 |
| Bogota | ppo_chaos | mid | 90.90 | 39.821 |
| Bogota | ppo_chaos | mid_high | 238.44 | 104.459 |
| Bogota | ppo_chaos | high | 350.40 | 153.508 |
| Bogota | ppo_chaos | extreme | 455.48 | 199.546 |

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
| Quito | ppo_chaos | 0.962 | 0.0000 | *** |
| Bogota | ppo_chaos | 0.980 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
