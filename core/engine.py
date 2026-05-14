import os
import requests
from datetime import datetime

class HermesEngine:
    """
    Moteur d'orchestration du réseau Hermes.
    Gère le flux complet de A1 à A4 avec optimisation des modèles.
    """
    def __init__(self):
        # Configuration optimisée des modèles selon le rôle de l'agent
        # Modèles légers pour les tâches simples, puissants pour la création
        models = {
            "light": "llama3.2:1b",
            "strong": "llama3.1:8b"
        }

        # Importation différée des agents
        from agents.a1_interaction import AgentA1
        from agents.a2_research import AgentA2
        from agents.a3_redactor import AgentA3
        from agents.a5_supervisor import AgentA5
        from agents.a4_delivery import AgentA4

        self.agents = {
            "A1": AgentA1(), # Pas de modèle LLM direct dans l'init d'A1
            "A2": AgentA2(model_name=models["strong"]),
            "A3": AgentA3(model_name=models["strong"]),
            "A5": AgentA5(model_name=models["strong"]),
            "A4": AgentA4()
        }

    def run_pipeline(self, user_preferences, task_id=None):
        """
        Exécute le pipeline complet à partir de préférences utilisateur.
        Soutient la mise à jour du statut pour l'interface utilisateur.
        """
        def update_status(msg):
            if task_id:
                from main import tasks_status
                tasks_status[task_id]["progress"] = msg

        # Bypass de la collecte interactive de A1
        self.agents["A1"].user_data = user_preferences
        update_status("A1: Initialisation du brief...")
        self.agents["A1"].generate_brief()

        # Lancement de la chaîne
        update_status("A2: Recherche d'informations en cours...")
        self.agents["A2"].perform_research()

        update_status("A3: Rédaction de la newsletter...")
        self.agents["A3"].write_newsletter()

        update_status("A5: Supervision et contrôle qualité...")
        is_valid = self.agents["A5"].supervise()

        if is_valid:
            update_status("A4: Livraison et archivage...")
            self.agents["A4"].deliver()
            return {"status": "success", "message": "Newsletter générée et archivée."}
        else:
            return {"status": "error", "message": "La newsletter a été rejetée par le superviseur A5."}

if __name__ == "__main__":
    # Test rapide du moteur
    engine = HermesEngine()
    test_prefs = {"type": "IA", "hour": "08:00", "sources": "auto"}
    print(engine.run_pipeline(test_prefs))
