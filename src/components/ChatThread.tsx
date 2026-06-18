import { useEffect, useRef } from 'react'
import type { Message } from '../types'
import { MessageBubble } from './MessageBubble'

export function ChatThread({ messages }: { messages: Message[] }) {
  const endRef = useRef<HTMLDivElement>(null)

  // Keep the latest turn in view as tokens stream in.
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages])

  return (
    <div className="mx-auto w-full max-w-2xl space-y-7 px-5 py-8">
      {messages.map((m) => (
        <MessageBubble key={m.id} message={m} />
      ))}
      <div ref={endRef} />
    </div>
  )
}
