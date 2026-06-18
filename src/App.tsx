import { useCallback, useMemo, useRef, useState } from 'react'
import { Menu } from 'lucide-react'
import type { Conversation, Message, ToolStep } from './types'
import { streamChat } from './lib/api'
import { Sidebar } from './components/Sidebar'
import { EmptyState } from './components/EmptyState'
import { ChatThread } from './components/ChatThread'
import { Composer } from './components/Composer'
import { StemMark } from './components/StemMark'

const uid = () => Math.random().toString(36).slice(2, 10)

function newConversation(): Conversation {
  return { id: uid(), title: 'New chat', messages: [] }
}

function titleFrom(text: string): string {
  const t = text.trim().replace(/\s+/g, ' ')
  return t.length > 38 ? `${t.slice(0, 38)}…` : t
}

export default function App() {
  const [conversations, setConversations] = useState<Conversation[]>([newConversation()])
  const [activeId, setActiveId] = useState(conversations[0].id)
  const [mobileOpen, setMobileOpen] = useState(false)
  const abortRef = useRef<AbortController | null>(null)

  const active = useMemo(
    () => conversations.find((c) => c.id === activeId) ?? conversations[0],
    [conversations, activeId],
  )
  const busy = active.messages.at(-1)?.status === 'streaming'

  /** Patch a single message inside a single conversation. */
  const patchMessage = useCallback(
    (convId: string, msgId: string, fn: (m: Message) => Message) => {
      setConversations((prev) =>
        prev.map((c) =>
          c.id !== convId
            ? c
            : { ...c, messages: c.messages.map((m) => (m.id === msgId ? fn(m) : m)) },
        ),
      )
    },
    [],
  )

  const startNew = useCallback(() => {
    abortRef.current?.abort()
    const conv = newConversation()
    setConversations((prev) => [conv, ...prev.filter((c) => c.messages.length > 0)])
    setActiveId(conv.id)
    setMobileOpen(false)
  }, [])

  const send = useCallback(
    async (text: string) => {
      if (busy) return
      const convId = activeId
      const userMsg: Message = {
        id: uid(),
        role: 'user',
        content: text,
        steps: [],
        status: 'done',
      }
      const assistantMsg: Message = {
        id: uid(),
        role: 'assistant',
        content: '',
        steps: [],
        status: 'streaming',
      }

      // History the model sees: everything so far, plus this turn (content only).
      const history = [...active.messages, userMsg].map((m) => ({
        role: m.role,
        content: m.content,
      }))

      setConversations((prev) =>
        prev.map((c) =>
          c.id !== convId
            ? c
            : {
                ...c,
                title: c.messages.length === 0 ? titleFrom(text) : c.title,
                messages: [...c.messages, userMsg, assistantMsg],
              },
        ),
      )

      const controller = new AbortController()
      abortRef.current = controller

      try {
        for await (const ev of streamChat(history, controller.signal)) {
          if (ev.type === 'token') {
            patchMessage(convId, assistantMsg.id, (m) => ({
              ...m,
              content: m.content + ev.text,
            }))
          } else if (ev.type === 'tool') {
            const step: ToolStep = { tool: ev.tool, input: ev.input }
            patchMessage(convId, assistantMsg.id, (m) => ({
              ...m,
              steps: [...m.steps, step],
            }))
          } else if (ev.type === 'tool_result') {
            patchMessage(convId, assistantMsg.id, (m) => {
              const steps = [...m.steps]
              // Attach the result to the most recent matching call awaiting output.
              for (let i = steps.length - 1; i >= 0; i--) {
                if (steps[i].tool === ev.tool && steps[i].output === undefined) {
                  steps[i] = { ...steps[i], output: ev.output }
                  break
                }
              }
              return { ...m, steps }
            })
          } else if (ev.type === 'error') {
            patchMessage(convId, assistantMsg.id, (m) => ({
              ...m,
              status: 'error',
              content: ev.message,
            }))
          } else if (ev.type === 'done') {
            patchMessage(convId, assistantMsg.id, (m) => ({
              ...m,
              status: m.status === 'error' ? 'error' : 'done',
            }))
          }
        }
      } catch (err) {
        if ((err as Error).name === 'AbortError') {
          patchMessage(convId, assistantMsg.id, (m) => ({
            ...m,
            status: 'done',
            content: m.content || '_Stopped._',
          }))
        } else {
          patchMessage(convId, assistantMsg.id, (m) => ({
            ...m,
            status: 'error',
            content: (err as Error).message,
          }))
        }
      } finally {
        // Guarantee the turn is never left stuck in "streaming".
        patchMessage(convId, assistantMsg.id, (m) =>
          m.status === 'streaming' ? { ...m, status: 'done' } : m,
        )
        abortRef.current = null
      }
    },
    [activeId, active.messages, busy, patchMessage],
  )

  const stop = useCallback(() => abortRef.current?.abort(), [])

  const hasMessages = active.messages.length > 0

  return (
    <div className="flex h-full overflow-hidden bg-ink">
      {/* Sidebar — persistent on desktop, slide-over on mobile. */}
      <div className="hidden md:block">
        <Sidebar
          conversations={conversations}
          activeId={activeId}
          onSelect={(id) => setActiveId(id)}
          onNew={startNew}
        />
      </div>
      {mobileOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <div
            className="absolute inset-0 bg-black/60"
            onClick={() => setMobileOpen(false)}
          />
          <div className="absolute inset-y-0 left-0">
            <Sidebar
              conversations={conversations}
              activeId={activeId}
              onSelect={(id) => {
                setActiveId(id)
                setMobileOpen(false)
              }}
              onNew={startNew}
              onClose={() => setMobileOpen(false)}
            />
          </div>
        </div>
      )}

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Mobile top bar */}
        <div className="flex items-center gap-3 border-b border-hairline px-4 py-3 md:hidden">
          <button
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
            className="grid size-9 place-items-center rounded-lg text-muted hover:text-paper"
          >
            <Menu size={20} />
          </button>
          <div className="flex items-center gap-2">
            <span className="text-paper">
              <StemMark size={20} />
            </span>
            <span className="font-display text-base text-paper">Stem</span>
          </div>
        </div>

        {hasMessages ? (
          <>
            <div className="min-h-0 flex-1 overflow-y-auto">
              <ChatThread messages={active.messages} />
            </div>
            <div className="border-t border-hairline bg-ink/80 px-5 py-4 backdrop-blur">
              <div className="mx-auto max-w-2xl">
                <Composer onSend={send} onStop={stop} busy={busy} autoFocus />
                <p className="mt-2 text-center text-[11px] text-faint">
                  Answers come from your docs and CRM. Verify anything before you act on it.
                </p>
              </div>
            </div>
          </>
        ) : (
          <div className="min-h-0 flex-1 overflow-y-auto">
            <EmptyState onSend={send} onStop={stop} busy={busy} />
          </div>
        )}
      </div>
    </div>
  )
}
