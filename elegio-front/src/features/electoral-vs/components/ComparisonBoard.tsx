import { useMemo } from 'react'
import type { Candidate } from '../../candidates/types'
import type { Proposal } from '../../proposals/types'
import { buildCoverageMetrics } from '../coverage'
import { CandidateProposalColumn } from './CandidateProposalColumn'
import { CoverageSummary } from './CoverageSummary'

type ComparisonBoardProps = {
  categoryName: string | undefined
  error: string | null
  isLoading: boolean
  proposalsByCandidate: Record<number, Proposal[]>
  selectedCandidates: Candidate[]
  shouldShow: boolean
}

export function ComparisonBoard({
  categoryName,
  error,
  isLoading,
  proposalsByCandidate,
  selectedCandidates,
  shouldShow,
}: ComparisonBoardProps) {
  const coverageMetrics = useMemo(
    () => buildCoverageMetrics(selectedCandidates, proposalsByCandidate),
    [proposalsByCandidate, selectedCandidates],
  )

  const columnsClass =
    selectedCandidates.length >= 3
      ? 'lg:grid-cols-3'
      : selectedCandidates.length === 2
        ? 'lg:grid-cols-2'
        : 'lg:grid-cols-1'

  if (!shouldShow) {
    return (
      <section className="mt-8 rounded-[2rem] border border-dashed border-coffee/20 bg-white/60 p-8 text-center">
        <p className="text-sm font-black uppercase tracking-[0.25em] text-clay">
          Comparativa limpia
        </p>
        <h2 className="mt-2 font-display text-3xl tracking-[-0.04em] text-ink">
          Seleccioná candidatos y categoría para empezar.
        </h2>
      </section>
    )
  }

  return (
    <section className="mt-8 rounded-[2.5rem] border border-coffee/10 bg-white p-5 shadow-2xl shadow-coffee/10 sm:p-6 lg:p-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.25em] text-clay">
            Tablero comparativo
          </p>
          <h2 className="mt-1 font-display text-3xl tracking-[-0.04em] text-ink">
            {categoryName ?? 'Categoría seleccionada'}
          </h2>
        </div>
        <span className="w-fit rounded-full bg-jade/10 px-3 py-1.5 text-xs font-black uppercase tracking-[0.15em] text-jade">
          {selectedCandidates.length} candidatura{selectedCandidates.length === 1 ? '' : 's'}
        </span>
      </div>

      {isLoading && (
        <div className={`mt-6 grid gap-4 ${columnsClass}`}>
          {selectedCandidates.map((candidate) => (
            <div key={candidate.id} className="h-64 animate-pulse rounded-[2rem] bg-coffee/5" />
          ))}
        </div>
      )}

      {error && <p className="mt-6 rounded-3xl bg-clay p-5 font-bold text-white">{error}</p>}

      {!isLoading && !error && (
        <>
          <CoverageSummary metrics={coverageMetrics} />

          <div className={`mt-6 grid gap-4 ${columnsClass}`}>
            {coverageMetrics.map((metric) => (
              <CandidateProposalColumn
                candidate={metric.candidate}
                coverageTone={metric.tone}
                key={metric.candidate.id}
                proposals={proposalsByCandidate[metric.candidate.id] ?? []}
                relativeCoverage={metric.percentage}
              />
            ))}
          </div>
        </>
      )}
    </section>
  )
}
