# src/benchmark.py
import os
import json
import random
from typing import List, Dict, Any
from kaggle_benchmarks import Benchmark, Task, TaskResult

# Importa il tuo motore logico (assicurati che sia nella stessa cartella o installabile)
from recursive_tom_engine import RecursiveToMEngine 

class RecursiveToMBenchmark(Benchmark):
    """
    Benchmark ufficiale per la valutazione della Teoria della Mente Ricorsiva.
    Track: Social Cognition
    """
    
    def __init__(self):
        super().__init__(
            name="Recursive-ToM",
            description="Procedural benchmark for higher-order social inference. Measures cognitive collapse under recursive belief tracking.",
            version="1.0.0"
        )
        self.engine = RecursiveToMEngine()
        self.num_samples_per_level = 5
        self.max_recursion_depth = 6

    def generate_tasks(self) -> List[Task]:
        """Genera proceduralmente tutte le task per il benchmark."""
        tasks = []
        task_id_counter = 1
        
        print(f"🚀 Generazione di {self.num_samples_per_level * self.max_recursion_depth} task procedurali...")
        
        for level in range(1, self.max_recursion_depth + 1):
            for i in range(self.num_samples_per_level):
                # Genera scenario con il tuo motore logico rigoroso
                scenario = self.engine.generate_scenario(tom_order=level)
                
                # Costruisci il prompt per il modello (System + User)
                system_prompt = (
                    "You are an expert in logical reasoning and social cognition. "
                    "Analyze the provided story carefully and answer the question based ONLY on the beliefs of the characters, not necessarily reality."
                )
                
                user_prompt = (
                    f"Story:\n{scenario['context']}\n\n"
                    f"Question:\n{scenario['question']}\n\n"
                    f"Answer concisely with only the location."
                )
                
                # Definisci la funzione di verifica (Grader)
                # Questa funzione viene eseguita DOPO che il modello ha risposto
                def create_grader(correct_answer: str):
                    def grader(model_output: str) -> TaskResult:
                        # Normalizzazione semplice per il confronto (puoi raffinarla)
                        normalized_output = model_output.strip().lower()
                        normalized_truth = correct_answer.strip().lower()
                        
                        # Controllo esatto o parziale (a seconda di quanto vuoi essere rigido)
                        is_correct = normalized_truth in normalized_output
                        
                        return TaskResult(
                            score=1.0 if is_correct else 0.0,
                            feedback=f"Expected: '{correct_answer}'. Got: '{model_output}'."
                        )
                    return grader

                task = Task(
                    id=f"tom_level_{level}_sample_{i+1}",
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    grader=create_grader(scenario['answer_key']),
                    metadata={
                        "recursion_depth": level,
                        "true_location": scenario['true_location'],
                        "agents": scenario['agents'],
                        "track": "Social Cognition"
                    }
                )
                tasks.append(task)
                task_id_counter += 1
                
        return tasks

# Punto di ingresso per Kaggle
if __name__ == "__main__":
    benchmark = RecursiveToMBenchmark()
    # Questo comando registra il benchmark sulla piattaforma Kaggle
    # Nota: Richiede autenticazione Kaggle CLI configurata
    benchmark.push() 
    print("✅ Benchmark caricato con successo su Kaggle!")
