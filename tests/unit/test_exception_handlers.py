"""Tests for exception handlers.

This module contains comprehensive tests for ExceptionHandlers class
covering all error types and status code mappings.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError as FastAPIValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class TestExceptionHandlersStatusCodeMapping:
    """Test cases for status code mapping in exception handlers."""

    def test_authentication_error_returns_401(self):
        """Test AuthenticationError maps to 401 Unauthorized."""
        from ingenious.errors import AuthenticationError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = AuthenticationError("Invalid credentials")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 401

    def test_authorization_error_returns_403(self):
        """Test AuthorizationError maps to 403 Forbidden."""
        from ingenious.errors import AuthorizationError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = AuthorizationError("Permission denied")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 403

    def test_validation_error_returns_422(self):
        """Test RequestValidationError maps to 422 Unprocessable Entity."""
        from ingenious.errors import RequestValidationError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = RequestValidationError("Invalid input")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 422

    def test_configuration_error_returns_400(self):
        """Test ConfigurationError maps to 400 Bad Request."""
        from ingenious.errors import ConfigurationError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = ConfigurationError("Invalid configuration")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 400

    def test_workflow_not_found_error_returns_404(self):
        """Test WorkflowNotFoundError maps to 404 Not Found."""
        from ingenious.errors import WorkflowNotFoundError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = WorkflowNotFoundError("Workflow not found")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 404

    def test_resource_error_returns_404(self):
        """Test ResourceError maps to 404 Not Found."""
        from ingenious.errors import ResourceError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = ResourceError("Resource not found")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 404

    def test_rate_limit_error_returns_429(self):
        """Test RateLimitError maps to 429 Too Many Requests."""
        from ingenious.errors import RateLimitError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = RateLimitError("Rate limit exceeded")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 429

    def test_database_error_returns_503(self):
        """Test DatabaseError maps to 503 Service Unavailable."""
        from ingenious.errors import DatabaseError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = DatabaseError("Database connection failed")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 503

    def test_service_error_returns_502(self):
        """Test ServiceError maps to 502 Bad Gateway."""
        from ingenious.errors import ServiceError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = ServiceError("Service unavailable")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 502

    def test_api_error_timeout_returns_504(self):
        """Test APIError with timeout message maps to 504 Gateway Timeout."""
        from ingenious.errors import APIError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = APIError("Request timeout occurred")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 504

    def test_api_error_not_found_returns_404(self):
        """Test APIError with 'not found' message maps to 404."""
        from ingenious.errors import APIError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = APIError("Resource not found in API")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 404

    def test_api_error_generic_returns_500(self):
        """Test generic APIError maps to 500."""
        from ingenious.errors import APIError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = APIError("API error occurred")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 500

    def test_unknown_error_returns_500(self):
        """Test unknown IngeniousError maps to 500."""
        from ingenious.errors import IngeniousError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = IngeniousError("Unknown error")
        status_code = ExceptionHandlers._get_status_code_for_error(error)
        assert status_code == 500


class TestGenericExceptionHandler:
    """Test cases for generic_exception_handler."""

    @pytest.fixture
    def mock_request(self):
        """Create mock request."""
        request = MagicMock()
        request.url.path = "/api/v1/test"
        request.method = "GET"
        return request

    @pytest.fixture
    def mock_logger(self):
        """Mock logger."""
        with patch("ingenious.main.exception_handlers.logger") as mock:
            yield mock

    @pytest.mark.asyncio
    async def test_ingenious_error_returns_proper_response(self, mock_request, mock_logger):
        """Test IngeniousError is handled properly."""
        from ingenious.errors import IngeniousError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = IngeniousError("Test error", user_message="User friendly message")

        with patch.dict("os.environ", {"LOADENV": "False"}):
            response = await ExceptionHandlers.generic_exception_handler(mock_request, error)

        assert response.status_code == 500
        body = response.body.decode()
        assert "error" in body
        assert "User friendly message" in body

    @pytest.mark.asyncio
    async def test_authentication_error_returns_401(self, mock_request, mock_logger):
        """Test AuthenticationError returns 401."""
        from ingenious.errors import AuthenticationError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = AuthenticationError("Invalid token")

        with patch.dict("os.environ", {"LOADENV": "False"}):
            response = await ExceptionHandlers.generic_exception_handler(mock_request, error)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_generic_exception_converted_to_ingenious_error(self, mock_request, mock_logger):
        """Test generic exception is converted to IngeniousError."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = ValueError("Something went wrong")

        with patch.dict("os.environ", {"LOADENV": "False"}):
            response = await ExceptionHandlers.generic_exception_handler(mock_request, error)

        assert response.status_code == 500
        body = response.body.decode()
        assert "error" in body
        assert "correlation_id" in body

    @pytest.mark.asyncio
    async def test_rate_limit_error_includes_retry_after_header(self, mock_request, mock_logger):
        """Test RateLimitError includes Retry-After header."""
        from ingenious.errors import RateLimitError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = RateLimitError("Rate limit exceeded")
        error.retry_after = 60

        with patch.dict("os.environ", {"LOADENV": "False"}):
            response = await ExceptionHandlers.generic_exception_handler(mock_request, error)

        assert response.status_code == 429
        assert response.headers.get("Retry-After") == "60"
        assert "X-RateLimit-Reset" in response.headers

    @pytest.mark.asyncio
    async def test_error_logging_includes_context(self, mock_request, mock_logger):
        """Test error logging includes request context."""
        from ingenious.errors import IngeniousError
        from ingenious.main.exception_handlers import ExceptionHandlers

        error = IngeniousError("Test error")

        with patch.dict("os.environ", {"LOADENV": "False"}):
            await ExceptionHandlers.generic_exception_handler(mock_request, error)

        mock_logger.error.assert_called()
        call_kwargs = mock_logger.error.call_args.kwargs
        assert call_kwargs.get("request_path") == "/api/v1/test"
        assert call_kwargs.get("request_method") == "GET"


