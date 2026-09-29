"""Table des utilisateurs."""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.models.base import Base

class User(Base):
    """Un compte utilisateur."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)

    # jamais le mot de passe en clair
    hashed_password: Mapped[str] = mapped_column(String(255))