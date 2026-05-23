import type { Candidate, CategoryAverage } from '../types'

export function getTotalProposals(candidate: Candidate): number {
  return candidate.category_averages.reduce(
    (total, category) => total + category.proposals_count,
    0,
  )
}

export function getStrongestCategories(candidate: Candidate): CategoryAverage[] {
  return candidate.category_averages
    .toSorted((left, right) => Math.abs(right.average) - Math.abs(left.average))
    .slice(0, 3)
}

export function formatAxisValue(value: number): string {
  return value > 0 ? `+${value.toFixed(2)}` : value.toFixed(2)
}
