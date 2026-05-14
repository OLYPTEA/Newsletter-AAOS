import os
from typing import List
from utils.visualizer import bridge

class AgentA1:
    """
    A1: L'agent d'interaction du réseau Hermes Newsletter.
    Il collecte les préférences utilisateur pour générer le brief.md.
    """
    def __init__(self):
        self.user_data = {
            "type": None,
            "hour": None,
            "sources": None
        }
        self.brief_path = "brief.md"

    def collect_info(self):
        bridge.send_action("A1", "interacting")
        print("\n--- 📨 Configuration de votre Newsletter Automatisée ---")

        # Étape 1 : Type de newsletter
        print("\n1. Quel type de newsletter voulez-vous automatiser ?")
        print("(Ex: Finance, IA, Tech, Cryptos, Santé, ou un sujet personnalisé)")
        self.user_data["type"] = input("Votre réponse : ")

        # Étape 2 : Heure de réception
        print("\n2. À quelle heure voulez-vous recevoir votre newsletter chaque jour ?")
        print("(ex: 07h00, demain matin, etc.)")
        self.user_data["hour"] = input("Votre réponse : ")

        # Étape 3 : Sources préférées
        print("\n3. Avez-vous des sources ou sites d'information préférés ?")
        print("(ex: Bloomberg, Wired, Le Monde. Si vous ne savez pas, tapez 'non' ou 'auto')")
        sources_input = input("Votre réponse : ")
        self.user_data["sources"] = "auto (fiables et récentes)" if sources_input.lower() in ["non", "peu importe", "auto"] else sources_input

        # Étape 4 : Confirmation
        self.confirm_and_generate()

    def confirm_and_generate(self):
        print("\n--- 📋 RÉCAPITULATIF ---")
        print(f"Sujet : {self.user_data['type']}")
        print(f"Heure : {self.user_data['hour']}")
        print(f"Sources : {self.user_data['sources']}")

        confirm = input("\nEst-ce que tout est correct ? (oui/non) : ")

        if confirm.lower() == "oui":
            self.generate_brief()
        else:
            print("Redémarrons la collecte...")
            self.collect_info()

    def generate_brief(self):
        content = f"""# Brief de Configuration Hermes Newsletter

## Paramètres de l'Utilisateur
- **Sujet principal** : {self.user_data['type']}
- **Heure de livraison souhaitée** : {self.user_data['hour']}
- **Sources à prioriser** : {self.user_data['sources']}

## Instructions pour A2 (Recherche)
Effectuer une recherche exhaustive sur le sujet ci-dessus en respectant la date et les sources indiquées.
"""
        with open(self.brief_path, "w", encoding="utf-8") as f:
            f.write(content)

        bridge.send_action("A1", "idle")
        print(f"\n✅ Succès ! Le fichier {self.brief_path} a été généré.")
        print("A2 peut maintenant prendre le relais.")

if __name__ == "__main__":
    a1 = AgentA1()
    a1.collect_info()
