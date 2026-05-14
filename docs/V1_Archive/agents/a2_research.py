import os
import json
import requests
from datetime import datetime

class AgentA2:
    """
    A2: L'agent de recherche du réseau Hermes Newsletter.
    Il lit le brief.md et génère un research.md avec des données brutes.
    """
    def __init__(self, model_name="llama3.1:8b"):
        self.model_name = model_name
        self.brief_path = "brief.md"
        self.research_path = "research.md"
        self.ollama_url = "http://localhost:11434/api/generate"

    def read_brief(self):
        if not os.path.exists(self.brief_path):
            print("[ERREUR A2] : brief.md introuvable. A1 doit être exécuté d'abord.")
            return None

        with open(self.brief_path, "r", encoding="utf-8") as f:
            return f.read()

    def call_llm(self, prompt):
        """Appel au modèle local via Ollama"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            print(f"[ERREUR LLM] : Impossible de contacter le modèle {self.model_name} : {e}")
            return ""

    def perform_research(self):
        brief_content = self.read_brief()
        if not brief_content:
            return

        print(f"\n🔍 A2 : Recherche en cours pour le sujet défini dans le brief...")

        # Construction du prompt basé sur ton instruction système A2
        prompt = f"""
        Tu es A2, l'agent de recherche du réseau Hermes Newsletter.

        Ceci est le brief de l'utilisateur :
        {brief_content}

        MISSION :
        Effectuer une recherche simulée exhaustive et neutre.
        Génère le contenu du fichier research.md en respectant STRICTEMENT la structure suivante :

        # Recherche Newsletter — [Sujet]
        ## Métadonnées
        - Sujet : [Sujet]
        - Date de recherche : {datetime.now().strftime('%Y-%m-%d %H:%M')}
        - Sources consultées : [Liste des domaines]

        ## Résultats bruts
        ### Info 1
        - Titre : [Titre]
        - Source : [Nom du média]
        - URL : [URL]
        - Date de publication : [Date]
        - Contenu brut : [Résumé factuel 3-5 lignes]

        (Répète pour 5 à 10 informations significatives)

        RÈGLES :
        - Ne rédige pas de phrases de transition.
        - Pas de prise de position politique.
        - Reste purement factuel.
        """

        research_data = self.call_llm(prompt)

        if research_data:
            with open(self.research_path, "w", encoding="utf-8") as f:
                f.write(research_data)
            print(f"✅ Succès ! Le fichier {self.research_path} a été généré.")
        else:
            print("[ERREUR A2] : Échec de la génération des recherches.")

if __name__ == "__main__":
    a2 = AgentA2()
    a2.perform_research()
