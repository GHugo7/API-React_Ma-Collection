# API — Ma Collection

API REST du projet Ma Collection : un catalogue de jeux vidéo issu de Steam, et une collection personnelle par utilisateur (statut, note, commentaire). Elle est utilisée par le front React du dossier [`web/`](../web).

**Stack** : FastAPI, SQLAlchemy 2 (async) avec psycopg 3, PostgreSQL 16 (Docker), Pydantic v2, JWT (PyJWT), hachage Argon2 (pwdlib).

## Prérequis

- Python 3.12 ou plus (développé avec 3.14)
- Docker et Docker Compose, pour PostgreSQL

## Installation et lancement

Lancer toutes les commandes depuis le dossier `api/` : l'application et Docker Compose lisent le fichier `.env` du dossier courant.

### 1. Configurer l'environnement

```bash
cd api
cp .env.example .env
```

Dans `.env`, remplacer les placeholders de `DATABASE_URL` par les valeurs `POSTGRES_*`. Avec les valeurs par défaut :

```env
DATABASE_URL=postgresql+psycopg://macollection:macollection@localhost:5432/macollection
```

Remplacer aussi `SECRET_KEY`, qui signe les tokens. Pour générer une clé :

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Démarrer PostgreSQL

```bash
docker compose up -d
```

### 3. Installer les dépendances

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Lancer l'API

```bash
uvicorn app.main:app --reload
```

L'API écoute sur http://localhost:8000, l'adresse attendue par le front (`VITE_API_URL` dans `web/.env`). Au démarrage, elle crée les tables qui n'existent pas encore.

Documentation interactive : http://localhost:8000/docs (Swagger) et http://localhost:8000/redoc.

### 5. Remplir le catalogue

L'API doit avoir été lancée au moins une fois, pour que les tables existent. Dans un autre terminal, avec le venv activé :

```bash
python seed.py
```

Le script insère les jeux de `data/items.json` qui ne sont pas encore en base (comparaison sur le titre). On peut le relancer sans créer de doublons.

## Variables d'environnement

| Variable | Lue par | Rôle | Défaut |
|---|---|---|---|
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Docker | Base et compte créés par le conteneur | — |
| `POSTGRES_PORT` | Docker | Port de PostgreSQL sur la machine | — |
| `DATABASE_URL` | API | URL de connexion SQLAlchemy (driver `postgresql+psycopg`) | obligatoire |
| `SECRET_KEY` | API | Clé de signature des JWT | obligatoire |
| `ALGORITHM` | API | Algorithme de signature des JWT | `HS256` |
| `TOKEN_EXPIRE_MIN` | API | Durée de validité d'un token, en minutes | `30` |
| `CORS_ORIGIN` | API | Origine autorisée à appeler l'API (le serveur Vite) | `http://localhost:5173` |

## Endpoints

Les routes marquées « oui » dans la colonne Auth demandent l'en-tête `Authorization: Bearer <token>`, avec le token renvoyé par `/auth/login`. Le token expire après `TOKEN_EXPIRE_MIN` minutes.

### Authentification

| Méthode | Route | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | | Crée un compte. Corps : `{"email", "password"}`, mot de passe de 8 caractères minimum. Renvoie `201` avec `{"id", "email"}`, ou `409` si l'e-mail est déjà utilisé. |
| `POST` | `/auth/login` | | Corps : `{"email", "password"}`. Renvoie `{"access_token", "token_type": "bearer"}`, ou `401` si les identifiants sont invalides. |
| `GET` | `/auth/me` | oui | Renvoie l'utilisateur connecté : `{"id", "email"}`. |

### Catalogue

| Méthode | Route | Auth | Description |
|---|---|---|---|
| `GET` | `/items` | | Liste paginée du catalogue. Renvoie `{"total", "page", "limit", "results"}`. |
| `GET` | `/items/{item_id}` | | Fiche d'un jeu, ou `404`. |

Paramètres de `GET /items` :

| Paramètre | Description | Défaut |
|---|---|---|
| `q` | Recherche dans le titre, insensible à la casse (2 caractères minimum) | — |
| `categorie` | Filtre sur la catégorie exacte (ex. `Action`) | — |
| `page` | Numéro de page, à partir de 1 | `1` |
| `limit` | Nombre de jeux par page, de 1 à 50 | `12` |

### Collection

