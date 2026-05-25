import { useState } from 'react'
import { normalizeMojibake } from '../../../utils/text'
import type { Candidate } from '../../candidates/types'
import type { Proposal } from '../../proposals/types'
import { getCoverageCopy, type CoverageTone } from '../coverage'

const COLLAPSED_PROPOSAL_LIMIT = 5

type CandidateProposalColumnProps = {
  candidate: Candidate
  coverageTone: CoverageTone
  proposals: Proposal[]
  relativeCoverage: number
}

export function CandidateProposalColumn({
  candidate,
  coverageTone,
  proposals,
  relativeCoverage,
}: CandidateProposalColumnProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const name = normalizeMojibake(candidate.presidential_candidate)
  const politicalGroup = normalizeMojibake(candidate.political_group)
  const coverageCopy = getCoverageCopy(coverageTone)
  const visibleProposals = isExpanded ? proposals : proposals.slice(0, COLLAPSED_PROPOSAL_LIMIT)
  const hasMoreProposals = proposals.length > COLLAPSED_PROPOSAL_LIMIT

  return (
    <article className="min-w-0 rounded-[2rem] border border-coffee/10 bg-surface p-4 shadow-sm shadow-coffee/5">
      <header className="border-b border-coffee/10 pb-4">
        <div className="flex items-center justify-between gap-3">
          <p className="text-xs font-black uppercase tracking-[0.18em] text-clay">
            {proposals.length} propuesta{proposals.length === 1 ? '' : 's'}
          </p>
          <span className={`rounded-full px-3 py-1 text-[0.65rem] font-black ${coverageCopy.lightBadgeClass}`}>
            {coverageCopy.label}
          </span>
        </div>
        <h3 className="mt-2 text-xl font-black leading-tight text-ink">{name}</h3>
        <p className="mt-1 text-sm font-semibold text-muted">{politicalGroup}</p>

        <div className="mt-4 rounded-2xl bg-white p-3 ring-1 ring-coffee/10">
          <div className="flex items-center justify-between gap-3 text-[0.68rem] font-black uppercase tracking-[0.16em] text-muted">
            <span>Cobertura relativa</span>
            <span>{relativeCoverage}%</span>
          </div>
          <div className="mt-2 h-2 overflow-hidden rounded-full bg-coffee/10">
            <div
              className={`h-full rounded-full ${coverageCopy.lightBarClass}`}
              style={{ width: `${relativeCoverage}%` }}
            />
          </div>
          <p className="mt-3 text-xs font-bold leading-5 text-muted">{coverageCopy.detail}</p>
        </div>
      </header>

      {proposals.length === 0 ? (
        <div className="mt-4 rounded-2xl border border-dashed border-clay/30 bg-white/70 p-4">
          <p className="text-sm font-black text-ink">Silencio programático en esta categoría.</p>
          <p className="mt-2 text-sm font-semibold leading-6 text-muted">
            No encontramos propuestas. Eso también es una señal: acá no hay suficiente material para
            comparar con justicia.
          </p>
        </div>
      ) : (
        <>
          <div className="mt-4 space-y-3">
            {visibleProposals.map((proposal, index) => (
              <ProposalMiniCard key={proposal.id} proposal={proposal} rank={index + 1} />
            ))}
          </div>

          {hasMoreProposals && (
            <button
              type="button"
              onClick={() => setIsExpanded((current) => !current)}
              className="mt-4 w-full rounded-2xl border border-coffee/15 bg-white px-4 py-3 text-xs font-black uppercase tracking-[0.14em] text-ink transition hover:border-jade/40 hover:bg-jade/5 hover:text-jade"
            >
              {isExpanded
                ? 'Volver a síntesis'
                : `Ver ${proposals.length - COLLAPSED_PROPOSAL_LIMIT} más`}
            </button>
          )}
        </>
      )}
    </article>
  )
}

function ProposalMiniCard({ proposal, rank }: { proposal: Proposal; rank: number }) {
  return (
    <div className="group rounded-2xl border border-coffee/10 bg-white p-4 shadow-sm shadow-coffee/5 transition hover:-translate-y-0.5 hover:border-jade/25 hover:shadow-xl hover:shadow-coffee/10">
      <div className="flex gap-3">
        <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-ink text-xs font-black text-white">
          {rank}
        </span>
        <h4 className="text-sm font-black leading-snug text-ink">
          {normalizeMojibake(proposal.title)}
        </h4>
      </div>
      {proposal.summary && (
        <p className="mt-3 text-sm leading-6 text-muted">{normalizeMojibake(proposal.summary)}</p>
      )}
      {proposal.sources.length > 0 && (
        <a
          href={proposal.sources[0].url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-3 inline-flex text-xs font-black uppercase tracking-[0.14em] text-jade underline-offset-4 hover:underline"
        >
          Ver fuente
        </a>
      )}
    </div>
  )
}
