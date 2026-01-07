"""Tests for authentication dependencies.

This module contains comprehensive tests for auth dependency injection functions:
- get_security_service
- get_security_service_optional
- get_auth_user
- get_conditional_security
- _validate_basic_auth_credentials
- _handle_basic_auth_header
"""

import base64
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasicCredentials


class TestGetSecurityService:
    """Test cases for get_security_service function."""

    @pytest.fixture
    def mock_config_auth_enabled(self):
        """Create mock config with auth enabled."""
        config = MagicMock()
        config.web_configuration.authentication.enable = True
        config.web_configuration.authentication.username = "admin"
        config.web_configuration.authentication.password = "password123"
        return config

    @pytest.fixture
    def mock_config_auth_disabled(self):
        """Create mock config with auth disabled."""
        config = MagicMock()
        config.web_configuration.authentication.enable = False
        return config

    def test_returns_anonymous_when_auth_disabled(self, mock_config_auth_disabled):
        """Test returns 'anonymous' when authentication is disabled."""
        from ingenious.services.auth_dependencies import get_security_service

        with patch("ingenious.services.auth_dependencies.logger"):
            result = get_security_service(
                token=None, credentials=None, config=mock_config_auth_disabled
            )

        assert result == "anonymous"

    def test_validates_bearer_token(self, mock_config_auth_enabled):
        """Test validates Bearer token and returns username."""
        from ingenious.services.auth_dependencies import get_security_service

        token = MagicMock(spec=HTTPAuthorizationCredentials)
        token.credentials = "valid-jwt-token"

        with patch(
            "ingenious.services.auth_dependencies.get_username_from_token"
        ) as mock_get_username:
            mock_get_username.return_value = "test-user"

            result = get_security_service(
                token=token, credentials=None, config=mock_config_auth_enabled
            )

        assert result == "test-user"

    def test_falls_back_to_basic_auth_when_token_invalid(self, mock_config_auth_enabled):
        """Test falls back to basic auth when token validation fails."""
        from ingenious.services.auth_dependencies import get_security_service

        token = MagicMock(spec=HTTPAuthorizationCredentials)
        token.credentials = "invalid-token"

        credentials = MagicMock(spec=HTTPBasicCredentials)
        credentials.username = "admin"
        credentials.password = "password123"

        with patch(
            "ingenious.services.auth_dependencies.get_username_from_token"
        ) as mock_get_username:
            mock_get_username.side_effect = HTTPException(status_code=401, detail="Invalid token")

            result = get_security_service(
                token=token, credentials=credentials, config=mock_config_auth_enabled
            )

        assert result == "admin"

    def test_raises_401_when_no_credentials(self, mock_config_auth_enabled):
        """Test raises 401 when no credentials provided."""
        from ingenious.services.auth_dependencies import get_security_service

        with pytest.raises(HTTPException) as exc_info:
            get_security_service(token=None, credentials=None, config=mock_config_auth_enabled)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Authentication required"

    def test_validates_basic_auth_credentials(self, mock_config_auth_enabled):
        """Test validates basic auth credentials."""
        from ingenious.services.auth_dependencies import get_security_service

        credentials = MagicMock(spec=HTTPBasicCredentials)
        credentials.username = "admin"
        credentials.password = "password123"

        result = get_security_service(
            token=None, credentials=credentials, config=mock_config_auth_enabled
        )

        assert result == "admin"

    def test_raises_401_for_invalid_basic_auth(self, mock_config_auth_enabled):
        """Test raises 401 for invalid basic auth credentials."""
        from ingenious.services.auth_dependencies import get_security_service

        credentials = MagicMock(spec=HTTPBasicCredentials)
        credentials.username = "admin"
        credentials.password = "wrong-password"

        with pytest.raises(HTTPException) as exc_info:
            get_security_service(
                token=None, credentials=credentials, config=mock_config_auth_enabled
            )

        assert exc_info.value.status_code == 401


