from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decoder_token
from app.db.database import get_db
from app.models.user import User

bearer = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
        session: AsyncSession = Depends(get_db),
) -> User:
    sub = decoder_token(credentials.credentials)

    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

    user = await session.get(User, int(sub))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

    return user