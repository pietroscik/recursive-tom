import json
import os
from recursive_tom_engine import RecursiveToMEngine

def create_sample_dataset(output_filename: str = "sample_benchmark.json", samples_per_level: int = 3, max_level: int = 5):
    """
    Genera un dataset JSON di esempio per il benchmark Recursive-ToM.
    
    Args:
        output_filename: Nome del file di output.
        samples_per_level: Quanti esempi generare per ogni livello di ricorsione.
        max_level: Il livello massimo di ToM da generare (es. 5).
    """
    engine = RecursiveToMEngine()
    dataset = {
        "meta": {
            "name": "Recursive-ToM Sample Benchmark",
            "version": "1.0",
            "description": "Procedurally generated scenarios for evaluating higher-order Theory of Mind in LLMs.",
            "author": "Pietro Maietta - Recursive-ToM Project",
            "total_samples": 0,
            "levels_included": list(range(1, max_level + 1))
        },
        "samples": []
    }

    print(f"🚀 Generazione dataset in corso... (Livelli 1-{max_level}, {samples_per_level} esempi/livello)")

    for level in range(1, max_level + 1):
        print(f"  -> Elaborazione Livello {level}...")
        
        for i in range(samples_per_level):
            # Genera scenario
            scenario = engine.generate_scenario(tom_order=level)
            
            # Formatta l'oggetto per il JSON
            sample_entry = {
                "id": f"L{level}_S{i+1}",
                "tom_order": level,
                "context": " ".join(scenario['story']), # Unisce la storia in un unico stringa testo
                "question": scenario['question'],
                "answer_key": scenario['correct_answer'], # La risposta corretta (Ground Truth)
                "metadata": {
                    "true_location": scenario['true_location'],
                    "object": scenario['object'],
                    "agents_involved": scenario['agents'],
                    "logic_note": "La risposta dipende dalla catena di visibilità degli eventi."
                }
            }
            
            dataset['samples'].append(sample_entry)
            dataset['meta']['total_samples'] += 1

    # Salva su file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Dataset generato con successo: {output_filename}")
    print(f"📊 Totale esempi: {dataset['meta']['total_samples']}")
    return output_filename

if __name__ == "__main__":
    # Configurazione
    FILENAME = "sample_benchmark.json"
    SAMPLES_PER_LEVEL = 3
    MAX_LEVEL = 5
    
    # Esegui generazione
    create_sample_dataset(FILENAME, SAMPLES_PER_LEVEL, MAX_LEVEL)
    
    # Anteprima rapida del primo elemento
    print("\n--- ANTEPRIMA PRIMO ESEMPIO (JSON) ---")
    with open(FILENAME, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(json.dumps(data['samples'][0], indent=2, ensure_ascii=False))
