import { useMemo, useState } from 'react'
import { useCandidates } from '../features/candidates/hooks/useCandidates'
import { NavBar } from '../features/home/components/NavBar'
import { ProposalHitCard } from '../features/proposals/components/ProposalHitCard'
import { useProposalSearch } from '../features/proposals/hooks/useProposalSearch'
import { Footer } from '../components/Footer'

const FILTER_CLASS =
  'min-w-[12rem] rounded-full border border-coffee/15 bg-white px-4 py-2.5 text-sm font-semibold text-ink shadow-sm shadow-coffee/5 outline-none transition focus:border-clay focus:ring-2 focus:ring-clay/30'

export function ProposalsPage() {
  const [query, setQuery] = useState('')
  const [candidateId, setCandidateId] = useState<number | undefined>()
  const [categoryId, setCategoryId] = useState<number | undefined>()

  const { candidates } = useCandidates()
  const { hits, total, isLoading, error, hasSearched } = useProposalSearch(
    query,
    candidateId,
    categoryId,
  )

  const categories = useMemo(() => {
    const seen = new Map<number, string>()
    candidates.forEach((candidate) => {
      candidate.category_averages.forEach((avg) => {
        if (!seen.has(avg.category_id)) {
          seen.set(avg.category_id, avg.category_name)
        }
      })
    })
    return Array.from(seen, ([id, name]) => ({ id, name })).sort((a, b) =>
      a.name.localeCompare(b.name, 'es'),
    )
  }, [candidates])

  const hasActiveFilters = candidateId !== undefined || categoryId !== undefined

  const clearFilters = () => {
    setCandidateId(undefined)
    setCategoryId(undefined)
  }

  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />

      <main className="mx-auto w-full max-w-5xl flex-grow px-6 py-16 sm:px-10 lg:px-16">

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

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <label className="sr-only" htmlFor="filter-category">
            Filtrar por categoría
          </label>
          <select
            id="filter-category"
            value={categoryId ?? ''}
            onChange={(event) =>
              setCategoryId(event.target.value ? Number(event.target.value) : undefined)
            }
            className={FILTER_CLASS}
          >
            <option value="">Todas las categorías</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>

          <label className="sr-only" htmlFor="filter-candidate">
            Filtrar por candidato
          </label>
          <select
            id="filter-candidate"
            value={candidateId ?? ''}
            onChange={(event) =>
              setCandidateId(event.target.value ? Number(event.target.value) : undefined)
            }
            className={FILTER_CLASS}
          >
            <option value="">Todos los candidatos</option>
            {candidates.map((candidate) => (
              <option key={candidate.id} value={candidate.id}>
                {candidate.presidential_candidate}
              </option>
            ))}
          </select>

          {hasActiveFilters && (
            <button
              type="button"
              onClick={clearFilters}
              className="text-sm font-semibold text-clay underline-offset-4 transition hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-clay focus-visible:ring-offset-2"
            >
              Limpiar filtros
            </button>
          )}
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
              No encontramos propuestas que coincidan con "{query}"
              {hasActiveFilters ? ' con los filtros seleccionados' : ''}.
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
      <Footer />
    </div>
  )
}