class TestGetSecurityServiceOptional:
    """Test cases for get_security_service_optional function."""

    @pytest.fixture
    def mock_config_auth_enabled(self):
        """Create mock config with auth enabled."""
        config = MagicMock()
        config.web_configuration.authentication.enable = True
        config.web_configuration.authentication.username = "admin"
        config.web_configuration.authentication.password = "password123"
        return config

    @pytest.fixture
    def mock_config_auth_disabled(self):
        """Create mock config with auth disabled."""
        config = MagicMock()
        config.web_configuration.authentication.enable = False
        return config

    def test_returns_none_when_auth_disabled(self, mock_config_auth_disabled):
        """Test returns None when authentication is disabled."""
        from ingenious.services.auth_dependencies import get_security_service_optional

        with patch("ingenious.services.auth_dependencies.logger"):
            result = get_security_service_optional(
                credentials=None, config=mock_config_auth_disabled
            )

        assert result is None

    def test_raises_401_when_no_credentials_and_auth_enabled(self, mock_config_auth_enabled):
        """Test raises 401 when no credentials and auth enabled."""
        from ingenious.services.auth_dependencies import get_security_service_optional

        with pytest.raises(HTTPException) as exc_info:
            get_security_service_optional(credentials=None, config=mock_config_auth_enabled)

        assert exc_info.value.status_code == 401
        assert "WWW-Authenticate" in exc_info.value.headers

    def test_validates_basic_auth_credentials(self, mock_config_auth_enabled):
        """Test validates basic auth credentials."""
        from ingenious.services.auth_dependencies import get_security_service_optional

        credentials = MagicMock(spec=HTTPBasicCredentials)
        credentials.username = "admin"
        credentials.password = "password123"

        result = get_security_service_optional(
            credentials=credentials, config=mock_config_auth_enabled
        )

        assert result == "admin"


class TestGetAuthUser:
    """Test cases for get_auth_user function."""

    @pytest.fixture
    def mock_config_auth_enabled(self):
        """Create mock config with auth enabled."""
        config = MagicMock()
        config.web_configuration.authentication.enable = True
        config.web_configuration.authentication.username = "admin"
        config.web_configuration.authentication.password = "password123"
        return config

    @pytest.fixture
    def mock_config_auth_disabled(self):
        """Create mock config with auth disabled."""
        config = MagicMock()
        config.web_configuration.authentication.enable = False
        return config

    @pytest.fixture
    def mock_request(self):
        """Create mock request."""
        request = MagicMock()
        request.headers = {}
        return request

    def test_returns_anonymous_when_auth_disabled(self, mock_request, mock_config_auth_disabled):
        """Test returns 'anonymous' when authentication is disabled."""
        from ingenious.services.auth_dependencies import get_auth_user

        with patch("ingenious.services.auth_dependencies.logger"):
            result = get_auth_user(mock_request, mock_config_auth_disabled)

        assert result == "anonymous"

    def test_validates_bearer_token(self, mock_request, mock_config_auth_enabled):
        """Test validates Bearer token from header."""
        from ingenious.services.auth_dependencies import get_auth_user

        mock_request.headers = {"Authorization": "Bearer valid-jwt-token"}

        with patch(
            "ingenious.services.auth_dependencies.get_username_from_token"
        ) as mock_get_username:
            mock_get_username.return_value = "test-user"

            result = get_auth_user(mock_request, mock_config_auth_enabled)

        assert result == "test-user"

    def test_falls_back_to_basic_auth_when_token_invalid(
        self, mock_request, mock_config_auth_enabled
    ):
        """Test falls back to basic auth when token validation fails."""
        from ingenious.services.auth_dependencies import get_auth_user

        # Create valid Basic auth header
        credentials = base64.b64encode(b"admin:password123").decode("utf-8")
        mock_request.headers = {"Authorization": f"Basic {credentials}"}

        with patch(
            "ingenious.services.auth_dependencies.get_username_from_token"
        ) as mock_get_username:
            mock_get_username.side_effect = HTTPException(status_code=401, detail="Invalid token")

            result = get_auth_user(mock_request, mock_config_auth_enabled)

        assert result == "admin"

    def test_validates_basic_auth_header(self, mock_request, mock_config_auth_enabled):
        """Test validates Basic auth header."""
        from ingenious.services.auth_dependencies import get_auth_user

        credentials = base64.b64encode(b"admin:password123").decode("utf-8")
        mock_request.headers = {"Authorization": f"Basic {credentials}"}

        result = get_auth_user(mock_request, mock_config_auth_enabled)

        assert result == "admin"

    def test_raises_401_when_no_auth_header(self, mock_request, mock_config_auth_enabled):
        """Test raises 401 when no auth header provided."""
        from ingenious.services.auth_dependencies import get_auth_user

        mock_request.headers = {}

        with pytest.raises(HTTPException) as exc_info:
            get_auth_user(mock_request, mock_config_auth_enabled)

        assert exc_info.value.status_code == 401

    def test_raises_401_for_invalid_auth_scheme(self, mock_request, mock_config_auth_enabled):
        """Test raises 401 for invalid auth scheme."""
        from ingenious.services.auth_dependencies import get_auth_user

        mock_request.headers = {"Authorization": "Digest abc123"}

        with pytest.raises(HTTPException) as exc_info:
            get_auth_user(mock_request, mock_config_auth_enabled)

        assert exc_info.value.status_code == 401


