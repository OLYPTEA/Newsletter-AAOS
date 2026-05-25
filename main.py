#=======================================
# main.py - Autor : germainia17-dev
# =====================================


#-------------------------------------------------------------
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn
import uuid
from core.engine import HermesEngine

#-------------------------------------------------------------
app = FastAPI(title="Hermes Newsletter API")

# Stockage temporaire des tâches en cours (en mémoire pour la V1)
tasks_status = {}

#-------------------------------------------------------------
class UserPreferences(BaseModel):
    subject: str
    hour: str
    sources: str

@app.get("/")
async def root():
    return {"message": "Le serveur Hermes est opérationnel. Prêt pour la V2."}

def run_pipeline_task(task_id: str, prefs: UserPreferences):
    """
    Fonction exécutée en arrière-plan pour ne pas bloquer l'utilisateur.
    """
    try:
        # Mise à jour initiale du statut
        tasks_status[task_id] = {"status": "processing", "progress": "A1: Initialisation..."}

        user_prefs = {
            "type": prefs.subject,
            "hour": prefs.hour,
            "sources": prefs.sources
        }

        engine = HermesEngine()
        # On passe le task_id au moteur pour qu'il puisse mettre à jour le statut
        result = engine.run_pipeline(user_prefs, task_id=task_id)

        if result["status"] == "success":
            tasks_status[task_id] = {"status": "completed", "progress": "100%", "message": result["message"]}
        else:
            tasks_status[task_id] = {"status": "error", "progress": "Failed", "message": result["message"]}

    except Exception as e:
        tasks_status[task_id] = {"status": "error", "progress": "Error", "message": str(e)}

#-------------------------------------------------------------
@app.post("/generate")
async def generate_newsletter(prefs: UserPreferences, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks_status[task_id] = {"status": "pending", "progress": "Queuing..."}

    # On lance le pipeline en arrière-plan
    background_tasks.add_task(run_pipeline_task, task_id, prefs)

    return {
        "task_id": task_id,
        "message": "La création de votre newsletter a été lancée en arrière-plan.",
        "status_url": f"/status/{task_id}"
    }

#-------------------------------------------------------------
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks_status:
        raise HTTPException(status_code=404, detail="Tâche introuvable")

    return tasks_status[task_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
