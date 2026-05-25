import { useEffect, useState } from 'react'
import { getProposals } from '../../proposals/api/getProposals'
import { buildRequestKey } from '../utils'
import { EMPTY_COMPARISON, type ComparisonState } from '../types'

type ElectoralComparisonState = ComparisonState & {
  canCompare: boolean
  isComparing: boolean
}

export function useElectoralComparison(
  selectedCandidateIds: number[],
  selectedCategoryId: number | undefined,
): ElectoralComparisonState {
  const [comparisonState, setComparisonState] =
    useState<ComparisonState>(EMPTY_COMPARISON)
  const requestKey = buildRequestKey(selectedCandidateIds, selectedCategoryId)
  const canCompare = requestKey.length > 0
  const isComparing = canCompare && comparisonState.requestKey !== requestKey

  useEffect(() => {
    if (!canCompare || selectedCategoryId === undefined) return

    let isMounted = true

    Promise.all(
      selectedCandidateIds.map(async (candidateId) => {
        const response = await getProposals({
          candidateId,
          categoryId: selectedCategoryId,
          limit: 100,
        })
        return [candidateId, response.items] as const
      }),
    )
      .then((entries) => {
        if (!isMounted) return
        setComparisonState({
          error: null,
          proposalsByCandidate: Object.fromEntries(entries),
          requestKey,
        })
      })
      .catch((compareError: Error) => {
        if (!isMounted) return
        setComparisonState({
          error: compareError.message,
          proposalsByCandidate: {},
          requestKey,
        })
      })

    return () => {
      isMounted = false
    }
  }, [canCompare, requestKey, selectedCandidateIds, selectedCategoryId])

  return {
    ...comparisonState,
    canCompare,
    isComparing,
  }
}
