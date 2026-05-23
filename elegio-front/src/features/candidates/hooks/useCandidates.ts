import { useEffect, useState } from 'react'
import { getCandidates } from '../api/getCandidates'
import type { Candidate } from '../types'

type CandidateState = {
  candidates: Candidate[]
  isLoading: boolean
  error: string | null
}

export function useCandidates(): CandidateState {
  const [state, setState] = useState<CandidateState>({
    candidates: [],
    isLoading: true,
    error: null,
  })

  useEffect(() => {
    let isMounted = true

    getCandidates()
      .then((data) => {
        if (isMounted) {
          setState({ candidates: data.items, isLoading: false, error: null })
        }
      })
      .catch((error: Error) => {
        if (isMounted) {
          setState({ candidates: [], isLoading: false, error: error.message })
        }
      })

    return () => {
      isMounted = false
    }
  }, [])

  return state
}
