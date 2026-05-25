import { useEffect, useState } from 'react'
import { getGovernmentPlans } from '../api/getGovernmentPlans'
import type { GovernmentPlan } from '../types'

type GovernmentPlansState = {
  plans: GovernmentPlan[]
  isLoading: boolean
  error: string | null
}

type GovernmentPlansRequestState = GovernmentPlansState & {
  candidateId: string | null
}

export function useGovernmentPlans(candidateId: string | undefined): GovernmentPlansState {
  const [state, setState] = useState<GovernmentPlansRequestState>({
    candidateId: null,
    plans: [],
    isLoading: false,
    error: null,
  })

  useEffect(() => {
    if (!candidateId) return

    let isMounted = true

    getGovernmentPlans(candidateId)
      .then((data) => {
        if (isMounted) {
          setState({ candidateId, plans: data.items, isLoading: false, error: null })
        }
      })
      .catch((error: Error) => {
        if (isMounted) {
          setState({ candidateId, plans: [], isLoading: false, error: error.message })
        }
      })

    return () => {
      isMounted = false
    }
  }, [candidateId])

  if (!candidateId) {
    return { plans: [], isLoading: false, error: null }
  }

  if (state.candidateId !== candidateId) {
    return { plans: [], isLoading: true, error: null }
  }

  return state
}
