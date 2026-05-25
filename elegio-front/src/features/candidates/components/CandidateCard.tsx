import { Link } from 'react-router'
import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import fallbackPartyImage from '../../../assets/party-fallback.svg'
import { buildCandidateDetailPath } from '../../../routes/paths'
import { normalizeMojibake } from '../../../utils/text'
import type { Candidate } from '../types'

type CandidateCardProps = {
  candidate: Candidate
}

export function CandidateCard({ candidate }: CandidateCardProps) {
  const imageSource = candidate.photo_president || fallbackCandidateImage
  const partyImageSource = candidate.photo_of_political_group || fallbackPartyImage
  const presidentialCandidate = normalizeMojibake(candidate.presidential_candidate)
  const vicePresidentialCandidate = normalizeMojibake(candidate.vice_presidential_candidate)
  const politicalGroup = normalizeMojibake(candidate.political_group)
  const politicalSpectrum = normalizeMojibake(candidate.political_spectrum)

  return (
    <article className="group flex flex-col overflow-hidden rounded-[2rem] border border-coffee/10 bg-white shadow-sm shadow-coffee/5 transition duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-coffee/10">
      <div className="relative h-72 bg-gradient-to-br from-white via-surface to-gold/10">
        <img
          src={imageSource}
          alt={presidentialCandidate}
          className="h-full w-full object-cover object-top transition duration-500 group-hover:scale-105"
          loading="lazy"
          onError={(event) => {
            event.currentTarget.onerror = null
            event.currentTarget.src = fallbackCandidateImage
          }}
        />
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-coffee/80 to-transparent p-5">
          <span className="rounded-full bg-white/95 px-3 py-1 text-xs font-black uppercase tracking-[0.2em] text-coffee shadow-sm">
            {politicalSpectrum}
          </span>
        </div>
      </div>

      <div className="flex flex-1 flex-col gap-5 p-5">
        <div className="flex items-start gap-4">
          <img
            src={partyImageSource}
            alt={`Logo de ${politicalGroup}`}
            className="mt-1 size-12 shrink-0 rounded-2xl border border-coffee/10 bg-white object-contain p-1.5 shadow-sm shadow-coffee/5"
            loading="lazy"
            onError={(event) => {
              event.currentTarget.onerror = null
              event.currentTarget.src = fallbackPartyImage
            }}
          />
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-jade">
              {politicalGroup}
            </p>
            <h3 className="mt-2 text-2xl font-black leading-tight text-ink">
              {presidentialCandidate}
            </h3>
            <p className="mt-1 text-sm text-muted">Vice: {vicePresidentialCandidate}</p>
          </div>
        </div>

        <Link
          to={buildCandidateDetailPath(candidate.id)}
          className="mt-auto inline-flex items-center justify-center gap-2 rounded-full bg-coffee px-5 py-3 text-xs font-black uppercase tracking-[0.25em] text-white transition hover:bg-jade focus:outline-none focus:ring-2 focus:ring-jade/40"
        >
          Ver candidato →
        </Link>
      </div>
    </article>
  )
}
