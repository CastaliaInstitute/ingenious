"""Traces module with mock data."""

from ingen_prompt_tuner.models import AgentTrace, ConversationTrace


def get_traces(revision: str | None = None, limit: int = 10) -> list[ConversationTrace]:
    """Get conversation traces."""
    traces = [
        ConversationTrace(
            trace_id="trace-001",
            thread_id="thread-abc123",
            workflow="bike-insights",
            revision="quickstart-1",
            user_query="What are the top selling bikes?",
            timestamp="2024-01-15T14:32:00Z",
            total_tokens=1234,
            agents=[
                AgentTrace(
                    agent_name="Router",
                    order=1,
                    input='User query: "What are the top selling bikes?"',
                    output="Routing to SQL Agent for data retrieval, then to Analyst for interpretation...",
                    token_usage=150,
                ),
                AgentTrace(
                    agent_name="SQL Agent",
                    order=2,
                    input="Generate SQL to find top selling bikes",
                    output="SELECT product_name, SUM(quantity) as total_sold FROM sales GROUP BY product_name ORDER BY total_sold DESC LIMIT 10",
                    token_usage=280,
                ),
                AgentTrace(
                    agent_name="Analyst",
                    order=3,
                    input="Analyze the top selling bikes data",
                    output="The top selling bike is the Mountain Pro X with 1,234 units sold, followed by...",
                    token_usage=450,
                ),
                AgentTrace(
                    agent_name="Summarizer",
                    order=4,
                    input="Summarize the analysis for the user",
                    output="Based on our sales data, here are your top 5 selling bikes:\n1. Mountain Pro X - 1,234 units\n2. Road Master 3000 - 987 units\n3. City Cruiser - 856 units...",
                    token_usage=354,
                ),
            ],
        ),
        ConversationTrace(
            trace_id="trace-002",
            thread_id="thread-def456",
            workflow="knowledge-base-agent",
            revision="quickstart-1",
            user_query="How do I configure authentication?",
            timestamp="2024-01-15T14:17:00Z",
            total_tokens=892,
            agents=[
                AgentTrace(
                    agent_name="KB Agent",
                    order=1,
                    input='User query: "How do I configure authentication?"',
                    output="To configure authentication in Ingenious, you need to set the following environment variables:\n\n1. INGENIOUS_WEB_CONFIGURATION__AUTHENTICATION__ENABLE=true\n2. INGENIOUS_WEB_CONFIGURATION__AUTHENTICATION__USERNAME=your_username\n3. INGENIOUS_WEB_CONFIGURATION__AUTHENTICATION__PASSWORD=your_password\n\nFor more details, see the authentication documentation.",
                    token_usage=892,
                ),
            ],
        ),
        ConversationTrace(
            trace_id="trace-003",
            thread_id="thread-ghi789",
            workflow="echo-agent",
            revision="quickstart-1",
            user_query="Testing custom workflow",
            timestamp="2024-01-15T13:30:00Z",
            total_tokens=156,
            agents=[
                AgentTrace(
                    agent_name="Echo Agent",
                    order=1,
                    input="Testing custom workflow",
                    output="Echo: Testing custom workflow",
                    token_usage=156,
                ),
            ],
        ),
        ConversationTrace(
            trace_id="trace-004",
            thread_id="thread-jkl012",
            workflow="bike-insights",
            revision="quickstart-1",
            user_query="Show me sales trends for Q4",
            timestamp="2024-01-15T12:00:00Z",
            total_tokens=2245,
            agents=[
                AgentTrace(
                    agent_name="Router",
                    order=1,
                    input='User query: "Show me sales trends for Q4"',
                    output="Routing to SQL Agent for trend data, then to Analyst for trend analysis...",
                    token_usage=145,
                ),
                AgentTrace(
                    agent_name="SQL Agent",
                    order=2,
                    input="Generate SQL for Q4 sales trends",
                    output="SELECT DATE_TRUNC('month', sale_date) as month, SUM(amount) as revenue FROM sales WHERE sale_date >= '2023-10-01' GROUP BY month ORDER BY month",
                    token_usage=320,
                ),
                AgentTrace(
                    agent_name="Analyst",
                    order=3,
                    input="Analyze Q4 sales trends",
                    output="Q4 showed strong growth with October at $1.2M, November at $1.5M (holiday prep), and December at $2.1M (holiday sales peak)...",
                    token_usage=890,
                ),
                AgentTrace(
                    agent_name="Summarizer",
                    order=4,
                    input="Summarize Q4 trends for user",
                    output="Q4 2023 Sales Summary:\n- Total Revenue: $4.8M (+23% YoY)\n- Peak Month: December ($2.1M)\n- Key Driver: Holiday season demand\n- Trend: Consistent month-over-month growth",
                    token_usage=890,
                ),
            ],
        ),
        ConversationTrace(
            trace_id="trace-005",
            thread_id="thread-mno345",
            workflow="bike-insights",
            revision="quickstart-1",
            user_query="Compare mountain bike models",
            timestamp="2024-01-15T11:00:00Z",
            total_tokens=1923,
            agents=[
                AgentTrace(
                    agent_name="Router",
                    order=1,
                    input='User query: "Compare mountain bike models"',
                    output="Routing to SQL Agent for model data, then to Analyst for comparison...",
                    token_usage=140,
                ),
                AgentTrace(
                    agent_name="SQL Agent",
                    order=2,
                    input="Generate SQL to compare mountain bike models",
                    output="SELECT model_name, price, weight, suspension_type, frame_material, rating FROM products WHERE category = 'mountain_bike' ORDER BY rating DESC",
                    token_usage=290,
                ),
                AgentTrace(
                    agent_name="Analyst",
                    order=3,
                    input="Compare mountain bike models from query results",
                    output="Comparing 5 mountain bike models based on price, weight, suspension, frame material, and customer ratings...",
                    token_usage=750,
                ),
                AgentTrace(
                    agent_name="Summarizer",
                    order=4,
                    input="Summarize bike comparison",
                    output="Mountain Bike Comparison:\n\n| Model | Price | Weight | Rating |\n|-------|-------|--------|--------|\n| Trail Pro | $2,499 | 12.5kg | 4.8 |\n| Summit X | $1,999 | 13.2kg | 4.6 |...",
                    token_usage=743,
                ),
            ],
        ),
    ]

    if revision:
        traces = [t for t in traces if t.revision == revision]

    return traces[:limit]


def get_trace(trace_id: str) -> ConversationTrace | None:
    """Get a specific trace."""
    traces = get_traces()
    for trace in traces:
        if trace.trace_id == trace_id:
            return trace
    return None
