"""Agent models and data structures."""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Optional, Type

from autogen_agentchat.base import Response
from autogen_agentchat.messages import TextMessage
from autogen_core import (
    CancellationToken,
    FunctionCall,
    MessageContext,
    SingleThreadedAgentRuntime,
    TypeSubscription,
)
from autogen_core.logging import LLMCallEvent
from autogen_core.models import FunctionExecutionResult
from autogen_core.tools import Tool
from pydantic import BaseModel

from ingenious.config import settings as ig_config
from ingenious.config.models import ModelSettings
from ingenious.config.settings import IngeniousSettings
from ingenious.db.chat_history_repository import ChatHistoryRepository
from ingenious.files.files_repository import FileStorage
from ingenious.models.llm_event_kwargs import LLMEventKwargs
from ingenious.models.message import Message as ChatHistoryMessage


class AgentChat(BaseModel):
    """A class used to represent a chat between an agent and a user or between agents.

    Attributes:
    ----------
    agent_name : str
        The name of the agent.
    user_message : str
        The message sent by the user.
    system_prompt : str
        The message sent by the agent.
    """

    chat_name: str
    target_agent_name: str
    source_agent_name: str
    user_message: str
    system_prompt: str
    identifier: Optional[str] = (
        None  # Identifies the data payload associated with the chat for live chat this could be the thread id
    )
    chat_response: Optional[Response] = None
    completion_tokens: int = 0
    prompt_tokens: int = 0
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def get_execution_time(self) -> float:
        """Calculate the execution time in seconds.

        Returns:
            float: The execution time in seconds, or 0.0 if start/end time is not set.
        """
        if self.end_time is None or self.start_time is None:
            return 0.0
        return self.end_time - self.start_time

    def get_execution_time_formatted(self) -> str:
        """Get the execution time formatted as MM:SS.

        Returns:
            str: The execution time in MM:SS format.
        """
        execution_time = self.get_execution_time()
        return f"{int(execution_time // 60)}:{int(execution_time % 60):02d}"

    def get_start_time_formatted(self) -> str:
        """Get the start time formatted as HH:MM:SS.

        Returns:
            str: The start time in HH:MM:SS format, or "00:00:00" if not set.
        """
        if self.start_time is None:
            return "00:00:00"
        return datetime.fromtimestamp(self.start_time).strftime("%H:%M:%S")

    def get_associated_agent_response_file_name(self, identifier: str, event_type: str) -> str:
        """Generate the filename for the agent response file.

        Args:
            identifier: The unique identifier for the chat session.
            event_type: The type of event being logged.

        Returns:
            str: The generated filename in markdown format.
        """
        return f"agent_response_{event_type}_{self.source_agent_name}_{self.target_agent_name}_{identifier.strip()}.md"


class AgentChats(BaseModel):
    """A class used to represent a list of AgentChats.

    Attributes:
    ----------
    agent_chats : List[AgentChat]
        A list of AgentChat objects.
    """

    _agent_chats: List[AgentChat] = []

    def __init__(self) -> None:
        """Initialize an empty AgentChats collection."""
        super().__init__()

    def add_agent_chat(self, agent_chat: AgentChat) -> None:
        """Add an AgentChat to the collection.

        Args:
            agent_chat: The AgentChat object to add.
        """
        self._agent_chats.append(agent_chat)

    def get_agent_chats(self) -> List[AgentChat]:
        """Get all AgentChats in the collection.

        Returns:
            List[AgentChat]: A list of all AgentChat objects.
        """
        return self._agent_chats

    def get_agent_chat_by_name(self, agent_name: str) -> AgentChat:
        """Get the first AgentChat matching the given agent name.

        Args:
            agent_name: The name of the agent to search for (source or target).

        Returns:
            AgentChat: The first matching AgentChat object.

        Raises:
            ValueError: If no AgentChat with the given name is found.
        """
        for agent_chat in self._agent_chats:
            if (
                agent_chat.source_agent_name == agent_name
                or agent_chat.target_agent_name == agent_name
            ):
                return agent_chat
        raise ValueError(f"AgentChat with name {agent_name} not found")

    def get_agent_chats_by_name(self, agent_name: str) -> List[AgentChat]:
        """Get all AgentChats matching the given agent name.

        Args:
            agent_name: The name of the agent to search for (source or target).

        Returns:
            List[AgentChat]: A list of all matching AgentChat objects.
        """
        agent_chats = []
        for agent_chat in self._agent_chats:
            if (
                agent_chat.source_agent_name == agent_name
                or agent_chat.target_agent_name == agent_name
            ):
                agent_chats.append(agent_chat)
        return agent_chats


