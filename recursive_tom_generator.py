import random
from typing import List, Dict, Optional, Any
from copy import deepcopy

class Agent:
    """Rappresenta un agente con conoscenze e credenze."""
    def __init__(self, name: str):
        self.name = name
        # Fatti che l'agente conosce come veri (es. "diamante" -> "cassaforte")
        self.knowledge: Dict[str, str] = {}
        # Credenze dell'agente (possono essere false se non aggiornate)
        # Inizialmente uguali alla conoscenza
        self.beliefs: Dict[str, str] = {}

    def observe(self, fact_key: str, fact_value: str):
        """L'agente osserva un fatto e aggiorna conoscenza e credenze."""
        self.knowledge[fact_key] = fact_value
        self.beliefs[fact_key] = fact_value

    def forget_or_mislead(self, fact_key: str, old_value: str):
        """
        Simula il mancato aggiornamento. 
        L'agente NON sa il nuovo valore, quindi mantiene la vecchia credenza.
        La sua 'knowledge' reale potrebbe essere vuota o errata rispetto alla realtà globale,
        ma per la ToM ci interessa cosa 'crede'.
        """
        # Mantiene la vecchia credenza (False Belief)
        if fact_key not in self.beliefs:
            self.beliefs[fact_key] = old_value
        
    def get_belief(self, fact_key: str) -> Optional[str]:
        return self.beliefs.get(fact_key)

