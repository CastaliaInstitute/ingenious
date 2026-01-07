"""Authentication module."""

from datetime import datetime, timedelta
from typing import Any, Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from ingen_prompt_tuner.config import settings
from ingen_prompt_tuner.models import User

security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    result: bool = bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    return result


def get_password_hash(password: str) -> str:
    """Hash a password."""
    hashed: bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_expire_minutes))
    to_encode.update({"exp": expire})
    token: str = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token."""
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """Get the current authenticated user."""
    if not settings.auth_enabled:
        return User(id="demo", email="demo@prompttuner.local")

    payload = decode_token(credentials.credentials)
    user_id = payload.get("sub")
    email = payload.get("email")
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return User(id=user_id, email=email)


# Pre-hash admin password at startup
_admin_password_hash = get_password_hash(settings.admin_password)


def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password."""
    if email == settings.admin_email and verify_password(password, _admin_password_hash):
        return User(id="admin", email=email)
    return None