class TestValidationExceptionHandler:
    """Test cases for validation_exception_handler."""

    @pytest.fixture
    def mock_request_chat(self):
        """Create mock request for chat endpoint."""
        request = MagicMock()
        request.url.path = "/api/v1/chat"
        request.method = "POST"
        return request

    @pytest.fixture
    def mock_request_prompts(self):
        """Create mock request for prompts endpoint."""
        request = MagicMock()
        request.url.path = "/api/v1/prompts/test"
        request.method = "PUT"
        return request

    @pytest.fixture
    def mock_request_generic(self):
        """Create mock request for generic endpoint."""
        request = MagicMock()
        request.url.path = "/api/v1/other"
        request.method = "POST"
        return request

    @pytest.fixture
    def mock_logger(self):
        """Mock logger."""
        with patch("ingenious.main.exception_handlers.logger") as mock:
            yield mock

    @pytest.mark.asyncio
    async def test_returns_422_status(self, mock_request_generic, mock_logger):
        """Test validation error returns 422 status."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        mock_exc = MagicMock()
        mock_exc.errors.return_value = [
            {"type": "missing", "loc": ["body", "field"], "msg": "Field required"}
        ]

        response = await ExceptionHandlers.validation_exception_handler(
            mock_request_generic, mock_exc
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_json_decode_error_handling_for_chat(self, mock_request_chat, mock_logger):
        """Test JSON decode error handling for chat endpoint."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        mock_exc = MagicMock()
        mock_exc.errors.return_value = [
            {
                "type": "json_invalid",
                "loc": ["body"],
                "msg": "JSON decode error",
                "ctx": {"error": "Extra data"},
            }
        ]

        response = await ExceptionHandlers.validation_exception_handler(mock_request_chat, mock_exc)
        body = response.body.decode()
        assert "Invalid JSON format" in body

    @pytest.mark.asyncio
    async def test_missing_field_error_handling_for_chat(self, mock_request_chat, mock_logger):
        """Test missing field error handling for chat endpoint."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        mock_exc = MagicMock()
        mock_exc.errors.return_value = [
            {"type": "missing", "loc": ["body", "user_prompt"], "msg": "Field required"}
        ]

        response = await ExceptionHandlers.validation_exception_handler(mock_request_chat, mock_exc)
        body = response.body.decode()
        assert "user_prompt" in body

    @pytest.mark.asyncio
    async def test_missing_field_error_for_prompts(self, mock_request_prompts, mock_logger):
        """Test missing field error handling for prompts endpoint."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        mock_exc = MagicMock()
        mock_exc.errors.return_value = [
            {"type": "missing", "loc": ["body", "content"], "msg": "Field required"}
        ]

        response = await ExceptionHandlers.validation_exception_handler(
            mock_request_prompts, mock_exc
        )
        body = response.body.decode()
        assert "content" in body

    @pytest.mark.asyncio
    async def test_type_error_handling(self, mock_request_chat, mock_logger):
        """Test type error handling."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        mock_exc = MagicMock()
        mock_exc.errors.return_value = [
            {
                "type": "type_error.string",
                "loc": ["body", "conversation_flow"],
                "msg": "str type expected",
            }
        ]

        response = await ExceptionHandlers.validation_exception_handler(mock_request_chat, mock_exc)
        body = response.body.decode()
        assert "conversation_flow" in body

    @pytest.mark.asyncio
    async def test_generic_validation_error(self, mock_request_generic, mock_logger):
        """Test generic validation error handling."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        mock_exc = MagicMock()
        mock_exc.errors.return_value = [
            {"type": "value_error", "loc": ["body", "count"], "msg": "value must be positive"}
        ]

        response = await ExceptionHandlers.validation_exception_handler(
            mock_request_generic, mock_exc
        )
        body = response.body.decode()
        assert "count" in body

    @pytest.mark.asyncio
    async def test_response_includes_recovery_suggestion(self, mock_request_generic, mock_logger):
        """Test response includes recovery suggestion."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        mock_exc = MagicMock()
        mock_exc.errors.return_value = [
            {"type": "missing", "loc": ["body", "field"], "msg": "Field required"}
        ]

        response = await ExceptionHandlers.validation_exception_handler(
            mock_request_generic, mock_exc
        )
        body = response.body.decode()
        assert "recovery_suggestion" in body


class TestExceptionHandlersRegistration:
    """Test cases for exception handler registration."""

    def test_register_handlers_adds_exception_handler(self):
        """Test register_handlers adds exception handler to app."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = MagicMock(spec=FastAPI)
        ExceptionHandlers.register_handlers(app)

        # Should have called add_exception_handler twice
        assert app.add_exception_handler.call_count == 2

    def test_register_handlers_registers_generic_handler(self):
        """Test register_handlers registers generic exception handler."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = MagicMock(spec=FastAPI)
        ExceptionHandlers.register_handlers(app)

        # Check first call is for Exception
        first_call = app.add_exception_handler.call_args_list[0]
        assert first_call[0][0] is Exception
        assert first_call[0][1] == ExceptionHandlers.generic_exception_handler

    def test_register_handlers_registers_validation_handler(self):
        """Test register_handlers registers validation exception handler."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = MagicMock(spec=FastAPI)
        ExceptionHandlers.register_handlers(app)

        # Check second call is for FastAPIValidationError
        second_call = app.add_exception_handler.call_args_list[1]
        assert second_call[0][0] == FastAPIValidationError


