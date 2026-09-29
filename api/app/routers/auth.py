"""Routes d'authentification."""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hasher, verifier, create_token
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import UserOut, RegisterIn, TokenOut, LoginIn
from app.dependencies.auth import get_current_user

from app.schemas.error import ErrorOut

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un compte",
    responses={409: {"model": ErrorOut, "description": "E-mail déjà utilisé"}}
)
async def register(
    data: RegisterIn,
    session: AsyncSession = Depends(get_db)
) -> User:
    """Crée un compte."""

    # 1. vérifier que l'e-mail est libre
    existant = await session.scalar(select(User).where(User.email == data.email))

    if existant is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cet e-mail est déjà utilisé"
        )

    # 2. créer l'utilisateur avec le mot de passe haché
    user = User(email=data.email, hashed_password=hasher(data.password))

    # 3. enregistrer en base
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

@router.post(
    "/login",
    response_model=TokenOut,
    summary="Connecter un compte",
    responses={401: {"model": ErrorOut, "description": "Identifiants invalides"}}
)
async def login(data: LoginIn, session: AsyncSession = Depends(get_db)) -> TokenOut:
    """Connecte l'utilisateur et renvoie un token."""
    user = await session.scalar(select(User).where(User.email == data.email))

    # même message si l'e-mail ou le mot de passe est faux
    if user is None or not verifier(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )

    return TokenOut(access_token=create_token(str(user.id)))

@router.get("/me", response_model=UserOut, summary="Utilisateur courant", responses={401: {"model": ErrorOut, "description": "Token invalide ou expiré"}})
async def me(user: User = Depends(get_current_user)) -> User:
    """Renvoie l'utilisateur connecté."""
    return user