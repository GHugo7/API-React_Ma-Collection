"""Schémas des entrées de collection."""

from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from app.schemas.item import ItemOut

Statut = Literal["a_decouvrir", "en_cours", "termine"]
Tri = Literal["date", "note"]

class EntryCreate(BaseModel):
    item_id: int
    statut: Statut
    note: int | None = Field(default=None, ge=1, le=5)
    commentaire: str | None = Field(default=None, max_length=1000)

class EntryUpdate(BaseModel):
    statut: Statut | None = None
    note: int | None = Field(default=None, ge=1, le=5)
    commentaire: str | None = Field(default=None, max_length=1000)

class EntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    statut: Statut
    note: int | None
    commentaire: str | None
    date_ajout: datetime
    item: ItemOut