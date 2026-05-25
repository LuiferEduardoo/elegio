import { useMemo, useState } from 'react'
import { Footer } from '../components/Footer'
import { useCandidates } from '../features/candidates/hooks/useCandidates'
import { CandidateVsSelector } from '../features/electoral-vs/components/CandidateVsSelector'
import { CategoryVsSelector } from '../features/electoral-vs/components/CategoryVsSelector'
import { ComparisonBoard } from '../features/electoral-vs/components/ComparisonBoard'
import { ElectoralVsHero } from '../features/electoral-vs/components/ElectoralVsHero'
import { StanceComparisonBar } from '../features/electoral-vs/components/StanceComparisonBar'
import { StickySelectionBar } from '../features/electoral-vs/components/StickySelectionBar'
import { useElectoralComparison } from '../features/electoral-vs/hooks/useElectoralComparison'
import { MAX_SELECTED_CANDIDATES } from '../features/electoral-vs/types'
import { getCategoryOptions } from '../features/electoral-vs/utils'
import { NavBar } from '../features/home/components/NavBar'

export function ElectoralVsPage() {
  const { candidates, isLoading, error } = useCandidates()
  const [selectedCandidateIds, setSelectedCandidateIds] = useState<number[]>([])
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | undefined>()
  const categories = useMemo(() => getCategoryOptions(candidates), [candidates])
  const selectedCandidates = useMemo(
    () => candidates.filter((candidate) => selectedCandidateIds.includes(candidate.id)),
    [candidates, selectedCandidateIds],
  )
  const selectedCategory = categories.find((category) => category.id === selectedCategoryId)
  const comparison = useElectoralComparison(selectedCandidateIds, selectedCategoryId)

  const toggleCandidate = (candidateId: number) => {
    setSelectedCandidateIds((current) => {
      if (current.includes(candidateId)) {
        return current.filter((selectedId) => selectedId !== candidateId)
      }
      if (current.length >= MAX_SELECTED_CANDIDATES) return current
      return [...current, candidateId]
    })
  }

  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />

      <main className="mx-auto w-full max-w-7xl flex-grow px-6 py-14 sm:px-10 lg:px-16">
        <ElectoralVsHero
          selectedCategory={selectedCategory}
          selectedCount={selectedCandidateIds.length}
        />

        {isLoading && (
          <p className="mt-8 rounded-3xl border border-coffee/10 bg-white p-6 text-muted">
            Cargando candidatos...
          </p>
        )}

        {error && <p className="mt-8 rounded-3xl bg-clay p-6 font-bold text-white">{error}</p>}

        {!isLoading && !error && (
          <>
            <StickySelectionBar
              selectedCandidates={selectedCandidates}
              selectedCategory={selectedCategory}
              onClear={() => setSelectedCandidateIds([])}
              onToggle={toggleCandidate}
            />

            <CandidateVsSelector
              candidates={candidates}
              selectedCandidateIds={selectedCandidateIds}
              onClear={() => setSelectedCandidateIds([])}
              onToggle={toggleCandidate}
            />

            <CategoryVsSelector
              categories={categories}
              selectedCategoryId={selectedCategoryId}
              onSelectCategory={setSelectedCategoryId}
            />

            {selectedCategory && selectedCandidates.length > 0 && (
              <StanceComparisonBar
                categoryId={selectedCategory.id}
                categoryName={selectedCategory.name}
                selectedCandidates={selectedCandidates}
              />
            )}

            <ComparisonBoard
              categoryName={selectedCategory?.name}
              error={comparison.error}
              isLoading={comparison.isComparing}
              proposalsByCandidate={comparison.proposalsByCandidate}
              selectedCandidates={selectedCandidates}
              shouldShow={comparison.canCompare}
            />
          </>
        )}
      </main>

      <Footer />
    </div>
  )
}
