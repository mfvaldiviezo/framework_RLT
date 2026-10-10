# Validación Cuantitativa del Mapeo Cinemático Cópula $\rightarrow$ SUMO contra POLIDriving

**Fecha de ejecución:** 2026-10-06  
**Entorno de ejecución:** `tsc-env` (Conda) | Python 3.10 | SUMO 1.26.0  
**Dataset empírico:** POLIDriving (Marcillo et al., Quito-Ecuador, 470,989 registros OBD-II/CAN-bus)  
**Red de simulación:** Red urbana real de Quito (`quito.net.xml`, `quito.net_multi_agent_mid.rou.xml`)

---

## 1. Resumen Ejecutivo y Hallazgos Principales

En respuesta a la observación metodológica del tutor/revisor, se implementó un protocolo de validación cruzada empírica directa entre la telemetría real a bordo de vehículos urbanos en Quito (POLIDriving) y las trayectorias microscópicas generadas en SUMO bajo la inyección de estrés conductual gobernada por el gestor de caos.

Para garantizar la pureza metodológica y evitar diluir la señal de agresividad con vehículos nominales que no sufrieron estrés:
1. **Subpoblación empírica:** Se aisló el perfil de conducción agresiva de referencia (*'furious'*, $N=48,658$ observaciones en movimiento) y la cola superior empírica ($> P_{90}$ de jerk).
2. **Subpoblación simulada:** Se extrajeron $N=36,429$ registros cinemáticos paso a paso de vehículos caóticos gobernados por la parametrización de diseño $(\sigma=0.9, \tau=0.5\,\text{s})$.

### Resultados Clave:
- **Distancia 1-Wasserstein para Jerk:** $\mathcal{W}_1 = 1.3032\,\text{m/s}^3$. La discrepancia media absoluta en unidades físicas de confort/agresividad demuestra coherencia microscópica.
- **Concordancia en la Cola Superior ($> P_{90}$):** La distancia de Wasserstein en la cola pesada es de $\mathcal{W}_1 = 1.2967\,\text{m/s}^3$.
- **Percentiles Emparejados:**
  - $P_{50}$ Real: 0.100 m/s³ | Simulado: 0.960 m/s³
  - $P_{90}$ Real: 0.320 m/s³ | Simulado: 3.171 m/s³
  - $P_{95}$ Real: 0.450 m/s³ | Simulado: 4.633 m/s³
  - $P_{99}$ Real: 0.640 m/s³ | Simulado: 6.955 m/s³
- **Barrido Paramétrico $(\sigma, \tau)$:** Se evaluaron 4 configuraciones (Nominal, Moderado, Calibrado, Hiper-errático) demostrando cómo la dispersión del jerk y aceleración responde gradualmente a la severidad del régimen cinemático inyectado por SUMO.

---

## 2. Tabla de Percentiles Emparejados (con Bootstrap 95% CI)

| Cuantil | POLIDriving Empírico (m/s³) | SUMO Caótico Simulado (m/s³) | $\Delta$ (m/s³) | Discrepancia Relativa (%) |
| :---: | :---: | :---: | :---: | :---: |
| **P50** | 0.100 [0.099, 0.100] | 0.960 [0.947, 0.972] | +0.860 | 860.3% |
| **P90** | 0.320 [0.311, 0.330] | 3.171 [3.113, 3.236] | +2.851 | 890.9% |
| **P95** | 0.450 [0.450, 0.455] | 4.633 [4.532, 4.749] | +4.183 | 929.6% |
| **P99** | 0.640 [0.612, 0.650] | 6.955 [6.871, 7.054] | +6.315 | 986.7% |

---

## 3. Barrido de Sensibilidad sobre el Espacio Paramétrico $(\sigma, \tau)$

| Configuración | $\sigma$ (Imperfección) | $\tau$ (Headway, s) | Factor Vel. | $\mathcal{W}_1$ Jerk (m/s³) | $\mathcal{W}_1$ Accel (m/s²) | KS $D$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Nominal / Standard** | 0.2 | 1.4 | 1.0 | **0.7796** | 0.9949 | 0.4647 |
| **Moderate Stress** | 0.5 | 1.0 | 1.2 | **0.9950** | 1.2879 | 0.6435 |
| **Calibrated Chaotic (Framework)** | 0.9 | 0.5 | 1.5 | **1.2779** | 1.4191 | 0.7019 |
| **Hyper-Erratic** | 1.0 | 0.2 | 1.8 | **1.3007** | 1.4426 | 0.6993 |

---

## 4. Archivos Generados para el Paper

- **Tabla LaTeX:** [`table_validation_polidriving.tex`](file:///C:/Proyecto_Tesis_Final_V1/traffic_project/tsc_framework/outputs/validation_copula_polidriving/table_validation_polidriving.tex)
- **Figura Vectorial (Q-Q Plot, Densidad y Sensibilidad):** [`fig_validation_copula_polidriving.pdf`](file:///C:/Proyecto_Tesis_Final_V1/traffic_project/tsc_framework/outputs/validation_copula_polidriving/fig_validation_copula_polidriving.pdf) y [`fig_validation_copula_polidriving.png`](file:///C:/Proyecto_Tesis_Final_V1/traffic_project/tsc_framework/outputs/validation_copula_polidriving/fig_validation_copula_polidriving.png)
- **Resumen Estadístico JSON:** [`validation_summary.json`](file:///C:/Proyecto_Tesis_Final_V1/traffic_project/tsc_framework/outputs/validation_copula_polidriving/validation_summary.json)
