import type { Candidate } from '../types'
import { CandidateCard } from './CandidateCard'

type CandidateGridProps = {
  candidates: Candidate[]
  error: string | null
  isLoading: boolean
}

export function CandidateGrid({ candidates, error, isLoading }: CandidateGridProps) {
  const secondRoundCandidates = candidates.filter(
    (candidate) => candidate.is_in_the_second_round,
  )

  return (
    <section className="mx-auto max-w-7xl px-6 py-14 sm:px-10 lg:px-16">
      <div className="mb-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-black uppercase tracking-[0.3em] text-clay">Candidatos</p>
            <h2 className="mt-2 font-display text-4xl tracking-[-0.04em] text-ink">
              El tarjetón, explicado.
            </h2>
          </div>
          <a
            href="https://wapp.registraduria.gov.co/electoral/2026/presidente-de-la-republica/IMG/pdf/tarjeta-electoral_presidente-2026.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex w-fit items-center justify-center rounded-full bg-ink px-5 py-2.5 text-sm font-bold text-white transition hover:bg-clay focus:outline-none focus-visible:ring-2 focus-visible:ring-clay focus-visible:ring-offset-2"
          >
            Ver tarjetón electoral
          </a>
        </div>
        <p className="mt-4 max-w-xl text-sm leading-6 text-muted">
          Cada tarjeta resume fórmula presidencial, espectro político y categorías
          donde sus propuestas tienen posiciones más marcadas.
        </p>
      </div>

      {isLoading && <p className="rounded-3xl border border-coffee/10 bg-white p-8 text-muted">Cargando candidatos...</p>}
      {error && <p className="rounded-3xl bg-clay p-8 font-bold text-white">{error}</p>}

      <div className="grid gap-8 py-2 md:grid-cols-2 xl:grid-cols-3">
        {secondRoundCandidates.map((candidate) => (
          <CandidateCard candidate={candidate} key={candidate.id} />
        ))}
      </div>
    </section>
  )
}
