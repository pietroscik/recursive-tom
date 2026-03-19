import os
import time
import random

import numpy as np
import pandas as pd

from generator import SocialScenarioGenerator

# CONFIGURAZIONE
N_ITERATIONS = 50  # Numero di volte che ripeti ogni livello per stabilità statistica
TOM_LEVELS = [1, 2, 3, 4]  # Livelli di ricorsione da testare
MODEL_NAME = "llama-3-70b-instruct"  # O il modello che stai usando su Kaggle

# Rate limiting simulato: configurabile via env per aumentare la velocità
DEFAULT_RATE_LIMIT = 0.1  # secondi
RATE_LIMIT_SECONDS = float(os.getenv("RECURSIVE_TOM_RATE_LIMIT", DEFAULT_RATE_LIMIT))


def mock_llm_call(prompt, tom_level: int):
    """
    SOSTITUIRE QUESTA FUNZIONE CON LA CHIAMATA REALE ALL'API (es. HuggingFace Inference API o LangChain).
    Per ora simula una risposta con probabilità di errore crescente con la ToM.
    """
    # Simulazione del "Collasso Cognitivo": più alto è l'ordine, più bassa è l'accuratezza.
    # Usiamo direttamente il livello di ToM invece di dedurlo dal prompt.
    difficulty_factor = 0.2 * (tom_level - 1)
    success_prob = max(0.1, 0.95 - difficulty_factor)
    
    is_correct = random.random() < success_prob
    return "Risposta Generata dal Modello...", is_correct

def run_benchmark():
    generator = SocialScenarioGenerator()
    results = []

    print(f"Inizio Benchmark: {N_ITERATIONS} iterazioni per livello ToM...")

    for level in TOM_LEVELS:
        print(f"--- Esecuzione Livello ToM-{level} ---")
        for i in range(N_ITERATIONS):
            # 1. Genera Scenario Unico
            scenario = generator.generate_scenario(level)
            
            # 2. Interroga il Modello
            start_time = time.time()
            response, is_correct = mock_llm_call(scenario["prompt"], level)
            latency = time.time() - start_time
            
            # 3. Salva Risultato
            results.append(
                {
                    "run_id": i,
                    "tom_level": level,
                    "scenario_id": scenario["id"],
                    "is_correct": int(is_correct),  # 1 o 0
                    "latency_sec": latency,
                    "prompt_length": len(scenario["prompt"]),
                    "model": MODEL_NAME,
                }
            )

            # Rate limiting simulato (può essere disattivato impostando RECURSIVE_TOM_RATE_LIMIT=0)
            if RATE_LIMIT_SECONDS > 0:
                time.sleep(RATE_LIMIT_SECONDS)

    return pd.DataFrame(results)

if __name__ == "__main__":
    df_results = run_benchmark()
    df_results.to_csv("benchmark_raw_results.csv", index=False)
    print("Benchmark completato. Dati salvati in 'benchmark_raw_results.csv'")
    print(df_results.groupby('tom_level')['is_correct'].mean())
