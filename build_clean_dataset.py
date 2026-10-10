import pandas as pd

df = pd.read_csv(r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_results.csv')

# Keep only real cities
ciudades_reales = ['Barcelona', 'Bogota', 'Quito', 'CDMX', 'Madrid', 'Berlin']
df = df[df['city'].isin(ciudades_reales)]

# Remove chaos='unknown' (ruido) and model='fixed_time' (solo 12 filas)
df = df[df['chaos_level'] != 'unknown']
df = df[df['model'] != 'fixed_time']

print(f"Filas: {len(df)}")
print(f"Ciudades: {sorted(df['city'].unique())}")
print(f"Chaos levels: {sorted(df['chaos_level'].unique())}")
print(f"Modelos: {sorted(df['model'].unique())}")
print(f"Episodios: {sorted(df['episode'].unique())}")
print()

# Verify balance
expected = 6 * 5 * len(df['model'].unique()) * 30
print(f"Esperado: 6 ciudades x 5 chaos x {len(df['model'].unique())} modelos x 30 episodios = {expected}")
print(f"Real: {len(df)}")
print(f"Diferencia: {expected - len(df)}")

# Check for any remaining gaps
import itertools
for city in sorted(df['city'].unique()):
    for chaos in sorted(df['chaos_level'].unique()):
        for model in sorted(df['model'].unique()):
            count = len(df[(df['city']==city) & (df['chaos_level']==chaos) & (df['model']==model)])
            if count != 30:
                print(f"  GAP: {city} | {chaos} | {model} -> {count} episodios")

if expected == len(df):
    print("\nDataset perfectamente balanceado!")
else:
    print(f"\nFaltan {expected - len(df)} registros")

output_path = r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_results_clean.csv'
df.to_csv(output_path, index=False)
print(f"\nGuardado en: {output_path}")
