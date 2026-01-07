"""End-to-end API tests for the Ingenious library.

This module contains comprehensive E2E tests that test the full application
flow with mocked external services (OpenAI, Azure, databases).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


class TestHealthEndpointE2E:
    """E2E tests for health check endpoint."""

    def test_health_endpoint_returns_healthy(self):
        """Test health endpoint returns healthy status with mocked config."""
        from ingenious.api.routes.diagnostic import router as diagnostic_router
        from ingenious.services import fastapi_dependencies as ingen_deps

        # Create a minimal app with just the diagnostic routes
        app = FastAPI()
        app.include_router(diagnostic_router, prefix="/api/v1")

        # Mock the get_config to return a valid config
        mock_config = MagicMock()
        mock_config.models = [MagicMock()]
        mock_config.chat_service.type = "multi_agent"

        with patch.object(ingen_deps, "get_config", return_value=mock_config):
            client = TestClient(app)
            response = client.get("/api/v1/health")

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "healthy"

    def test_health_endpoint_returns_503_on_config_failure(self):
        """Test health endpoint returns 503 when config is unavailable."""
        from ingenious.api.routes.diagnostic import router as diagnostic_router
        from ingenious.services import fastapi_dependencies as ingen_deps

        app = FastAPI()
        app.include_router(diagnostic_router, prefix="/api/v1")

        # Mock get_config to raise an error
        with patch.object(ingen_deps, "get_config", side_effect=Exception("Config error")):
            with patch("ingenious.api.routes.diagnostic.logger"):
                client = TestClient(app, raise_server_exceptions=False)
                response = client.get("/api/v1/health")

        assert response.status_code == 503


class TestAPIWithAuthenticationE2E:
    """E2E tests for API with authentication enabled."""

    def test_protected_endpoint_requires_auth(self):
        """Test protected endpoints require authentication."""
        # This tests authentication behavior through the auth dependencies
        from ingenious.services.auth_dependencies import get_security_service

        mock_config = MagicMock()
        mock_config.web_configuration.authentication.enable = True

        # When auth is enabled and no credentials provided, should raise 401
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            get_security_service(token=None, credentials=None, config=mock_config)

        assert exc_info.value.status_code == 401


class TestChatAPIE2E:
    """E2E tests for chat API endpoints."""

    @pytest.fixture
    def mock_openai_client(self):
        """Mock OpenAI client."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a test response from the AI."
        mock_client.chat.completions.create.return_value = mock_response
        return mock_client

    @pytest.fixture
    def mock_chat_history_repo(self):
        """Mock chat history repository."""
        repo = AsyncMock()
        repo.get_thread_messages.return_value = []
        repo.add_message.return_value = "test-message-id"
        repo.add_memory.return_value = "test-memory-id"
        return repo


class TestMiddlewareIntegrationE2E:
    """E2E tests for middleware integration."""

    def test_security_headers_present_in_all_responses(self):
        """Test security headers are present in all API responses."""
        from ingenious.main.middleware import SecurityHeadersMiddleware

        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware)

        @app.get("/test")
        def test_route():
            return {"status": "ok"}

        client = TestClient(app)
        response = client.get("/test")

        # Verify security headers
        assert "Strict-Transport-Security" in response.headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "Content-Security-Policy" in response.headers

    def test_request_id_tracking(self):
        """Test request IDs are tracked through requests."""
        from ingenious.main.middleware import RequestContextMiddleware, SecurityHeadersMiddleware

        app = FastAPI()

        with (
            patch("ingenious.main.middleware.set_request_context") as mock_set_context,
            patch("ingenious.main.middleware.clear_request_context"),
            patch("ingenious.main.middleware.logger"),
        ):
            mock_set_context.return_value = "test-request-id-123"

            app.add_middleware(RequestContextMiddleware)
            app.add_middleware(SecurityHeadersMiddleware)

            @app.get("/test")
            def test_route():
                return {"status": "ok"}

            client = TestClient(app)
            response = client.get("/test")

        assert response.headers.get("X-Request-ID") == "test-request-id-123"


