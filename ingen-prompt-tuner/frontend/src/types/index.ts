export interface User {
  id: string
  email: string
}

export interface Revision {
  id: string
  name: string
  createdAt: string
  promptCount: number
}

export interface Prompt {
  filename: string
  description?: string
  content: string
  size: number
  tags: string[]
  variables: string[]
}

export interface AgentTrace {
  agentName: string
  order: number
  input: string
  output: string
  tokenUsage: number
  systemPrompt: string
  userPrompt: string
}

export interface ConversationTrace {
  traceId: string
  threadId: string
  workflow: string
  revision: string
  userQuery: string
  timestamp: string
  agents: AgentTrace[]
  totalTokens: number
}

export type TabName = 'home' | 'prompts' | 'test'
