export type Role = 'user' | 'assistant'

/** One tool the agent invoked, paired with its result once it returns. */
export interface ToolStep {
  tool: string
  input: Record<string, unknown>
  output?: string
}

export type MessageStatus = 'streaming' | 'done' | 'error'

export interface Message {
  id: string
  role: Role
  content: string
  steps: ToolStep[]
  status: MessageStatus
}

export interface Conversation {
  id: string
  title: string
  messages: Message[]
}

/** Events emitted by the /api/chat SSE stream (mirror of agent.core.stream_agent). */
export type StreamEvent =
  | { type: 'token'; text: string }
  | { type: 'tool'; tool: string; input: Record<string, unknown> }
  | { type: 'tool_result'; tool: string; output: string }
  | { type: 'done' }
  | { type: 'error'; message: string }
