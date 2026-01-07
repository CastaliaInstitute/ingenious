"""Comprehensive tests for chat service core functionality.

Tests cover chat service initialization, dynamic module loading, request handling,
streaming responses, and error scenarios with full mocking of external services.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from ingenious.errors import ChatServiceError
from ingenious.models.chat import ChatRequest, ChatResponse, ChatResponseChunk
from ingenious.services.chat_service import ChatService, IChatService


class TestIChatServiceInterface:
    """Test the abstract chat service interface."""

    def test_interface_defines_required_methods(self):
        """Test that IChatService defines required abstract methods."""
        assert hasattr(IChatService, "get_chat_response")
        assert hasattr(IChatService, "get_streaming_chat_response")

    def test_cannot_instantiate_abstract_class(self):
        """Test that IChatService cannot be instantiated directly."""
        with pytest.raises(TypeError):
            IChatService()


class TestChatServiceInitialization:
    """Test ChatService initialization and module loading."""

    def test_initialization_loads_service_class(self):
        """Test that initialization dynamically loads the service class."""
        mock_config = Mock()
        mock_repo = Mock()
        mock_service_instance = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            mock_service_class = Mock(return_value=mock_service_instance)
            mock_import.return_value = mock_service_class

            service = ChatService(
                chat_service_type="multi_agent",
                chat_history_repository=mock_repo,
                conversation_flow="test_flow",
                config=mock_config,
            )

            # Verify import was called with correct module and class names
            mock_import.assert_called_once_with(
                "services.chat_services.multi_agent.service",
                "MultiAgentChatService",
                expected_methods=["get_chat_response"],
            )

            # Verify service class was instantiated
            mock_service_class.assert_called_once_with(
                config=mock_config,
                chat_history_repository=mock_repo,
                conversation_flow="test_flow",
            )

            assert service.service_class == mock_service_instance

    def test_initialization_converts_service_type_to_class_name(self):
        """Test that service type is properly converted to class name."""
        mock_config = Mock()
        mock_repo = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            mock_import.return_value = Mock(return_value=Mock())

            # Test various service type formats
            ChatService(
                chat_service_type="simple_chat",
                chat_history_repository=mock_repo,
                conversation_flow="test_flow",
                config=mock_config,
            )

            mock_import.assert_called_with(
                "services.chat_services.simple_chat.service",
                "SimpleChatChatService",
                expected_methods=["get_chat_response"],
            )

    def test_initialization_raises_on_import_error(self):
        """Test that ImportError is wrapped in ChatServiceError."""
        mock_config = Mock()
        mock_repo = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            mock_import.side_effect = ImportError("Module not found")

            with pytest.raises(ChatServiceError) as exc_info:
                ChatService(
                    chat_service_type="nonexistent",
                    chat_history_repository=mock_repo,
                    conversation_flow="test_flow",
                    config=mock_config,
                )

            assert "Failed to import chat service module" in str(exc_info.value)

    def test_initialization_raises_on_attribute_error(self):
        """Test that AttributeError is wrapped in ChatServiceError."""
        mock_config = Mock()
        mock_repo = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            mock_import.side_effect = AttributeError("Class not found")

            with pytest.raises(ChatServiceError) as exc_info:
                ChatService(
                    chat_service_type="invalid",
                    chat_history_repository=mock_repo,
                    conversation_flow="test_flow",
                    config=mock_config,
                )

            assert "Chat service class not found" in str(exc_info.value)

    def test_initialization_raises_on_unexpected_error(self):
        """Test that unexpected errors are wrapped in ChatServiceError."""
        mock_config = Mock()
        mock_repo = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            mock_import.side_effect = RuntimeError("Unexpected error")

            with pytest.raises(ChatServiceError) as exc_info:
                ChatService(
                    chat_service_type="broken",
                    chat_history_repository=mock_repo,
                    conversation_flow="test_flow",
                    config=mock_config,
                )

            assert "Unexpected error during chat service initialization" in str(exc_info.value)


class TestChatServiceGetChatResponse:
    """Test ChatService.get_chat_response method."""

    @pytest.fixture
    def mock_chat_service(self):
        """Create a mock chat service for testing."""
        mock_config = Mock()
        mock_repo = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            mock_service_instance = Mock()
            mock_service_instance.get_chat_response = AsyncMock()
            mock_import.return_value = Mock(return_value=mock_service_instance)

            service = ChatService(
                chat_service_type="test",
                chat_history_repository=mock_repo,
                conversation_flow="test_flow",
                config=mock_config,
            )
            return service

    @pytest.mark.asyncio
    async def test_get_chat_response_delegates_to_service_class(self, mock_chat_service):
        """Test that get_chat_response delegates to the underlying service."""
        mock_response = ChatResponse(
            thread_id="thread-123",
            message_id="msg-456",
            agent_response="Hello!",
            token_count=10,
            max_token_count=4096,
        )
        mock_chat_service.service_class.get_chat_response.return_value = mock_response

        request = ChatRequest(
            thread_id="thread-123",
            user_id="user-1",
            user_prompt="Hi",
            conversation_flow="test_flow",
        )

        result = await mock_chat_service.get_chat_response(request)

        mock_chat_service.service_class.get_chat_response.assert_called_once_with(request)
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_chat_response_raises_on_missing_conversation_flow(self, mock_chat_service):
        """Test that ValueError is raised when conversation_flow is not set."""
        request = ChatRequest(
            thread_id="thread-123",
            user_id="user-1",
            user_prompt="Hi",
            conversation_flow=None,
        )

        with pytest.raises(ValueError, match="conversation_flow not set"):
            await mock_chat_service.get_chat_response(request)


class TestChatServiceStreamingResponse:
    """Test ChatService streaming response functionality."""

    @pytest.fixture
    def mock_streaming_service(self):
        """Create a mock streaming chat service."""
        mock_config = Mock()
        mock_repo = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            mock_service_instance = Mock()
            mock_service_instance.get_streaming_chat_response = AsyncMock()
            mock_import.return_value = Mock(return_value=mock_service_instance)

            service = ChatService(
                chat_service_type="test",
                chat_history_repository=mock_repo,
                conversation_flow="test_flow",
                config=mock_config,
            )
            return service

    @pytest.mark.asyncio
    async def test_streaming_response_yields_chunks(self, mock_streaming_service):
        """Test that streaming response yields chunks from underlying service."""
        chunks = [
            ChatResponseChunk(
                thread_id="t1", message_id="m1", chunk_type="content", content="Hello"
            ),
            ChatResponseChunk(
                thread_id="t1", message_id="m1", chunk_type="content", content=" World"
            ),
            ChatResponseChunk(thread_id="t1", message_id="m1", chunk_type="final", is_final=True),
        ]

        async def mock_stream(request):
            for chunk in chunks:
                yield chunk

        mock_streaming_service.service_class.get_streaming_chat_response = mock_stream

        request = ChatRequest(
            thread_id="t1",
            user_id="u1",
            user_prompt="test",
            conversation_flow="flow",
        )

        received_chunks = []
        async for chunk in mock_streaming_service.get_streaming_chat_response(request):
            received_chunks.append(chunk)

        assert len(received_chunks) == 3
        assert received_chunks[0].content == "Hello"
        assert received_chunks[1].content == " World"
        assert received_chunks[2].is_final is True

    @pytest.mark.asyncio
    async def test_streaming_fallback_when_not_supported(self):
        """Test fallback to chunked response when streaming not supported."""
        mock_config = Mock()
        mock_config.web = {"streaming_chunk_size": 5}
        mock_repo = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            # Service without get_streaming_chat_response method
            mock_service_instance = Mock(spec=["get_chat_response"])
            mock_service_instance.get_chat_response = AsyncMock(
                return_value=ChatResponse(
                    thread_id="t1",
                    message_id="m1",
                    agent_response="Hello World",
                    token_count=5,
                    max_token_count=4096,
                )
            )
            mock_import.return_value = Mock(return_value=mock_service_instance)

            service = ChatService(
                chat_service_type="test",
                chat_history_repository=mock_repo,
                conversation_flow="test_flow",
                config=mock_config,
            )

            request = ChatRequest(
                thread_id="t1",
                user_id="u1",
                user_prompt="test",
                conversation_flow="flow",
            )

            received_chunks = []
            async for chunk in service.get_streaming_chat_response(request):
                received_chunks.append(chunk)

            # Should have content chunks + final chunk
            assert len(received_chunks) >= 2
            assert received_chunks[-1].is_final is True

    @pytest.mark.asyncio
    async def test_streaming_raises_on_missing_conversation_flow(self, mock_streaming_service):
        """Test streaming raises ValueError when conversation_flow is not set."""
        request = ChatRequest(
            thread_id="t1",
            user_id="u1",
            user_prompt="test",
            conversation_flow=None,
        )

        with pytest.raises(ValueError, match="conversation_flow not set"):
            async for _ in mock_streaming_service.get_streaming_chat_response(request):
                pass


class TestChatRequestModel:
    """Test ChatRequest model validation."""

    def test_chat_request_with_all_fields(self):
        """Test creating a ChatRequest with all fields."""
        request = ChatRequest(
            thread_id="thread-123",
            user_id="user-456",
            user_prompt="Hello, how are you?",
            conversation_flow="default_flow",
            topic="greeting",
        )

        assert request.thread_id == "thread-123"
        assert request.user_id == "user-456"
        assert request.user_prompt == "Hello, how are you?"
        assert request.conversation_flow == "default_flow"
        assert request.topic == "greeting"

    def test_chat_request_with_minimal_fields(self):
        """Test creating a ChatRequest with minimal required fields."""
        request = ChatRequest(
            thread_id="thread-123",
            user_id="user-456",
            user_prompt="Hello",
        )

        assert request.thread_id == "thread-123"
        assert request.user_id == "user-456"
        assert request.user_prompt == "Hello"


class TestChatResponseModel:
    """Test ChatResponse model."""

    def test_chat_response_with_all_fields(self):
        """Test creating a ChatResponse with all fields."""
        response = ChatResponse(
            thread_id="thread-123",
            message_id="msg-456",
            agent_response="Hello! How can I help?",
            token_count=10,
            max_token_count=1000,
            topic="greeting",
            memory_summary="User greeted assistant",
            followup_questions={"q1": "What would you like to know?"},
        )

        assert response.thread_id == "thread-123"
        assert response.message_id == "msg-456"
        assert response.agent_response == "Hello! How can I help?"
        assert response.token_count == 10
        assert response.followup_questions == {"q1": "What would you like to know?"}


class TestChatResponseChunkModel:
    """Test ChatResponseChunk model."""

    def test_content_chunk(self):
        """Test creating a content chunk."""
        chunk = ChatResponseChunk(
            thread_id="t1",
            message_id="m1",
            chunk_type="content",
            content="Hello",
            is_final=False,
        )

        assert chunk.chunk_type == "content"
        assert chunk.content == "Hello"
        assert chunk.is_final is False

    def test_final_chunk(self):
        """Test creating a final chunk with metadata."""
        chunk = ChatResponseChunk(
            thread_id="t1",
            message_id="m1",
            chunk_type="final",
            token_count=100,
            max_token_count=1000,
            is_final=True,
        )

        assert chunk.chunk_type == "final"
        assert chunk.token_count == 100
        assert chunk.is_final is True


class TestChatServiceErrorHandling:
    """Test error handling in chat service."""

    @pytest.mark.asyncio
    async def test_handles_service_exception(self):
        """Test that exceptions from underlying service are propagated."""
        mock_config = Mock()
        mock_repo = Mock()

        with patch("ingenious.services.chat_service.import_class_with_fallback") as mock_import:
            mock_service_instance = Mock()
            mock_service_instance.get_chat_response = AsyncMock(
                side_effect=RuntimeError("Service error")
            )
            mock_import.return_value = Mock(return_value=mock_service_instance)

            service = ChatService(
                chat_service_type="test",
                chat_history_repository=mock_repo,
                conversation_flow="test_flow",
                config=mock_config,
            )

            request = ChatRequest(
                thread_id="t1",
                user_id="u1",
                user_prompt="test",
                conversation_flow="flow",
            )

            with pytest.raises(RuntimeError, match="Service error"):
                await service.get_chat_response(request)
