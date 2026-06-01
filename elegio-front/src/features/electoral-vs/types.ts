import type { Proposal } from '../proposals/types'

export const MAX_SELECTED_CANDIDATES = 2

export type CategoryOption = {
  id: number
  name: string
}

export type ComparisonState = {
  error: string | null
  proposalsByCandidate: Record<number, Proposal[]>
  requestKey: string
}

export const EMPTY_COMPARISON: ComparisonState = {
  error: null,
  proposalsByCandidate: {},
  requestKey: '',
}
