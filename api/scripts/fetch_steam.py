"""Génère data/items.json depuis Steam."""

import requests
import re
import time
import json
from pathlib import Path

# genres trop génériques pour servir de catégorie
EXCLUS = {"Free-to-play", "Utilitaires", "Accès anticipé", "Indépendant"}

# appids traités lors du premier run (arrêté à l'indice 20 650)
# sert à amorcer la reprise si appids_vus.json n'existe pas encore
DEJA_TRAITES = 20_650

def get_appids(pages: int | None = None) -> list[str]:
    """Récupère les appids depuis SteamSpy, page par page."""
    appids: list[str] = []
    page = 0

    while pages is None or page < pages:
        url = f"https://steamspy.com/api.php?request=all&page={page}"
        reponse = requests.get(url, timeout=30)

        if reponse.status_code != 200:
            print(f"page {page} : erreur {reponse.status_code}, arrêt")
            break

        data = reponse.json()
        if not data:
            print(f"page {page} vide, fin du catalogue")
            break

        appids.extend(data.keys())
        print(f"page {page} : {len(data)} appids (total {len(appids)})")

        page += 1
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
    plateformes = [nom for nom, actif in data.get("platforms", {}).items() if actif]

    return {
        "titre": data["name"].replace("\u2028", " ").replace("\u2029", " "),
        "categorie": categorie,
        # description coupée à 400 caractères
        "description": (
            data["short_description"]
            .replace("\xa0", " ")
            .replace("\u2028", " ")
            .replace("\u2029", " ")[:400]
        ),
        "image_url": data.get("header_image", ""),
        "annee": int(annee_match.group()),
        "studio": (data.get("developers") or ["Inconnu"])[0],
        "plateforme": plateformes
    }

def get_games(appid: str) -> dict | None:
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
    data_dir = Path(__file__).parent.parent / "data"
    path = data_dir / "items.json"
    vus_path = data_dir / "appids_vus.json"

    def sauvegarder(items: list[dict], appids_vus: set[str]) -> None:
        """Écrit les items et les appids déjà traités."""
        path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
        vus_path.write_text(json.dumps(sorted(appids_vus)), encoding="utf-8")

    # 1. reprendre là où on s'était arrêté
    items = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    titres_vus = {i["titre"] for i in items}

    # appids déjà interrogés, qu'ils aient donné un item ou non
    appids_vus: set[str] = set(json.loads(vus_path.read_text())) if vus_path.exists() else set()
    print(f"Reprise avec {len(items)} items et {len(appids_vus)} appids déjà traités")

    # 2. récupérer les appids (sans argument = tout le catalogue)
    appids = get_appids()
    print(f"{len(appids)} appids à parcourir")

    # 3. amorcer la reprise si le fichier n'existait pas encore
    #    les DEJA_TRAITES premiers appids sont ceux du premier run
    if not appids_vus and items:
        appids_vus = set(appids[:DEJA_TRAITES])
        sauvegarder(items, appids_vus)
        print(f"amorçage : {len(appids_vus)} appids marqués comme traités")

    # 4. télécharger et convertir chaque jeu
    for i, appid in enumerate(appids, 1):

        # déjà interrogé lors d'un run précédent, on passe sans requête
        if appid in appids_vus:
            continue

        # réessayer tant que Steam renvoie un rate limit
        while True:
            try:
                data = get_games(appid)
                break
            except RuntimeError:
                print("rate limit, pause 60 s")
                time.sleep(60)

        appids_vus.add(appid)

        if data:
            item = extraire(data)
            # éviter les doublons de titre
            if item and item["titre"] not in titres_vus:
                items.append(item)
                titres_vus.add(item["titre"])

                # sauvegarde tous les 500 items en cas de crash
                if len(items) % 500 == 0:
                    sauvegarder(items, appids_vus)
                    print(f"[{i}/{len(appids)}] {len(items)} items — sauvegardé")

        time.sleep(1.5)

    # 5. écrire les fichiers finaux
    sauvegarder(items, appids_vus)
    print(f"{len(items)} items écrits dans {path}")