# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-15
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Bogota | ppo_coop_chaos | low | 30 | 44.1 | 112.9 | [43.5, 45.2] | 0.2326 | 0.0058 | 109.5 | 0.0% |
| Bogota | ppo_coop_chaos | mid | 30 | 2033.7 | 2470.4 | [1029.0, 2528.2] | 0.3759 | 0.0131 | 8210.3 | 13.3% |
| Bogota | ppo_coop_chaos | mid_high | 30 | 30149.0 | 10346.5 | [24251.8, 32995.8] | 0.5266 | 0.0183 | 95438.9 | 100.0% |
| Bogota | ppo_coop_chaos | high | 30 | 79111.8 | 9938.6 | [75003.9, 82698.9] | 0.5791 | 0.0142 | 176630.2 | 100.0% |
| Bogota | ppo_coop_chaos | extreme | 30 | 146795.3 | 16816.3 | [139643.3, 151771.6] | 0.5601 | 0.0157 | 296626.9 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Bogota | ppo_coop_chaos | low | 24.64 | 10.792 |
| Bogota | ppo_coop_chaos | mid | 87.35 | 38.266 |
| Bogota | ppo_coop_chaos | mid_high | 240.21 | 105.235 |
| Bogota | ppo_coop_chaos | high | 347.40 | 152.197 |
| Bogota | ppo_coop_chaos | extreme | 458.98 | 201.079 |

## Tabla 3: Resultados de Mann-Whitney U (ppo_coop_chaos vs ppo_coop_ideal)

| Ciudad | Caos | Metrica | U stat | p-valor | Signif. | r (efecto) | Magnitud |
|---|---|---|---|---|---|---|---|

## Tabla 4: Resultados de Kruskal-Wallis y Comparaciones Post-hoc

### Pruebas Globales de Kruskal-Wallis

| Ciudad | Caos | H stat | p-valor | Signif. |
|---|---|---|---|---|
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
| Bogota | ppo_coop_chaos | 0.979 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
