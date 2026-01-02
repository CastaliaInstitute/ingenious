import type { ConversationTrace } from '@/types'

// Mock data for demo
const mockTraces: ConversationTrace[] = [
  {
    traceId: 't1',
    threadId: 'thread-1',
    workflow: 'bike-insights',
    revision: 'quickstart-1',
    userQuery: 'What are the top selling bikes?',
    timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
    totalTokens: 1234,
    agents: [
      {
        agentName: 'Router',
        order: 1,
        input: 'User query: "What are the top selling bikes?"',
        output: 'Routing to SQL Agent for data retrieval, then to Analyst for interpretation...',
        tokenUsage: 150,
      },
      {
        agentName: 'SQL Agent',
        order: 2,
        input: 'Generate SQL for: top selling bikes',
        output:
          'SELECT product_name, SUM(quantity) as total_sold FROM sales GROUP BY product_name ORDER BY total_sold DESC LIMIT 10',
        tokenUsage: 280,
      },
      {
        agentName: 'Analyst',
        order: 3,
        input: 'SQL results with top 10 bikes',
        output: 'The analysis shows Mountain Pro X leads with 1,234 units sold...',
        tokenUsage: 520,
      },
      {
        agentName: 'Summarizer',
        order: 4,
        input: 'Analyst findings',
        output: 'Here are the top selling bikes: 1. Mountain Pro X...',
        tokenUsage: 284,
      },
    ],
  },
  {
    traceId: 't2',
    threadId: 'thread-2',
    workflow: 'knowledge-base-agent',
    revision: 'quickstart-1',
    userQuery: 'How do I configure authentication?',
    timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
    totalTokens: 892,
    agents: [
      {
        agentName: 'KB Agent',
        order: 1,
        input: 'Query: configure authentication',
        output:
          'To configure authentication, set INGENIOUS_WEB_CONFIGURATION__AUTHENTICATION__ENABLE=true...',
        tokenUsage: 892,
      },
    ],
  },
  {
    traceId: 't3',
    threadId: 'thread-3',
    workflow: 'echo-agent',
    revision: 'quickstart-1',
    userQuery: 'Testing custom workflow',
    timestamp: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
    totalTokens: 156,
    agents: [
      {
        agentName: 'Echo Agent',
        order: 1,
        input: 'Testing custom workflow',
        output: 'Echo: Testing custom workflow',
        tokenUsage: 156,
      },
    ],
  },
  {
    traceId: 't4',
    threadId: 'thread-4',
    workflow: 'bike-insights',
    revision: 'quickstart-1',
    userQuery: 'Show me sales trends for Q4',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    totalTokens: 2156,
    agents: [
      {
        agentName: 'Router',
        order: 1,
        input: 'User query about Q4 sales',
        output: 'Routing to SQL for data, Analyst for trend analysis',
        tokenUsage: 180,
      },
      {
        agentName: 'SQL Agent',
        order: 2,
        input: 'Q4 sales data query',
        output: 'SELECT month, SUM(revenue) FROM sales WHERE quarter = 4...',
        tokenUsage: 320,
      },
      {
        agentName: 'Analyst',
        order: 3,
        input: 'Q4 sales data',
        output: 'Q4 shows strong growth with 23% increase over Q3...',
        tokenUsage: 850,
      },
      {
        agentName: 'Summarizer',
        order: 4,
        input: 'Q4 trend analysis',
        output: 'Q4 2024 Summary: Revenue grew 23% compared to Q3...',
        tokenUsage: 806,
      },
    ],
  },
  {
    traceId: 't5',
    threadId: 'thread-5',
    workflow: 'bike-insights',
    revision: 'quickstart-1',
    userQuery: 'Compare mountain bike models',
    timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
    totalTokens: 1891,
    agents: [
      {
        agentName: 'Router',
        order: 1,
        input: 'Mountain bike comparison request',
        output: 'Routing to SQL and Analyst',
        tokenUsage: 165,
      },
      {
        agentName: 'SQL Agent',
        order: 2,
        input: 'Get mountain bike specs',
        output: 'SELECT * FROM products WHERE category = "mountain_bike"...',
        tokenUsage: 295,
      },
      {
        agentName: 'Analyst',
        order: 3,
        input: 'Mountain bike product data',
        output: 'Comparing 5 mountain bike models across price, weight, features...',
        tokenUsage: 780,
      },
      {
        agentName: 'Summarizer',
        order: 4,
        input: 'Comparison analysis',
        output: 'Mountain Bike Comparison: The Pro X offers best value...',
        tokenUsage: 651,
      },
    ],
  },
]

export const tracesService = {
  async list(revision: string): Promise<ConversationTrace[]> {
    // In production, fetch from API
    return mockTraces.filter((t) => t.revision === revision)
  },

  async get(traceId: string): Promise<ConversationTrace | null> {
    return mockTraces.find((t) => t.traceId === traceId) || null
  },
}
