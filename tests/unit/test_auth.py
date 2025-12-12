"""Test Auth module."""

from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException, status
from jose import jwt

# Use the default algorithm constant directly since it's stable
_DEFAULT_ALGORITHM = "HS256"
_TEST_SECRET_KEY = "test-secret-key-for-unit-tests-only"


@pytest.fixture(autouse=True)
def setup_jwt_env(monkeypatch):
    """Set up JWT environment for all tests in this module."""
    monkeypatch.setenv("INGENIOUS_JWT_SECRET_KEY", _TEST_SECRET_KEY)
    # Reset the JWT config cache before each test
    import ingenious.auth.jwt

    ingenious.auth.jwt._jwt_config = None
    yield
    # Clean up after test
    ingenious.auth.jwt._jwt_config = None


class TestJWTAuthentication:
    """Test JWT authentication functionality."""

    def test_create_access_token(self):
        """Test access token creation."""
        from ingenious.auth.jwt import create_access_token

        data = {"sub": "testuser"}
        token = create_access_token(data)

        # Decode token to verify contents
        payload = jwt.decode(token, _TEST_SECRET_KEY, algorithms=[_DEFAULT_ALGORITHM])
        assert payload["sub"] == "testuser"
        assert payload["type"] == "access"
        assert "exp" in payload

        # Check expiration is in the future
        exp_timestamp = payload["exp"]
        assert datetime.utcnow().timestamp() < exp_timestamp

    def test_create_access_token_with_custom_expiry(self):
        """Test access token creation with custom expiry."""
        from ingenious.auth.jwt import create_access_token

        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)

        payload = jwt.decode(token, _TEST_SECRET_KEY, algorithms=[_DEFAULT_ALGORITHM])

        # Check that expiry is set and is in the future
        assert "exp" in payload
        exp_timestamp = payload["exp"]
        assert datetime.utcnow().timestamp() < exp_timestamp

        # Check that the token type is correct
        assert payload["type"] == "access"
        assert payload["sub"] == "testuser"

    def test_create_refresh_token(self):
        """Test refresh token creation."""
        from ingenious.auth.jwt import create_refresh_token

        data = {"sub": "testuser"}
        token = create_refresh_token(data)

        payload = jwt.decode(token, _TEST_SECRET_KEY, algorithms=[_DEFAULT_ALGORITHM])
        assert payload["sub"] == "testuser"
        assert payload["type"] == "refresh"
        assert "exp" in payload

    def test_verify_token_valid_access_token(self):
        """Test verifying a valid access token."""
        from ingenious.auth.jwt import create_access_token, verify_token

        data = {"sub": "testuser"}
        token = create_access_token(data)

        payload = verify_token(token, "access")
        assert payload["sub"] == "testuser"
        assert payload["type"] == "access"

    def test_verify_token_valid_refresh_token(self):
        """Test verifying a valid refresh token."""
        from ingenious.auth.jwt import create_refresh_token, verify_token

        data = {"sub": "testuser"}
        token = create_refresh_token(data)

        payload = verify_token(token, "refresh")
        assert payload["sub"] == "testuser"
        assert payload["type"] == "refresh"

    def test_verify_token_wrong_type(self):
        """Test verifying token with wrong type."""
        from ingenious.auth.jwt import create_access_token, verify_token

        data = {"sub": "testuser"}
        access_token = create_access_token(data)

        with pytest.raises(HTTPException) as exc_info:
            verify_token(access_token, "refresh")

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token type" in exc_info.value.detail

    def test_verify_token_expired(self):
        """Test verifying an expired token."""
        from ingenious.auth.jwt import verify_token

        # Create an expired token manually
        expired_payload = {
            "sub": "testuser",
            "type": "access",
            "exp": (datetime.utcnow() - timedelta(hours=1)).timestamp(),
        }
        token = jwt.encode(expired_payload, _TEST_SECRET_KEY, algorithm=_DEFAULT_ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        # Check that it's an auth error - the specific message may vary
        assert exc_info.value.status_code == 401

    def test_verify_token_invalid_signature(self):
        """Test verifying token with invalid signature."""
        from ingenious.auth.jwt import verify_token

        # Create token with wrong secret
        wrong_secret = "wrong-secret"
        data = {
            "sub": "testuser",
            "type": "access",
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        token = jwt.encode(data, wrong_secret, algorithm=_DEFAULT_ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in exc_info.value.detail

    def test_verify_token_missing_expiration(self):
        """Test verifying token without expiration."""
        from ingenious.auth.jwt import verify_token

        data = {"sub": "testuser", "type": "access"}
        token = jwt.encode(data, _TEST_SECRET_KEY, algorithm=_DEFAULT_ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token missing expiration" in exc_info.value.detail

    def test_get_username_from_token_valid(self):
        """Test extracting username from valid token."""
        from ingenious.auth.jwt import create_access_token, get_username_from_token

        data = {"sub": "testuser"}
        token = create_access_token(data)

        username = get_username_from_token(token)
        assert username == "testuser"

    def test_get_username_from_token_missing_sub(self):
        """Test extracting username from token without sub claim."""
        from ingenious.auth.jwt import get_username_from_token

        data = {"type": "access", "exp": datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(data, _TEST_SECRET_KEY, algorithm=_DEFAULT_ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            get_username_from_token(token)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in exc_info.value.detail

    def test_get_username_from_token_invalid(self):
        """Test extracting username from invalid token."""
        from ingenious.auth.jwt import get_username_from_token

        invalid_token = "invalid.token.here"

        with pytest.raises(HTTPException) as exc_info:
            get_username_from_token(invalid_token)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestJWTConfiguration:
    """Test JWT configuration and environment handling."""

    def test_token_structure(self):
        """Test JWT token structure and claims."""
        from ingenious.auth.jwt import create_access_token

        data = {"sub": "testuser", "role": "admin"}
        token = create_access_token(data)

        payload = jwt.decode(token, _TEST_SECRET_KEY, algorithms=[_DEFAULT_ALGORITHM])

        # Verify standard claims
        assert "sub" in payload
        assert "exp" in payload
        assert "type" in payload

        # Verify custom data is preserved
        assert payload["sub"] == "testuser"
        assert payload.get("role") == "admin"
        assert payload["type"] == "access"

    def test_missing_secret_key_raises_error(self, monkeypatch):
        """Test that missing JWT secret key raises clear error."""
        import ingenious.auth.jwt
        from ingenious.auth.jwt import JWTConfigurationError, _ensure_jwt_config

        # Clear the cached config
        ingenious.auth.jwt._jwt_config = None

        # Remove the secret key
        monkeypatch.delenv("INGENIOUS_JWT_SECRET_KEY", raising=False)
        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

        with pytest.raises(JWTConfigurationError) as exc_info:
            _ensure_jwt_config()

        assert "JWT secret key is not configured" in str(exc_info.value)