| Méthode | Route | Auth | Description |
|---|---|---|---|
| `GET` | `/me/collection` | oui | Liste mes entrées. Paramètres : `statut` (filtre) et `tri` = `date` (défaut, ajout le plus récent d'abord) ou `note` (note décroissante, jeux sans note en dernier). |
| `POST` | `/me/collection` | oui | Ajoute un jeu. Corps : `{"item_id", "statut", "note", "commentaire"}`, `note` et `commentaire` facultatifs. Renvoie `201`, `404` si le jeu n'existe pas, `409` s'il est déjà dans la collection. |
| `PATCH` | `/me/collection/{entry_id}` | oui | Modifie seulement les champs envoyés parmi `statut`, `note`, `commentaire`. `404` si l'entrée n'existe pas ou appartient à un autre utilisateur. |
| `DELETE` | `/me/collection/{entry_id}` | oui | Supprime l'entrée. Renvoie `204`, ou `404`. |
| `GET` | `/me/stats` | oui | Renvoie `{"total", "par_statut", "note_moyenne"}`. `note_moyenne` vaut `null` si aucun jeu n'est noté. |

Valeurs acceptées :

- `statut` : `a_decouvrir`, `en_cours` ou `termine`
- `note` : entier de 1 à 5, ou `null`
- `commentaire` : 1000 caractères maximum, ou `null`

Une entrée renvoyée par l'API contient le jeu complet :

```json
{
  "id": 1,
  "statut": "en_cours",
  "note": 4,
  "commentaire": "Très bon",
  "date_ajout": "2026-10-11T14:32:00",
  "item": {
    "id": 1,
    "titre": "Counter-Strike 2",
    "categorie": "Action",
    "description": "Counter-Strike, c'est l'expérience compétitive par excellence…",
    "image_url": "https://shared.akamai.steamstatic.com/…/header.jpg",
    "annee": 2012,
    "plateforme": ["windows", "linux"],
    "studio": "Valve"
  }
}
```

### Exemple avec curl

```bash
# créer un compte
curl -X POST localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "motdepasse"}'

# se connecter et garder le token
TOKEN=$(curl -s -X POST localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "motdepasse"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# ajouter le jeu 1 à sa collection
curl -X POST localhost:8000/me/collection \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"item_id": 1, "statut": "en_cours"}'
```

Dans Swagger (`/docs`), le bouton **Authorize** attend le token seul, sans le préfixe `Bearer`.

## Format des erreurs

Toutes les erreurs, HTTP comme validation, ont la même forme :

```json
{ "error": { "code": 404, "message": "Item introuvable" } }
```

Pour une erreur de validation (`422`), le message ne donne que le premier champ en erreur, par exemple `"password : String should have at least 8 characters"`.

| Code | Cas |
|---|---|
| `401` | Token absent, invalide ou expiré ; identifiants de connexion faux |
| `404` | Jeu ou entrée introuvable |
| `409` | E-mail déjà utilisé ; jeu déjà dans la collection |
| `422` | Corps ou paramètres invalides |

## Base de données

| Table | Contenu |
|---|---|
| `items` | Catalogue : `titre`, `categorie`, `description`, `image_url`, `annee`, `plateforme` (tableau), `studio` |
| `users` | Comptes : `email` (unique), `hashed_password` (Argon2, jamais le mot de passe en clair) |
| `collection_entries` | Collections : `user_id`, `item_id`, `statut`, `note`, `commentaire`, `date_ajout`. Un même jeu ne peut être ajouté qu'une fois par utilisateur. |

Il n'y a pas de migrations : les tables sont créées par `Base.metadata.create_all` au démarrage de l'API, qui ne modifie jamais une table existante. Après un changement dans un modèle, il faut repartir d'une base vide, puis relancer l'API et `seed.py` :

```bash
docker compose down -v   # supprime le volume, donc toutes les données
docker compose up -d
```

## Le catalogue Steam

`data/items.json` (environ 81 000 jeux, 38 Mo) est versionné : il n'est pas nécessaire de le régénérer. Il a été produit par `scripts/fetch_steam.py`, qui :

1. récupère la liste des appids sur l'API SteamSpy, une page de 1 000 par minute ;
2. télécharge la fiche de chaque jeu sur l'API du Steam Store, en français, avec une requête toutes les 1,5 s et une pause de 60 s quand Steam renvoie `429` ;
3. garde seulement les jeux qui ont un genre, une image, une description et une année de sortie. La catégorie est le premier genre qui n'est pas Free-to-play, Utilitaires, Accès anticipé ou Indépendant. La description est coupée à 400 caractères et les titres en double sont écartés.

```bash
python scripts/fetch_steam.py
```

Le script sauvegarde tous les 500 jeux et reprend là où il s'était arrêté grâce à `data/appids_vus.json` (non versionné). Un parcours complet prend plusieurs dizaines d'heures.

## Structure

```
api/
├── app/
│   ├── main.py             # création de l'app, CORS, routers, création des tables
│   ├── core/               # configuration (.env), sécurité (Argon2, JWT), format des erreurs
│   ├── db/                 # moteur async et session par requête
│   ├── dependencies/       # utilisateur connecté, pagination
│   ├── models/             # tables SQLAlchemy : User, Item, Entry
│   ├── routers/            # routes : auth, items, collection
│   └── schemas/            # schémas Pydantic des entrées et sorties
├── data/items.json         # catalogue de jeux Steam
├── scripts/fetch_steam.py  # génération de data/items.json
├── seed.py                 # import de data/items.json en base
├── docker-compose.yml      # PostgreSQL 16
└── requirements.txt
```
