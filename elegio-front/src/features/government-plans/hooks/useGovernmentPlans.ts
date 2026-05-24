import { useEffect, useState } from 'react'
import { getGovernmentPlans } from '../api/getGovernmentPlans'
import type { GovernmentPlan } from '../types'

type GovernmentPlansState = {
  plans: GovernmentPlan[]
  isLoading: boolean
  error: string | null
}

export function useGovernmentPlans(candidateId: string | undefined): GovernmentPlansState {
  const [state, setState] = useState<GovernmentPlansState>({
    plans: [],
    isLoading: true,
    error: null,
  })

  useEffect(() => {
    if (!candidateId) {
      setState({ plans: [], isLoading: false, error: null })
      return
    }

    let isMounted = true
    setState({ plans: [], isLoading: true, error: null })

    getGovernmentPlans(candidateId)
      .then((data) => {
        if (isMounted) {
          setState({ plans: data.items, isLoading: false, error: null })
        }
      })
      .catch((error: Error) => {
        if (isMounted) {
          setState({ plans: [], isLoading: false, error: error.message })
        }
      })

    return () => {
      isMounted = false
    }
  }, [candidateId])

  return state
}
