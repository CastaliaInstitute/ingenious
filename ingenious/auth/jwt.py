"""JWT token creation and validation utilities.

This module provides JWT authentication functionality including token generation
and verification.
"""

import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

from fastapi import HTTPException, status
from jose import JWTError, jwt

from ingenious.core.structured_logging import get_logger

logger = get_logger(__name__)

# Default JWT configuration values (this is intentionally a placeholder default)
_DEFAULT_SECRET_KEY = "your-secret-key-change-this-in-production"  # nosec B105
_DEFAULT_ALGORITHM = "HS256"
_DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 1440
_DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS = 7


def _get_env_str(*keys: str, default: str = "") -> str:
    """Get the first non-empty value from environment variables."""
    for key in keys:
        value = os.getenv(key, "")
        if value:
            return value
    return default


def _get_env_int(*keys: str, default: int = 0) -> int:
    """Get the first non-zero int value from environment variables."""
    for key in keys:
        value = os.getenv(key, "0")
        try:
            parsed = int(value)
            if parsed:
                return parsed
        except ValueError:
            continue
    return default


def _get_jwt_config_from_env() -> Tuple[str, str, int, int]:
    """Get JWT configuration purely from environment variables."""
    return (
        _get_env_str("INGENIOUS_JWT_SECRET_KEY", "JWT_SECRET_KEY", default=_DEFAULT_SECRET_KEY),
        _get_env_str("INGENIOUS_JWT_ALGORITHM", default=_DEFAULT_ALGORITHM),
        _get_env_int(
            "INGENIOUS_JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            default=_DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
        _get_env_int(
            "INGENIOUS_JWT_REFRESH_TOKEN_EXPIRE_DAYS", default=_DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS
        ),
    )


def _get_jwt_config() -> Tuple[str, str, int, int]:
    """Get JWT configuration from settings or environment variables."""
    try:
        from ingenious.config.config import get_config

        config = get_config()
        auth_config = config.web_configuration.authentication

        secret_key = auth_config.jwt_secret_key or _get_env_str(
            "INGENIOUS_JWT_SECRET_KEY", "JWT_SECRET_KEY", default=_DEFAULT_SECRET_KEY
        )

        algorithm = auth_config.jwt_algorithm or _get_env_str(
            "INGENIOUS_JWT_ALGORITHM", default=_DEFAULT_ALGORITHM
        )

        access_token_expire = auth_config.jwt_access_token_expire_minutes or _get_env_int(
            "INGENIOUS_JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            default=_DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        refresh_token_expire = auth_config.jwt_refresh_token_expire_days or _get_env_int(
            "INGENIOUS_JWT_REFRESH_TOKEN_EXPIRE_DAYS",
            "JWT_REFRESH_TOKEN_EXPIRE_DAYS",
            default=_DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS,
        )

        return secret_key, algorithm, access_token_expire, refresh_token_expire
    except Exception:
        return _get_jwt_config_from_env()


SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS = _get_jwt_config()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return str(encoded_jwt)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token with extended expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return str(encoded_jwt)


def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:  # nosec B107
    """Verify and decode a JWT token, checking type and expiration."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if token type matches expected type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if token has expired
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing expiration",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return dict(payload)

    except JWTError as e:
        logger.debug("JWT verification failed", error=str(e), token_type=token_type)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_username_from_token(token: str) -> str:
    """Extract username from a valid JWT token after verification."""
    payload = verify_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return str(username)
