import type { Candidate } from '../candidates/types'
import { normalizeMojibake } from '../../utils/text'
import type { CategoryOption } from './types'

export function buildRequestKey(
  candidateIds: number[],
  categoryId: number | undefined,
): string {
  if (!categoryId || candidateIds.length === 0) return ''
  return `${categoryId}:${candidateIds.join(',')}`
}

export function getCategoryOptions(candidates: Candidate[]): CategoryOption[] {
  const categories = new Map<number, string>()

  candidates.forEach((candidate) => {
    candidate.category_averages.forEach((category) => {
      if (!categories.has(category.category_id)) {
        categories.set(category.category_id, normalizeMojibake(category.category_name))
      }
    })
  })

  return Array.from(categories, ([id, name]) => ({ id, name })).sort((a, b) =>
    a.name.localeCompare(b.name, 'es'),
  )
}
