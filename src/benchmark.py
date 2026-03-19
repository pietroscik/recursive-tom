"""
Benchmark Recursive-ToM per kaggle_benchmarks (API moderna).

Definisce un singolo task parametrico tramite il decoratore @kbench.task.
Su Kaggle, potrai selezionarlo con `%choose recursive_tom_task` nel notebook.
"""

from typing import Any, Dict

import kaggle_benchmarks as kbench

from recursive_tom_engine import RecursiveToMEngine


@kbench.task(name="recursive_tom_task")
def recursive_tom_task(
    llm,
    tom_level: int = 1,
    seed: int = 0,
) -> None:
    """
    Task di benchmark per un singolo scenario di Teoria della Mente ricorsiva.

    Parametri:
        llm: modello fornito da kaggle_benchmarks (kbench.llm).
        tom_level: livello di ricorsione (1 = false belief, >1 = higher-order).
        seed: per riproducibilità opzionale degli scenari.
    """
    import random

    random.seed(seed)
    engine = RecursiveToMEngine()

    scenario: Dict[str, Any] = engine.generate_scenario(tom_order=tom_level)
    context_text = " ".join(scenario["story"])

    system_prompt = (
        "You are an expert in logical reasoning and social cognition. "
        "Analyze the provided story carefully and answer the question based ONLY "
        "on the beliefs of the characters, not necessarily reality."
    )

    user_prompt = (
        f"Story:\n{context_text}\n\n"
        f"Question:\n{scenario['question']}\n\n"
        "Answer concisely with only the location."
    )

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    # Chiamata al modello via Kaggle Proxy
    response = llm.prompt(full_prompt)

    # Validazione: la risposta deve contenere la location corretta (case-insensitive)
    correct_answer = scenario["correct_answer"]
    pattern = rf"(?i){correct_answer}"

    kbench.assertions.assert_contains_regex(
        pattern,
        response,
        expectation=(
            f"LLM should mention the correct believed location '{correct_answer}' "
            f"for ToM recursion level {tom_level}."
        ),
    )


if __name__ == "__main__":
    # Esecuzione di esempio locale/Kaggle: loop su alcuni livelli di ToM.
    # In un notebook Kaggle per il leaderboard userai invece:
    #   %choose recursive_tom_task
    # e poi chiamerai recursive_tom_task.run(...)
    for level in [1, 2, 3, 4]:
        print(f"Running demo for ToM level {level}...")
        recursive_tom_task.run(llm=kbench.llm, tom_level=level, seed=0)
