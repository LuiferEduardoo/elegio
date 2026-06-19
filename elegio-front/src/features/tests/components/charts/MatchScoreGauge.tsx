import { useEffect, useState } from 'react'
import { formatPercent } from '../../utils/text'

type MatchScoreGaugeProps = {
  /** Affinity in [0, 1]. */
  value: number
  label?: string
}

const SIZE = 180
const STROKE = 16
const RADIUS = (SIZE - STROKE) / 2
const CENTER = SIZE / 2
// Semicircle length: the arc goes from the left to the right over the top half.
const ARC_LENGTH = Math.PI * RADIUS

/**
 * SVG semicircle gauge for the headline match score. Animates the arc on mount
 * so the number "fills up" toward the candidate's affinity.
 */
export function MatchScoreGauge({ value, label = 'de match' }: MatchScoreGaugeProps) {
  const [progress, setProgress] = useState(0)
  const clamped = Math.max(0, Math.min(1, value))

  useEffect(() => {
    const frame = requestAnimationFrame(() => setProgress(clamped))
    return () => cancelAnimationFrame(frame)
  }, [clamped])

  const dashOffset = ARC_LENGTH * (1 - progress)

  return (
    <div className="flex w-full flex-col items-center">
      <svg
        viewBox={`0 0 ${SIZE} ${SIZE / 2 + STROKE}`}
        className="w-full max-w-[11rem] sm:max-w-[15rem]"
        role="img"
        aria-label={`${formatPercent(clamped)} ${label}`}
      >
        <defs>
          <linearGradient id="match-gauge" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#c98a5e" />
            <stop offset="100%" stopColor="#6bb7a2" />
          </linearGradient>
        </defs>
        {/* Track */}
        <path
          d={`M ${STROKE / 2} ${CENTER} A ${RADIUS} ${RADIUS} 0 0 1 ${SIZE - STROKE / 2} ${CENTER}`}
          fill="none"
          stroke="currentColor"
          className="text-coffee/10"
          strokeWidth={STROKE}
          strokeLinecap="round"
        />
        {/* Value */}
        <path
          d={`M ${STROKE / 2} ${CENTER} A ${RADIUS} ${RADIUS} 0 0 1 ${SIZE - STROKE / 2} ${CENTER}`}
          fill="none"
          stroke="url(#match-gauge)"
          strokeWidth={STROKE}
          strokeLinecap="round"
          strokeDasharray={ARC_LENGTH}
          strokeDashoffset={dashOffset}
          style={{ transition: 'stroke-dashoffset 1.1s cubic-bezier(0.22, 1, 0.36, 1)' }}
        />
      </svg>
      <div className="-mt-9 text-center sm:-mt-12">
        <p className="font-display text-4xl leading-none tracking-[-0.04em] text-ink sm:text-5xl">
          {formatPercent(clamped)}
        </p>
        <p className="mt-1 text-[0.65rem] font-black uppercase tracking-[0.2em] text-muted sm:text-xs sm:tracking-[0.25em]">
          {label}
        </p>
      </div>
    </div>
  )
}