class TestGetConditionalSecurity:
    """Test cases for get_conditional_security function."""

    @pytest.fixture
    def mock_request(self):
        """Create mock request."""
        request = MagicMock()
        request.headers = {}
        return request

    def test_wrapper_calls_get_auth_user(self, mock_request):
        """Test wrapper calls get_auth_user."""
        from ingenious.services.auth_dependencies import get_conditional_security

        with patch("ingenious.services.auth_dependencies.get_auth_user") as mock_get_auth_user:
            mock_get_auth_user.return_value = "test-user"

            result = get_conditional_security(mock_request)

        mock_get_auth_user.assert_called_once_with(mock_request)
        assert result == "test-user"


class TestValidateBasicAuthCredentials:
    """Test cases for _validate_basic_auth_credentials function."""

    @pytest.fixture
    def mock_config(self):
        """Create mock config."""
        config = MagicMock()
        config.web_configuration.authentication.username = "admin"
        config.web_configuration.authentication.password = "secret123"
        return config

    def test_valid_credentials_returns_username(self, mock_config):
        """Test valid credentials returns username."""
        from ingenious.services.auth_dependencies import _validate_basic_auth_credentials

        credentials = MagicMock(spec=HTTPBasicCredentials)
        credentials.username = "admin"
        credentials.password = "secret123"

        result = _validate_basic_auth_credentials(credentials, mock_config)

        assert result == "admin"

    def test_invalid_username_raises_401(self, mock_config):
        """Test invalid username raises 401."""
        from ingenious.services.auth_dependencies import _validate_basic_auth_credentials

        credentials = MagicMock(spec=HTTPBasicCredentials)
        credentials.username = "wrong-user"
        credentials.password = "secret123"

        with pytest.raises(HTTPException) as exc_info:
            _validate_basic_auth_credentials(credentials, mock_config)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Incorrect username or password"

    def test_invalid_password_raises_401(self, mock_config):
        """Test invalid password raises 401."""
        from ingenious.services.auth_dependencies import _validate_basic_auth_credentials

        credentials = MagicMock(spec=HTTPBasicCredentials)
        credentials.username = "admin"
        credentials.password = "wrong-password"

        with pytest.raises(HTTPException) as exc_info:
            _validate_basic_auth_credentials(credentials, mock_config)

        assert exc_info.value.status_code == 401

    def test_timing_safe_comparison_used(self, mock_config):
        """Test that secrets.compare_digest is used for timing-safe comparison."""
        from ingenious.services.auth_dependencies import _validate_basic_auth_credentials

        credentials = MagicMock(spec=HTTPBasicCredentials)
        credentials.username = "admin"
        credentials.password = "secret123"

        with patch("ingenious.services.auth_dependencies.secrets.compare_digest") as mock_compare:
            mock_compare.return_value = True

            _validate_basic_auth_credentials(credentials, mock_config)

        # compare_digest should be called twice (username and password)
        assert mock_compare.call_count == 2