class Agent(BaseModel):
    """A class used to represent an Agent.

    Attributes:
    ----------
    agent_name : str
        The name of the agent.
    agent_model_name : str
        The name of the model associated with the agent. This should match the name of the associated model in config.yml
    agent_display_name : str
        The display name of the agent.
    agent_description : str
        A brief description of the agent.
    agent_type : str
        The type/category of the agent.
    """

    agent_name: str
    agent_model_name: str
    agent_display_name: str
    agent_description: str
    agent_type: str
    input_topics: list[str] = []
    model: Optional[ModelSettings] = None
    system_prompt: Optional[str] = None
    log_to_prompt_tuner: bool = True
    return_in_response: bool = False
    agent_chats: list[AgentChat] = []

    def add_agent_chat(
        self,
        content: str,
        identifier: str,
        ctx: Optional[MessageContext] = None,
        source: Optional[str] = None,
    ) -> AgentChat:
        """Add a new agent chat to this agent's chat history.

        Args:
            content: The message content.
            identifier: The unique identifier for the chat session.
            ctx: Optional message context containing topic information.
            source: Optional source agent name (overridden by ctx if provided).

        Returns:
            AgentChat: The newly created AgentChat object.
        """
        if ctx and ctx.topic_id:
            source = ctx.topic_id.source

        agent_chat: AgentChat = AgentChat(
            chat_name=self.agent_name + "",
            target_agent_name=self.agent_name,
            source_agent_name=source,
            user_message=content,
            system_prompt=self.system_prompt,
            identifier=identifier,
            chat_response=Response(chat_message=TextMessage(content=content, source=source)),
            start_time=datetime.now().timestamp(),
            end_time=datetime.now().timestamp() + 36000,
        )
        self.agent_chats.append(agent_chat)
        return agent_chat

    def get_agent_chat_by_source(self, source: str) -> AgentChat:
        """Get the agent chat from a specific source agent.

        Args:
            source: The source agent name to search for.

        Returns:
            AgentChat: The matching AgentChat object.

        Raises:
            ValueError: If no AgentChat with the given source is found.
        """
        for agent_chat in self.agent_chats:
            if agent_chat.source_agent_name == source:
                return agent_chat
        raise ValueError(f"AgentChat with source {source} not found")

    async def log(self, agent_chat: AgentChat, queue: asyncio.Queue[AgentChat]) -> None:
        """Log an agent chat to the queue if logging is enabled.

        Args:
            agent_chat: The AgentChat object to log.
            queue: The asyncio queue to add the chat to.
        """
        if self.log_to_prompt_tuner or self.return_in_response:
            await queue.put(agent_chat)

    async def execute_tool_call(
        self,
        call: FunctionCall,
        cancellation_token: CancellationToken,
        tools: List[Tool] = [],
    ) -> FunctionExecutionResult:
        """Execute a tool call from a function call request.

        Args:
            call: The function call to execute.
            cancellation_token: Token to cancel the operation.
            tools: List of available tools to execute.

        Returns:
            FunctionExecutionResult: The result of the tool execution.
        """
        # Find the tool by name.
        tool = next((tool for tool in tools if tool.name == call.name), None)
        assert tool is not None

        # Run the tool and capture the result.
        try:
            arguments = json.loads(call.arguments)
            result = await tool.run_json(arguments, cancellation_token)
            return FunctionExecutionResult(
                call_id=call.id,
                name=call.name,
                content=tool.return_value_as_string(result),
                is_error=False,
            )
        except Exception as e:
            return FunctionExecutionResult(
                call_id=call.id, name=call.name, content=str(e), is_error=True
            )


