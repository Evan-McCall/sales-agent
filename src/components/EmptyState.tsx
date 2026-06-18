import { PROMPT_GROUPS } from '../data/prompts'
import { Composer } from './Composer'

interface EmptyStateProps {
  onSend: (text: string) => void
  onStop: () => void
  busy: boolean
}

export function EmptyState({ onSend, onStop, busy }: EmptyStateProps) {
  return (
    <div className="mx-auto flex h-full w-full max-w-2xl flex-col justify-center px-5 py-10">
      <p className="mb-3 font-mono text-xs uppercase tracking-[0.2em] text-faint">
        Sales assistant
      </p>
      <h1 className="font-display text-4xl leading-[1.05] tracking-tight text-paper sm:text-5xl">
        Ask your handbook,
        <br />
        your scripts, and your{' '}
        <span className="italic text-accent">pipeline</span>.
      </h1>
      <p className="mt-4 max-w-md text-[15px] leading-relaxed text-muted">
        One place for the whole sales motion. Type a question — Stem routes it to your
        docs or your live CRM and answers, with its work shown.
      </p>

      <div className="mt-8">
        <Composer onSend={onSend} onStop={onStop} busy={busy} autoFocus />
      </div>

      <div className="mt-7 grid gap-3 sm:grid-cols-3">
        {PROMPT_GROUPS.map((group) => (
          <div key={group.label}>
            <div className="mb-2 flex items-baseline gap-2">
              <span className="text-sm font-medium text-paper">{group.label}</span>
              <span className="text-xs text-faint">{group.hint}</span>
            </div>
            <div className="space-y-1.5">
              {group.prompts.map((prompt) => (
                <button
                  key={prompt}
                  onClick={() => onSend(prompt)}
                  className="block w-full rounded-lg border border-hairline bg-raised/40 px-3 py-2 text-left text-[13px] leading-snug text-muted transition-colors hover:border-faint hover:text-paper"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
