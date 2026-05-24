import { Link } from 'react-router'
import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import { buildCandidateDetailPath } from '../../../routes/paths'
import type { CandidateAffinity } from '../types'
import { formatPercent } from '../utils/text'

type TestResultsPanelProps = {
  candidates: CandidateAffinity[]
}

export function TestResultsPanel({ candidates }: TestResultsPanelProps) {
  return (
    <div>
      <p className="text-sm font-black uppercase tracking-[0.25em] text-clay">Resultados</p>
      <h2 className="mt-3 font-display text-4xl tracking-[-0.04em]">
        Tus candidatos más afines
      </h2>
      <div className="mt-8 grid gap-4">
        {candidates.map((candidate, index) => (
          <article
            key={candidate.candidate_id}
            className="flex gap-4 rounded-[2rem] border border-coffee/10 bg-surface p-4"
          >
            <img
              src={candidate.photo_president || fallbackCandidateImage}
              alt={candidate.presidential_candidate}
              className="h-24 w-20 rounded-2xl object-cover object-top"
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
              <h3 className="mt-2 text-xl font-black leading-tight">
                {candidate.presidential_candidate}
              </h3>
              <p className="mt-1 text-sm text-muted">
                {candidate.political_group} · {candidate.political_spectrum}
              </p>
              <Link
                to={buildCandidateDetailPath(candidate.candidate_id)}
                className="mt-3 inline-flex text-sm font-black text-clay underline-offset-4 hover:underline"
              >
                Ver candidato →
              </Link>
            </div>
          </article>
        ))}
      </div>

      <p className="mt-8 rounded-3xl border border-coffee/10 bg-surface p-5 text-sm font-semibold text-muted">
        Tu resultado queda guardado en este navegador. Cuando vuelvas a entrar al test, te
        mostramos esta misma pantalla.
      </p>
    </div>
  )
}
