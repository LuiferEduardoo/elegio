import { useMemo, useState } from 'react'
import { useCandidates } from '../features/candidates/hooks/useCandidates'
import { NavBar } from '../features/home/components/NavBar'
import { ProposalCandidatePicker } from '../features/proposals/components/ProposalCandidatePicker'
import { ProposalCard } from '../features/proposals/components/ProposalCard'
import { ProposalCategoryFilter } from '../features/proposals/components/ProposalCategoryFilter'
import { ProposalCategoryMap } from '../features/proposals/components/ProposalCategoryMap'
import { ProposalHitCard } from '../features/proposals/components/ProposalHitCard'
import { ProposalPagination } from '../features/proposals/components/ProposalPagination'
import { useProposals } from '../features/proposals/hooks/useProposals'
import { useProposalSearch } from '../features/proposals/hooks/useProposalSearch'
import { Footer } from '../components/Footer'
import { normalizeMojibake } from '../utils/text'

const PAGE_SIZE = 6

function getPageItems<T>(items: T[], page: number): T[] {
  const start = (page - 1) * PAGE_SIZE
  return items.slice(start, start + PAGE_SIZE)
}

export function ProposalsPage() {
  const [query, setQuery] = useState('')
  const [selectedCandidateIds, setSelectedCandidateIds] = useState<number[]>([])
  const [categoryId, setCategoryId] = useState<number | undefined>()
  const [proposalPage, setProposalPage] = useState(1)
  const [searchPage, setSearchPage] = useState(1)
  const trimmedQuery = query.trim()
  const isSearching = trimmedQuery.length > 0
  const hasSelectedFilters = selectedCandidateIds.length > 0 || categoryId !== undefined

  const { candidates } = useCandidates()
  const {
    proposals,
    total: proposalsTotal,
    isLoading: isLoadingProposals,
    error: proposalsError,
  } = useProposals(selectedCandidateIds, categoryId, hasSelectedFilters)
  const { hits, total, isLoading, error, hasSearched } = useProposalSearch(
    query,
    selectedCandidateIds,
    categoryId,
  )

  const categories = useMemo(() => {
    const seen = new Map<number, string>()
    candidates.forEach((candidate) => {
      candidate.category_averages.forEach((avg) => {
        if (!seen.has(avg.category_id)) {
          seen.set(avg.category_id, normalizeMojibake(avg.category_name))
        }
      })
    })
    return Array.from(seen, ([id, name]) => ({ id, name })).sort((a, b) =>
      a.name.localeCompare(b.name, 'es'),
    )
  }, [candidates])

  const paginatedProposals = useMemo(
    () => getPageItems(proposals, proposalPage),
    [proposals, proposalPage],
  )
  const paginatedHits = useMemo(() => getPageItems(hits, searchPage), [hits, searchPage])

  const hasActiveFilters = hasSelectedFilters

  const updateQuery = (value: string) => {
    setQuery(value)
    setSearchPage(1)
  }

  const toggleCandidate = (candidateId: number) => {
    setSelectedCandidateIds((current) =>
      current.includes(candidateId)
        ? current.filter((selectedId) => selectedId !== candidateId)
        : [...current, candidateId],
    )
    setProposalPage(1)
    setSearchPage(1)
  }

  const updateCategory = (nextCategoryId: number | undefined) => {
    setCategoryId(nextCategoryId)
    setProposalPage(1)
    setSearchPage(1)
  }

  const clearFilters = () => {
    setSelectedCandidateIds([])
    updateCategory(undefined)
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
            Explorá el mapa completo por defecto o buscá por tema, palabra clave o
            intención. También podés filtrar por candidato y categoría.
          </p>
        </header>

        <div className="relative">
          <input
            type="search"
            value={query}
            onChange={(event) => updateQuery(event.target.value)}
            placeholder="Ej: pensiones, energía, educación rural..."
            aria-label="Buscar propuestas"
            className="w-full rounded-full border border-coffee/15 bg-white px-6 py-4 text-base text-ink shadow-sm shadow-coffee/5 outline-none transition placeholder:text-muted/70 focus:border-clay focus:ring-2 focus:ring-clay/30"
            autoFocus
          />
        </div>

        <ProposalCandidatePicker
          candidates={candidates}
          selectedCandidateIds={selectedCandidateIds}
          onToggleCandidate={toggleCandidate}
          onClearCandidates={() => {
            setSelectedCandidateIds([])
            setProposalPage(1)
            setSearchPage(1)
          }}
        />

        <ProposalCategoryFilter
          categories={categories}
          selectedCategoryId={categoryId}
          onSelectCategory={updateCategory}
        />

        <div className="mt-4 flex justify-end">
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
          {!isSearching && !hasActiveFilters && (
            <div className="rounded-[2rem] border border-dashed border-coffee/20 bg-white/60 p-6 text-center shadow-sm shadow-coffee/5">
              <p className="text-sm font-black uppercase tracking-[0.2em] text-clay">
                Búsqueda limpia
              </p>
              <h2 className="mt-2 font-display text-2xl tracking-[-0.03em] text-ink">
                Elegí un filtro o escribí para empezar.
              </h2>
              <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-muted">
                Al entrar no hay candidatos, categorías ni términos seleccionados. Así el
                mapa arranca neutro y vos decidís qué comparar.
              </p>
            </div>
          )}

          {!isSearching && hasActiveFilters && isLoadingProposals && (
            <p className="rounded-3xl border border-coffee/10 bg-white p-6 text-muted">
              Cargando propuestas...
            </p>
          )}

          {!isSearching && hasActiveFilters && proposalsError && (
            <p className="rounded-3xl bg-clay p-6 font-bold text-white">{proposalsError}</p>
          )}

          {!isSearching &&
            hasActiveFilters &&
            !isLoadingProposals &&
            !proposalsError &&
            proposals.length === 0 && (
            <p className="rounded-3xl border border-coffee/10 bg-white p-6 text-muted">
              No encontramos propuestas{hasActiveFilters ? ' con los filtros seleccionados' : ''}.
            </p>
          )}

          {!isSearching && hasActiveFilters && paginatedProposals.length > 0 && (
            <>
              <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-muted">
                    {proposalsTotal} {proposalsTotal === 1 ? 'propuesta' : 'propuestas'} disponibles
                  </p>
                  <h2 className="mt-1 font-display text-2xl tracking-[-0.03em] text-ink">
                    Propuestas destacadas
                  </h2>
                </div>
                <span className="rounded-full bg-jade/10 px-3 py-1 text-xs font-black uppercase tracking-[0.15em] text-jade">
                  {selectedCandidateIds.length === 0
                    ? 'Sin filtro de candidatura'
                    : `${selectedCandidateIds.length} candidaturas`}
                </span>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                {paginatedProposals.map((proposal) => (
                  <ProposalCard key={proposal.id} proposal={proposal} />
                ))}
              </div>

              <ProposalPagination
                currentPage={proposalPage}
                pageSize={PAGE_SIZE}
                totalItems={proposals.length}
                onPageChange={setProposalPage}
              />

              <ProposalCategoryMap proposals={paginatedProposals} />
            </>
          )}

          {isSearching && isLoading && (
            <p className="rounded-3xl border border-coffee/10 bg-white p-6 text-muted">
              Buscando...
            </p>
          )}

          {isSearching && error && (
            <p className="rounded-3xl bg-clay p-6 font-bold text-white">{error}</p>
          )}

          {isSearching && !isLoading && !error && hasSearched && hits.length === 0 && (
            <p className="rounded-3xl border border-coffee/10 bg-white p-6 text-muted">
              No encontramos propuestas que coincidan con "{query}"
              {hasActiveFilters ? ' con los filtros seleccionados' : ''}.
            </p>
          )}

          {isSearching && paginatedHits.length > 0 && (
            <>
              <p className="mb-4 text-sm font-semibold text-muted">
                {total} {total === 1 ? 'resultado' : 'resultados'}
              </p>
              <ul className="flex flex-col gap-4">
                {paginatedHits.map((hit) => (
                  <li key={hit.proposal_id}>
                    <ProposalHitCard hit={hit} />
                  </li>
                ))}
              </ul>

              <ProposalPagination
                currentPage={searchPage}
                pageSize={PAGE_SIZE}
                totalItems={hits.length}
                onPageChange={setSearchPage}
              />
            </>
          )}
        </section>
      </main>
      <Footer />
    </div>
  )
}
