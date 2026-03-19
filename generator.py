import random
import json

class SocialScenarioGenerator:
    def __init__(self):
        self.roles = ["CEO", "Spia Industriale", "Collezionista", "Avvocato", "Medico", "Giornalista"]
        self.objects = ["prototipo segreto", "documento riservato", "chiave crittografata", "diamante raro", "testamento nascosto"]
        self.locations = ["ufficio blindato", "asta privata", "caffetteria affollata", "server remoto", "cassaforte di famiglia"]
        self.actions = ["nascondere", "scambiare", "distruggere", "fingere di possedere", "rubare"]
        
        # Template per diversi ordini di ToM
        self.templates = {
            1: "{A} ha {action} il {object} nel {location}. {B} non ha visto l'azione. Dove pensa {B} che sia il {object}?",
            2: "{A} sa che {B} non ha visto l'azione di {action} il {object}. {A} vuole ingannare {B}. Cosa dirà {A} a {C} riguardo al {object}?",
            3: "{C} sospetta che {A} stia mentendo a {B} sul {object}. {C} sa che {A} conosce la vera posizione ({location}). Cosa penserà {C} che {B} farà?",
            4: "{D} osserva l'interazione tra {A}, {B} e {C}. {D} sa che tutti stanno nascondendo qualcosa sul {object}. Qual è la strategia ottimale per {D} per scoprire la verità senza essere scoperto?"
        }

    def generate_scenario(self, tom_order):
        # Selezione casuale degli attori per garantire variabilità
        actors = random.sample(self.roles, 4) 
        scenario_data = {
            "A": actors[0],
            "B": actors[1],
            "C": actors[2],
            "D": actors[3],
            "object": random.choice(self.objects),
            "location": random.choice(self.locations),
            "action": random.choice(self.actions),
            "tom_order": tom_order
        }
        
        # Costruzione del testo narrativo
        prompt_text = self.templates[tom_order].format(**scenario_data)
        
        # Aggiunta di contesto "rumore" per rendere il task più realistico (opzionale)
        noise = f"\nContesto: È una giornata di pioggia a Napoli, vicino ai Campi Flegrei c'è tensione. Tutti sono distratti."
        
        return {
            "id": f"TOM{tom_order}_{random.randint(1000,9999)}",
            "prompt": prompt_text + noise,
            "ground_truth": self._calculate_ground_truth(scenario_data, tom_order),
            "metadata": scenario_data
        }

    def _calculate_ground_truth(self, data, order):
        # Logica semplificata per la risposta corretta (da espandere in base alla complessità)
        if order == 1:
            return f"{data['B']} pensa che il {data['object']} sia ancora nella sua posizione originale o ignora il {data['location']}."
        elif order == 2:
            return f"{data['A']} dirà una falsità a {data['C']} per proteggere il segreto."
        elif order == 3:
            return f"{data['C']} prevede che {data['B']} agirà basandosi sull'informazione falsa di {data['A']}."
        else:
            return f"{data['D']} deve orchestrare una situazione dove la verità emerge indirettamente."

# Esempio di utilizzo rapido
if __name__ == "__main__":
    gen = SocialScenarioGenerator()
    print(json.dumps(gen.generate_scenario(3), indent=2))
