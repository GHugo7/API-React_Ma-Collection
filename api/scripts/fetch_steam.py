import requests
import re
import time
import json
from pathlib import Path

urlMostPlayed = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
EXCLUS = {"Free-to-play", "Utilitaires", "Accès anticipé", "Indépendant"}

def get_appids() -> list[int]:
    r = requests.get(urlMostPlayed)
    return [jeu["appid"] for jeu in r.json()["response"]["ranks"]]

def extraire(data: dict) -> dict | None:
    # 1. Ecarter les DLC, logiciels, demos
    if data.get("type") != "game":
        return None

    # 2. Ecarter ce qui n'a pas de genre
    genres = data.get("genres")
    if not genres:
        return None

    noms = [g["description"] for g in genres]
    categorie = next((n for n in noms if n not in EXCLUS), noms[0])

    # 3. Extraire l'annee
    date_brute = data.get("release_date", {}).get("date", "")
    annee_match = re.search(r"\d{4}", date_brute)
    if not annee_match:
        return None

    # 4. Les plateformes : garder les clés dont la valeur est True
    plateformes = [nom for nom, actif in data.get("platforms" , {}).items() if actif]
    

    return {
        "titre": data["name"],
        "categorie": categorie,
        "description": data.get("short_description", "").replace("\xa0", " "),
        "image_url": data.get("header_image", ""),
        "annee": int(annee_match.group()),
        "studio": (data.get("developers") or ["Inconnu"])[0],
        "plateforme": plateformes
    }

def get_games(appid: int) -> dict | None:
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=french"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    entree = next(iter(data.values()))
    if not entree.get("success"):
        return None

    return entree["data"]

if __name__ == "__main__":
    appids = get_appids()
    items = []

    for i, appid in enumerate(appids, 1):
        data = get_games(appid)
        if data:
            item = extraire(data)
            if item:
                items.append(item)
        print(f"[{i}/{len(appids)}] {len(items)} items valides")
        time.sleep(1)

    path = Path(__file__).parent.parent / "data" / "items.json"
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(items)} items ecrits dams {path}")