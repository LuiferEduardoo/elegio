import type { CandidateAffinity } from '../types'
import { AffinityRankingCard } from './AffinityRankingCard'
import { AffinityWinnerCard } from './AffinityWinnerCard'

type AffinityResultsSectionProps = {
  candidates: CandidateAffinity[]
}

export function AffinityResultsSection({ candidates }: AffinityResultsSectionProps) {
  const topCandidates = candidates.slice(0, 6)
  if (topCandidates.length === 0) return null

  const [winner, ...otherCandidates] = topCandidates

  return (
    <section className="mt-10 overflow-hidden rounded-[2.5rem] border border-coffee/10 bg-white shadow-2xl shadow-coffee/10">
      <div className="grid min-w-0 lg:grid-cols-[minmax(0,0.95fr)_minmax(0,1.05fr)]">
        <AffinityWinnerCard candidate={winner} />

        <div className="min-w-0 p-5 sm:p-8 lg:p-10">
          <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-xs font-black uppercase tracking-[0.28em] text-clay">
                Ranking de afinidad
              </p>
              <h3 className="mt-2 font-display text-3xl leading-tight tracking-[-0.04em] text-ink">
                Tus coincidencias más fuertes.
              </h3>
            </div>
            <span className="w-fit rounded-full bg-jade/10 px-3 py-1.5 text-xs font-black uppercase tracking-[0.15em] text-jade">
              Top {topCandidates.length}
            </span>
          </div>

          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-1">
            {otherCandidates.map((candidate, index) => (
              <AffinityRankingCard candidate={candidate} key={candidate.candidate_id} rank={index + 2} />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
