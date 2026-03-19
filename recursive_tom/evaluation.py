"""
Sistema di valutazione a consiglio di pari per scenari ToM + decisione.

Include:
- Giudice normativo (correttezza logica).
- Giudice "avvocato del diavolo" (robustezza / ambiguità).
- Giudice strategico (razionalità rispetto a una matrice di payoff).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .game_theory import PayoffMatrix, Payoff


@dataclass
class JudgeScore:
    name: str
    role: str
    score: float
    notes: str


@dataclass
class CouncilResult:
    """
    Risultato aggregato del consiglio di pari.
    """

    accuracy: float
    robustness: float
    rationality: float
    judges: List[JudgeScore]


class PeerJudge:
    """
    Interfaccia base per un giudice.
    """

    name: str = "peer_judge"
    role: str = "generic"

    def evaluate(
        self,
        *,
        scenario: Dict[str, Any],
        model_answer: str,
        is_correct: bool,
        tom_level: int,
        payoff_matrix: Optional[PayoffMatrix] = None,
        chosen_action: Optional[str] = None,
    ) -> JudgeScore:
        raise NotImplementedError


class NormativeJudge(PeerJudge):
    """
    Valuta la pura correttezza rispetto al ground truth.
    """

    name = "normative_judge"
    role = "good_cop"

    def evaluate(
        self,
        *,
        scenario: Dict[str, Any],
        model_answer: str,
        is_correct: bool,
        tom_level: int,
        payoff_matrix: Optional[PayoffMatrix] = None,
        chosen_action: Optional[str] = None,
    ) -> JudgeScore:
        score = 1.0 if is_correct else 0.0
        notes = "Risposta corretta rispetto al ground truth." if is_correct else "Risposta errata rispetto al ground truth."
        return JudgeScore(name=self.name, role=self.role, score=score, notes=notes)


class DevilsAdvocateJudge(PeerJudge):
    """
    Cerca fragilità nella risposta: penalizza errori a livelli bassi
    e premia stabilità su livelli ToM elevati.
    """

    name = "devils_advocate"
    role = "bad_cop"

    def evaluate(
        self,
        *,
        scenario: Dict[str, Any],
        model_answer: str,
        is_correct: bool,
        tom_level: int,
        payoff_matrix: Optional[PayoffMatrix] = None,
        chosen_action: Optional[str] = None,
    ) -> JudgeScore:
        if not is_correct:
            score = max(0.0, 0.5 - 0.1 * tom_level)
            notes = "Errore già a livello di ricorsione basso: risposta fragile."
        else:
            score = min(1.0, 0.6 + 0.1 * tom_level)
            notes = "Risposta stabile anche con ricorsione più profonda."
        return JudgeScore(name=self.name, role=self.role, score=score, notes=notes)


class StrategicJudge(PeerJudge):
    """
    Valuta la razionalità dell'azione rispetto a una matrice di payoff.
    Se non viene fornita una matrice, restituisce un punteggio neutro.
    """

    name = "strategic_judge"
    role = "game_theory"

    def evaluate(
        self,
        *,
        scenario: Dict[str, Any],
        model_answer: str,
        is_correct: bool,
        tom_level: int,
        payoff_matrix: Optional[PayoffMatrix] = None,
        chosen_action: Optional[str] = None,
    ) -> JudgeScore:
        if payoff_matrix is None or chosen_action is None:
            return JudgeScore(
                name=self.name,
                role=self.role,
                score=0.5,
                notes="Nessuna matrice di payoff/azione fornita: punteggio neutro.",
            )

        env_action = scenario.get("env_action", "pressione_forte")
        try:
            chosen_payoff: Payoff = payoff_matrix.get(chosen_action, env_action)
        except KeyError:
            return JudgeScore(
                name=self.name,
                role=self.role,
                score=0.0,
                notes="Azione scelta non presente nella matrice di payoff.",
            )

        # Calcolo del payoff migliore/peggiore per quell'ambiente
        model_values = [
            payoff_matrix.get(a, env_action).model for a in payoff_matrix.model_actions
        ]
        best_model_value = max(model_values)
        worst_model_value = min(model_values)

        if best_model_value == worst_model_value:
            score = 0.5
        else:
            # Normalizzazione lineare: worst -> 0, best -> 1
            raw = (chosen_payoff.model - worst_model_value) / (
                best_model_value - worst_model_value
            )
            score = max(0.0, min(1.0, raw))

        notes = (
            f"Azione '{chosen_action}' con payoff {chosen_payoff.model:.2f} "
            f"(worst {worst_model_value:.2f}, best {best_model_value:.2f})."
        )
        return JudgeScore(name=self.name, role=self.role, score=score, notes=notes)


class PeerJudgementCouncil:
    """
    Colleziona diversi giudici e aggrega i loro punteggi.
    """

    def __init__(self, judges: Optional[List[PeerJudge]] = None) -> None:
        if judges is None:
            judges = [NormativeJudge(), DevilsAdvocateJudge(), StrategicJudge()]
        self.judges = judges

    def evaluate(
        self,
        *,
        scenario: Dict[str, Any],
        model_answer: str,
        is_correct: bool,
        tom_level: int,
        payoff_matrix: Optional[PayoffMatrix] = None,
        chosen_action: Optional[str] = None,
    ) -> CouncilResult:
        scores: List[JudgeScore] = []
        for judge in self.judges:
            scores.append(
                judge.evaluate(
                    scenario=scenario,
                    model_answer=model_answer,
                    is_correct=is_correct,
                    tom_level=tom_level,
                    payoff_matrix=payoff_matrix,
                    chosen_action=chosen_action,
                )
            )

        # Aggregazione: media pesata semplice per ruolo
        accuracy_scores = [
            s.score for s in scores if s.role == "good_cop"
        ] or [0.0]
        robustness_scores = [
            s.score for s in scores if s.role == "bad_cop"
        ] or [0.0]
        rationality_scores = [
            s.score for s in scores if s.role == "game_theory"
        ] or [0.0]

        return CouncilResult(
            accuracy=sum(accuracy_scores) / len(accuracy_scores),
            robustness=sum(robustness_scores) / len(robustness_scores),
            rationality=sum(rationality_scores) / len(rationality_scores),
            judges=scores,
        )

