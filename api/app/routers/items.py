"""Routes du catalogue."""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.item import Item
from app.schemas.item import ItemPage, ItemOut
from app.dependencies.pagination import pagination

from app.schemas.error import ErrorOut

router = APIRouter(prefix="/items", tags=["Catalogue"])

@router.get("", response_model=ItemPage, summary="Lister le catalogue")
async def lister_get(
    q: str | None = Query(None, min_length=2),
    categorie: str | None = None,
    page_limit: tuple[int, int] = Depends(pagination),
    session: AsyncSession = Depends(get_db),
) -> ItemPage:
    """Liste le catalogue avec recherche, filtre et pagination."""
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

@router.get("/{item_id}", response_model=ItemOut, summary="Fiche d'un item", responses={404: {"model": ErrorOut, "description": "Item introuvable"}})
async def get_item_by_id(item_id: int, session: AsyncSession = Depends(get_db)) -> Item:
    """Renvoie un jeu par son id."""
    item = await session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item introuvable"
        )
    
    return item