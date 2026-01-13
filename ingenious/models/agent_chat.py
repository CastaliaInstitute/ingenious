"""Agent chat models for tracking conversations between agents.

This module provides models for representing and managing chat interactions
between agents, including individual chats and collections of chats.
"""

from typing import List, Optional

from autogen_agentchat.base import Response
from pydantic import BaseModel


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
