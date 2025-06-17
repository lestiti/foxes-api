from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Foxes"}

@app.get("/actus")
def get_actus():
    return {"actus": ["Match du 20 juin", "Nouvel entraîneur annoncé"]}

# 👉 Route pour servir le fichier ai-plugin.json
@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
    return FileResponse(".well-known/ai-plugin.json", media_type="application/json")
