from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.item import Item
from app.schemas.item import ItemPage
from app.dependencies.pagination import pagination

router = APIRouter(prefix="/items", tags=["Catalogue"])

@router.get("", response_model=ItemPage, summary="Lister le catalogue")
async def lister_get(
    q: str | None = Query(None, min_length=2),
    categorie: str | None = None,
    page_limit: tuple[int, int] = Depends(pagination),
    session: AsyncSession = Depends(get_db),
    ) -> ItemPage:
    page, limit = page_limit

    # 1. construire la requête avec les filtres
    requete = select(Item)
    if q:
        requete = requete.where(Item.titre.ilike(f"%{q}%"))
    if categorie:
        requete = requete.where(Item.categorie == categorie)

    # 2. compter avant de paginer
    total_req = select(func.count()).select_from(requete.subquery())
    total = (await session.execute(total_req)).scalar_one()

    # 3. paginer puis exécuter
    requete = requete.offset((page - 1) * limit).limit(limit)
    items = (await session.execute(requete)).scalars().all()

    return ItemPage(total=total, page=page, limit=limit, results=items)