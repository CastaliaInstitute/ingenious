"""Tests for middleware components.

This module contains comprehensive tests for:
- SecurityHeadersMiddleware
- RequestContextMiddleware
"""

import base64
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


class TestSecurityHeadersMiddleware:
    """Test cases for SecurityHeadersMiddleware."""

    def test_middleware_adds_security_headers(self):
        """Test that all security headers are added to response."""
        from ingenious.main.middleware import SecurityHeadersMiddleware

        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware)

        @app.get("/test")
        def test_route():
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        # Verify all security headers are present
        assert (
            response.headers.get("Strict-Transport-Security")
            == "max-age=31536000; includeSubDomains"
        )
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert "Content-Security-Policy" in response.headers
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        assert "Permissions-Policy" in response.headers

    def test_csp_header_content(self):
        """Test Content-Security-Policy header has correct directives."""
        from ingenious.main.middleware import SecurityHeadersMiddleware

        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware)

        @app.get("/test")
        def test_route():
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        csp = response.headers.get("Content-Security-Policy")
        assert "default-src 'self'" in csp
        assert "script-src 'self' 'unsafe-inline' 'unsafe-eval'" in csp
        assert "style-src 'self' 'unsafe-inline'" in csp
        assert "img-src 'self' data: https:" in csp
        assert "frame-ancestors 'none'" in csp

    def test_permissions_policy_header_content(self):
        """Test Permissions-Policy header disables unnecessary features."""
        from ingenious.main.middleware import SecurityHeadersMiddleware

        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware)

        @app.get("/test")
        def test_route():
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        permissions = response.headers.get("Permissions-Policy")
        assert "accelerometer=()" in permissions
        assert "camera=()" in permissions
        assert "geolocation=()" in permissions
        assert "microphone=()" in permissions

    def test_headers_applied_to_all_routes(self):
        """Test security headers are applied to all routes."""
        from ingenious.main.middleware import SecurityHeadersMiddleware

        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware)

        @app.get("/route1")
        def route1():
            return {"message": "route1"}

        @app.post("/route2")
        def route2():
            return {"message": "route2"}

        client = TestClient(app)

        response1 = client.get("/route1")
        response2 = client.post("/route2")

        # Both routes should have security headers
        assert "Strict-Transport-Security" in response1.headers
        assert "Strict-Transport-Security" in response2.headers

    def test_headers_applied_when_exception_is_handled(self):
        """Test security headers are applied when exceptions are caught by handlers."""
        from fastapi.responses import JSONResponse

        from ingenious.main.middleware import SecurityHeadersMiddleware

        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware)

        @app.exception_handler(ValueError)
        async def value_error_handler(request, exc):
            return JSONResponse(status_code=400, content={"error": str(exc)})

        @app.get("/error")
        def error_route():
            raise ValueError("Test error")

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/error")

        # Security headers should be present when exception is handled
        assert response.status_code == 400
        assert "Strict-Transport-Security" in response.headers


class TestRequestContextMiddleware:
    """Test cases for RequestContextMiddleware."""

    @pytest.fixture
    def mock_set_request_context(self):
        """Mock set_request_context function."""
        with patch("ingenious.main.middleware.set_request_context") as mock:
            mock.return_value = "test-request-id"
            yield mock

    @pytest.fixture
    def mock_clear_request_context(self):
        """Mock clear_request_context function."""
        with patch("ingenious.main.middleware.clear_request_context") as mock:
            yield mock

    @pytest.fixture
    def mock_logger(self):
        """Mock logger."""
        with patch("ingenious.main.middleware.logger") as mock:
            yield mock

    def test_request_id_added_to_response_headers(
        self, mock_set_request_context, mock_clear_request_context, mock_logger
    ):
        """Test request ID is added to response headers."""
        from ingenious.main.middleware import RequestContextMiddleware

        app = FastAPI()
        app.add_middleware(RequestContextMiddleware)

        @app.get("/test")
        def test_route():
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        assert response.headers.get("X-Request-ID") == "test-request-id"

    def test_processing_time_added_to_response_headers(
        self, mock_set_request_context, mock_clear_request_context, mock_logger
    ):
        """Test processing time is added to response headers."""
        from ingenious.main.middleware import RequestContextMiddleware

        app = FastAPI()
        app.add_middleware(RequestContextMiddleware)

        @app.get("/test")
        def test_route():
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        processing_time = response.headers.get("X-Processing-Time")
        assert processing_time is not None
        assert processing_time.endswith("s")

    def test_context_cleared_after_request(
        self, mock_set_request_context, mock_clear_request_context, mock_logger
    ):
        """Test request context is cleared after request completes."""
        from ingenious.main.middleware import RequestContextMiddleware

        app = FastAPI()
        app.add_middleware(RequestContextMiddleware)

        @app.get("/test")
        def test_route():
            return {"message": "test"}

        client = TestClient(app)
        client.get("/test")

        mock_clear_request_context.assert_called_once()

    def test_context_cleared_on_exception(
        self, mock_set_request_context, mock_clear_request_context, mock_logger
    ):
        """Test request context is cleared even when exception occurs."""
        from ingenious.main.middleware import RequestContextMiddleware

        app = FastAPI()
        app.add_middleware(RequestContextMiddleware)

        @app.get("/error")
        def error_route():
            raise ValueError("Test error")

        client = TestClient(app, raise_server_exceptions=False)
        client.get("/error")

        mock_clear_request_context.assert_called_once()

    def test_session_id_extracted_from_header(
        self, mock_set_request_context, mock_clear_request_context, mock_logger
    ):
        """Test session ID is extracted from X-Session-ID header."""
        from ingenious.main.middleware import RequestContextMiddleware

        app = FastAPI()
        app.add_middleware(RequestContextMiddleware)

        @app.get("/test")
        def test_route():
            return {"message": "test"}

        client = TestClient(app)
        client.get("/test", headers={"X-Session-ID": "test-session-123"})

        # Check set_request_context was called with session_id
        mock_set_request_context.assert_called()
        call_kwargs = mock_set_request_context.call_args.kwargs
        assert call_kwargs.get("session_id") == "test-session-123"

    def test_request_logging_on_success(
        self, mock_set_request_context, mock_clear_request_context, mock_logger
    ):
        """Test request start and completion are logged."""
        from ingenious.main.middleware import RequestContextMiddleware

        app = FastAPI()
        app.add_middleware(RequestContextMiddleware)

        @app.get("/test")
        def test_route():
            return {"message": "test"}

        client = TestClient(app)
        client.get("/test")

        # Check that info was called for request start and completion
        assert mock_logger.info.call_count >= 2

    def test_request_logging_on_error(
        self, mock_set_request_context, mock_clear_request_context, mock_logger
    ):
        """Test request error is logged."""
        from ingenious.main.middleware import RequestContextMiddleware

        app = FastAPI()
        app.add_middleware(RequestContextMiddleware)

        @app.get("/error")
        def error_route():
            raise ValueError("Test error")

        client = TestClient(app, raise_server_exceptions=False)
        client.get("/error")

        # Check that error was logged
        mock_logger.error.assert_called()


