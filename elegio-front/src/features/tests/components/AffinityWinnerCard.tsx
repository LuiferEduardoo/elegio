import { Link } from 'react-router'
import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import { buildCandidateDetailPath } from '../../../routes/paths'
import type { CandidateAffinity } from '../types'
import { formatPercent, normalizeMojibake } from '../utils/text'

type AffinityWinnerCardProps = {
  candidate: CandidateAffinity
}

export function AffinityWinnerCard({ candidate }: AffinityWinnerCardProps) {
  const name = normalizeMojibake(candidate.presidential_candidate)
  const group = normalizeMojibake(candidate.political_group)
  const spectrum = candidate.political_spectrum
    ? normalizeMojibake(candidate.political_spectrum)
    : null

  return (
    <article className="relative overflow-hidden bg-ink p-5 text-white sm:p-8 lg:p-10">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.18),transparent_28%),radial-gradient(circle_at_80%_0%,rgba(107,183,162,0.28),transparent_26%)]" />
      <div className="relative z-10 flex h-full flex-col">
        <p className="text-xs font-black uppercase tracking-[0.28em] text-white/65">Mayor afinidad</p>

        <div className="mt-7 flex flex-col gap-6 sm:flex-row sm:items-end lg:flex-col lg:items-start">
          <img
            src={candidate.photo_president || fallbackCandidateImage}
            alt={name}
            className="h-48 w-40 rounded-[2rem] border border-white/15 object-cover object-top shadow-2xl shadow-black/30 sm:h-56 sm:w-44"
            loading="lazy"
            onError={(event) => {
              event.currentTarget.onerror = null
              event.currentTarget.src = fallbackCandidateImage
            }}
          />

          <div className="min-w-0">
            <span className="rounded-full bg-white px-4 py-1.5 text-xs font-black uppercase tracking-[0.18em] text-ink">
              {formatPercent(candidate.affinity)} match
            </span>
            <h2 className="mt-4 font-display text-3xl leading-[0.95] tracking-[-0.05em] sm:text-4xl lg:text-5xl">
              {name}
            </h2>
            <p className="mt-3 text-sm font-semibold leading-6 text-white/75">
              {group}
              {spectrum ? ` · ${spectrum}` : ''}
            </p>
          </div>
        </div>

        <div className="mt-8 rounded-[2rem] border border-white/10 bg-white/10 p-5 backdrop-blur">
          <p className="text-[0.65rem] font-black uppercase tracking-[0.22em] text-white/45">
            Lectura rápida
          </p>
          <p className="mt-2 text-sm leading-6 text-white/70">
            Este es el candidato que quedó más cerca de tus respuestas según la distancia ponderada
            por categorías.
          </p>
        </div>

        {candidate.candidate_id >= 0 && (
          <Link
            to={buildCandidateDetailPath(candidate.candidate_id)}
            className="mt-8 inline-flex w-fit rounded-full bg-white px-5 py-3 text-xs font-black uppercase tracking-[0.2em] text-ink transition hover:bg-jade hover:text-white"
          >
            Ver candidato →
          </Link>
        )}
      </div>
    </article>
  )
}
