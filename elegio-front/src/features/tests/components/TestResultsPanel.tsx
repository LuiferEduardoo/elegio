import { Link } from 'react-router'
import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import { ROUTE_PATHS, buildCandidateDetailPath } from '../../../routes/paths'
import type { AffinityResponse } from '../types'
import { formatPercent, normalizeMojibake } from '../utils/text'

type TestResultsPanelProps = {
  affinity: AffinityResponse
}

export function TestResultsPanel({ affinity }: TestResultsPanelProps) {
  const topCandidates = affinity.candidates.slice(0, 5)

  return (
    <div className="min-w-0">
      <p className="text-sm font-black uppercase tracking-[0.25em] text-clay">Resultados</p>
      <h2 className="mt-3 font-display text-3xl tracking-[-0.04em] sm:text-4xl">
        Tus candidatos más afines
      </h2>

      <div className="mt-8 grid gap-4">
        {topCandidates.map((candidate, index) => {
          const name = normalizeMojibake(candidate.presidential_candidate)
          const group = normalizeMojibake(candidate.political_group)
          const spectrum = candidate.political_spectrum
            ? normalizeMojibake(candidate.political_spectrum)
            : null

          return (
            <article
              key={candidate.candidate_id}
              className="flex gap-4 rounded-[2rem] border border-coffee/10 bg-surface p-4"
            >
              <img
                src={candidate.photo_president || fallbackCandidateImage}
                alt={name}
                className="h-24 w-20 shrink-0 rounded-2xl object-cover object-top"
                loading="lazy"
                onError={(event) => {
                  event.currentTarget.onerror = null
                  event.currentTarget.src = fallbackCandidateImage
                }}
              />
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-full bg-ink px-3 py-1 text-xs font-black text-white">
                    #{index + 1}
                  </span>
                  <span className="text-sm font-black text-jade">
                    {formatPercent(candidate.affinity)} afinidad
                  </span>
                </div>
                <h3 className="mt-2 truncate text-xl font-black leading-tight">{name}</h3>
                <p className="mt-1 truncate text-sm text-muted">
                  {group}
                  {spectrum ? ` · ${spectrum}` : ''}
                </p>
                <Link
                  to={buildCandidateDetailPath(candidate.candidate_id)}
                  className="mt-3 inline-flex text-sm font-black text-clay underline-offset-4 hover:underline"
                >
                  Ver candidato →
                </Link>
              </div>
            </article>
          )
        })}
      </div>

      <Link
        to={ROUTE_PATHS.results}
        className="mt-8 inline-flex w-full items-center justify-center rounded-full bg-ink px-6 py-4 text-xs font-black uppercase tracking-[0.2em] text-white transition hover:bg-jade sm:w-auto"
      >
        Ver resultados completos y comparativa →
      </Link>

      <p className="mt-6 rounded-3xl border border-coffee/10 bg-surface p-5 text-sm font-semibold text-muted">
        Tu resultado queda guardado en este navegador. Cuando vuelvas a entrar al test, te mostramos
        esta misma pantalla.
      </p>
    </div>
  )
}
