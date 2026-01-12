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
