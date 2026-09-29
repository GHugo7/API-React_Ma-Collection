"""Connexion à la base de données."""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from collections.abc import AsyncGenerator
from app.core.config import settings

# connexion à la base
engine = create_async_engine(settings.database_url)

# fabrique de sessions
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Creation d'une session vers la db
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Fournit une session par requête."""
    async with SessionLocal() as db:
        yield db