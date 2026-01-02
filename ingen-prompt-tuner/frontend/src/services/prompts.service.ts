import type { Prompt } from '@/types'

// Mock data for demo
const mockPrompts: Prompt[] = [
  {
    filename: 'router_prompt.jinja',
    description: 'Routes user queries to appropriate agents',
    content: `You are a routing agent that determines which specialized agent should handle a user query.

Available agents:
{% for agent in available_agents %}
- {{ agent.name }}: {{ agent.description }}
{% endfor %}

User query: {{ user_query }}

Analyze the query and respond with the agent name that should handle it.`,
    size: 2100,
    tags: ['system', 'routing'],
    variables: ['available_agents', 'user_query']
  },
  {
    filename: 'sql_agent_prompt.jinja',
    description: 'Generates SQL queries from natural language',
    content: `You are a SQL expert. Generate SQL queries based on natural language requests.

Database schema:
{{ schema }}

User request: {{ user_request }}

Generate a valid SQL query that answers the request. Only output the SQL, no explanations.`,
    size: 3400,
    tags: ['agent', 'sql'],
    variables: ['schema', 'user_request']
  },
  {
    filename: 'analyst_prompt.jinja',
    description: 'Analyzes data and provides insights',
    content: `You are a data analyst specializing in {{ domain }} data.

Your task is to analyze the provided data and extract
meaningful insights for the user.

{# Analysis guidelines #}
{% if include_recommendations %}
Include actionable recommendations based on the data.
{% endif %}

Format your response as:
1. Key Findings (bullet points)
2. Trends Analysis
3. Recommendations

Data to analyze:
{{ data }}`,
    size: 1800,
    tags: ['agent', 'analysis'],
    variables: ['domain', 'data', 'include_recommendations']
  },
  {
    filename: 'summary_prompt.jinja',
    description: 'Summarizes findings for user consumption',
    content: `Summarize the following analysis results for a non-technical audience.

Analysis results:
{{ results }}

Keep the summary concise (2-3 paragraphs) and focus on key takeaways.`,
    size: 1200,
    tags: ['agent', 'output'],
    variables: ['results']
  }
]

export const promptsService = {
  async list(revision: string): Promise<Prompt[]> {
    // In production, fetch from API
    return mockPrompts
  },

  async get(revision: string, filename: string): Promise<Prompt | null> {
    return mockPrompts.find(p => p.filename === filename) || null
  },

  async update(revision: string, filename: string, content: string): Promise<void> {
    // In production, save to API
  }
}
