import os
import requests
from datetime import datetime

class AgentA3:
    """
    A3: L'agent de rédaction et de direction artistique.
    Transforme research.md en contenu de newsletter.
    """
    def __init__(self, model_name="llama3.1:8b"):
        self.model_name = model_name
        self.brief_path = "brief.md"
        self.research_path = "research.md"
        self.output_path = "newsletter_draft.md"
        self.ollama_url = "http://localhost:11434/api/generate"

    def read_files(self):
        if not os.path.exists(self.brief_path) or not os.path.exists(self.research_path):
            print("[ERREUR A3] : Fichiers sources manquants.")
            return None, None

        with open(self.brief_path, "r", encoding="utf-8") as f:
            brief = f.read()
        with open(self.research_path, "r", encoding="utf-8") as f:
            research = f.read()
        return brief, research

    def call_llm(self, prompt):
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            print(f"[ERREUR LLM A3] : {e}")
            return ""

    def write_newsletter(self):
        brief, research = self.read_files()
        if not brief or not research: return

        print("\n✍️ A3 : Rédaction de la newsletter en cours...")

        prompt = f"""
        Tu es A3, l'agent de rédaction du réseau Hermes.

        BRIEF : {brief}
        RECHERCHES : {research}

        MISSION : Transforme ces recherches en une newsletter professionnelle.
        STRUCTURE OBLIGATOIRE :
        1. Titre Accrocheur
        2. Introduction synthétique
        3. Corps : Sections thématiques avec citations des sources (Source: Nom du média)
        4. Conclusion et appel à l'action.

        RÈGLES :
        - Langue : celle du brief.
        - Ton : Professionnel, factuel, accessible.
        - NE PAS inventer d'informations.
        - Neutralité totale.
        """

        content = self.call_llm(prompt)
        if content:
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Succès ! Brouillon généré : {self.output_path}")

if __name__ == "__main__":
    a3 = AgentA3()
    a3.write_newsletter()
