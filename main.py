from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/news")
def get_latest_news():
    url = "https://foxesbasketball.ch"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = soup.select("article")  # ⚠️ À adapter selon la structure réelle du site
    results = []

    for article in articles[:5]:
        titre = article.select_one("h2") or article.select_one("h3")
        extrait = article.select_one("p")
        if titre and extrait:
            results.append({
                "titre": titre.text.strip(),
                "extrait": extrait.text.strip()
            })

    return {"actus": results}
