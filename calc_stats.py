import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import kendalltau, ks_2samp

ROOT = Path(r"c:\Proyecto_Tesis_Final_V1\traffic_project")
sys.path.insert(0, str(ROOT))

try:
    from tsc_framework.src.copulas.vine_generator import load_joint_data
except ImportError:
    print("Error importando load_joint_data")
    sys.exit(1)

def main():
    # 1. Cargar datos empíricos (joint data)
    print("Cargando datos empíricos...")
    empirical_df = load_joint_data(random_state=42)
    
    # 2. Cargar escenarios simulados
    sim_file = ROOT / "tsc_framework" / "data" / "processed" / "stress_scenarios.csv"
    if not sim_file.exists():
        print(f"No se encontró: {sim_file}")
        sys.exit(1)
    
    print("Cargando escenarios simulados...")
    sim_df = pd.read_csv(sim_file)
    
    variables = ['demand', 'accel_magnitude', 'jerk']
    
    # Asegurar que ambos tengan las mismas columnas
    emp_data = empirical_df[variables]
    sim_data = sim_df[variables]
    
    print("\n--- RESULTADOS KENDALL TAU ---")
    pairs = [('demand', 'accel_magnitude'), ('demand', 'jerk'), ('accel_magnitude', 'jerk')]
    tau_results = []
    for var1, var2 in pairs:
        tau_emp, _ = kendalltau(emp_data[var1], emp_data[var2])
        tau_sim, _ = kendalltau(sim_data[var1], sim_data[var2])
        diff = abs(tau_emp - tau_sim)
        tau_results.append(f"{var1} vs {var2}: Empírico={tau_emp:.4f}, Simulado={tau_sim:.4f} (Dif={diff:.4f})")
        print(tau_results[-1])
        
    print("\n--- RESULTADOS PRUEBA KS (Kolmogorov-Smirnov) ---")
    ks_results = []
    for var in variables:
        ks_stat, p_val = ks_2samp(emp_data[var], sim_data[var])
        # Un KS-stat cercano a 0 indica que las distribuciones son muy similares.
        # En bootstrap/copulas sintéticas a veces el p_val es bajo por la cantidad de muestras,
        # pero el ks_stat es la métrica de distancia de ECDF.
        ks_results.append(f"{var}: KS-Stat={ks_stat:.4f}, p-value={p_val:.4e}")
        print(ks_results[-1])
        
    print("\nVALORES RECOMENDADOS PARA LA TABLA:")
    # Promedio de las diferencias de Kendall Tau
    avg_diff_tau = np.mean([abs(kendalltau(emp_data[v1], emp_data[v2])[0] - kendalltau(sim_data[v1], sim_data[v2])[0]) for v1, v2 in pairs])
    print(f"Kendall Tau (Diferencia Media Absoluta): {avg_diff_tau:.4f} (Valores cercanos a 0 indican preservación casi perfecta de dependencia)")
    
    # Máximo estadístico KS
    max_ks = max([ks_2samp(emp_data[var], sim_data[var]).statistic for var in variables])
    print(f"Prueba KS (Estadístico Máximo): {max_ks:.4f} (Valores cercanos a 0 indican alta fidelidad en los márgenes)")

if __name__ == "__main__":
    main()
