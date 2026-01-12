"""Tests for multi-agent chat service.

This module contains comprehensive tests for:
- MultiAgentChatService
- stream_response_as_chunks utility
- IConversationFlow abstract base class
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ingenious.models.chat import ChatResponse


class TestStreamResponseAsChunks:
    """Test cases for stream_response_as_chunks utility function."""

    @pytest.mark.asyncio
    async def test_streams_content_in_chunks(self):
        """Test content is streamed in specified chunk size."""
        from ingenious.services.chat_services.multi_agent.service import stream_response_as_chunks

        response = ChatResponse(
            thread_id="test-thread",
            message_id="test-message",
            agent_response="This is a test response that should be chunked.",
            token_count=10,
            max_token_count=100,
        )

        chunks = []
        async for chunk in stream_response_as_chunks(response, chunk_size=10):
            chunks.append(chunk)

        # Should have multiple content chunks plus final chunk
        content_chunks = [c for c in chunks if c.chunk_type == "content"]
        final_chunks = [c for c in chunks if c.chunk_type == "final"]

        assert len(content_chunks) > 1
        assert len(final_chunks) == 1

    @pytest.mark.asyncio
    async def test_final_chunk_contains_metadata(self):
        """Test final chunk contains all metadata."""
        from ingenious.services.chat_services.multi_agent.service import stream_response_as_chunks

        response = ChatResponse(
            thread_id="test-thread",
            message_id="test-message",
            agent_response="Test response",
            token_count=10,
            max_token_count=100,
            topic="test-topic",
            memory_summary="memory summary",
            followup_questions={"q1": "Question 1", "q2": "Question 2"},
        )

        chunks = []
        async for chunk in stream_response_as_chunks(response, chunk_size=100):
            chunks.append(chunk)

        final_chunk = [c for c in chunks if c.chunk_type == "final"][0]

        assert final_chunk.is_final is True
        assert final_chunk.token_count == 10
        assert final_chunk.max_token_count == 100
        assert final_chunk.topic == "test-topic"
        assert final_chunk.memory_summary == "memory summary"
        assert final_chunk.followup_questions == {"q1": "Question 1", "q2": "Question 2"}

    @pytest.mark.asyncio
    async def test_empty_response_only_yields_final_chunk(self):
        """Test empty response only yields final chunk."""
        from ingenious.services.chat_services.multi_agent.service import stream_response_as_chunks

        response = ChatResponse(
            thread_id="test-thread",
            message_id="test-message",
            agent_response="",
            token_count=0,
            max_token_count=100,
        )

        chunks = []
        async for chunk in stream_response_as_chunks(response, chunk_size=100):
            chunks.append(chunk)

        assert len(chunks) == 1
        assert chunks[0].chunk_type == "final"

    @pytest.mark.asyncio
    async def test_preserves_thread_and_message_ids(self):
        """Test thread and message IDs are preserved in chunks."""
        from ingenious.services.chat_services.multi_agent.service import stream_response_as_chunks

        response = ChatResponse(
            thread_id="specific-thread-id",
            message_id="specific-message-id",
            agent_response="Test response",
            token_count=10,
            max_token_count=100,
        )

        async for chunk in stream_response_as_chunks(response, chunk_size=100):
            assert chunk.thread_id == "specific-thread-id"
            assert chunk.message_id == "specific-message-id"


class TestMultiAgentChatServiceInit:
    """Test cases for MultiAgentChatService initialization."""

    @pytest.fixture
    def mock_config(self):
        """Create mock config."""
        config = MagicMock()
        config.openai_service_instance = MagicMock()
        config.chat_history = MagicMock()
        config.chat_history.memory_path = "/tmp/memory"  # nosec B108
        return config

    @pytest.fixture
    def mock_chat_history_repo(self):
        """Create mock chat history repository."""
        return AsyncMock()

    def test_init_with_openai_service(self, mock_config, mock_chat_history_repo):
        """Test initialization with OpenAI service configured."""
        from ingenious.services.chat_services.multi_agent.service import MultiAgentChatService

        service = MultiAgentChatService(
            config=mock_config,
            chat_history_repository=mock_chat_history_repo,
            conversation_flow="test-flow",
        )

        assert service.config == mock_config
        assert service.chat_history_repository == mock_chat_history_repo
        assert service.conversation_flow == "test-flow"

    def test_init_raises_without_openai_service(self, mock_chat_history_repo):
        """Test initialization raises error without OpenAI service."""
        from ingenious.services.chat_services.multi_agent.service import MultiAgentChatService

        config = MagicMock(spec=[])  # No openai_service_instance attribute

        with pytest.raises(RuntimeError) as exc_info:
            MultiAgentChatService(
                config=config,
                chat_history_repository=mock_chat_history_repo,
                conversation_flow="test-flow",
            )

        assert "OpenAI service not properly configured" in str(exc_info.value)


class TestMultiAgentChatServiceHelpers:
    """Test cases for MultiAgentChatService helper methods."""

    @pytest.fixture
    def service(self):
        """Create service with mocked dependencies."""
        from ingenious.services.chat_services.multi_agent.service import MultiAgentChatService

        config = MagicMock()
        config.openai_service_instance = MagicMock()

        with patch.object(MultiAgentChatService, "__init__", lambda x, *args, **kwargs: None):
            service = MultiAgentChatService.__new__(MultiAgentChatService)
            service.config = config
            service.chat_history_repository = AsyncMock()
            service.conversation_flow = "test-flow"
            return service

    def test_build_thread_memory_empty(self, service):
        """Test build thread memory with no messages."""
        result = service._build_thread_memory(None)
        assert result == "no existing context."

        result = service._build_thread_memory([])
        assert result == "no existing context."

    def test_build_thread_memory_with_messages(self, service):
        """Test build thread memory with messages."""
        messages = [
            MagicMock(role="user", content="Hello"),
            MagicMock(role="assistant", content="Hi there!"),
        ]

        result = service._build_thread_memory(messages)

        assert "user: Hello" in result
        assert "assistant: Hi there!" in result

    def test_build_thread_memory_truncates_long_content(self, service):
        """Test build thread memory truncates long content."""
        long_content = "x" * 300
        messages = [MagicMock(role="user", content=long_content)]

        result = service._build_thread_memory(messages)

        # Content should be truncated to 200 chars + "..."
        assert len(result) < len(long_content) + 20

    def test_build_thread_memory_respects_max_messages(self, service):
        """Test build thread memory respects max_messages limit."""
        messages = [MagicMock(role="user", content=f"msg{i}") for i in range(20)]

        result = service._build_thread_memory(messages, max_messages=5)

        # Should only contain last 5 messages
        assert "msg15" in result
        assert "msg19" in result
        assert "msg0" not in result

    def test_validate_thread_messages_no_errors(self, service):
        """Test validate thread messages with no filter results."""
        messages = [
            MagicMock(content_filter_results=None),
            MagicMock(content_filter_results=None),
        ]

        # Should not raise
        service._validate_thread_messages(messages)

    def test_validate_thread_messages_raises_on_filter_results(self, service):
        """Test validate thread messages raises on content filter results."""
        from ingenious.errors.content_filter_error import ContentFilterError

        messages = [
            MagicMock(content_filter_results={"hate": {"filtered": True}}),
        ]

        with pytest.raises(ContentFilterError):
            service._validate_thread_messages(messages)

    def test_append_thread_history_no_history(self, service):
        """Test append thread history with no existing history."""
        chat_request = MagicMock()
        chat_request.thread_chat_history = None

        # Should not raise
        service._append_thread_history(chat_request, [])

    def test_append_thread_history_appends_messages(self, service):
        """Test append thread history appends messages when history is not empty."""
        # Use a real list with initial content (method returns early if empty)
        thread_history = [{"role": "system", "content": "initial"}]
        chat_request = MagicMock()
        chat_request.thread_chat_history = thread_history

        messages = [
            MagicMock(role="user", content="Hello"),
            MagicMock(role="assistant", content="Hi"),
        ]

        service._append_thread_history(chat_request, messages)

        # Check using the actual list reference (initial + 2 new)
        assert len(thread_history) == 3
        assert thread_history[1]["role"] == "user"
        assert thread_history[1]["content"] == "Hello"
        assert thread_history[2]["role"] == "assistant"
        assert thread_history[2]["content"] == "Hi"


class TestMultiAgentChatServiceGetChatResponse:
    """Test cases for get_chat_response method."""

    @pytest.fixture
    def service(self):
        """Create service with mocked dependencies."""
        from ingenious.services.chat_services.multi_agent.service import MultiAgentChatService

        config = MagicMock()
        config.openai_service_instance = MagicMock()

        with patch.object(MultiAgentChatService, "__init__", lambda x, *args, **kwargs: None):
            service = MultiAgentChatService.__new__(MultiAgentChatService)
            service.config = config
            service.chat_history_repository = AsyncMock()
            service.chat_history_repository.get_thread_messages = AsyncMock(return_value=[])
            service.conversation_flow = "test-flow"
            return service

    @pytest.mark.asyncio
    async def test_raises_when_no_conversation_flow(self, service):
        """Test raises ValueError when conversation_flow not set."""
        chat_request = MagicMock()
        chat_request.conversation_flow = None

        with pytest.raises(ValueError) as exc_info:
            await service.get_chat_response(chat_request)

        assert "conversation_flow not set" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_generates_thread_id_if_not_provided(self, service):
        """Test generates thread_id if not provided."""
        chat_request = MagicMock()
        chat_request.conversation_flow = "test-flow"
        chat_request.topic = None
        chat_request.thread_id = None
        chat_request.user_id = None
        chat_request.user_prompt = "test"

        with patch.object(service, "_execute_conversation_flow") as mock_execute:
            mock_execute.return_value = ChatResponse(
                thread_id="gen-thread",
                message_id="gen-message",
                agent_response="response",
                token_count=0,
                max_token_count=100,
            )

            await service.get_chat_response(chat_request)

        # thread_id should be set
        assert chat_request.thread_id is not None

    @pytest.mark.asyncio
    async def test_processes_topic_as_string(self, service):
        """Test processes topic string into list."""
        chat_request = MagicMock()
        chat_request.conversation_flow = "test-flow"
        chat_request.topic = "topic1, topic2, topic3"
        chat_request.thread_id = "test-thread"
        chat_request.user_id = None
        chat_request.user_prompt = "test"

        with patch.object(service, "_execute_conversation_flow") as mock_execute:
            mock_execute.return_value = ChatResponse(
                thread_id="test-thread",
                message_id="test-message",
                agent_response="response",
                token_count=0,
                max_token_count=100,
            )

            await service.get_chat_response(chat_request)

        # topic should be a list
        assert isinstance(chat_request.topic, list)
        assert len(chat_request.topic) == 3

    @pytest.mark.asyncio
    async def test_saves_chat_history_when_memory_enabled(self, service):
        """Test saves chat history when memory_record is enabled."""
        chat_request = MagicMock()
        chat_request.conversation_flow = "test-flow"
        chat_request.topic = None
        chat_request.thread_id = "test-thread"
        chat_request.user_id = "test-user"
        chat_request.user_prompt = "test prompt"
        chat_request.memory_record = True

        with (
            patch.object(service, "_execute_conversation_flow") as mock_execute,
            patch.object(service, "_save_chat_history") as mock_save,
        ):
            mock_execute.return_value = ChatResponse(
                thread_id="test-thread",
                message_id="test-message",
                agent_response="response",
                token_count=0,
                max_token_count=100,
            )

            await service.get_chat_response(chat_request)

        mock_save.assert_called_once()


class TestMultiAgentChatServiceNormalizeResponse:
    """Test cases for _normalize_response method."""

    @pytest.fixture
    def service(self):
        """Create service with mocked dependencies."""
        from ingenious.services.chat_services.multi_agent.service import MultiAgentChatService

        config = MagicMock()
        config.openai_service_instance = MagicMock()

        with patch.object(MultiAgentChatService, "__init__", lambda x, *args, **kwargs: None):
            service = MultiAgentChatService.__new__(MultiAgentChatService)
            service.config = config
            service.chat_history_repository = AsyncMock()
            service.conversation_flow = "test-flow"
            return service

    def test_returns_chat_response_unchanged(self, service):
        """Test returns ChatResponse unchanged."""
        chat_request = MagicMock()
        chat_request.thread_id = "test-thread"

        response = ChatResponse(
            thread_id="test-thread",
            message_id="test-message",
            agent_response="response",
            token_count=10,
            max_token_count=100,
        )

        result = service._normalize_response(response, chat_request)

        assert result == response

    def test_normalizes_tuple_response(self, service):
        """Test normalizes tuple response to ChatResponse."""
        chat_request = MagicMock()
        chat_request.thread_id = "test-thread"

        response = ("This is the response text", "This is the memory summary")

        result = service._normalize_response(response, chat_request)

        assert isinstance(result, ChatResponse)
        assert result.agent_response == "This is the response text"
        assert result.memory_summary == "This is the memory summary"

    def test_normalizes_string_response(self, service):
        """Test normalizes string response to ChatResponse."""
        chat_request = MagicMock()
        chat_request.thread_id = "test-thread"

        response = "Simple string response"

        result = service._normalize_response(response, chat_request)

        assert isinstance(result, ChatResponse)
        assert result.agent_response == "Simple string response"


class TestMultiAgentChatServiceStreaming:
    """Test cases for streaming chat response."""

    @pytest.fixture
    def service(self):
        """Create service with mocked dependencies."""
        from ingenious.services.chat_services.multi_agent.service import MultiAgentChatService

        config = MagicMock()
        config.openai_service_instance = MagicMock()

        with patch.object(MultiAgentChatService, "__init__", lambda x, *args, **kwargs: None):
            service = MultiAgentChatService.__new__(MultiAgentChatService)
            service.config = config
            service.chat_history_repository = AsyncMock()
            service.conversation_flow = "test-flow"
            return service

    @pytest.mark.asyncio
    async def test_raises_when_no_conversation_flow(self, service):
        """Test raises ValueError when conversation_flow not set."""
        chat_request = MagicMock()
        chat_request.conversation_flow = None

        with pytest.raises(ValueError) as exc_info:
            async for _ in service.get_streaming_chat_response(chat_request):
                pass

        assert "conversation_flow not set" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_yields_error_chunk_on_import_error(self, service):
        """Test yields error chunk when conversation flow import fails."""
        chat_request = MagicMock()
        chat_request.conversation_flow = "nonexistent-flow"
        chat_request.thread_id = "test-thread"
        chat_request.thread_memory = ""
        chat_request.memory_record = True
        chat_request.thread_chat_history = []
        chat_request.user_prompt = "test"

        with (
            patch(
                "ingenious.services.chat_services.multi_agent.service.import_class_with_fallback"
            ) as mock_import,
            patch("ingenious.services.chat_services.multi_agent.service.logger"),
        ):
            mock_import.side_effect = ImportError("Module not found")

            chunks = []
            async for chunk in service.get_streaming_chat_response(chat_request):
                chunks.append(chunk)

        assert len(chunks) == 1
        assert chunks[0].chunk_type == "error"
        assert "not found" in chunks[0].content


class TestIConversationFlow:
    """Test cases for IConversationFlow abstract base class."""

    @pytest.fixture
    def mock_parent_service(self):
        """Create mock parent service."""
        from ingenious.services.chat_services.multi_agent.service import MultiAgentChatService

        config = MagicMock()
        config.chat_history = MagicMock()
        config.chat_history.memory_path = "/tmp/memory"  # nosec B108
        config.models = MagicMock()

        parent = MagicMock(spec=MultiAgentChatService)
        parent.config = config

        return parent

    def test_cannot_instantiate_abstract_class(self):
        """Test IConversationFlow cannot be instantiated directly."""
        from ingenious.services.chat_services.multi_agent.service import IConversationFlow

        with pytest.raises(TypeError) as exc_info:
            IConversationFlow(parent_multi_agent_chat_service=MagicMock())

        assert "abstract" in str(exc_info.value).lower()

    def test_concrete_implementation_works(self, mock_parent_service):
        """Test concrete implementation can be instantiated."""
        from ingenious.models.chat import IChatRequest, IChatResponse
        from ingenious.services.chat_services.multi_agent.service import IConversationFlow

        class ConcreteFlow(IConversationFlow):
            async def get_conversation_response(self, chat_request: IChatRequest) -> IChatResponse:
                return ChatResponse(
                    thread_id="test",
                    message_id="test",
                    agent_response="response",
                    token_count=0,
                    max_token_count=100,
                )

        with patch("ingenious.services.memory_manager.get_memory_manager"):
            flow = ConcreteFlow(parent_multi_agent_chat_service=mock_parent_service)

        assert flow is not None
        assert flow._config == mock_parent_service.config

    def test_get_config_returns_config(self, mock_parent_service):
        """Test get_config returns configuration."""
        from ingenious.models.chat import IChatRequest, IChatResponse
        from ingenious.services.chat_services.multi_agent.service import IConversationFlow

        class ConcreteFlow(IConversationFlow):
            async def get_conversation_response(self, chat_request: IChatRequest) -> IChatResponse:
                return ChatResponse(
                    thread_id="t",
                    message_id="m",
                    agent_response="r",
                    token_count=0,
                    max_token_count=0,
                )

        with patch("ingenious.services.memory_manager.get_memory_manager"):
            flow = ConcreteFlow(parent_multi_agent_chat_service=mock_parent_service)

        assert flow.get_config() == mock_parent_service.config

    def test_get_models_returns_models(self, mock_parent_service):
        """Test get_models returns models configuration."""
        from ingenious.models.chat import IChatRequest, IChatResponse
        from ingenious.services.chat_services.multi_agent.service import IConversationFlow

        class ConcreteFlow(IConversationFlow):
            async def get_conversation_response(self, chat_request: IChatRequest) -> IChatResponse:
                return ChatResponse(
                    thread_id="t",
                    message_id="m",
                    agent_response="r",
                    token_count=0,
                    max_token_count=0,
                )

        with patch("ingenious.services.memory_manager.get_memory_manager"):
            flow = ConcreteFlow(parent_multi_agent_chat_service=mock_parent_service)

        assert flow.get_models() == mock_parent_service.config.models

    def test_get_memory_path_returns_path(self, mock_parent_service):
        """Test get_memory_path returns memory path."""
        from ingenious.models.chat import IChatRequest, IChatResponse
        from ingenious.services.chat_services.multi_agent.service import IConversationFlow

        class ConcreteFlow(IConversationFlow):
            async def get_conversation_response(self, chat_request: IChatRequest) -> IChatResponse:
                return ChatResponse(
                    thread_id="t",
                    message_id="m",
                    agent_response="r",
                    token_count=0,
                    max_token_count=0,
                )

        with patch("ingenious.services.memory_manager.get_memory_manager"):
            flow = ConcreteFlow(parent_multi_agent_chat_service=mock_parent_service)

        assert flow.get_memory_path() == "/tmp/memory"  # nosec B108

    def test_get_memory_file_returns_full_path(self, mock_parent_service):
        """Test get_memory_file returns full memory file path."""
        from ingenious.models.chat import IChatRequest, IChatResponse
        from ingenious.services.chat_services.multi_agent.service import IConversationFlow

        class ConcreteFlow(IConversationFlow):
            async def get_conversation_response(self, chat_request: IChatRequest) -> IChatResponse:
                return ChatResponse(
                    thread_id="t",
                    message_id="m",
                    agent_response="r",
                    token_count=0,
                    max_token_count=0,
                )

        with patch("ingenious.services.memory_manager.get_memory_manager"):
            flow = ConcreteFlow(parent_multi_agent_chat_service=mock_parent_service)

        assert flow.get_memory_file() == "/tmp/memory/context.md"  # nosec B108

    @pytest.mark.asyncio
    async def test_default_streaming_falls_back_to_chunks(self, mock_parent_service):
        """Test default streaming implementation falls back to chunking."""
        from ingenious.models.chat import IChatRequest, IChatResponse
        from ingenious.services.chat_services.multi_agent.service import IConversationFlow

        class ConcreteFlow(IConversationFlow):
            async def get_conversation_response(self, chat_request: IChatRequest) -> IChatResponse:
                return ChatResponse(
                    thread_id="test",
                    message_id="test",
                    agent_response="Test response",
                    token_count=0,
                    max_token_count=100,
                )

        with patch("ingenious.services.memory_manager.get_memory_manager"):
            flow = ConcreteFlow(parent_multi_agent_chat_service=mock_parent_service)

        chat_request = MagicMock()

        chunks = []
        async for chunk in flow.get_streaming_conversation_response(chat_request):
            chunks.append(chunk)

        assert len(chunks) > 0
        assert chunks[-1].is_final is True
