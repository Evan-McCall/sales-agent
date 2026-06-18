import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

/** Assistant answers are markdown (tables, lists, bold, cited sources). Styled to
 *  sit quietly in the dark theme — generous line-height, hairline table rules. */
export function Markdown({ children }: { children: string }) {
  return (
    <div className="text-[15px] leading-relaxed text-paper [&_p]:my-3 first:[&_p]:mt-0 last:[&_p]:mb-0">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: (props) => (
            <a
              {...props}
              target="_blank"
              rel="noreferrer"
              className="text-accent underline underline-offset-2 hover:text-accent-press"
            />
          ),
          ul: (props) => <ul {...props} className="my-3 list-disc space-y-1 pl-5" />,
          ol: (props) => <ol {...props} className="my-3 list-decimal space-y-1 pl-5" />,
          strong: (props) => <strong {...props} className="font-semibold text-paper" />,
          code: (props) => (
            <code
              {...props}
              className="rounded bg-raised-2 px-1.5 py-0.5 font-mono text-[13px] text-paper"
            />
          ),
          table: (props) => (
            <div className="my-4 overflow-x-auto rounded-lg border border-hairline">
              <table {...props} className="w-full border-collapse text-sm" />
            </div>
          ),
          th: (props) => (
            <th
              {...props}
              className="border-b border-hairline bg-raised-2 px-3 py-2 text-left font-medium text-muted"
            />
          ),
          td: (props) => (
            <td {...props} className="border-b border-hairline px-3 py-2 align-top" />
          ),
          h1: (props) => <h2 {...props} className="mt-5 mb-2 text-lg font-semibold" />,
          h2: (props) => <h2 {...props} className="mt-5 mb-2 text-lg font-semibold" />,
          h3: (props) => <h3 {...props} className="mt-4 mb-2 text-base font-semibold" />,
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  )
}
