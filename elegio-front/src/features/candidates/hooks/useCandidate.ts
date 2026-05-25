import { useEffect, useState } from 'react'
import { getCandidate } from '../api/getCandidate'
import type { Candidate } from '../types'

type CandidateDetailState = {
  candidate: Candidate | null
  isLoading: boolean
  error: string | null
}

type CandidateDetailRequestState = CandidateDetailState & {
  candidateId: string | null
}

export function useCandidate(id: string | undefined): CandidateDetailState {
  const [state, setState] = useState<CandidateDetailRequestState>({
    candidateId: null,
    candidate: null,
    isLoading: false,
    error: null,
  })

  useEffect(() => {
    if (!id) return

    let isMounted = true

    getCandidate(id)
      .then((data) => {
        if (isMounted) {
          setState({ candidateId: id, candidate: data, isLoading: false, error: null })
        }
      })
      .catch((error: Error) => {
        if (isMounted) {
          setState({ candidateId: id, candidate: null, isLoading: false, error: error.message })
        }
      })

    return () => {
      isMounted = false
    }
  }, [id])

  if (!id) {
    return { candidate: null, isLoading: false, error: 'Candidato no encontrado.' }
  }

  if (state.candidateId !== id) {
    return { candidate: null, isLoading: true, error: null }
  }

  return state
}