class TestExceptionHandlersIntegration:
    """Integration tests for exception handlers with FastAPI."""

    def test_validation_error_handled_correctly(self):
        """Test validation error is handled correctly in real app."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = FastAPI()
        ExceptionHandlers.register_handlers(app)

        class TestModel(BaseModel):
            required_field: str = Field(...)

        @app.post("/test")
        def test_route(data: TestModel):
            return {"message": "success"}

        with patch("ingenious.main.exception_handlers.logger"):
            client = TestClient(app, raise_server_exceptions=False)
            response = client.post("/test", json={})

        assert response.status_code == 422
        body = response.json()
        assert "error" in body
        assert "required_field" in body["error"]["message"]

    def test_generic_exception_handled_correctly(self):
        """Test generic exception is handled correctly in real app."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = FastAPI()
        ExceptionHandlers.register_handlers(app)

        @app.get("/error")
        def error_route():
            raise ValueError("Something went wrong")

        with patch("ingenious.main.exception_handlers.logger"):
            client = TestClient(app, raise_server_exceptions=False)
            response = client.get("/error")

        assert response.status_code == 500
        body = response.json()
        assert "error" in body
        assert "correlation_id" in body["error"]

    def test_ingenious_error_handled_correctly(self):
        """Test IngeniousError is handled correctly in real app."""
        from ingenious.errors import AuthenticationError
        from ingenious.main.exception_handlers import ExceptionHandlers

        app = FastAPI()
        ExceptionHandlers.register_handlers(app)

        @app.get("/auth-error")
        def auth_error_route():
            raise AuthenticationError("Invalid credentials")

        with patch("ingenious.main.exception_handlers.logger"):
            client = TestClient(app, raise_server_exceptions=False)
            response = client.get("/auth-error")

        assert response.status_code == 401
        body = response.json()
        assert "error" in body


class TestUserFriendlyValidationMessages:
    """Test cases for user-friendly validation message generation."""

    def test_empty_errors_returns_fallback(self):
        """Test empty errors returns fallback message."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        mock_exc = MagicMock()
        mock_exc.errors.return_value = []

        message, suggestion = ExceptionHandlers._generate_user_friendly_validation_message(
            mock_exc, "/api/v1/test"
        )

        assert "Invalid request format" in message
        assert "API requirements" in suggestion

    def test_no_errors_method_returns_fallback(self):
        """Test missing errors method returns fallback message."""
        from ingenious.main.exception_handlers import ExceptionHandlers

        # Create a mock that doesn't have an errors method at all
        mock_exc = MagicMock(spec=[])  # No errors method

        message, suggestion = ExceptionHandlers._generate_user_friendly_validation_message(
            mock_exc, "/api/v1/test"
        )

        assert "Invalid request format" in message
