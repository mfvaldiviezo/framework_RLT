import pandas as pd

raw = pd.read_csv(r'c:\Proyecto_Tesis_Final_V1\traffic_project\tsc_framework\outputs\results\master_results_clean.csv')

print("Quito: ppo_coop_ideal vs ppo_coop_chaos")
for model in ['ppo_coop_ideal', 'ppo_coop_chaos']:
    for chaos in ['low','mid','mid_high','high','extreme']:
        sub = raw[(raw['city']=='Quito') & (raw['model']==model) & (raw['chaos_level']==chaos)]
        if len(sub) > 0:
            print(f"  {model:>20s} {chaos:>9s}: delay_median={sub['delay_mean'].median():.0f}s")

print("\nDegradation (chaos vs ideal) in Quito:")
for chaos in ['low','mid','mid_high','high','extreme']:
    ideal = raw[(raw['city']=='Quito') & (raw['model']=='ppo_coop_ideal') & (raw['chaos_level']==chaos)]['delay_mean'].median()
    chaos_d = raw[(raw['city']=='Quito') & (raw['model']=='ppo_coop_chaos') & (raw['chaos_level']==chaos)]['delay_mean'].median()
    if ideal > 0:
        deg = ((chaos_d - ideal) / ideal) * 100
        print(f"  {chaos:>9s}: ideal={ideal:.0f}s, chaos={chaos_d:.0f}s, degradation={deg:+.1f}%")
