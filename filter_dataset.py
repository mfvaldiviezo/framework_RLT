import pandas as pd

df = pd.read_csv(r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_results.csv')

ciudades_reales = ['Barcelona', 'Bogota', 'Quito', 'CDMX', 'Madrid', 'Berlin']
df_filtrado = df[df['city'].isin(ciudades_reales)]

print(f"Original: {len(df)} filas")
print(f"Filtrado (solo ciudades): {len(df_filtrado)} filas")
print(f"Eliminadas (Unknown): {len(df) - len(df_filtrado)} filas")
print()
print(f"Ciudades: {sorted(df_filtrado['city'].unique())}")
print(f"Chaos levels: {sorted(df_filtrado['chaos_level'].unique())}")
print(f"Modelos: {sorted(df_filtrado['model'].unique())}")

output_path = r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_results_filtrado.csv'
df_filtrado.to_csv(output_path, index=False)
print(f"\nGuardado en: {output_path}")
