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

const INITIAL_STATE: SearchState = {
  hits: [],
  total: 0,
  isLoading: false,
  error: null,
  hasSearched: false,
}

export function useProposalSearch(query: string, debounceMs = 350): SearchState {
  const [state, setState] = useState<SearchState>(INITIAL_STATE)

  useEffect(() => {
    const trimmed = query.trim()
    if (trimmed.length === 0) {
      setState(INITIAL_STATE)
      return
    }

    let isMounted = true
    const timeoutId = setTimeout(() => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }))
      searchProposals(trimmed)
        .then((data) => {
          if (!isMounted) return
          setState({
            hits: data.items,
            total: data.total,
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
  }, [query, debounceMs])

  return state
}