class Agents(BaseModel):
    """A class used to represent a list of Agents.

    Attributes:
    ----------
    agents : List[Agent]
        A list of Agent objects.
    """

    _agents: List[Agent]

    def __init__(self, agents: List[Agent], config: IngeniousSettings):
        """Initialize the Agents collection with validation.

        Args:
            agents: List of Agent objects to manage.
            config: IngeniousSettings instance containing model configurations.

        Raises:
            ValueError: If an agent's model is not found in the config.
        """
        super().__init__()
        self._agents = agents
        for agent in self._agents:
            for model in config.models:
                if model.model == agent.agent_model_name:
                    agent.model = model
                    break
            if not agent.model:
                raise ValueError(f"Model {agent.agent_model_name} not found in config.yml")

    def get_agents(self) -> List[Agent]:
        """Get all agents in the collection.

        Returns:
            List[Agent]: A list of all Agent objects.
        """
        return self._agents

    def get_agents_for_prompt_tuner(self) -> List[Agent]:
        """Get all agents that have logging to prompt tuner enabled.

        Returns:
            List[Agent]: A list of agents with log_to_prompt_tuner set to True.
        """
        return [agent for agent in self._agents if agent.log_to_prompt_tuner]

    def get_agent_by_name(self, agent_name: str) -> Agent:
        """Get an agent by its name.

        Args:
            agent_name: The name of the agent to retrieve.

        Returns:
            Agent: The matching Agent object.

        Raises:
            ValueError: If no agent with the given name is found.
        """
        for agent in self._agents:
            if agent.agent_name == agent_name:
                return agent
        raise ValueError(f"Agent with name {agent_name} not found")

    async def register_agent(
        self,
        ag_class: Type[Any],
        runtime: SingleThreadedAgentRuntime,
        agent_name: str,
        data_identifier: str,
        next_agent_topic: str,
        tools: List[Tool] = [],
    ) -> None:
        """Register an agent with the runtime and subscribe it to its topic.

        Args:
            ag_class: The agent class to instantiate.
            runtime: The agent runtime to register with.
            agent_name: The name of the agent to register.
            data_identifier: Identifier for the data payload.
            next_agent_topic: The topic for the next agent in the chain.
            tools: List of tools available to the agent.
        """
        agent = self.get_agent_by_name(agent_name=agent_name)
        reg_agent = await ag_class.register(
            runtime=runtime,
            type=agent.agent_name,
            factory=lambda: ag_class(
                agent=agent,
                data_identifier=data_identifier,
                next_agent_topic=next_agent_topic,
                tools=tools,
            ),
        )
        await runtime.add_subscription(
            TypeSubscription(topic_type=agent_name, agent_type=reg_agent.type)
        )


class AgentMessage(BaseModel):
    """A simple message container for agent communication.

    Attributes:
        content: The message content string.
    """

    content: str


