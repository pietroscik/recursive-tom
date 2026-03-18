import random
from typing import List, Dict, Tuple

class RecursiveToMGenerator:
    """
    Generatore procedurale per scenari di Teoria della Mente (ToM) ricorsiva.
    Obiettivo: Creare trame infinite per testare il 'collasso cognitivo' negli LLM.
    """

    def __init__(self):
        # Database lessicale modulare (facile da espandere)
        self.characters = ["Marco", "Anna", "Luca", "Giulia", "Sofia", "Alessandro", "Elena", "Davide"]
        self.objects = ["il diamante rosso", "la chiave USB criptata", "il testamento segreto", 
                        "l'oro dei pirati", "il microchip sperimentale", "la mappa del tesoro"]
        self.locations = ["nella cassaforte", "sotto il tappeto", "nel vecchio baule", 
                          "dietro il quadro", "nel cassetto bloccato", "sotto il letto"]
        
        # Azioni per creare contesto (opzionale, per rendere la storia più ricca)
        self.actions = ["nasconde", "sposta", "rubano", "scambiano"]

    def generate_scenario_base(self) -> Dict[str, str]:
        """Crea i fatti oggettivi dello scenario (La Realtà)."""
        chars = random.sample(self.characters, 3) # Prendi 3 personaggi unici
        obj = random.choice(self.objects)
        loc = random.choice(self.locations)
        
        return {
            "agent_1": chars[0],
            "agent_2": chars[1],
            "agent_3": chars[2],
            "object": obj,
            "true_location": loc,
            "initial_action": f"{chars[0]} nasconde {obj} {loc}."
        }

    def build_belief_chain(self, scenario: Dict, order: int) -> List[str]:
        """
        Costruisce la catena di eventi che genera le credenze false/vere.
        order: Livello di ToM richiesto (1 = Cosa pensa A?, 2 = Cosa pensa A che pensi B?, ecc.)
        """
        chain = []
        agents = [scenario['agent_1'], scenario['agent_2'], scenario['agent_3']]
        
        # Evento 1: Agente 1 nasconde l'oggetto (Tutti vedono o solo alcuni? Per ora assumiamo visibilità parziale)
        # Per semplicità procedurale iniziale:
        # 1. A nasconde l'oggetto in X. (B vede, C no) -> B sa dov'è, C no.
        # 2. A sposta l'oggetto in Y. (Nessuno vede) -> A sa che è in Y, B crede sia in X.
        
        current_loc = scenario['true_location']
        fake_loc = random.choice([l for l in self.locations if l != current_loc])
        
        events = []
        
        # Fase 1: Posizionamento iniziale (Visibile a tutti gli agenti coinvolti nella catena fino a quel punto)
        events.append(f"{scenario['agent_1']} mette {scenario['object']} {current_loc}.")
        
        # Fase 2: Manipolazione (Per creare falsa credenza)
        # Se l'ordine è >= 2, dobbiamo creare uno spostamento che qualcuno non vede.
        if order >= 2:
            # Agent 1 sposta l'oggetto mentre Agent 2 non guarda
            events.append(f"Mentre {scenario['agent_2']} è distratto, {scenario['agent_1']} sposta {scenario['object']} {fake_loc}.")
            # Ora: A sa che è in fake_loc. B crede che sia in current_loc.
            
        if order >= 3:
            # Agent 3 ha visto lo spostamento? O ha visto solo l'inizio?
            # Complichiamo: Agent 3 ha visto Agent 2 essere distratto, ma non ha visto lo spostamento.
            events.append(f"{scenario['agent_3']} ha visto {scenario['agent_2']} essere distratto, ma non ha visto lo spostamento.")
            
        return events

    def generate_question(self, scenario: Dict, order: int) -> Tuple[str, str]:
        """
        Genera la domanda ricorsiva e la risposta corretta.
        """
        agents = [scenario['agent_1'], scenario['agent_2'], scenario['agent_3']]
        obj = scenario['object']
        
        # Logica semplificata per la risposta corretta (Ground Truth)
        # Ordine 1: Dove pensa AGENTE_1 che sia l'oggetto? (Sa la verità)
        # Ordine 2: Dove pensa AGENTE_2 che AGENTE_1 pensi che sia? (Dipende da cosa ha visto)
        
        # Per questo prototipo, usiamo una logica standard di "False Belief":
        # A sa la verità (fake_loc se ha spostato).
        # B crede che sia nel luogo originale (current_loc).
        
        true_loc = scenario['true_location'] # Luogo iniziale
        # Nel nostro script semplice, supponiamo che A abbia spostato l'oggetto in un luogo segreto 'secret_loc'
        # Ma per mantenere la coerenza con build_belief_chain, definiamo qui la logica:
        
        # Semplificazione per demo:
        # Livello 1: Cosa pensa A? -> Sa dove l'ha messo ultimamente.
        # Livello 2: Cosa pensa B che A pensi? -> B non ha visto lo spostamento, quindi crede che A pensi sia al posto vecchio.
        
        # Nota: In una versione completa, questa logica deve essere un motore di stati formale.
        # Qui simuliamo il risultato per mostrare la struttura della domanda.
        
        question_parts = []
        current_subject = agents[0]
        
        # Costruzione frase ricorsiva
        # Esempio Order 3: "Dove pensa C che B pensi che A creda che sia l'oggetto?"
        subjects_chain = agents[:order] if order <= 3 else agents * (order // 3 + 1)
        subjects_chain = subjects_chain[:order]
        
        phrase = "Dove pensa "
        for i, agent in enumerate(subjects_chain):
            if i == len(subjects_chain) - 1:
                phrase += f"{agent} che si trovi {obj}?"
            else:
                phrase += f"{agent} che "
        
        # Calcolo risposta (Logica semplificata per il prototype)
        # Regola: Se l'ultimo agente della catena non ha visto lo spostamento, la risposta è il luogo originale.
        # Se l'ha visto, è il nuovo luogo.
        # Per ora, fissiamo: Odd orders -> True Location, Even orders -> False Location (per variare)
        # Questo va raffinato nel motore logico reale.
        
        answer = true_loc if order % 2 != 0 else "nel luogo originale (dove è stato visto per l'ultima volta)"

        return phrase, answer

    def generate_sample(self, order: int) -> Dict:
        """Genera un campione completo."""
        scenario = self.generate_scenario_base()
        events = self.build_belief_chain(scenario, order)
        question, answer = self.generate_question(scenario, order)
        
        return {
            "tom_order": order,
            "scenario_facts": events,
            "question": question,
            "correct_answer": answer,
            "metadata": scenario
        }

# --- Esecuzione Demo ---
if __name__ == "__main__":
    generator = RecursiveToMGenerator()
    
    print("--- GENERATORE RECURSIVE-TOM (PROTOTIPO) ---\n")
    
    for level in [1, 2, 3]:
        print(f"### LIVELLO ToM: {level} ###")
        sample = generator.generate_sample(level)
        
        print("Contesto:")
        for event in sample['scenario_facts']:
            print(f"- {event}")
        
        print(f"\nDomanda: {sample['question']}")
        print(f"Risposta Corretta (Ground Truth): {sample['correct_answer']}")
        print("-" * 40 + "\n")
