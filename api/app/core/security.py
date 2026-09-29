"""Hachage des mots de passe et tokens JWT."""

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

import jwt
from datetime import datetime, timezone, timedelta

from app.core.config import settings

# hachage avec Argon2
password_hash = PasswordHash((Argon2Hasher(),))


def hasher(password: str) -> str:
    """Hache un mot de passe."""
    return password_hash.hash(password)
    
def verifier(password: str, hashed: str) -> bool:
    """Vérifie un mot de passe avec son hash."""
    return password_hash.verify(password, hashed)

def create_token(user: str) -> str:
    """Crée un token JWT pour un utilisateur."""

    # date d'expiration du token
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.token_expire_min)

    # sub = id de l'utilisateur, exp = expiration
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
    """Renvoie l'id du token, ou None s'il est invalide."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

    # token expiré ou falsifié
    except jwt.PyJWTError:
        return None

    sub = payload.get("sub")
    return sub if isinstance(sub, str) else None