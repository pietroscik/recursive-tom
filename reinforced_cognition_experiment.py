"""
Esempio di esperimento con "cognizione rinforzata":
- Genera uno scenario ToM.
- Associa una matrice di payoff good cop / bad cop.
- Valuta una risposta del modello tramite un consiglio di pari.
"""

from recursive_tom.engine import RecursiveToMEngine
from recursive_tom.evaluation import PeerJudgementCouncil
from recursive_tom.game_theory import good_cop_bad_cop_matrix


def run_demo(tom_level: int = 2) -> None:
    engine = RecursiveToMEngine()
    council = PeerJudgementCouncil()
    payoff = good_cop_bad_cop_matrix()

    scenario = engine.generate_scenario(tom_level)
    scenario["env_action"] = "pressione_forte"  # bad cop di default

    # Placeholder: in un setup reale, qui useresti la risposta dell'LLM.
    model_answer = "Risposta dimostrativa del modello"
    is_correct = True  # ipotizziamo sia corretta per la demo
    chosen_action = "confessa"

    result = council.evaluate(
        scenario=scenario,
        model_answer=model_answer,
        is_correct=is_correct,
        tom_level=tom_level,
        payoff_matrix=payoff,
        chosen_action=chosen_action,
    )

    print("=== DEMO COGNIZIONE RINFORZATA ===")
    print("Storia:")
    for line in scenario["story"]:
        print(" -", line)
    print("\nDomanda:", scenario["question"])
    print("Risposta modello:", model_answer)
    print("Azione decisionale:", chosen_action)
    print("\nPunteggi consiglio di pari:")
    for s in result.judges:
        print(f" - {s.name} ({s.role}): {s.score:.2f} -> {s.notes}")
    print(
        f"\nIndice aggregato | Accuracy: {result.accuracy:.2f}, "
        f"Robustness: {result.robustness:.2f}, Rationality: {result.rationality:.2f}"
    )


if __name__ == "__main__":
    run_demo(tom_level=3)

