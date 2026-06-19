import { useEffect, useState } from 'react'
import fallbackCandidateImage from '../../../../assets/candidate-fallback.svg'
import type { CandidateAffinity } from '../../types'
import { formatPercent, normalizeMojibake } from '../../utils/text'

type AffinityBarChartProps = {
  candidates: CandidateAffinity[]
}

/**
 * Animated horizontal bar chart ranking every candidate by affinity. The top
 * candidate gets the jade gradient; the rest fade to a quieter coffee tone.
 */
export function AffinityBarChart({ candidates }: AffinityBarChartProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    const frame = requestAnimationFrame(() => setMounted(true))
    return () => cancelAnimationFrame(frame)
  }, [])

  if (candidates.length === 0) return null

  return (
    <ul className="flex flex-col gap-4">
      {candidates.map((candidate, index) => {
        const name = normalizeMojibake(candidate.presidential_candidate)
        const pct = Math.max(0, Math.min(1, candidate.affinity))
        const isLeader = index === 0

        return (
          <li key={candidate.candidate_id} className="flex min-w-0 items-center gap-3 sm:gap-4">
            <img
              src={candidate.photo_president || fallbackCandidateImage}
              alt={name}
              className="size-10 shrink-0 rounded-xl object-cover object-top sm:size-12"
              loading="lazy"
              onError={(event) => {
                event.currentTarget.onerror = null
                event.currentTarget.src = fallbackCandidateImage
              }}
            />
            <div className="min-w-0 flex-1">
              <div className="mb-1.5 flex items-baseline justify-between gap-3">
                <span className="truncate text-sm font-black text-ink">{name}</span>
                <span
                  className={`shrink-0 text-sm font-black tabular-nums ${
                    isLeader ? 'text-jade' : 'text-muted'
                  }`}
                >
                  {formatPercent(pct)}
                </span>
              </div>
              <div className="h-3 w-full overflow-hidden rounded-full bg-coffee/10">
                <div
                  className={`h-full rounded-full ${
                    isLeader
                      ? 'bg-gradient-to-r from-clay to-jade'
                      : 'bg-coffee/40'
                  }`}
                  style={{
                    width: mounted ? `${pct * 100}%` : '0%',
                    transition: 'width 1s cubic-bezier(0.22, 1, 0.36, 1)',
                    transitionDelay: `${index * 90}ms`,
                  }}
                />
              </div>
            </div>
          </li>
        )
      })}
    </ul>
  )
}
