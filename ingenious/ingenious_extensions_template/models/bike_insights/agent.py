"""Project agents configuration for bike insights workflow.

This module defines the agent configuration for the bike insights
multi-agent conversation flow.
"""

from ingenious.models.agent import Agent, Agents, IProjectAgents
from ingenious.models.config import Config


class ProjectAgents(IProjectAgents):
    """Project agents configuration for bike insights.

    This class defines and configures all agents used in the bike insights
    workflow, including sentiment analysis, fiscal analysis, and summary agents.
    """

    def Get_Project_Agents(self, config: Config) -> Agents:
        """Get the configured project agents for bike insights workflow.

        Args:
            config: The application configuration object.

        Returns:
            An Agents collection containing all configured agents.
        """
        local_agents = []
        local_agents.append(
            Agent(
                agent_name="customer_sentiment_agent",
                agent_model_name="gpt-5-mini",
                agent_display_name="Customer Sentiment",
                agent_description="A sample agent.",
                agent_type="researcher",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=False,
            )
        )
        local_agents.append(
            Agent(
                agent_name="fiscal_analysis_agent",
                agent_model_name="gpt-5-mini",
                agent_display_name="Fiscal Analysis",
                agent_description="A sample agent.",
                agent_type="researcher",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=False,
            )
        )
        local_agents.append(
            Agent(
                agent_name="summary",
                agent_model_name="gpt-5-mini",
                agent_display_name="Summarizer",
                agent_description="A sample agent.",
                agent_type="summary",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=True,
            )
        )
        local_agents.append(
            Agent(
                agent_name="user_proxy",
                agent_model_name="gpt-5-mini",
                agent_display_name="user_proxy_agent",
                agent_description="A sample agent.",
                agent_type="user_proxy",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=False,
                return_in_response=False,
            )
        )
        local_agents.append(
            Agent(
                agent_name="bike_lookup_agent",
                agent_model_name="gpt-5-mini",
                agent_display_name="bike_lookup_agent",
                agent_description="A sample agent.",
                agent_type="user_proxy",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=False,
            )
        )

        return Agents(agents=local_agents, config=config)
