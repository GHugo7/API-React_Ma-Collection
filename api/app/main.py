"""Point d'entrée de l'API."""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from collections.abc import AsyncGenerator

from app.db.database import engine
from app.core.config import settings
from app.models import Base
from app.routers import items, auth, collection
from app.core.exceptions import enregistrer_handlers

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Crée les tables au démarrage, ferme la connexion à l'arrêt."""

    # créer les tables si elles n'existent pas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    # fermer les connexions à l'arrêt
    await engine.dispose()

app = FastAPI(title="Ma Collection", lifespan=lifespan)

# autoriser le front React à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# brancher les routes
app.include_router(items.router)
app.include_router(auth.router)
app.include_router(collection.router)
enregistrer_handlers(app)