import os
import json
import glob
import pandas as pd

def parse_resco_results():
    results_dir = os.path.join("..", "baselines", "RESCO", "results")
    # Buscar todos los unified_metrics_ep1.json en los subdirectorios
    json_files = glob.glob(os.path.join(results_dir, "**", "unified_metrics_ep1.json"), recursive=True)
    
    if not json_files:
        print("No se encontraron resultados JSON (unified_metrics) en la carpeta de RESCO.")
        return
        
    data = []
    
    for jf in json_files:
        with open(jf, "r") as f:
            try:
                res = json.load(f)
            except:
                continue
        
        algo = res.get("algorithm", "Unknown").upper()
        scenario = res.get("scenario", "Unknown").upper()
        
        row = {
            "Algoritmo": algo,
            "Escenario": scenario,
            "Recompensa (RL)": res.get("episode_reward", "N/A"),
            "Cola Media": res.get("avg_queue_length", "N/A"),
            "Throughput": res.get("throughput_total", "N/A"),
            "Choques/Teleports": res.get("teleports_total", 0),
            "Equidad (Gini)": res.get("gini_temporal", "N/A"),
            "Riesgo (CVaR95)": res.get("cvar95_queue", "N/A"),
            "Espera Total": res.get("cumulative_wait_proxy", "N/A")
        }
        data.append(row)
        
    if not data:
        print("No se extrajeron datos.")
        return
        
    df = pd.DataFrame(data)
    
    # Agrupar si hay múltiples ejecuciones del mismo algoritmo (tomar el último)
    df = df.drop_duplicates(subset=['Algoritmo', 'Escenario'], keep='last')
    
    print("\n" + "="*80)
    print(" RESULTADOS FASE 2: SOTA vs LATAM CHAOS")
    print("="*80)
    
    # Sort for nice display
    df = df.sort_values(by=["Algoritmo", "Escenario"])
    
    # Mostrar la tabla sin dependencias externas
    print(df.to_string(index=False))
    print("="*80)
    
if __name__ == "__main__":
    parse_resco_results()
