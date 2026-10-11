# Ma Collection

Application de suivi de jeux vidéo : un catalogue issu de Steam (environ 81 000 jeux) et une collection personnelle par utilisateur, avec statut (à découvrir, en cours, terminé), note et commentaire.

Le projet est séparé en deux dossiers, chacun avec son propre README détaillé :

- [`api/`](api/README.md) — API REST en FastAPI (authentification JWT, catalogue, collection, statistiques)
- [`web/`](web/README.md) — Front en React, qui consomme l'API

## Démarrage rapide

Les deux parties doivent tourner en parallèle, chacune dans son terminal.

```bash
# 1. l'API : PostgreSQL, dépendances, puis lancement — voir api/README.md
cd api
cp .env.example .env
docker compose up -d
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 2. une fois l'API lancée, dans un autre terminal : remplir le catalogue
cd api && source .venv/bin/activate
python seed.py

# 3. le front — voir web/README.md
cd web
cp .env.example .env
npm install
npm run dev
```

Le front est servi sur http://localhost:5173 et l'API sur http://localhost:8000 (documentation interactive sur `/docs`). Voir les README de chaque dossier pour le détail des variables d'environnement, des routes et de la structure du code.
