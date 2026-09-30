"""Paramètres de pagination."""

from fastapi import Query

def pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
) -> tuple[int, int]:
    """Renvoie (page, limit)."""
    return page, limit