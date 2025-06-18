from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
from bs4 import BeautifulSoup
import os

app = FastAPI()

def scrape_foxes_news(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail=f"Impossible de récupérer les actus depuis {url}")

    soup = BeautifulSoup(response.text, "html.parser")
    actus = []

    # Exemple de sélecteurs à adapter selon la structure du site
    # Je me base sur une hypothèse, tu peux adapter avec un inspecteur HTML

    # Sur la home, supposons que les actus sont dans <section class="actualites"> et articles dans des div.article
    # Sur /news/, peut être des <article> ou div spécifiques

    # Pour faire simple, on cherche tous les articles/news dans une liste 
    articles = soup.select("article, .news-item, .actualite, .post")  # essayer plusieurs sélecteurs

    if not articles:
        # fallback : essayer un autre sélecteur spécifique à la page
        articles = soup.select(".news-list .news-item") 

    for article in articles[:5]:  # limiter à 5 actus max pour ne pas trop charger
        titre_el = article.select_one("h2, h3, .title")
        resume_el = article.select_one("p, .summary, .description")
        date_el = article.select_one(".date, time")
        image_el = article.select_one("img")

        titre = titre_el.text.strip() if titre_el else "Titre non disponible"
        resume = resume_el.text.strip() if resume_el else ""
        date = date_el.text.strip() if date_el else ""
        image_url = ""

        if image_el and image_el.has_attr("src"):
            image_url = image_el["src"]
            if not image_url.startswith("http"):
                image_url = f"https://www.foxesbasketball.ch{image_url}"

        actus.append({
            "titre": titre,
            "resume": resume,
            "date": date,
            "image_url": image_url
        })

    return actus

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Foxes"}

@app.get("/actus")
def get_actus():
    # Scrape page d'accueil
    actus_home = scrape_foxes_news("https://www.foxesbasketball.ch/")

    # Scrape page news complète
    actus_news = scrape_foxes_news("https://www.foxesbasketball.ch/news/")

    # On combine et on enlève les doublons éventuels (par titre)
    all_actus = actus_home + actus_news
    seen_titles = set()
    unique_actus = []
    for a in all_actus:
        if a["titre"] not in seen_titles:
            unique_actus.append(a)
            seen_titles.add(a["titre"])

    return {"actus": unique_actus}

@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
    manifest_path = os.path.join(os.path.dirname(__file__), ".well-known", "ai-plugin.json")
    if not os.path.exists(manifest_path):
        raise HTTPException(status_code=404, detail="Manifest plugin introuvable")
    return FileResponse(manifest_path, media_type="application/json")
