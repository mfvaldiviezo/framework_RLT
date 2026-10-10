# INFORME DE EVALUACION DE TRANSFERENCIA ZERO-SHOT
Fecha: 2026-06-16
Configuracion del experimento: n=30 episodios por combinacion de modelo, ciudad y nivel de caos.
Estadistico central: Mediana. Medida de dispersion: Rango Intercuartilico (IQR).
Tests estadisticos aplicados: Mann-Whitney U bilateral, Kruskal-Wallis global con correccion post-hoc de Bonferroni, correlacion de Spearman.

---

## Tabla 1: Metricas de Desempeno por Ciudad, Modelo y Nivel de Caos (Mediana [IQR])

| Ciudad | Modelo | Caos | n | Delay Mediana (s) | Delay IQR (s) | Delay IC 95% | Gini Mediana | Gini IQR | CVaR90 Mediana (s) | Colapsos (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Quito | ppo_ideal | low | 30 | 222.8 | 118.8 | [179.7, 253.7] | 0.1286 | 0.0250 | 958.0 | 0.0% |
| Quito | ppo_ideal | mid | 30 | 1990.9 | 659.5 | [1793.7, 2067.6] | 0.3462 | 0.0344 | 5673.6 | 0.0% |
| Quito | ppo_ideal | mid_high | 30 | 2525.9 | 680.7 | [2309.0, 2729.4] | 0.3990 | 0.0279 | 7315.8 | 0.0% |
| Quito | ppo_ideal | high | 30 | 3931.0 | 1046.7 | [3721.8, 4513.7] | 0.4506 | 0.0247 | 10131.8 | 23.3% |
| Quito | ppo_ideal | extreme | 30 | 5154.0 | 1189.2 | [4583.5, 5489.4] | 0.5641 | 0.0256 | 12013.9 | 53.3% |
| Bogota | ppo_ideal | low | 30 | 43.3 | 2.8 | [42.6, 44.6] | 0.2336 | 0.0067 | 107.4 | 0.0% |
| Bogota | ppo_ideal | mid | 30 | 2143.0 | 2343.2 | [1351.2, 3164.8] | 0.3752 | 0.0054 | 9328.1 | 16.7% |
| Bogota | ppo_ideal | mid_high | 30 | 29029.8 | 12868.9 | [23679.9, 35378.0] | 0.5256 | 0.0130 | 96821.2 | 100.0% |
| Bogota | ppo_ideal | high | 30 | 81834.7 | 12392.0 | [76928.7, 86988.5] | 0.5922 | 0.0115 | 193072.8 | 100.0% |
| Bogota | ppo_ideal | extreme | 30 | 145151.5 | 22293.2 | [136409.3, 152152.0] | 0.5659 | 0.0122 | 298495.2 | 100.0% |

## Tabla 2: Metricas de Sostenibilidad y Emisiones (Mediana)

| Ciudad | Modelo | Caos | CO2 Total (kg) | Combustible Total (L) |
|---|---|---|---|---|
| Quito | ppo_ideal | low | 3.68 | 1.614 |
| Quito | ppo_ideal | mid | 19.98 | 8.754 |
| Quito | ppo_ideal | mid_high | 25.80 | 11.305 |
| Quito | ppo_ideal | high | 37.16 | 16.279 |
| Quito | ppo_ideal | extreme | 47.26 | 20.703 |
| Bogota | ppo_ideal | low | 24.64 | 10.796 |
| Bogota | ppo_ideal | mid | 88.25 | 38.662 |
| Bogota | ppo_ideal | mid_high | 235.59 | 103.210 |
| Bogota | ppo_ideal | high | 349.07 | 152.929 |
| Bogota | ppo_ideal | extreme | 455.90 | 199.730 |

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
| Quito | ppo_ideal | 0.936 | 0.0000 | *** |
| Bogota | ppo_ideal | 0.980 | 0.0000 | *** |

---

## Notas Metodologicas

1. **Coeficiente de Gini**: Mide la desigualdad en la distribucion de los tiempos de espera entre carriles controlados. Un valor cercano a 0 indica equidad perfecta, mientras que un valor cercano a 1 indica desigualdad maxima.
2. **CVaR al 90% (Valor en Riesgo Condicional)**: Representa el promedio del 10% peor de los tiempos de espera registrados durante el episodio, sirviendo como metrica robusta para evaluar la severidad de la congestion en eventos extremos.
3. **Intervalo de Confianza para la Mediana**: Calculado utilizando bootstrap percentil no parametrico con 1000 remuestreos deterministas. Este metodo no asume normalidad en los datos de entrada.
4. **Test de Mann-Whitney U**: Prueba no parametrica bilateral para evaluar si la distribucion de un modelo difiere significativamente de otro. El efecto r se calcula a partir de la correlacion rango-biserial.
5. **Test de Kruskal-Wallis**: Prueba no parametrica para comparar tres o mas grupos independientes. Las comparaciones post-hoc por pares se corrigen multiplicando los p-valores por el numero total de comparaciones posibles (Bonferroni).
6. **Correlacion de Spearman**: Evalua la relacion monotonica entre el nivel de caos operacional (codificado como ordinal 1 a 5) y el retraso promedio registrado en la simulacion.
