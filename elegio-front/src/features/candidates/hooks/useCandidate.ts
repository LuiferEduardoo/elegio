import { useEffect, useState } from 'react'
import { getCandidate } from '../api/getCandidate'
import type { Candidate } from '../types'

type CandidateDetailState = {
  candidate: Candidate | null
  isLoading: boolean
  error: string | null
}

export function useCandidate(id: string | undefined): CandidateDetailState {
  const [state, setState] = useState<CandidateDetailState>({
    candidate: null,
    isLoading: true,
    error: null,
  })

  useEffect(() => {
    if (!id) {
      setState({ candidate: null, isLoading: false, error: 'Candidato no encontrado.' })
      return
    }

    let isMounted = true
    setState({ candidate: null, isLoading: true, error: null })

    getCandidate(id)
      .then((data) => {
        if (isMounted) {
          setState({ candidate: data, isLoading: false, error: null })
        }
      })
      .catch((error: Error) => {
        if (isMounted) {
          setState({ candidate: null, isLoading: false, error: error.message })
        }
      })

    return () => {
      isMounted = false
    }
  }, [id])

  return state
}
