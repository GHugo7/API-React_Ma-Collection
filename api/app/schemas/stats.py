"""Schéma des statistiques."""

from pydantic import BaseModel

from app.schemas.entry import Statut

class StatsOut(BaseModel):
    total: int
    par_statut: dict[Statut, int]
    note_moyenne: float | None
