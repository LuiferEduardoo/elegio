import { useEffect, useState } from 'react'
import fallbackCandidateImage from '../../../../assets/candidate-fallback.svg'
import type { CandidateAffinity } from '../../types'
import { formatPercent, normalizeMojibake } from '../../utils/text'

type MatchVersusProps = {
  left: CandidateAffinity
  right: CandidateAffinity
}

/**
 * Head-to-head "tug of war" for the segunda vuelta: two candidates facing each
 * other with a split bar whose share is each candidate's relative affinity.
 */
export function MatchVersus({ left, right }: MatchVersusProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    const frame = requestAnimationFrame(() => setMounted(true))
    return () => cancelAnimationFrame(frame)
  }, [])

  const total = left.affinity + right.affinity
  const leftShare = total > 0 ? left.affinity / total : 0.5

  return (
    <div className="flex flex-col gap-4 sm:gap-5">
      <div className="grid min-w-0 grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center gap-2 sm:gap-4">
        <CandidateFace candidate={left} align="left" />
        <span className="font-display text-xl italic tracking-[-0.04em] text-muted sm:text-2xl">vs</span>
        <CandidateFace candidate={right} align="right" />
      </div>

      <div className="flex h-5 w-full overflow-hidden rounded-full bg-coffee/10">
        <div
          className="h-full bg-gradient-to-r from-clay to-clay/70"
          style={{
            width: mounted ? `${leftShare * 100}%` : '50%',
            transition: 'width 1.1s cubic-bezier(0.22, 1, 0.36, 1)',
          }}
        />
        <div
          className="h-full flex-1 bg-gradient-to-r from-jade/70 to-jade"
        />
      </div>
    </div>
  )
}

function CandidateFace({
  candidate,
  align,
}: {
  candidate: CandidateAffinity
  align: 'left' | 'right'
}) {
  const name = normalizeMojibake(candidate.presidential_candidate)

  return (
    <div className={`flex min-w-0 items-center gap-2 sm:gap-3 ${align === 'right' ? 'flex-row-reverse text-right' : ''}`}>
      <img
        src={candidate.photo_president || fallbackCandidateImage}
        alt={name}
        className="size-9 shrink-0 rounded-xl object-cover object-top sm:size-14 sm:rounded-2xl"
        loading="lazy"
        onError={(event) => {
          event.currentTarget.onerror = null
          event.currentTarget.src = fallbackCandidateImage
        }}
      />
      <div className="min-w-0">
        <p className="truncate text-xs font-black leading-tight text-ink sm:text-sm">{name}</p>
        <p className={`text-base font-black sm:text-lg ${align === 'left' ? 'text-clay' : 'text-jade'}`}>
          {formatPercent(Math.max(0, Math.min(1, candidate.affinity)))}
        </p>
      </div>
    </div>
  )
}
