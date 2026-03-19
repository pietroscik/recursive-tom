"""
Motore logico per scenari di Teoria della Mente ricorsiva.

Attenzione: il codice è preso da `recursive_tom_generator.py` e
rilocalizzato in un modulo di libreria riutilizzabile.
"""

from typing import Any, Dict, List, Optional
import random


class Agent:
    """Rappresenta un agente con conoscenze e credenze."""

    def __init__(self, name: str):
        self.name = name
        # Fatti che l'agente conosce come veri (es. "diamante" -> "cassaforte")
        self.knowledge: Dict[str, str] = {}
        # Credenze dell'agente (possono essere false se non aggiornate)
        # Inizialmente uguali alla conoscenza
        self.beliefs: Dict[str, str] = {}

    def observe(self, fact_key: str, fact_value: str) -> None:
        """L'agente osserva un fatto e aggiorna conoscenza e credenze."""
        self.knowledge[fact_key] = fact_value
        self.beliefs[fact_key] = fact_value

    def forget_or_mislead(self, fact_key: str, old_value: str) -> None:
        """
        Simula il mancato aggiornamento.
        L'agente NON sa il nuovo valore, quindi mantiene la vecchia credenza.
        """
        if fact_key not in self.beliefs:
            self.beliefs[fact_key] = old_value

    def get_belief(self, fact_key: str) -> Optional[str]:
        return self.beliefs.get(fact_key)


class RecursiveToMEngine:
    """
    Motore procedurale che genera scenari con stati mentali ricorsivi.
    """

    def __init__(self) -> None:
        self.names_pool = ["Marco", "Anna", "Luca", "Giulia", "Sofia", "Alessandro"]
        self.objects_pool = [
            "il diamante",
            "la chiave USB",
            "il testamento",
            "l'oro",
            "il microchip",
        ]
        self.locations_pool = [
            "nella cassaforte",
            "sotto il tappeto",
            "nel baule",
            "dietro il quadro",
        ]

    def generate_scenario(self, tom_order: int) -> Dict[str, Any]:
        """
        Genera uno scenario completo con logica di stati mentali rigorosa.
        Restituisce un dizionario con:
        - tom_order, agents, object, true_location, story, question,
          correct_answer, logic_trace.
        """
        # 1. Setup Personaggi e Oggetti
        num_agents = min(tom_order + 1, len(self.names_pool))
        agents_names = random.sample(self.names_pool, num_agents)
        agents = {name: Agent(name) for name in agents_names}

        obj = random.choice(self.objects_pool)
        loc_start = random.choice(self.locations_pool)
        loc_end = random.choice([l for l in self.locations_pool if l != loc_start])

        story_log: List[str] = []

        # 2. Evento Iniziale
        actor = agents[agents_names[0]]
        story_log.append(f"{actor.name} nasconde {obj} {loc_start}.")
        for agent in agents.values():
            agent.observe(obj, loc_start)

        # 3. Evento di Manipolazione (creazione False Belief)
        story_log.append(f"Mentre alcuni sono distratti, {actor.name} sposta {obj} {loc_end}.")
        true_location = loc_end

        for i, name in enumerate(agents_names):
            agent = agents[name]
            if i == 0:
                agent.observe(obj, loc_end)
            elif i % 2 != 0:
                # Indici dispari NON vedono lo spostamento -> mantengono loc_start
                agent.forget_or_mislead(obj, loc_start)
            else:
                # Indici pari vedono lo spostamento -> credono loc_end
                agent.observe(obj, loc_end)

        # 4. Costruzione catena di domanda ricorsiva
        chain_indices = list(range(1, tom_order + 1))
        if chain_indices and max(chain_indices) >= len(agents_names):
            chain_indices = [i % len(agents_names) for i in range(1, tom_order + 1)]
        chain_agents = [agents[agents_names[i]] for i in chain_indices]

        question_text = "Dove pensa "
        for i, agent in enumerate(chain_agents):
            if i == len(chain_agents) - 1:
                question_text += f"{agent.name} che si trovi {obj}?"
            else:
                question_text += f"{agent.name} che "

        # 5. Risoluzione logica ricorsiva
        resolved_location = self._resolve_recursive_belief(
            chain_agents, obj, loc_start, loc_end
        )

        return {
            "tom_order": tom_order,
            "agents": [a.name for a in agents.values()],
            "object": obj,
            "true_location": true_location,
            "story": story_log,
            "question": question_text,
            "correct_answer": resolved_location,
            "logic_trace": f"Realtà: {loc_end}. Credenze individuali calcolate dal motore.",
        }

    def _resolve_recursive_belief(
        self, chain: List[Agent], obj: str, loc_old: str, loc_new: str
    ) -> str:
        """
        Risolve ricorsivamente la credenza lungo la catena di agenti.
        """
        current_thought = loc_new
        for thinker in chain:
            thinker_belief = thinker.get_belief(obj)
            if thinker_belief == loc_old:
                current_thought = loc_old
            else:
                current_thought = loc_new
        return current_thought


