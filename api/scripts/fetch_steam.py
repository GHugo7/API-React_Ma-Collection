"""Génère data/items.json depuis Steam."""

import requests
import re
import time
import json
from pathlib import Path

# genres trop génériques pour servir de catégorie
EXCLUS = {"Free-to-play", "Utilitaires", "Accès anticipé", "Indépendant"}

def get_appids(pages: int = 20) -> list[int]:
    """Renvoie les appids des jeux les plus possédés, par pages de 1000."""
    appids: list[int] = []
    for page in range(pages):
        r = requests.get(f"https://steamspy.com/api.php?request=all&page={page}", timeout=30)
        if r.status_code != 200:
            print(f"SteamSpy page {page} : {r.status_code}, arrêt")
            break
        appids.extend(int(a) for a in r.json().keys())
        print(f"SteamSpy page {page} → {len(appids)} appids")

        # SteamSpy limite à 1 page par minute
        if page < pages - 1:
            time.sleep(60)
    return appids

def extraire(data: dict) -> dict | None:
    """Convertit une fiche Steam en item, ou None."""

    # 1. Ecarter les DLC, logiciels, demos
    if data.get("type") != "game":
        return None

    # 2. Ecarter ce qui n'a pas de genre
    genres = data.get("genres")
    if not genres:
        return None

    # 3. Ecarter ce qui n'a pas d'image ou de description
    if not data.get("header_image") or not data.get("short_description"):
        return None

    # 4. Premier genre qui n'est pas exclu
    noms = [g["description"] for g in genres]
    categorie = next((n for n in noms if n not in EXCLUS), noms[0])

    # 5. Extraire l'annee
    date_brute = data.get("release_date", {}).get("date", "")
    annee_match = re.search(r"\d{4}", date_brute)
    if not annee_match:
        return None

    # 6. Les plateformes : garder les clés dont la valeur est True
    plateformes = [nom for nom, actif in data.get("platforms" , {}).items() if actif]


    return {
        "titre": data["name"],
        "categorie": categorie,
        # description coupée à 400 caractères
        "description": data["short_description"].replace("\xa0", " ")[:400],
        "image_url": data.get("header_image", ""),
        "annee": int(annee_match.group()),
        "studio": (data.get("developers") or ["Inconnu"])[0],
        "plateforme": plateformes
    }

def get_games(appid: int) -> dict | None:
    """Télécharge la fiche d'un jeu."""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=french"
    try:
        response = requests.get(url, timeout=30)
    except requests.RequestException:
        return None

    # 429 = trop de requêtes, on prévient la boucle pour qu'elle attende
    if response.status_code == 429:
        raise RuntimeError("rate_limit")

    if response.status_code != 200:
        return None

    # réponse : {"<appid>": {"success": true, "data": {...}}}
    data = response.json()
    if not data:
        return None
    entree = next(iter(data.values()), None)
    if not entree or not entree.get("success"):
        return None

    return entree["data"]

if __name__ == "__main__":
    OBJECTIF = 20_000 
    path = Path(__file__).parent.parent / "data" / "items.json"

    # 1. reprendre là où on s'était arrêté
    items = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    titres_vus = {i["titre"] for i in items}
    print(f"Reprise avec {len(items)} items")

    # 2. récupérer les appids
    appids = get_appids(22)  # TEST : remettre get_appids()
    print(f"{len(appids)} appids à parcourir")

    # 3. télécharger et convertir chaque jeu
    for i, appid in enumerate(appids, 1):
        if len(items) >= OBJECTIF:
            break

        # réessayer tant que Steam renvoie un rate limit
        while True:
            try:
                data = get_games(appid)
                break
            except RuntimeError:
                print("rate limit, pause 60 s")
                time.sleep(60)

        if data:
            item = extraire(data)
            # éviter les doublons de titre
            if item and item["titre"] not in titres_vus:
                items.append(item)
                titres_vus.add(item["titre"])

                # sauvegarde tous les 25 items en cas de crash
                if len(items) % 25 == 0:
                    path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
                    print(f"[{i}/{len(appids)}] {len(items)} items — sauvegardé")

        time.sleep(1.5)

    # 4. écrire le fichier final
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(items)} items écrits dans {path}")
