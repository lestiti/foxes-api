from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Foxes"}

@app.get("/.well-known/ai-plugin.json")
def get_plugin_manifest():
    return JSONResponse({
        "schema_version": "v1",
        "name_for_human": "FOXES Actus API",
        "name_for_model": "foxesApi",
        "description_for_human": "Accède aux actualités et à la page d’accueil du site foxesbasketball.ch",
        "description_for_model": "Utilise cette API pour récupérer les dernières nouvelles des Foxes et le titre de la page d’accueil.",
        "auth": {"type": "none"},
        "api": {
            "type": "openapi",
            "url": "https://foxes-api.onrender.com/openapi.json",
            "is_user_authenticated": False
        },
        "logo_url": "https://upload.wikimedia.org/wikipedia/fr/thumb/5/5b/Foxes_Logo_Basketball.svg/800px-Foxes_Logo_Basketball.svg.png",
        "contact_email": "support@foxesbasketball.ch",
        "legal_info_url": "https://foxesbasketball.ch/legal"
    })
