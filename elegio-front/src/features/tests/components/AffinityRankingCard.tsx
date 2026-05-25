import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import type { CandidateAffinity } from '../types'
import { formatPercent, normalizeMojibake } from '../utils/text'

type AffinityRankingCardProps = {
  candidate: CandidateAffinity
  rank: number
}

export function AffinityRankingCard({ candidate, rank }: AffinityRankingCardProps) {
  const name = normalizeMojibake(candidate.presidential_candidate)
  const politicalGroup = normalizeMojibake(candidate.political_group)
  const politicalSpectrum = candidate.political_spectrum
    ? normalizeMojibake(candidate.political_spectrum)
    : null
  const affinity = formatPercent(candidate.affinity)

  return (
    <article className="rounded-[1.75rem] border border-coffee/10 bg-surface p-4 transition hover:-translate-y-0.5 hover:bg-white hover:shadow-xl hover:shadow-coffee/10">
      <div className="flex min-w-0 gap-4">
        <img
          src={candidate.photo_president || fallbackCandidateImage}
          alt={name}
          className="size-16 shrink-0 rounded-2xl object-cover object-top"
          loading="lazy"
          onError={(event) => {
            event.currentTarget.onerror = null
            event.currentTarget.src = fallbackCandidateImage
          }}
        />

        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-ink px-2.5 py-1 text-xs font-black text-white">
              #{rank}
            </span>
            <span className="text-sm font-black text-jade">{affinity} afinidad</span>
          </div>
          <h4 className="mt-2 truncate text-lg font-black leading-tight text-ink">{name}</h4>
          <p className="mt-1 truncate text-sm font-semibold text-muted">
            {politicalGroup}
            {politicalSpectrum ? ` · ${politicalSpectrum}` : ''}
          </p>
        </div>
      </div>
    </article>
  )
}
