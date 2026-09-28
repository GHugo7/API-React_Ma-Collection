from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

import jwt
from datetime import datetime, timezone, timedelta

from app.core.config import settings

password_hash = PasswordHash((Argon2Hasher(),))


def hasher(passowrd: str) -> str:
    return password_hash.hash(passowrd)
    
def verifier(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)

def create_token(user: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.token_expire_min)

    payload = {
        "sub": user,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

def decoder_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except jwt.PyJWTError:
        return None

    sub = payload.get("sub")
    return sub if isinstance(sub, str) else None