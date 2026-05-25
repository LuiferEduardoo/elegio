import { useState } from 'react'
import { normalizeMojibake } from '../../../utils/text'
import { useCandidate } from '../../candidates/hooks/useCandidate'
import type { CategoryAverage } from '../../candidates/types'
import type { CandidateAffinity } from '../types'
import { CandidatePickerStrip } from './CandidatePickerStrip'
import { ComparisonOverview } from './ComparisonOverview'
import { ComparisonSpectrumBar } from './ComparisonSpectrumBar'

type CandidateComparisonProps = {
  candidates: CandidateAffinity[]
  userAverages: Record<number, number>
}

export function CandidateComparison({ candidates, userAverages }: CandidateComparisonProps) {
  const [selectedId, setSelectedId] = useState(() => candidates[0]?.candidate_id)

  const selected =
    candidates.find((candidate) => candidate.candidate_id === selectedId) ?? candidates[0]
  const { candidate, isLoading, error } = useCandidate(
    selected ? String(selected.candidate_id) : undefined,
  )

  if (!selected) return null

  return (
    <section className="mt-12 min-w-0 overflow-hidden border-t border-coffee/10 pt-10">
      <p className="text-sm font-black uppercase tracking-[0.25em] text-clay">Comparativa</p>
      <h3 className="mt-3 font-display text-2xl tracking-[-0.03em] sm:text-3xl">
        Mirate frente a cada candidato
      </h3>
      <p className="mt-2 max-w-xl text-sm leading-6 text-muted">
        Elegí cualquier candidato —no solo los más afines— y compará tu postura con la suya en cada
        categoría.
      </p>

      <CandidatePickerStrip
        candidates={candidates}
        selectedId={selected.candidate_id}
        onSelect={setSelectedId}
      />

      <ComparisonOverview
        affinity={selected.affinity}
        categoriesCompared={selected.categories_compared}
        distance={selected.distance}
        name={normalizeMojibake(selected.presidential_candidate)}
        photo={selected.photo_president}
        politicalGroup={normalizeMojibake(selected.political_group)}
      />

      <div className="mt-10">
        {isLoading && <ComparisonSkeleton />}
        {error && (
          <p className="rounded-3xl border border-coffee/10 bg-surface p-5 text-sm font-semibold text-muted">
            {error}
          </p>
        )}
        {!isLoading && !error && candidate && <ComparedCategories
          categoryAverages={candidate.category_averages}
          userAverages={userAverages}
        />}
      </div>
    </section>
  )
}

type ComparedCategoriesProps = {
  categoryAverages: CategoryAverage[]
  userAverages: Record<number, number>
}

function ComparedCategories({ categoryAverages, userAverages }: ComparedCategoriesProps) {
  const comparedCategories = [...categoryAverages]
    .filter((category) => userAverages[category.category_id] !== undefined)
    .sort((a, b) => b.weight - a.weight)

  if (comparedCategories.length === 0) {
    return (
      <p className="rounded-3xl border border-coffee/10 bg-surface p-5 text-sm font-semibold text-muted">
        No hay categorías en común para comparar con este candidato.
      </p>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {comparedCategories.map((category) => (
        <ComparisonSpectrumBar
          key={category.category_id}
          category={category}
          userAverage={userAverages[category.category_id]}
        />
      ))}
    </div>
  )
}

function ComparisonSkeleton() {
  return (
    <div className="grid gap-5 lg:grid-cols-2">
      {[0, 1, 2, 3].map((key) => (
        <div key={key} className="h-44 animate-pulse rounded-3xl border border-coffee/10 bg-coffee/5" />
      ))}
    </div>
  )
}
