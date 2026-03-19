import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Caricamento Dati
try:
    df = pd.read_csv("benchmark_raw_results.csv")
except FileNotFoundError:
    print("Errore: Esegui prima main_experiment.py per generare i dati.")
    exit()

print("--- Analisi Statistica del Collasso Cognitivo ---")

# 1. Statistiche Descrittive per Livello
summary = df.groupby('tom_level')['is_correct'].agg(['mean', 'std', 'count']).reset_index()
summary.columns = ['ToM_Level', 'Accuracy_Mean', 'Accuracy_Std', 'N_Samples']
summary['CI_95_Low'] = summary['Accuracy_Mean'] - 1.96 * (summary['Accuracy_Std'] / np.sqrt(summary['N_Samples']))
summary['CI_95_High'] = summary['Accuracy_Mean'] + 1.96 * (summary['Accuracy_Std'] / np.sqrt(summary['N_Samples']))

print("\nRiepilogo Performance con Intervalli di Confidenza (95%):")
print(summary.to_string(index=False))

# 2. Test ANOVA (Analisi della Varianza)
# Verifica se le differenze tra i livelli sono statisticamente significative
groups = [df[df['tom_level'] == l]['is_correct'] for l in df['tom_level'].unique()]
f_stat, p_val = stats.f_oneway(*groups)

print(f"\nRisultato ANOVA One-Way:")
print(f"F-statistic: {f_stat:.4f}")
print(f"P-value: {p_val:.4e}")
if p_val < 0.05:
    print(">> Conclusione: Esiste una differenza significativa nelle performance tra i livelli di ToM (Rifiuto H0).")
else:
    print(">> Conclusione: Nessuna differenza significativa rilevata (Non rifiuto H0).")

# 3. Visualizzazione Professionale
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(data=df, x='tom_level', y='is_correct', errorbar=('ci', 95), ax=ax, palette="viridis")
ax.set_title(f"Impatto della Ricorsione Sociale sulla Performance del Modello ({MODEL_NAME})", fontsize=14, fontweight='bold')
ax.set_xlabel("Ordine della Teoria della Mente (ToM)", fontsize=12)
ax.set_ylabel("Accuratezza Media (Proporzione Corrette)", fontsize=12)
ax.set_ylim(0, 1.05)

# Annotazione P-value
ax.text(0.5, 0.95, f'ANOVA p-value: {p_val:.2e}', transform=ax.transAxes, 
        fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig("tom_cognitive_collapse_analysis.png", dpi=300)
print("\nGrafico salvato come 'tom_cognitive_collapse_analysis.png'")
plt.show()

# 4. Analisi Opzionale: Regressione Logistica (per vedere l'odds ratio del collasso)
import statsmodels.api as sm
X = sm.add_constant(df['tom_level'])
y = df['is_correct']
logit_model = sm.Logit(y, X)
result = logit_model.fit(disp=0)
print("\nRisultati Regressione Logistica (Impatto ToM sulla probabilità di successo):")
print(result.summary().tables[1])
