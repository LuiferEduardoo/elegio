import { useEffect, useState } from 'react'
import { searchProposals } from '../api/searchProposals'
import type { ProposalHit } from '../types'

type SearchState = {
  hits: ProposalHit[]
  total: number
  isLoading: boolean
  error: string | null
  hasSearched: boolean
}

function mergeHitsByProposal(hits: ProposalHit[]): ProposalHit[] {
  const hitsByProposal = new Map<number, ProposalHit>()

  hits.forEach((hit) => {
    const current = hitsByProposal.get(hit.proposal_id)
    if (!current || hit.score > current.score) {
      hitsByProposal.set(hit.proposal_id, hit)
    }
  })

  return Array.from(hitsByProposal.values()).sort((a, b) => b.score - a.score)
}

async function searchAcrossCandidates(
  query: string,
  candidateIds: number[],
  categoryId?: number,
): Promise<Pick<SearchState, 'hits' | 'total'>> {
  if (candidateIds.length === 0) {
    const data = await searchProposals(query, { categoryId, limit: 50 })
    return { hits: data.items, total: data.total }
  }

  const responses = await Promise.all(
    candidateIds.map((candidateId) =>
      searchProposals(query, { candidateId, categoryId, limit: 50 }),
    ),
  )
  const hits = mergeHitsByProposal(responses.flatMap((response) => response.items))

  return { hits, total: hits.length }
}

const INITIAL_STATE: SearchState = {
  hits: [],
  total: 0,
  isLoading: false,
  error: null,
  hasSearched: false,
}

export function useProposalSearch(
  query: string,
  candidateIds: number[],
  categoryId?: number,
  debounceMs = 350,
): SearchState {
  const [state, setState] = useState<SearchState>(INITIAL_STATE)

  useEffect(() => {
    const trimmed = query.trim()
    if (trimmed.length === 0) {
      return
    }

    let isMounted = true
    const timeoutId = setTimeout(() => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }))
      searchAcrossCandidates(trimmed, candidateIds, categoryId)
        .then(({ hits, total }) => {
          if (!isMounted) return
          setState({
            hits,
            total,
            isLoading: false,
            error: null,
            hasSearched: true,
          })
        })
        .catch((error: Error) => {
          if (!isMounted) return
          setState({
            hits: [],
            total: 0,
            isLoading: false,
            error: error.message,
            hasSearched: true,
          })
        })
    }, debounceMs)

    return () => {
      isMounted = false
      clearTimeout(timeoutId)
    }
  }, [query, candidateIds, categoryId, debounceMs])

  return query.trim().length === 0 ? INITIAL_STATE : state
}
