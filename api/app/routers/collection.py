from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.entry import EntryCreate, EntryOut, EntryUpdate, Statut, Tri
from app.schemas.stats import StatsOut
from app.models.entry import Entry
from app.models.user import User
from app.models.item import Item

router = APIRouter(prefix="/me", tags=["Collection"])

@router.get("/collection", response_model=list[EntryOut], summary="Ma collection")
async def get_user_collection(
    statut: Statut | None = None,
    tri: Tri = "date",
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
) -> list[Entry]:
    requete = select(Entry).where(Entry.user_id == user.id)

    if statut:
        requete = requete.where(Entry.statut == statut)

    requete = requete.order_by(
        Entry.note.desc() if tri == "note" else Entry.date_ajout.desc()
    )

    return list((await session.scalars(requete)).all())

@router.post("/collection", response_model=EntryOut, status_code=status.HTTP_201_CREATED, summary="Ajouter un élément à ma collection")
async def post_user_collection(
    data: EntryCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
) -> Entry:
    item = await session.get(Item, data.item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="L'élément est introuvable"
        )
    
    entry = Entry(user_id=user.id, **data.model_dump())

    try:
        session.add(entry)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="L'élément est deja present dans votre collection"
        )

    await session.refresh(entry)
    return entry

@router.patch("/collection/{entry_id}", response_model=EntryOut, summary="Modifier un élément de votre collection")
async def patch_user_collection(
    entry_id: int, 
    data: EntryUpdate, 
    user: User = Depends(get_current_user), 
    session: AsyncSession = Depends(get_db)
) -> Entry:
    entry = await session.scalar(
        select(Entry).where(Entry.id == entry_id, Entry.user_id == user.id)
    )

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrée introuvable",
        )

    for i, valeur in data.model_dump(exclude_unset=True).items():
        setattr(entry, i, valeur)

    await session.commit()
    await session.refresh(entry)
    
    return entry

@router.delete("/collection/{entry_id}",status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer un élément de votre collection")
async def delete_user_collection(
    entry_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
) -> None:
    entry = await session.scalar(
        select(Entry).where(Entry.id == entry_id, Entry.user_id == user.id)
    )

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrée introuvable"
        )

    await session.delete(entry)
    await session.commit()

@router.get("/stats", response_model=StatsOut, summary="Affiche vos stats")
async def get_user_stats(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
) -> StatsOut:
    total = await session.scalar(
        select(func.count()).select_from(Entry).where(Entry.user_id == user.id)
    )

    moyenne = await session.scalar(
        select(func.avg(Entry.note)).where(Entry.user_id == user.id)
    )

    lignes = await session.execute(
        select(Entry.statut, func.count()).where(Entry.user_id == user.id)
        .group_by(Entry.statut)
    )

    par_statut = {"a_decouvrir": 0, "en_cours": 0, "termine": 0}
    for statut, nombre in lignes:
        par_statut[statut] = nombre

    return StatsOut(
        total=total or 0,
        par_statut=par_statut,
        note_moyenne=round(float(moyenne), 2) if moyenne is not None else None,
    )