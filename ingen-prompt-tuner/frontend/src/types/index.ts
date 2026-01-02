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

export interface ActivityItem {
  id: string
  type: 'edit' | 'revision' | 'test'
  title: string
  subtitle: string
  timestamp: string
}

export type TabName = 'home' | 'prompts' | 'test'
