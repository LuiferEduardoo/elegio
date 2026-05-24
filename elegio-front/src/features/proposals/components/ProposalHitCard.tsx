import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import type { ProposalHit } from '../types'

type ProposalHitCardProps = {
  hit: ProposalHit
}

export function ProposalHitCard({ hit }: ProposalHitCardProps) {
  const photo = hit.candidate.photo_president || fallbackCandidateImage

  return (
    <article className="group overflow-hidden rounded-3xl border border-coffee/10 bg-white p-6 shadow-sm shadow-coffee/5 transition duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-coffee/10">
      <div className="flex items-start gap-4">
        <img
          src={photo}
          alt={hit.candidate.presidential_candidate}
          className="size-14 shrink-0 rounded-2xl border border-coffee/10 bg-surface object-cover object-top"
          loading="lazy"
          onError={(event) => {
            event.currentTarget.onerror = null
            event.currentTarget.src = fallbackCandidateImage
          }}
        />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-jade/10 px-3 py-1 text-xs font-bold uppercase tracking-[0.15em] text-jade">
              {hit.category.name}
            </span>
            <span className="text-xs font-semibold text-muted">
              {hit.candidate.presidential_candidate} · {hit.candidate.political_group}
            </span>
          </div>
          <h3 className="mt-3 font-display text-xl leading-snug tracking-[-0.02em] text-ink">
            {hit.title}
          </h3>
          {hit.summary && (
            <p className="mt-2 text-sm leading-6 text-muted">{hit.summary}</p>
          )}
          {hit.excerpt && (
            <blockquote className="mt-3 rounded-2xl border-l-4 border-clay/40 bg-surface/60 px-4 py-3 text-sm italic leading-6 text-muted">
              “{hit.excerpt}”
            </blockquote>
          )}
        </div>
      </div>
    </article>
  )
}