class TestRequestContextMiddlewareUserExtraction:
    """Test cases for user extraction in RequestContextMiddleware."""

    @pytest.fixture
    def mock_context_functions(self):
        """Mock context functions."""
        with (
            patch("ingenious.main.middleware.set_request_context") as mock_set,
            patch("ingenious.main.middleware.clear_request_context") as mock_clear,
            patch("ingenious.main.middleware.logger") as mock_logger,
        ):
            mock_set.return_value = "test-request-id"
            yield {"set": mock_set, "clear": mock_clear, "logger": mock_logger}

    def test_extract_user_from_bearer_token(self, mock_context_functions):
        """Test user extraction from Bearer token."""
        from ingenious.main.middleware import RequestContextMiddleware

        with patch(
            "ingenious.main.middleware.RequestContextMiddleware._extract_user_from_auth_header"
        ) as mock_extract:
            mock_extract.return_value = "test-user"

            app = FastAPI()
            app.add_middleware(RequestContextMiddleware)

            @app.get("/test")
            def test_route():
                return {"message": "test"}

            client = TestClient(app)
            client.get("/test", headers={"Authorization": "Bearer test-token"})

            mock_extract.assert_called_with("Bearer test-token")

    def test_extract_user_from_basic_auth(self, mock_context_functions):
        """Test user extraction from Basic auth."""
        from ingenious.main.middleware import RequestContextMiddleware

        # Create a middleware instance to test the method directly
        middleware = RequestContextMiddleware(app=MagicMock())

        credentials = base64.b64encode(b"testuser:testpass").decode("utf-8")
        auth_header = f"Basic {credentials}"

        result = middleware._extract_user_from_auth_header(auth_header)
        assert result == "testuser"

    def test_extract_user_returns_anonymous_without_auth(self, mock_context_functions):
        """Test user extraction returns anonymous without auth header."""
        from ingenious.main.middleware import RequestContextMiddleware

        middleware = RequestContextMiddleware(app=MagicMock())

        result = middleware._extract_user_from_auth_header(None)
        assert result == "anonymous"

    def test_extract_user_handles_invalid_bearer_token(self, mock_context_functions):
        """Test user extraction handles invalid bearer token gracefully."""
        from ingenious.main.middleware import RequestContextMiddleware

        with patch("ingenious.auth.jwt.get_username_from_token") as mock_get_username:
            mock_get_username.side_effect = Exception("Invalid token")

            middleware = RequestContextMiddleware(app=MagicMock())
            result = middleware._extract_user_from_auth_header("Bearer invalid-token")

            # Should return 'unauthenticated' on token validation failure
            assert result == "unauthenticated"

    def test_extract_user_handles_invalid_basic_auth(self, mock_context_functions):
        """Test user extraction handles invalid basic auth gracefully."""
        from ingenious.main.middleware import RequestContextMiddleware

        middleware = RequestContextMiddleware(app=MagicMock())

        # Invalid base64
        result = middleware._extract_user_from_auth_header("Basic not-valid-base64!!!")
        assert result == "unauthenticated"
