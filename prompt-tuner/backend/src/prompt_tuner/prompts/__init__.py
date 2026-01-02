"""Prompts module with mock data."""

from prompt_tuner.models import Prompt, Revision


def get_revisions() -> list[Revision]:
    """Get all revisions."""
    return [
        Revision(
            id="quickstart-1",
            name="quickstart-1",
            createdAt="2024-01-15T10:00:00Z",
            promptCount=4,
        ),
        Revision(
            id="magical-crystal-51211a8b",
            name="magical-crystal-51211a8b",
            createdAt="2024-01-14T15:30:00Z",
            promptCount=4,
        ),
        Revision(
            id="production-v2",
            name="production-v2",
            createdAt="2024-01-10T09:00:00Z",
            promptCount=4,
        ),
    ]


def get_prompts(revision: str) -> list[Prompt]:
    """Get prompts for a revision."""
    return [
        Prompt(
            filename="router_prompt.jinja",
            description="Routes user queries to appropriate agents",
            content="""You are a routing agent for the {{ workflow }} workflow.
Your job is to analyze the user's query and determine which agent should handle it.

Available agents:
{% for agent in agents %}
- {{ agent.name }}: {{ agent.description }}
{% endfor %}

User query: {{ user_query }}

Respond with the name of the agent that should handle this query.""",
            size=2150,
            tags=["system", "routing"],
            variables=["workflow", "agents", "user_query"],
        ),
        Prompt(
            filename="sql_agent_prompt.jinja",
            description="Generates SQL queries from natural language",
            content="""You are a SQL generation agent.
Given the user's natural language query, generate a SQL query for the {{ database }} database.

Schema:
{{ schema }}

User query: {{ user_query }}

Generate a valid SQL query that answers the user's question.""",
            size=3300,
            tags=["agent", "sql"],
            variables=["database", "schema", "user_query"],
        ),
        Prompt(
            filename="analyst_prompt.jinja",
            description="Analyzes data and provides insights",
            content="""You are a data analyst agent.
Analyze the following data and provide insights.

Data:
{{ data }}

User question: {{ user_query }}

Provide a clear, concise analysis with key insights.""",
            size=1800,
            tags=["agent", "analysis"],
            variables=["data", "user_query"],
        ),
        Prompt(
            filename="summary_prompt.jinja",
            description="Summarizes findings for user consumption",
            content="""You are a summary agent.
Summarize the following findings in a user-friendly format.

Findings:
{{ findings }}

Original question: {{ user_query }}

Provide a clear, helpful summary.""",
            size=1200,
            tags=["agent", "output"],
            variables=["findings", "user_query"],
        ),
    ]


def get_prompt(revision: str, filename: str) -> Prompt | None:
    """Get a specific prompt."""
    prompts = get_prompts(revision)
    for prompt in prompts:
        if prompt.filename == filename:
            return prompt
    return None


# In-memory storage for edited prompts
_edited_prompts: dict[str, dict[str, str]] = {}


def update_prompt(revision: str, filename: str, content: str) -> bool:
    """Update a prompt's content."""
    if revision not in _edited_prompts:
        _edited_prompts[revision] = {}
    _edited_prompts[revision][filename] = content
    return True
