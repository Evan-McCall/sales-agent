import { Plus, X } from 'lucide-react'
import type { Conversation } from '../types'
import { StemMark } from './StemMark'

interface SidebarProps {
  conversations: Conversation[]
  activeId: string
  onSelect: (id: string) => void
  onNew: () => void
  onClose?: () => void
}

export function Sidebar({
  conversations,
  activeId,
  onSelect,
  onNew,
  onClose,
}: SidebarProps) {
  return (
    <div className="flex h-full w-64 shrink-0 flex-col border-r border-hairline bg-raised/40">
      <div className="flex items-center justify-between px-4 py-4">
        <div className="flex items-center gap-2">
          <span className="text-paper">
            <StemMark size={24} />
          </span>
          <span className="font-display text-lg tracking-tight text-paper">Stem</span>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            aria-label="Close menu"
            className="grid size-8 place-items-center rounded-lg text-muted hover:text-paper md:hidden"
          >
            <X size={18} />
          </button>
        )}
      </div>

      <div className="px-3">
        <button
          onClick={onNew}
          className="flex w-full items-center gap-2 rounded-xl border border-hairline px-3 py-2.5 text-sm font-medium text-paper transition-colors hover:border-faint hover:bg-raised"
        >
          <Plus size={16} className="text-accent" />
          New chat
        </button>
      </div>

      <div className="mt-5 min-h-0 flex-1 overflow-y-auto px-3">
        <div className="mb-2 px-1 font-mono text-[10px] uppercase tracking-[0.18em] text-faint">
          History
        </div>
        {conversations.filter((c) => c.messages.length > 0).length === 0 && (
          <p className="px-1 text-xs text-faint">Your conversations show up here.</p>
        )}
        <div className="space-y-0.5">
          {conversations
            .filter((c) => c.messages.length > 0)
            .map((c) => (
              <button
                key={c.id}
                onClick={() => onSelect(c.id)}
                className={`block w-full truncate rounded-lg px-3 py-2 text-left text-[13px] transition-colors ${
                  c.id === activeId
                    ? 'bg-raised text-paper'
                    : 'text-muted hover:bg-raised/60 hover:text-paper'
                }`}
              >
                {c.id === activeId && (
                  <span className="mr-2 inline-block size-1.5 rounded-full bg-accent align-middle" />
                )}
                {c.title}
              </button>
            ))}
        </div>
      </div>

      <div className="border-t border-hairline px-4 py-3">
        <p className="font-mono text-[10px] leading-relaxed text-faint">
          Docs + CRM, one prompt.
        </p>
      </div>
    </div>
  )
}
