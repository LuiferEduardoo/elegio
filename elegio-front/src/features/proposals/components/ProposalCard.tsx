import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import type { Proposal } from '../types'

type ProposalCardProps = {
  proposal: Proposal
}

export function ProposalCard({ proposal }: ProposalCardProps) {
  const photo = proposal.candidate.photo_president || fallbackCandidateImage

  return (
    <article className="group h-full overflow-hidden rounded-3xl border border-coffee/10 bg-white p-5 shadow-sm shadow-coffee/5 transition duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-coffee/10">
      <div className="flex items-start gap-3">
        <img
          src={photo}
          alt={proposal.candidate.presidential_candidate}
          className="size-12 shrink-0 rounded-2xl border border-coffee/10 bg-surface object-cover object-top"
          loading="lazy"
          onError={(event) => {
            event.currentTarget.onerror = null
            event.currentTarget.src = fallbackCandidateImage
          }}
        />

        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-jade/10 px-3 py-1 text-xs font-bold uppercase tracking-[0.15em] text-jade">
              {proposal.category.name}
            </span>
            <span className="text-xs font-semibold text-muted">
              {proposal.candidate.presidential_candidate} · {proposal.candidate.political_group}
            </span>
          </div>

          <h3 className="mt-3 font-display text-lg leading-snug tracking-[-0.02em] text-ink">
            {proposal.title}
          </h3>

          {proposal.summary && (
            <p className="mt-2 text-sm leading-6 text-muted">{proposal.summary}</p>
          )}

          {proposal.taggings.length > 0 && (
            <ul className="mt-3 flex flex-wrap gap-2">
              {proposal.taggings.slice(0, 4).map((tag) => (
                <li
                  key={tag.id}
                  className="rounded-full border border-coffee/15 bg-surface/60 px-2.5 py-1 text-xs font-semibold text-coffee"
                >
                  #{tag.name}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </article>
  )
}
