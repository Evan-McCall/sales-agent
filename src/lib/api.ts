import type { Message, StreamEvent } from '../types'

/** API base. Same-origin in production (Vercel) and via the Vite dev proxy locally,
 *  so this is empty by default; override with VITE_API_BASE only to point at a
 *  separately-hosted backend. */
const API_BASE = import.meta.env.VITE_API_BASE ?? ''

/**
 * POST the conversation to /api/chat and yield typed events as they stream in.
 * Uses fetch + ReadableStream (not EventSource, which can't POST a body) and
 * parses the SSE `data:` frames ourselves.
 */
export async function* streamChat(
  messages: Pick<Message, 'role' | 'content'>[],
  signal?: AbortSignal,
): AsyncGenerator<StreamEvent> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: messages.map((m) => ({ role: m.role, content: m.content })),
    }),
    signal,
  })

  if (!res.ok || !res.body) {
    throw new Error(`The assistant is unreachable (HTTP ${res.status}).`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })

    // SSE frames are separated by a blank line. Keep the last partial frame buffered.
    const frames = buffer.split('\n\n')
    buffer = frames.pop() ?? ''

    for (const frame of frames) {
      const dataLine = frame
        .split('\n')
        .find((line) => line.startsWith('data:'))
      if (!dataLine) continue
      try {
        yield JSON.parse(dataLine.slice(5).trim()) as StreamEvent
      } catch {
        // Ignore keep-alives or malformed partials.
      }
    }
  }
}
