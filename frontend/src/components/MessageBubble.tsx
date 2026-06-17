import { AlertCircle } from 'lucide-react'
import type { Message } from '../types'
import { Markdown } from './Markdown'
import { ReasoningTrace } from './ReasoningTrace'
import { StemMark } from './StemMark'

export function MessageBubble({ message }: { message: Message }) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-2xl rounded-br-sm bg-raised px-4 py-2.5 text-[15px] leading-relaxed text-paper">
          {message.content}
        </div>
      </div>
    )
  }

  const thinking = message.status === 'streaming' && message.content === ''

  return (
    <div className="flex gap-3">
      <div className="mt-0.5 shrink-0 text-paper">
        <StemMark size={26} thinking={message.status === 'streaming'} />
      </div>
      <div className="min-w-0 flex-1">
        {/* Tool steps appear above the answer the moment they start. */}
        <ReasoningTrace steps={message.steps} />

        {message.status === 'error' ? (
          <div className="mt-2 flex items-center gap-2 text-sm text-accent">
            <AlertCircle size={15} className="shrink-0" />
            <span>{message.content || "Couldn't reach the assistant. Try again."}</span>
          </div>
        ) : thinking ? (
          <p className="mt-2 font-mono text-xs text-faint">Working on it…</p>
        ) : (
          <div className={message.steps.length ? 'mt-3' : ''}>
            <Markdown>{message.content}</Markdown>
            {message.status === 'streaming' && <span className="stream-caret" />}
          </div>
        )}
      </div>
    </div>
  )
}
