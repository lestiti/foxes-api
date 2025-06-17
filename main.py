from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import json

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Foxes"}

@app.get("/actus")
def get_actus():
    return {"actus": ["Match du 20 juin", "Nouvel entraîneur annoncé"]}

@app.get("/.well-known/ai-plugin.json")
def get_manifest():
    return FileResponse(".well-known/ai-plugin.json", media_type="application/json")

@app.get("/openapi.json")
def custom_openapi():
    return FileResponse("openapi.json", media_type="application/json")