class RecursiveToMEngine:
    def __init__(self):
        self.names_pool = ["Marco", "Anna", "Luca", "Giulia", "Sofia", "Alessandro"]
        self.objects_pool = ["il diamante", "la chiave USB", "il testamento", "l'oro", "il microchip"]
        self.locations_pool = ["nella cassaforte", "sotto il tappeto", "nel baule", "dietro il quadro"]

    def generate_scenario(self, tom_order: int) -> Dict[str, Any]:
        """
        Genera uno scenario completo con logica di stati mentali rigorosa.
        """
        # 1. Setup Personaggi e Oggetti
        num_agents = min(tom_order + 1, len(self.names_pool))
        agents_names = random.sample(self.names_pool, num_agents)
        agents = {name: Agent(name) for name in agents_names}
        
        obj = random.choice(self.objects_pool)
        loc_start = random.choice(self.locations_pool)
        loc_end = random.choice([l for l in self.locations_pool if l != loc_start])
        
        story_log = []
        
        # 2. Evento Iniziale: Tutti vedono il posizionamento iniziale
        # Agente 0 nasconde l'oggetto. Tutti gli agenti presenti osservano.
        actor = agents[agents_names[0]]
        story_log.append(f"{actor.name} nasconde {obj} {loc_start}.")
        
        for agent in agents.values():
            agent.observe(obj, loc_start)
            
        # 3. Evento di Manipolazione (Creazione False Belief)
        # Per avere ToM > 1, serve uno spostamento non visto da tutti.
        # Logica: Agente 0 sposta l'oggetto. Agente 1 NON vede. Agente 2 vede? Dipende dall'ordine.
        
        # Regola procedurale per garantire ricorsione:
        # - Chi è pari nell'indice (0, 2, 4...) vede lo spostamento (conosce la verità).
        # - Chi è dispari (1, 3, 5...) NON vede lo spostamento (mantiene falsa credenza).
        # Questo crea un'alternanza perfetta per testare la ricorsione.
        
        story_log.append(f"Mentre alcuni sono distratti, {actor.name} sposta {obj} {loc_end}.")
        
        true_location = loc_end # La realtà fisica
        
        for i, name in enumerate(agents_names):
            agent = agents[name]
            if i == 0:
                # L'attore sa sempre dove ha messo l'oggetto
                agent.observe(obj, loc_end)
            elif i % 2 != 0:
                # Indici dispari (1, 3...) NON vedono lo spostamento -> False Belief
                # Non chiamiamo observe, lasciamo che mantengano la credenza precedente (loc_start)
                pass 
            else:
                # Indici pari (2, 4...) vedono lo spostamento -> True Belief
                agent.observe(obj, loc_end)

        # 4. Costruzione della Domanda Ricorsiva
        # Catena: Agente N chiede cosa pensa Agente N-1 ... che pensa Agente 1.
        # Esempio Order 2: "Cosa pensa Agente 1 che pensi Agente 0?"
        # Nota: La domanda parte dall'ultimo agente della catena verso il primo.
        
        chain_indices = list(range(1, tom_order + 1)) # [1, 2] per order 2
        # Assicuriamoci di non superare il numero di agenti disponibili
        if max(chain_indices) >= len(agents_names):
            # Fallback sicuro se l'ordine è troppo alto per gli agenti generati
            chain_indices = [i % len(agents_names) for i in range(1, tom_order + 1)]
            
        chain_agents = [agents[agents_names[i]] for i in chain_indices]
        
        # Costruzione testo domanda
        # "Dove pensa [A_n] che [A_n-1] ... che [A_1] creda che sia [obj]?"
        question_text = f"Dove pensa "
        for i, agent in enumerate(chain_agents):
            if i == len(chain_agents) - 1:
                question_text += f"{agent.name} che si trovi {obj}?"
            else:
                question_text += f"{agent.name} che "
        
        # 5. Risoluzione Logica (Ground Truth)
        # Dobbiamo simulare il ragionamento ricorsivo partendo dall'interno.
        # Livello 0 (Interno): Cosa crede realmente l'Agente 0 (il primo nella catena di pensiero)?
        # Livello 1: Cosa crede l'Agente 1 che creda l'Agente 0?
        # ...
        
        current_belief_holder = agents[agents_names[0]] # Il soggetto finale del pensiero (chi ha nascosto)
        current_belief_value = current_belief_holder.get_belief(obj)
        
        # Ora risaliamo la catena: ogni agente successivo proietta la propria credenza sul precedente.
        # Se l'Agente X non sa che l'Agente Y ha visto lo spostamento, X crederà che Y abbia ancora la vecchia credenza.
        
        # Semplificazione per questo motore procedurale:
        # Assumiamo che ogni agente nella catena proietti la PROPRIA credenza sull'altro,
        # a meno che non sappia specificamente che l'altro ha visto qualcosa che lui non ha visto.
        # Nel nostro setup semplice (Vedo/Non Vedo alternato):
        # Se Agente K non ha visto lo spostamento, crederà che TUTTI quelli prima di lui (che non hanno visto) abbiano la vecchia credenza.
        # Ma se Agente K HA visto lo spostamento, sa che anche quelli che hanno visto sanno la verità.
        
        # Algoritmo di risoluzione "Naive Theory of Mind" (simula come ragiona un umano medio):
        # Ogni agente assume che gli altri sappiano ciò che sa lui, a meno che non ci sia evidenza contraria esplicita.
        # Qui usiamo una regola deterministica basata sulla visibilità definita sopra.
        
        resolved_location = self._resolve_recursive_belief(chain_agents, obj, loc_start, loc_end)

        return {
            "tom_order": tom_order,
            "agents": [a.name for a in agents.values()],
            "object": obj,
            "true_location": true_location,
            "story": story_log,
            "question": question_text,
            "correct_answer": resolved_location,
            "logic_trace": f"Realtà: {loc_end}. Credenze individuali calcolate dal motore."
        }

    def _resolve_recursive_belief(self, chain: List[Agent], obj: str, loc_old: str, loc_new: str) -> str:
        """
        Risolve ricorsivamente la credenza.
        Partiamo dal soggetto più interno (chi ha compiuto l'azione) e usciamo verso l'esterno.
        """
        # Il soggetto interno è sempre l'Agente 0 (quello che ha nascosto/spostato)
        # La catena di domanda è: A_n -> A_{n-1} -> ... -> A_1 -> (pensiero su A_0)
        
        # Stato attuale del pensiero: Cosa crede A_0?
        # A_0 ha sempre visto tutto (è l'attore).
        current_thought = loc_new 
        
        # Ora iteriamo dalla prospettiva di A_1, poi A_2, ecc.
        # Se A_1 non ha visto lo spostamento, A_1 crede che A_0 creda ancora nel vecchio posto?
        # Sì, perché A_1 non sa che A_0 ha spostato l'oggetto (o non sa che A_0 sa che A_1 non ha visto? No, semplifichiamo).
        
        # Regola del motore:
        # Se l'agente corrente nella catena (che sta pensando) NON ha visto lo spostamento,
        # allora egli attribuisce all'agente interno la CREDENZA CHE EGLI STESSO HA (False Belief projection).
        # Se l'agente corrente HA visto lo spostamento, attribuisce la verità.
        
        for thinker in chain:
            # Verifichiamo cosa crede 'thinker'. 
            # Se thinker crede che sia nel vecchio posto, allora penserà che anche l'agente interno creda nel vecchio posto.
            thinker_belief = thinker.get_belief(obj)
            
            if thinker_belief == loc_old:
                # Thinker ha una falsa credenza. Proietta questa falsità sull'agente interno.
                current_thought = loc_old
            else:
                # Thinker sa la verità. Assume che anche l'agente interno (se razionale) sappia la verità?
                # Nel nostro scenario, se thinker ha visto, sa che l'attore ha visto. Quindi proietta verità.
                current_thought = loc_new
                
        return current_thought

# --- Esecuzione e Test ---
if __name__ == "__main__":
    engine = RecursiveToMEngine()
    
    print("=== RECURSIVE-TOM ENGINE v1.0 ===\n")
    
    for level in [1, 2, 3, 4]:
        print(f"--- TEST LIVELLO {level} ---")
        result = engine.generate_scenario(level)
        
        print("STORIA:")
        for line in result['story']:
            print(f"  - {line}")
        
        print(f"\nDOMANDA ({level}-order ToM):")
        print(f"  {result['question']}")
        
        print(f"\nRISPOSTA CORRETTA: {result['correct_answer']}")
        print(f"POSIZIONE REALE: {result['true_location']}")
        print("-" * 50)
