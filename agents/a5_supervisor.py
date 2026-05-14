import os
import requests

class AgentA5:
    """
    A5: L'agent superviseur.
    Vérifie la conformité de la newsletter avant livraison.
    """
    def __init__(self, model_name="llama3.1:8b"):
        self.model_name = model_name
        self.brief_path = "brief.md"
        self.research_path = "research.md"
        self.draft_path = "newsletter_draft.md"
        self.ollama_url = "http://localhost:11434/api/generate"

    def call_llm(self, prompt):
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            print(f"[ERREUR LLM A5] : {e}")
            return ""

    def supervise(self):
        if not os.path.exists(self.draft_path):
            print("[ERREUR A5] : Pas de brouillon à superviser.")
            return False

        with open(self.brief_path, "r", encoding="utf-8") as f: brief = f.read()
        with open(self.research_path, "r", encoding="utf-8") as f: research = f.read()
        with open(self.draft_path, "r", encoding="utf-8") as f: draft = f.read()

        print("\n🛡️ A5 : Supervision et contrôle qualité en cours...")

        prompt = f"""
        Tu es A5, le superviseur du réseau Hermes.

        BRIEF : {brief}
        RECHERCHES : {research}
        BROUILLON : {draft}

        Vérifie :
        1. Conformité au sujet.
        2. Neutralité politique.
        3. Présence des sources.
        4. Qualité rédactionnelle.

        Réponds UNIQUEMENT par :
        - "APPROUVÉ" si tout est parfait.
        - "REJETÉ : [raison précise]" si des corrections sont nécessaires.
        """

        decision = self.call_llm(prompt).strip().upper()

        if "APPROUVÉ" in decision:
            print("✅ A5 : Newsletter validée !")
            return True
        else:
            print(f"❌ A5 : Newsletter rejetée. Motif : {decision}")
            return False
