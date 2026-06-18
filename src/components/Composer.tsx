import { useEffect, useRef, useState } from 'react'
import { ArrowUp, Square } from 'lucide-react'

interface ComposerProps {
  onSend: (text: string) => void
  onStop: () => void
  busy: boolean
  autoFocus?: boolean
}

export function Composer({ onSend, onStop, busy, autoFocus }: ComposerProps) {
  const [value, setValue] = useState('')
  const ref = useRef<HTMLTextAreaElement>(null)

  // Grow with content, up to a cap.
  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`
  }, [value])

  useEffect(() => {
    if (autoFocus) ref.current?.focus()
  }, [autoFocus])

  function submit() {
    const text = value.trim()
    if (!text || busy) return
    onSend(text)
    setValue('')
  }

  return (
    <div className="flex items-end gap-2 rounded-2xl border border-hairline bg-raised px-3 py-2.5 transition-colors focus-within:border-faint">
      <textarea
        ref={ref}
        value={value}
        rows={1}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            submit()
          }
        }}
        placeholder="Ask about policies, scripts, or your pipeline…"
        className="max-h-[200px] flex-1 resize-none bg-transparent py-1.5 text-[15px] leading-relaxed text-paper outline-none placeholder:text-faint"
      />
      {busy ? (
        <button
          onClick={onStop}
          aria-label="Stop generating"
          className="grid size-9 shrink-0 place-items-center rounded-xl border border-hairline text-muted transition-colors hover:text-paper"
        >
          <Square size={15} fill="currentColor" />
        </button>
      ) : (
        <button
          onClick={submit}
          disabled={!value.trim()}
          aria-label="Send"
          className="grid size-9 shrink-0 place-items-center rounded-xl bg-accent text-ink transition-colors enabled:hover:bg-accent-press disabled:cursor-not-allowed disabled:bg-hairline disabled:text-faint"
        >
          <ArrowUp size={18} strokeWidth={2.5} />
        </button>
      )}
    </div>
  )
}