class TestHandleBasicAuthHeader:
    """Test cases for _handle_basic_auth_header function."""

    @pytest.fixture
    def mock_config(self):
        """Create mock config."""
        config = MagicMock()
        config.web_configuration.authentication.username = "admin"
        config.web_configuration.authentication.password = "password123"
        return config

    def test_valid_basic_auth_header(self, mock_config):
        """Test valid Basic auth header returns username."""
        from ingenious.services.auth_dependencies import _handle_basic_auth_header

        credentials = base64.b64encode(b"admin:password123").decode("utf-8")
        auth_header = f"Basic {credentials}"

        result = _handle_basic_auth_header(auth_header, mock_config)

        assert result == "admin"

    def test_invalid_base64_raises_401(self, mock_config):
        """Test invalid base64 raises 401."""
        from ingenious.services.auth_dependencies import _handle_basic_auth_header

        auth_header = "Basic not-valid-base64!!!"

        with pytest.raises(HTTPException) as exc_info:
            _handle_basic_auth_header(auth_header, mock_config)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid authentication format"

    def test_missing_colon_raises_401(self, mock_config):
        """Test missing colon in credentials raises 401."""
        from ingenious.services.auth_dependencies import _handle_basic_auth_header

        # Encode without colon
        credentials = base64.b64encode(b"adminpassword").decode("utf-8")
        auth_header = f"Basic {credentials}"

        with pytest.raises(HTTPException) as exc_info:
            _handle_basic_auth_header(auth_header, mock_config)

        assert exc_info.value.status_code == 401

    def test_wrong_credentials_raises_401(self, mock_config):
        """Test wrong credentials raises 401."""
        from ingenious.services.auth_dependencies import _handle_basic_auth_header

        credentials = base64.b64encode(b"admin:wrongpassword").decode("utf-8")
        auth_header = f"Basic {credentials}"

        with pytest.raises(HTTPException) as exc_info:
            _handle_basic_auth_header(auth_header, mock_config)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Incorrect username or password"

    def test_password_with_colon(self, mock_config):
        """Test password containing colon is handled correctly."""
        from ingenious.services.auth_dependencies import _handle_basic_auth_header

        # Update config to have password with colon
        mock_config.web_configuration.authentication.password = "pass:word:123"

        credentials = base64.b64encode(b"admin:pass:word:123").decode("utf-8")
        auth_header = f"Basic {credentials}"

        result = _handle_basic_auth_header(auth_header, mock_config)

        assert result == "admin"


class TestAuthDependenciesLogging:
    """Test cases for logging in auth dependencies."""

    @pytest.fixture
    def mock_config_auth_disabled(self):
        """Create mock config with auth disabled."""
        config = MagicMock()
        config.web_configuration.authentication.enable = False
        return config

    def test_warning_logged_when_auth_disabled_get_security_service(
        self, mock_config_auth_disabled
    ):
        """Test warning is logged when auth is disabled in get_security_service."""
        from ingenious.services.auth_dependencies import get_security_service

        with patch("ingenious.services.auth_dependencies.logger") as mock_logger:
            get_security_service(token=None, credentials=None, config=mock_config_auth_disabled)

        mock_logger.warning.assert_called()
        call_args = mock_logger.warning.call_args[0][0]
        assert "Authentication is disabled" in call_args

    def test_warning_logged_when_auth_disabled_get_security_service_optional(
        self, mock_config_auth_disabled
    ):
        """Test warning is logged when auth is disabled in get_security_service_optional."""
        from ingenious.services.auth_dependencies import get_security_service_optional

        with patch("ingenious.services.auth_dependencies.logger") as mock_logger:
            get_security_service_optional(credentials=None, config=mock_config_auth_disabled)

        mock_logger.warning.assert_called()

    def test_warning_logged_when_auth_disabled_get_auth_user(self, mock_config_auth_disabled):
        """Test warning is logged when auth is disabled in get_auth_user."""
        from ingenious.services.auth_dependencies import get_auth_user

        mock_request = MagicMock()
        mock_request.headers = {}

        with patch("ingenious.services.auth_dependencies.logger") as mock_logger:
            get_auth_user(mock_request, mock_config_auth_disabled)

        mock_logger.warning.assert_called()
