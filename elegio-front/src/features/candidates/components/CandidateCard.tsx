import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import fallbackPartyImage from '../../../assets/party-fallback.svg'
import type { Candidate } from '../types'

type CandidateCardProps = {
  candidate: Candidate
}

export function CandidateCard({ candidate }: CandidateCardProps) {
  const imageSource = candidate.photo_president || fallbackCandidateImage
  const partyImageSource = candidate.photo_of_political_group || fallbackPartyImage

  return (
    <article className="group overflow-hidden rounded-[2rem] border border-coffee/10 bg-white shadow-sm shadow-coffee/5 transition duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-coffee/10">
      <div className="relative h-72 bg-gradient-to-br from-white via-surface to-gold/10">
        <img
          src={imageSource}
          alt={candidate.presidential_candidate}
          className="h-full w-full object-cover object-top transition duration-500 group-hover:scale-105"
          loading="lazy"
          onError={(event) => {
            event.currentTarget.onerror = null
            event.currentTarget.src = fallbackCandidateImage
          }}
        />
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-coffee/80 to-transparent p-5">
          <span className="rounded-full bg-white/95 px-3 py-1 text-xs font-black uppercase tracking-[0.2em] text-coffee shadow-sm">
            {candidate.political_spectrum}
          </span>
        </div>
      </div>

      <div className="p-5">
        <div className="flex items-start gap-4">
          <img
            src={partyImageSource}
            alt={`Logo de ${candidate.political_group}`}
            className="mt-1 size-12 shrink-0 rounded-2xl border border-coffee/10 bg-white object-contain p-1.5 shadow-sm shadow-coffee/5"
            loading="lazy"
            onError={(event) => {
              event.currentTarget.onerror = null
              event.currentTarget.src = fallbackPartyImage
            }}
          />
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-jade">
              {candidate.political_group}
            </p>
            <h3 className="mt-2 text-2xl font-black leading-tight text-ink">
              {candidate.presidential_candidate}
            </h3>
            <p className="mt-1 text-sm text-muted">Vice: {candidate.vice_presidential_candidate}</p>
          </div>
        </div>
      </div>
    </article>
  )
}