class LLMUsageTracker(logging.Handler):
    """Logging handler that tracks LLM token usage and agent chat interactions.

    This handler intercepts LLM call events, tracks token counts, and manages
    a queue of agent chats for logging and analysis purposes.
    """

    def __init__(
        self,
        agents: Agents,
        config: ig_config.IngeniousSettings,
        chat_history_repository: ChatHistoryRepository,
        revision_id: str,
        identifier: str,
        event_type: str,
    ) -> None:
        """Initialize the LLM usage tracker.

        Args:
            agents: Agents collection to track interactions for.
            config: IngeniousSettings instance for configuration.
            chat_history_repository: Repository for storing chat history.
            revision_id: Identifier for the current revision.
            identifier: Unique identifier for the session.
            event_type: Type of event being tracked.
        """
        super().__init__()
        self._prompt_tokens = 0
        self._agents = agents
        self._completion_tokens = 0
        self._queue: List[AgentChat] = []
        self._config = config
        self._chat_history_database: ChatHistoryRepository = chat_history_repository
        self._revision_id: str = revision_id
        self._identifier: str = identifier
        self._event_type: str = event_type

    @property
    def tokens(self) -> int:
        """Get the total number of tokens used (prompt + completion).

        Returns:
            int: The sum of prompt and completion tokens.
        """
        return self._prompt_tokens + self._completion_tokens

    @property
    def prompt_tokens(self) -> int:
        """Get the number of prompt tokens used.

        Returns:
            int: The number of prompt tokens.
        """
        return self._prompt_tokens

    @property
    def completion_tokens(self) -> int:
        """Get the number of completion tokens used.

        Returns:
            int: The number of completion tokens.
        """
        return self._completion_tokens

    def reset(self) -> None:
        """Reset the token counters to zero."""
        self._prompt_tokens = 0
        self._completion_tokens = 0

    async def write_llm_responses_to_file(self, file_prefixes: List[str] = []) -> None:
        """Write LLM responses from the queue to files.

        Args:
            file_prefixes: List of prefix strings to prepend to the filename.
        """
        for agent_chat in self._queue:
            agent = self._agents.get_agent_by_name(agent_chat.target_agent_name)
            if agent.log_to_prompt_tuner:
                fs = FileStorage(self._config)
                output_path = await fs.get_output_path(self._revision_id)
                content = agent_chat.model_dump_json()
                temp_file_prefixes = file_prefixes.copy()
                temp_file_prefixes.append("agent_response")
                temp_file_prefixes.append(self._event_type)
                temp_file_prefixes.append(agent_chat.source_agent_name)
                temp_file_prefixes.append(agent_chat.target_agent_name)
                temp_file_prefixes.append(self._identifier)
                await fs.write_file(content, f"{'_'.join(temp_file_prefixes)}.md", output_path)

    # TODO: Implement this function
    async def write_llm_responses_to_repository(
        self, user_id: str, thread_id: str, message_id: str
    ) -> None:
        """Write LLM responses from the queue to the chat history repository.

        Args:
            user_id: The ID of the user.
            thread_id: The ID of the conversation thread.
            message_id: The ID of the message.
        """
        for agent_chat in self._queue:
            agent = self._agents.get_agent_by_name(agent_chat.target_agent_name)
            if agent.log_to_prompt_tuner:
                fs = FileStorage(self._config)
                output_path = await fs.get_output_path(self._revision_id)
                content = agent_chat.model_dump_json()
                await fs.write_file(
                    content,
                    f"agent_response_{self._event_type}_{agent_chat.source_agent_name}_{agent_chat.target_agent_name}_{self._identifier}.md",
                    output_path,
                )

                message: ChatHistoryMessage = ChatHistoryMessage(
                    user_id=user_id,
                    thread_id=thread_id,
                    message_id=message_id,
                    role="agent_chat",
                    # Get the item from the queue where chat_name = "summary"
                    content=agent_chat.model_dump_json(),
                    content_filter_results=None,
                    tool_calls=None,
                    tool_call_id=None,
                    tool_call_function=None,
                )

                await self._chat_history_database.add_message(message=message)

    async def post_chats_to_queue(self, target_queue: asyncio.Queue[AgentChat]) -> None:
        """Post agent chats from the internal queue to a target queue.

        Args:
            target_queue: The asyncio queue to post chats to.
        """
        for agent_chat in self._queue:
            agent = self._agents.get_agent_by_name(agent_chat.target_agent_name)
            await agent.log(agent_chat, target_queue)

    def emit(self, record: logging.LogRecord) -> None:
        """Emit the log record."""
        try:
            add_chat = True
            if isinstance(record.msg, LLMCallEvent):
                event: LLMCallEvent = record.msg
                kwargs: LLMEventKwargs = LLMEventKwargs.model_validate(event.kwargs)

                if kwargs.agent_id:
                    agent_name = kwargs.agent_id.split("/")[0]
                    source_name = kwargs.agent_id.split("/")[1]
                else:
                    return

                # Handle both Agents object and list
                agent = None
                if hasattr(self._agents, "get_agent_by_name"):
                    try:
                        agent = self._agents.get_agent_by_name(agent_name)
                    except ValueError:
                        # Agent not found in the list
                        pass
                response = ""
                system_input = ""
                user_input = ""
                if kwargs.response and kwargs.response.choices:
                    for r in kwargs.response.choices:
                        content = r.message.content if r.message else None
                        if content:
                            response += content + "\n\n"
                        if r.message and r.message.tool_calls:
                            for tool_call in r.message.tool_calls:
                                add_chat = False

                        system_input = "\n\n".join(
                            [
                                r.content
                                for r in (kwargs.messages or [])
                                if r and r.role == "system" and r.content
                            ]
                        )
                        user_input = "\n\n".join(
                            [
                                r.content
                                for r in (kwargs.messages or [])
                                if r and r.role == "user" and r.content
                            ]
                        )

                        # Get all messages with role 'tool'
                        tool_messages = [
                            m for m in (kwargs.messages or []) if m and m.role == "tool"
                        ]
                        if tool_messages:
                            user_input += "\n\n---\n\n"
                            user_input += "# Tool Messages\n\n"
                            for m in tool_messages:
                                if m.content:
                                    user_input += f"{m.content}\n\n"

                # Update token counts regardless of agent availability
                self._prompt_tokens += event.prompt_tokens
                self._completion_tokens += event.completion_tokens

                # Only update agent-specific data if agent is available
                if agent:
                    chat = agent.get_agent_chat_by_source(source=source_name)
                    chat.chat_response = Response(
                        chat_message=TextMessage(content=response, source=source_name)
                    )
                    chat.prompt_tokens = event.prompt_tokens
                    chat.completion_tokens = event.completion_tokens
                    chat.system_prompt = system_input
                    chat.user_message = user_input
                    chat.end_time = datetime.now().timestamp()
                    if add_chat:
                        self._queue.append(chat)

        except Exception as e:
            print(f"Failed to emit log record :{e}")
            self.handleError(record)


class IProjectAgents(ABC):
    """Abstract base class for project-specific agent configurations.

    This interface defines the contract for retrieving project-specific
    agent configurations. Implementations should provide the agents
    appropriate for their project context.
    """

    def __init__(self) -> None:
        """Initialize the project agents interface."""
        pass

    @abstractmethod
    def Get_Project_Agents(self, config: IngeniousSettings) -> Agents:
        """Get the project-specific agents configuration.

        Args:
            config: The Ingenious settings configuration.

        Returns:
            Agents: The configured Agents collection for the project.
        """
        pass
