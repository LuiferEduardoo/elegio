import { useState } from 'react'
import { NavBar } from '../features/home/components/NavBar'
import { ProposalHitCard } from '../features/proposals/components/ProposalHitCard'
import { useProposalSearch } from '../features/proposals/hooks/useProposalSearch'

export function ProposalsPage() {
  const [query, setQuery] = useState('')
  const { hits, total, isLoading, error, hasSearched } = useProposalSearch(query)

  return (
    <div className="min-h-screen bg-surface text-ink">
      <NavBar />

      <main className="mx-auto max-w-5xl px-6 py-16 sm:px-10 lg:px-16">
        <header className="mb-10">
          <p className="text-sm font-black uppercase tracking-[0.3em] text-clay">Buscador</p>
          <h1 className="mt-3 font-display text-4xl leading-[1.05] tracking-[-0.04em] text-ink sm:text-5xl">
            Encontrá propuestas con evidencia.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-muted">
            Buscá por tema, palabra clave o intención. Comparamos por título, resumen y
            extractos de los planes de gobierno de cada candidato.
          </p>
        </header>

        <div className="relative">
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Ej: pensiones, energía, educación rural..."
            aria-label="Buscar propuestas"
            className="w-full rounded-full border border-coffee/15 bg-white px-6 py-4 text-base text-ink shadow-sm shadow-coffee/5 outline-none transition placeholder:text-muted/70 focus:border-clay focus:ring-2 focus:ring-clay/30"
            autoFocus
          />
        </div>

        <section className="mt-10" aria-live="polite">
          {!hasSearched && !isLoading && (
            <p className="rounded-3xl border border-dashed border-coffee/15 bg-white/60 p-6 text-muted">
              Escribí un término para empezar la búsqueda.
            </p>
          )}

          {isLoading && (
            <p className="rounded-3xl border border-coffee/10 bg-white p-6 text-muted">
              Buscando...
            </p>
          )}

          {error && (
            <p className="rounded-3xl bg-clay p-6 font-bold text-white">{error}</p>
          )}

          {!isLoading && !error && hasSearched && hits.length === 0 && (
            <p className="rounded-3xl border border-coffee/10 bg-white p-6 text-muted">
              No encontramos propuestas que coincidan con "{query}".
            </p>
          )}

          {hits.length > 0 && (
            <>
              <p className="mb-4 text-sm font-semibold text-muted">
                {total} {total === 1 ? 'resultado' : 'resultados'}
              </p>
              <ul className="flex flex-col gap-4">
                {hits.map((hit) => (
                  <li key={hit.proposal_id}>
                    <ProposalHitCard hit={hit} />
                  </li>
                ))}
              </ul>
            </>
          )}
        </section>
      </main>
    </div>
  )
}
