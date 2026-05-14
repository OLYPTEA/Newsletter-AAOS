import requests

class PixelBridge:
    """
    Pont de communication entre le cerveau Hermes et l'interface Pixel Agents.
    Envoie des signaux pour animer les personnages en 2D.
    """
    def __init__(self, port=5173):
        self.url = f"http://localhost:{port}/api/agent-action"

    def send_action(self, agent_id, action):
        """
        Envoie une action à un agent spécifique dans le monde Pixel.
        agent_id: 'A1', 'A2', etc.
        action: 'searching', 'writing', 'supervising', 'delivering', 'idle'
        """
        payload = {
            "agentId": agent_id,
            "action": action,
            "timestamp": "" # géré par le serveur
        }
        try:
            # On utilise un timeout très court pour ne pas ralentir le cerveau
            requests.post(self.url, json=payload, timeout=0.2)
        except:
            # On ignore les erreurs pour ne pas bloquer le pipeline principal
            pass

# Instance unique pour tout le projet
bridge = PixelBridge()
