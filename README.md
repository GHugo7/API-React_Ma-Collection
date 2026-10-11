<div align="center">

# 🎮 Ma Collection

**Ludothèque personnelle adossée au catalogue Steam**

Un catalogue de **81 164 jeux** répartis en **27 catégories**, et une collection
personnelle par utilisateur — statut, note, commentaire.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL%2016-4169E1?logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React%2019-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind%204-06B6D4?logo=tailwindcss&logoColor=white)

</div>

---

## Le projet

Deux applications indépendantes dans un seul dépôt :

| Dossier | Rôle | Documentation |
|---|---|---|
| [`api/`](api/) | API REST FastAPI — authentification JWT, catalogue, collection, statistiques | [api/README.md](api/README.md) |
| [`web/`](web/) | Interface React qui consomme l'API | [web/README.md](web/README.md) |

### Fonctionnalités

- **Catalogue public** — grille de jeux issus de Steam, consultable sans compte, avec pagination et recherche par titre
- **Comptes** — inscription, connexion, déconnexion, mots de passe hachés en Argon2
- **Collection personnelle** — ajout depuis le catalogue, statut (à découvrir / en cours / terminé), note de 1 à 5, commentaire
- **Filtre et tri** — par statut, par date d'ajout ou par note
- **Statistiques** — total, répartition par statut, note moyenne
- **Isolation stricte** — un utilisateur ne voit et ne modifie que sa propre collection, vérifié côté serveur

### Le catalogue

Les données ne viennent pas d'une API appelée à la volée : elles ont été collectées en amont par [`api/scripts/fetch_steam.py`](api/scripts/fetch_steam.py), qui interroge SteamSpy pour la liste des appids puis le Steam Store pour chaque fiche. Le script est reprenable après interruption et sauvegarde tous les 500 jeux — une collecte complète a demandé **32 heures** pour 94 % de conversion.

Le résultat, `api/data/items.json` (37 Mo), est versionné : il n'y a rien à régénérer.

---

## Stack

**Backend** — FastAPI · SQLAlchemy 2 en asynchrone · psycopg 3 · PostgreSQL 16 (Docker) · Pydantic v2 · PyJWT · Argon2 via pwdlib

**Frontend** — React 19 · TypeScript en `strict` · Vite · React Router 7 · Tailwind CSS 4 · aucune librairie de composants

---

## Prérequis

- Python 3.12 ou plus
- Node.js 20.19+ ou 22.12+
- Docker et Docker Compose

---

## Démarrage rapide

Les deux parties tournent en parallèle, chacune dans son terminal.

### 1. L'API

```bash
cd api
cp .env.example .env
```

Renseigner `DATABASE_URL` et `SECRET_KEY` dans `.env` — voir [api/README.md](api/README.md) pour le détail. Pour générer une clé :

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Puis :

```bash
docker compose up -d
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

L'API écoute sur **http://localhost:8000** — documentation interactive sur [`/docs`](http://localhost:8000/docs).

### 2. Remplir le catalogue

L'API doit avoir été lancée au moins une fois, pour que les tables existent. Dans un autre terminal :

```bash
cd api && source .venv/bin/activate
python seed.py
```

Le script est idempotent : on peut le relancer sans créer de doublons.

### 3. Le front

```bash
cd web
cp .env.example .env
npm install
npm run dev
```

L'interface est servie sur **http://localhost:5173**.

---

## Architecture

```
.
├── api/
│   ├── app/
│   │   ├── core/           # configuration, sécurité (Argon2, JWT), format d’erreur
│   │   ├── db/             # moteur async, session par requête
│   │   ├── dependencies/   # utilisateur courant, pagination
│   │   ├── models/         # tables SQLAlchemy
│   │   ├── routers/        # auth, items, collection
│   │   └── schemas/        # schémas Pydantic
│   ├── data/items.json     # catalogue Steam
│   ├── scripts/            # collecte des données
│   └── seed.py             # import en base
└── web/src/
    ├── components/ui/      # composants réutilisables
    ├── contexts/           # AuthContext
    ├── hooks/              # useLocalStorage (générique)
    ├── pages/              # une page par route
    ├── routes/             # routes protégées
    ├── services/           # client HTTP unique + un service par domaine
    └── types/api.ts        # types du contrat d’API, écrits à la main
```

Deux principes structurants :

- **Un seul point de sortie réseau.** Tous les appels passent par `apiFetch` dans [`web/src/services/httpClient.ts`](web/src/services/httpClient.ts), qui ajoute le token, traduit le format d'erreur de l'API en `Error` affichable et gère les réponses `204`. Aucun `fetch` ailleurs dans le code.
- **Aucun `any`.** Le typage repose sur `unknown` suivi de vérifications explicites — notamment un type guard pour distinguer une erreur de l'API d'une réponse valide.

---

## Sécurité

- Mots de passe hachés en **Argon2id**, jamais stockés ni journalisés en clair, absents de tous les `response_model`
- Clé de signature JWT hors du dépôt, token à durée de vie courte
- CORS restreint à l'origine du serveur de développement
- Requêtes construites avec l'ORM, jamais par concaténation de chaînes
- Propriété d'une entrée vérifiée côté serveur sur chaque route `/me/*` : masquer un bouton dans l'interface ne protège rien

---

## Limites connues

- Le garde de route vérifie la présence du token, pas sa validité — un token expiré passe la barrière et c'est l'API qui répond `401`
- Pas de migrations : les tables sont créées au démarrage, un changement de modèle demande de repartir d'une base vide
- Le token est stocké en `localStorage`, donc exposé au XSS ; un cookie `httpOnly` serait plus sûr, au prix d'une protection CSRF à ajouter

---

<div align="center">
<sub>Projet transversal · Bachelor Informatique · Ynov Campus Bordeaux</sub>
</div>