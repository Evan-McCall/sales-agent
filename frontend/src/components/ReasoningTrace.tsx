import { useState } from 'react'
import { ChevronRight, Database, BookOpen } from 'lucide-react'
import type { ToolStep } from '../types'

/** Which engine a tool belongs to — the real signal the trace encodes. */
function engineOf(tool: string): { label: string; Icon: typeof Database } {
  if (tool === 'search_knowledge_base') return { label: 'Knowledge base', Icon: BookOpen }
  return { label: 'CRM', Icon: Database }
}

function summarize(steps: ToolStep[]): string {
  const engines = Array.from(new Set(steps.map((s) => engineOf(s.tool).label)))
  const n = steps.length
  return `${n} ${n === 1 ? 'lookup' : 'lookups'} · ${engines.join(', ')}`
}

export function ReasoningTrace({ steps }: { steps: ToolStep[] }) {
  const [open, setOpen] = useState(false)
  if (steps.length === 0) return null

  return (
    <div className="mt-3 overflow-hidden rounded-lg border border-hairline bg-raised/60">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-2 px-3 py-2 text-left font-mono text-xs text-muted transition-colors hover:text-paper"
        aria-expanded={open}
      >
        <ChevronRight
          size={13}
          className={`shrink-0 transition-transform ${open ? 'rotate-90' : ''}`}
        />
        <span className="tracking-tight">{summarize(steps)}</span>
      </button>

      {open && (
        <div className="space-y-3 border-t border-hairline px-3 py-3">
          {steps.map((step, i) => {
            const { label, Icon } = engineOf(step.tool)
            return (
              <div key={i} className="font-mono text-xs">
                <div className="flex items-center gap-2 text-muted">
                  <Icon size={13} className="text-accent" />
                  <span className="uppercase tracking-wide text-faint">{label}</span>
                  <span className="text-paper">{step.tool}</span>
                </div>
                <div className="mt-1 pl-[21px] text-faint">
                  {Object.entries(step.input).map(([k, v]) => (
                    <span key={k} className="mr-3">
                      {k}=<span className="text-muted">{String(v)}</span>
                    </span>
                  ))}
                </div>
                {step.output && (
                  <pre className="mt-1 ml-[21px] max-h-40 overflow-auto whitespace-pre-wrap break-words rounded bg-ink/70 p-2 text-faint">
                    {step.output}
                  </pre>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
