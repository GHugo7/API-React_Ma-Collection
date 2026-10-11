# Front — Ma Collection

Interface web du projet Ma Collection : parcourir le catalogue de jeux, créer un compte, se connecter et gérer sa collection. Elle consomme l'API du dossier [`api/`](../api), qui doit tourner en parallèle.

**Stack** : React 19, TypeScript, Vite, React Router 7, Tailwind CSS 4.

## Prérequis

- Node.js 20.19+ ou 22.12+ (version exigée par Vite)
- L'API lancée et son catalogue rempli : voir le [README de l'API](../api/README.md)

## Installation et lancement

```bash
cd web
cp .env.example .env
npm install
npm run dev
```

L'application est servie sur http://localhost:5173. C'est l'origine autorisée par défaut côté API (`CORS_ORIGIN`). Si le port change, il faut aussi changer `CORS_ORIGIN` dans `api/.env`, sinon le navigateur bloque les appels.

| Script | Rôle |
|---|---|
| `npm run dev` | Serveur de développement avec rechargement à chaud |
| `npm run build` | Vérification TypeScript, puis build de production dans `dist/` |
| `npm run preview` | Sert le build de `dist/` en local |
| `npm run lint` | Lance ESLint |

## Variables d'environnement

| Variable | Rôle | Valeur dans `.env.example` |
|---|---|---|
| `VITE_API_URL` | URL de base de l'API, sans `/` final | `http://localhost:8000` |

Vite lit le `.env` au démarrage : après une modification, relancer `npm run dev`. La variable est typée dans `src/vite-env.d.ts`.

## Pages

| Route | Page | Accès |
|---|---|---|
| `/` | Catalogue : grille de jeux. Une fois connecté, le bouton « Ajouter » met le jeu dans la collection avec le statut « À découvrir ». | Public |
| `/register` | Création de compte (mot de passe de 8 caractères minimum, avec confirmation). Redirige vers `/login`. | Public |
| `/login` | Connexion. Redirige vers `/collection`. | Public |
| `/collection` | Ma collection, avec filtre par statut et tri par date d'ajout ou par note. | Connecté |
| autre | Page 404 | Public |

Toutes les pages partagent la barre de navigation (`pages/layout/Navbar.tsx`), qui affiche les liens de connexion et d'inscription, ou le bouton de déconnexion quand l'utilisateur est connecté.

## Authentification

- `/auth/login` renvoie un token JWT, stocké dans le `localStorage` sous la clé `authToken`.
- `AuthContext` expose `token`, `user`, `login()` et `logout()` via le hook `useAuth()`. Quand le token change, il recharge l'utilisateur avec `/auth/me`.
- `httpClient` lit le token et ajoute l'en-tête `Authorization: Bearer <token>` à chaque requête.
- `ProtectedRoute` redirige vers `/login` s'il n'y a pas de token.
- `logout()` supprime le token. Il n'y a pas d'appel à l'API : un JWT ne se révoque pas côté serveur, il expire au bout de `TOKEN_EXPIRE_MIN` minutes (30 par défaut).

## Appels à l'API

Les composants n'appellent jamais `fetch` directement : ils passent par les services de `src/services/`, qui utilisent tous `apiFetch` (`httpClient.ts`). `apiFetch` :

- préfixe le chemin par `VITE_API_URL` et envoie du JSON ;
- ajoute le token s'il existe ;
- en cas d'erreur, lève une `Error` dont le message est celui renvoyé par l'API (format `{"error": {"code", "message"}}`), qu'il suffit d'afficher ;
- renvoie `undefined` pour une réponse `204`.

| Service | Fonctions | Routes de l'API |
|---|---|---|
| `authService` | `login`, `register`, `me` | `/auth/login`, `/auth/register`, `/auth/me` |
| `itemsService` | `lister(page, limit, q?, categorie?)`, `byId(id)` | `GET /items`, `GET /items/{id}` |
| `collectionService` | `lister(statut?, tri?)`, `add`, `modify`, `del`, `stats` | `/me/collection`, `/me/collection/{id}`, `/me/stats` |

Les types des réponses (`Item`, `Entry`, `Stats`…) sont dans `src/types/api.ts` et reprennent les schémas Pydantic de l'API. Si un schéma change côté API, il faut mettre ce fichier à jour à la main.

## Structure

```
web/src/
├── main.tsx              # point d'entrée : BrowserRouter et AuthProvider
├── App.tsx               # déclaration des routes
├── index.css             # import de Tailwind
├── assets/img/           # images (favicon, page 404)
├── components/ui/        # composants réutilisables (Button)
├── contexts/             # AuthContext : token et utilisateur connecté
├── hooks/                # useLocalStorage
├── pages/                # une page par route, layout/ pour la barre de navigation
├── routes/               # ProtectedRoute
├── services/             # appels à l'API
└── types/api.ts          # types des données échangées avec l'API
```

Le composant `Button` accepte une prop `variante` (`primaire`, `secondaire` ou `danger`) en plus des props d'un `<button>` classique.
