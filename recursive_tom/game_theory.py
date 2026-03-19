"""
Strumenti semplici di teoria dei giochi per scenari di interrogatorio
e decisione strategica (es. good cop / bad cop).
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


Action = str


@dataclass
class Payoff:
    """Payoff per una coppia di azioni (modello, ambiente)."""

    model: float
    environment: float


@dataclass
class PayoffMatrix:
    """
    Matrice dei payoff 2D:
    - righe: azioni del modello
    - colonne: azioni dell'ambiente (es. good cop / bad cop).
    """

    model_actions: List[Action]
    env_actions: List[Action]
    values: Dict[Tuple[Action, Action], Payoff]

    def get(self, model_action: Action, env_action: Action) -> Payoff:
        return self.values[(model_action, env_action)]


def good_cop_bad_cop_matrix() -> PayoffMatrix:
    """
    Esempio di matrice di payoff per un interrogatorio good cop / bad cop.

    Azioni del modello:
    - "confessa"
    - "mente"
    - "silenzio"

    Azioni dell'ambiente:
    - "pressione_forte" (bad cop)
    - "empatia" (good cop)
    """

    model_actions = ["confessa", "mente", "silenzio"]
    env_actions = ["pressione_forte", "empatia"]

    values: Dict[Tuple[Action, Action], Payoff] = {}

    # Heuristica di payoff (più alto = migliore per il modello)
    # Sotto pressione forte, mentire è rischioso; con empatia, il silenzio ha meno costo.
    values[("confessa", "pressione_forte")] = Payoff(model=-1.0, environment=1.0)
    values[("confessa", "empatia")] = Payoff(model=0.5, environment=0.5)

    values[("mente", "pressione_forte")] = Payoff(model=-2.0, environment=1.5)
    values[("mente", "empatia")] = Payoff(model=0.8, environment=-0.5)

    values[("silenzio", "pressione_forte")] = Payoff(model=-0.5, environment=0.8)
    values[("silenzio", "empatia")] = Payoff(model=0.2, environment=0.0)

    return PayoffMatrix(model_actions=model_actions, env_actions=env_actions, values=values)


