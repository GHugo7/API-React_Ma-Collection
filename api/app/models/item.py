from app.models.base import Base
from sqlalchemy import String, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)

    titre: Mapped[str] = mapped_column(String(200), index=True)
    categorie: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(500))
    annee: Mapped[int] = mapped_column(index=True)

    plateforme: Mapped[list[str]] = mapped_column(ARRAY(String))
    studio: Mapped[str] = mapped_column(String(200))