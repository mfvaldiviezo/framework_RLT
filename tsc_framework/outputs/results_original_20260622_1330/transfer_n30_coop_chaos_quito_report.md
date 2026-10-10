# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-16
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Quito | ppo_coop_chaos | low | 30 | 388.9 | 134.6 | [365.1, 468.8] | 0.2006 | 0.0257 | 1126.9 | 0.0% |
| Quito | ppo_coop_chaos | mid | 30 | 2101.8 | 340.9 | [1942.3, 2207.3] | 0.3577 | 0.0289 | 6019.1 | 0.0% |
| Quito | ppo_coop_chaos | mid_high | 30 | 2806.8 | 405.5 | [2611.8, 2888.8] | 0.4084 | 0.0252 | 7412.2 | 0.0% |
| Quito | ppo_coop_chaos | high | 30 | 4149.7 | 873.0 | [3838.6, 4494.8] | 0.4796 | 0.0275 | 10631.8 | 20.0% |
| Quito | ppo_coop_chaos | extreme | 30 | 5891.1 | 1173.1 | [5531.4, 6347.6] | 0.5852 | 0.0223 | 13430.2 | 90.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Quito | ppo_coop_chaos | low | 4.74 | 2.075 |
| Quito | ppo_coop_chaos | mid | 20.35 | 8.913 |
| Quito | ppo_coop_chaos | mid_high | 26.65 | 11.677 |
| Quito | ppo_coop_chaos | high | 39.07 | 17.115 |
| Quito | ppo_coop_chaos | extreme | 51.29 | 22.469 |

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

### Comparaciones Post-hoc con Correccion de Bonferroni (delay_mean)

| Ciudad | Caos | Modelo A | Modelo B | p-raw | p-adj | Signif. |
|---|---|---|---|---|---|---|

## Tabla 5: Correlaciones de Spearman (Nivel de Caos vs Delay Promedio)

| Ciudad | Modelo | Spearman rho | p-valor | Signif. |
|---|---|---|---|---|
| Quito | ppo_coop_chaos | 0.963 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
