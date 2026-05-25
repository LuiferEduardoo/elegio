import { Link } from 'react-router'
import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import fallbackPartyImage from '../../../assets/party-fallback.svg'
import { ROUTE_PATHS } from '../../../routes/paths'
import { normalizeMojibake } from '../../../utils/text'
import type { Candidate } from '../types'

type CandidateDetailHeroProps = {
  candidate: Candidate
}

export function CandidateDetailHero({ candidate }: CandidateDetailHeroProps) {
  const presidentialCandidate = normalizeMojibake(candidate.presidential_candidate)
  const vicePresidentialCandidate = normalizeMojibake(candidate.vice_presidential_candidate)
  const politicalGroup = normalizeMojibake(candidate.political_group)
  const politicalSpectrum = normalizeMojibake(candidate.political_spectrum)

  return (
    <header className="relative overflow-hidden border-b border-coffee/10 bg-gradient-to-br from-white via-surface to-jade/5">
      <div className="mx-auto max-w-7xl px-6 py-12 sm:px-10 lg:px-16">
        <Link
          to={ROUTE_PATHS.home}
          className="inline-flex items-center gap-2 text-xs font-black uppercase tracking-[0.3em] text-clay hover:text-jade"
        >
          ← Volver al tarjetón
        </Link>

        <div className="mt-8 grid gap-10 lg:grid-cols-[1.1fr_1fr] lg:items-center">
          <div>
            <div className="flex items-center gap-3">
              <img
                src={candidate.photo_of_political_group || fallbackPartyImage}
                alt={`Logo de ${politicalGroup}`}
                className="size-14 rounded-2xl border border-coffee/10 bg-white object-contain p-2 shadow-sm shadow-coffee/5"
                onError={(event) => {
                  event.currentTarget.onerror = null
                  event.currentTarget.src = fallbackPartyImage
                }}
              />
              <div>
                <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">
                  {politicalGroup}
                </p>
                <span className="mt-1 inline-flex rounded-full bg-coffee px-3 py-1 text-[0.65rem] font-black uppercase tracking-[0.25em] text-white">
                  {politicalSpectrum}
                </span>
              </div>
            </div>

            <h1 className="mt-6 font-display text-5xl leading-[1.05] tracking-[-0.04em] text-ink sm:text-6xl">
              {presidentialCandidate}
            </h1>
            <p className="mt-3 text-base text-muted">
              Fórmula vicepresidencial:{' '}
              <span className="font-bold text-ink">{vicePresidentialCandidate}</span>
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <figure className="overflow-hidden rounded-[2rem] border border-coffee/10 bg-white shadow-lg shadow-coffee/10">
              <img
                src={candidate.photo_president || fallbackCandidateImage}
                alt={presidentialCandidate}
                className="aspect-[3/4] w-full object-cover object-top"
                onError={(event) => {
                  event.currentTarget.onerror = null
                  event.currentTarget.src = fallbackCandidateImage
                }}
              />
              <figcaption className="px-4 py-3 text-[0.65rem] font-black uppercase tracking-[0.25em] text-coffee">
                Presidente
              </figcaption>
            </figure>
            <figure className="mt-8 overflow-hidden rounded-[2rem] border border-coffee/10 bg-white shadow-lg shadow-coffee/10">
              <img
                src={candidate.photo_vice_president || fallbackCandidateImage}
                alt={vicePresidentialCandidate}
                className="aspect-[3/4] w-full object-cover object-top"
                onError={(event) => {
                  event.currentTarget.onerror = null
                  event.currentTarget.src = fallbackCandidateImage
                }}
              />
              <figcaption className="px-4 py-3 text-[0.65rem] font-black uppercase tracking-[0.25em] text-coffee">
                Vicepresidente
              </figcaption>
            </figure>
          </div>
        </div>
      </div>
    </header>
  )
}
