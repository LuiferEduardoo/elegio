import { useEffect, useState } from 'react'
import { getProposals } from '../api/getProposals'
import type { Proposal } from '../types'

type ProposalsState = {
  proposals: Proposal[]
  total: number
  isLoading: boolean
  error: string | null
}

type InternalProposalsState = ProposalsState & {
  requestKey: string
}

const LOADING_STATE: InternalProposalsState = {
  proposals: [],
  total: 0,
  isLoading: true,
  error: null,
  requestKey: '',
}

function getRequestKey(candidateIds: number[], categoryId?: number): string {
  return `${candidateIds.join(',') || 'all'}:${categoryId ?? 'all'}`
}

async function getProposalsForCandidates(
  candidateIds: number[],
  categoryId?: number,
): Promise<Pick<ProposalsState, 'proposals' | 'total'>> {
  if (candidateIds.length === 0) {
    const data = await getProposals({ categoryId })
    return { proposals: data.items, total: data.total }
  }

  const responses = await Promise.all(
    candidateIds.map((candidateId) => getProposals({ candidateId, categoryId })),
  )

  return {
    proposals: responses.flatMap((response) => response.items),
    total: responses.reduce((sum, response) => sum + response.total, 0),
  }
}

export function useProposals(
  candidateIds: number[],
  categoryId?: number,
  enabled = true,
): ProposalsState {
  const [state, setState] = useState<InternalProposalsState>(LOADING_STATE)
  const requestKey = enabled ? getRequestKey(candidateIds, categoryId) : 'idle'

  useEffect(() => {
    if (!enabled) return

    let isMounted = true

    getProposalsForCandidates(candidateIds, categoryId)
      .then(({ proposals, total }) => {
        if (!isMounted) return

        setState({
          proposals,
          total,
          isLoading: false,
          error: null,
          requestKey,
        })
      })
      .catch((error: Error) => {
        if (!isMounted) return

        setState({
          proposals: [],
          total: 0,
          isLoading: false,
          error: error.message,
          requestKey,
        })
      })

    return () => {
      isMounted = false
    }
  }, [candidateIds, categoryId, enabled, requestKey])

  if (!enabled) {
    return {
      proposals: [],
      total: 0,
      isLoading: false,
      error: null,
    }
  }

  if (state.requestKey !== requestKey) {
    return {
      proposals: [],
      total: 0,
      isLoading: true,
      error: null,
    }
  }

  return {
    proposals: state.proposals,
    total: state.total,
    isLoading: state.isLoading,
    error: state.error,
  }
}
