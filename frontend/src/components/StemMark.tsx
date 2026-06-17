interface StemMarkProps {
  size?: number
  thinking?: boolean
  /** Bloom color. Defaults to the accent; pass 'currentColor' to inherit text color. */
  bloom?: string
  className?: string
}

/**
 * The brand signature. A thin stem with a five-point bloom.
 * When `thinking`, the stem draws upward and the bloom opens + breathes
 * (animation defined in theme.css; reduced-motion shows it static).
 */
export function StemMark({
  size = 28,
  thinking = false,
  bloom = 'var(--color-accent)',
  className = '',
}: StemMarkProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      aria-hidden="true"
      className={`${thinking ? 'stem--thinking' : ''} ${className}`}
    >
      <path
        className="stem-line"
        d="M16 30 V11"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        opacity={0.55}
      />
      <path
        d="M16 22 C12 22 9 19 9 19 C12 18 15 20 16 22Z"
        fill="currentColor"
        opacity={0.4}
      />
      <g className="stem-bloom">
        <g stroke={bloom} strokeWidth="2" strokeLinecap="round">
          <path d="M16 10 V3" />
          <path d="M16 10 L21.5 6.5" />
          <path d="M16 10 L10.5 6.5" />
          <path d="M16 10 L21 13.5" />
          <path d="M16 10 L11 13.5" />
        </g>
        <circle cx="16" cy="10" r="2.4" fill={bloom} />
      </g>
    </svg>
  )
}