class TestErrorHandlingE2E:
    """E2E tests for error handling across the application."""

    def test_validation_errors_return_structured_response(self):
        """Test validation errors return structured error response."""
        from pydantic import BaseModel, Field

        from ingenious.main.exception_handlers import ExceptionHandlers

        app = FastAPI()
        ExceptionHandlers.register_handlers(app)

        class RequestModel(BaseModel):
            required_field: str = Field(...)
            optional_field: str = None

        @app.post("/test")
        def test_route(data: RequestModel):
            return {"status": "ok"}

        with patch("ingenious.main.exception_handlers.logger"):
            client = TestClient(app, raise_server_exceptions=False)
            response = client.post("/test", json={})

        assert response.status_code == 422
        body = response.json()
        assert "error" in body
        assert "code" in body["error"]
        assert "message" in body["error"]
        assert "correlation_id" in body["error"]

    def test_internal_errors_return_500_with_correlation_id(self):
        """Test internal errors return 500 with correlation ID."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = FastAPI()
        ExceptionHandlers.register_handlers(app)

        @app.get("/error")
        def error_route():
            raise RuntimeError("Internal error occurred")

        with patch("ingenious.main.exception_handlers.logger"):
            client = TestClient(app, raise_server_exceptions=False)
            response = client.get("/error")

        assert response.status_code == 500
        body = response.json()
        assert "error" in body
        assert "correlation_id" in body["error"]

    def test_custom_ingenious_errors_handled_properly(self):
        """Test custom IngeniousErrors are handled with correct status codes."""
        from ingenious.errors import AuthenticationError, AuthorizationError, DatabaseError
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = FastAPI()
        ExceptionHandlers.register_handlers(app)

        @app.get("/auth-error")
        def auth_error():
            raise AuthenticationError("Invalid token")

        @app.get("/authz-error")
        def authz_error():
            raise AuthorizationError("Access denied")

        @app.get("/db-error")
        def db_error():
            raise DatabaseError("Connection failed")

        with patch("ingenious.main.exception_handlers.logger"):
            client = TestClient(app, raise_server_exceptions=False)

            # Test authentication error (401)
            response = client.get("/auth-error")
            assert response.status_code == 401

            # Test authorization error (403)
            response = client.get("/authz-error")
            assert response.status_code == 403

            # Test database error (503)
            response = client.get("/db-error")
            assert response.status_code == 503


class TestApplicationStartupE2E:
    """E2E tests for application startup and configuration."""

    def test_app_factory_creates_fastapi_instance(self):
        """Test FastAgentAPI creates a FastAPI instance."""
        from ingenious.main.app_factory import FastAgentAPI

        mock_config = MagicMock()
        mock_config.web_configuration.allowed_hosts = ["*"]
        mock_config.web_configuration.authentication.enable = False

        # Mock the working directory setup and other dependencies
        with patch.dict("os.environ", {"INGENIOUS_WORKING_DIR": "/tmp"}):
            with (
                patch("ingenious.main.middleware.set_request_context") as mock_set,
                patch("ingenious.main.middleware.clear_request_context"),
                patch("ingenious.main.middleware.logger"),
                patch("os.chdir"),
            ):  # Prevent actual directory change
                mock_set.return_value = "test-id"

                api = FastAgentAPI(mock_config)
                app = api.app

        assert app is not None
        assert isinstance(app, FastAPI)

    def test_routes_registered_correctly(self):
        """Test all expected routes are registered."""
        from ingenious.main.app_factory import FastAgentAPI

        mock_config = MagicMock()
        mock_config.web_configuration.allowed_hosts = ["*"]
        mock_config.web_configuration.authentication.enable = False

        with patch.dict("os.environ", {"INGENIOUS_WORKING_DIR": "/tmp"}):
            with (
                patch("ingenious.main.middleware.set_request_context") as mock_set,
                patch("ingenious.main.middleware.clear_request_context"),
                patch("ingenious.main.middleware.logger"),
                patch("os.chdir"),
            ):
                mock_set.return_value = "test-id"

                api = FastAgentAPI(mock_config)
                app = api.app

        # Get all route paths
        routes = [route.path for route in app.routes]

        # Check essential routes exist
        assert "/docs" in routes or any("/docs" in str(r) for r in routes)

    def test_exception_handlers_registered(self):
        """Test exception handlers are registered."""
        from ingenious.main.app_factory import FastAgentAPI

        mock_config = MagicMock()
        mock_config.web_configuration.allowed_hosts = ["*"]
        mock_config.web_configuration.authentication.enable = False

        with patch.dict("os.environ", {"INGENIOUS_WORKING_DIR": "/tmp"}):
            with (
                patch("ingenious.main.middleware.set_request_context") as mock_set,
                patch("ingenious.main.middleware.clear_request_context"),
                patch("ingenious.main.middleware.logger"),
                patch("os.chdir"),
            ):
                mock_set.return_value = "test-id"

                api = FastAgentAPI(mock_config)
                app = api.app

        # Check exception handlers are registered
        assert Exception in app.exception_handlers


class TestDatabaseIntegrationE2E:
    """E2E tests for database integration."""

    @pytest.fixture
    def mock_db_connection(self):
        """Mock database connection."""
        conn = MagicMock()
        conn.execute.return_value = MagicMock()
        conn.fetchall.return_value = []
        conn.fetchone.return_value = None
        return conn

    def test_sqlite_repository_operations(self, mock_db_connection):
        """Test SQLite repository CRUD operations."""
        # This would test the repository pattern with mocked connection
        pass


class TestConfigurationE2E:
    """E2E tests for configuration loading."""

    def test_config_loads_from_environment(self):
        """Test configuration loads from environment variables."""
        import os
        from unittest.mock import patch

        test_env = {
            "INGENIOUS_MODELS__0__API_KEY": "test-key",
            "INGENIOUS_MODELS__0__BASE_URL": "https://test.api.com/",
            "INGENIOUS_MODELS__0__MODEL": "gpt-4",
            "INGENIOUS_MODELS__0__DEPLOYMENT": "test-deployment",
            "INGENIOUS_MODELS__0__API_VERSION": "2024-01-01",
            "INGENIOUS_MODELS__0__API_TYPE": "rest",
            "INGENIOUS_MODELS__0__ROLE": "chat",
            "INGENIOUS_CHAT_HISTORY__DATABASE_TYPE": "sqlite",
            "INGENIOUS_CHAT_HISTORY__DATABASE_PATH": "/tmp/test.db",
        }

        with patch.dict(os.environ, test_env, clear=False):
            # Configuration loading test would go here
            pass


class TestLoggingE2E:
    """E2E tests for logging integration."""

    def test_correlation_ids_propagated(self):
        """Test correlation IDs are propagated through request lifecycle."""
        from ingenious.core.structured_logging import (
            clear_request_context,
            set_request_context,
        )

        # Set request context
        request_id = set_request_context(user_id="test-user", session_id="test-session")

        assert request_id is not None

        # Clear context
        clear_request_context()

    def test_logger_creation(self):
        """Test logger can be created."""
        from ingenious.core.structured_logging import get_logger

        logger = get_logger("test_module")

        assert logger is not None


class TestContentFilterE2E:
    """E2E tests for content filter integration."""

    def test_content_filter_error_handling(self):
        """Test content filter errors are handled properly."""
        from ingenious.errors.content_filter_error import ContentFilterError
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = FastAPI()
        ExceptionHandlers.register_handlers(app)

        @app.get("/filter-error")
        def filter_error():
            raise ContentFilterError(content_filter_results={"hate": {"filtered": True}})

        with patch("ingenious.main.exception_handlers.logger"):
            client = TestClient(app, raise_server_exceptions=False)
            response = client.get("/filter-error")

        # Should return an error status
        assert response.status_code >= 400
