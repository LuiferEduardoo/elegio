import { useEffect, useState } from 'react'
import { getAffinity, getCurrentTestAttempt } from '../api/testApi'
import type { AffinityResponse } from '../types'
import { getVisitorTokenCookie } from '../../../utils/visitorToken'

export type AffinityResultStatus = 'loading' | 'ready' | 'empty' | 'error'

type AffinityResultState = {
  affinity: AffinityResponse | null
  status: AffinityResultStatus
}

/**
 * Loads the affinity result for the visitor's finished test, reading the token
 * from the cookie. Use on standalone routes (e.g. /resultados) that don't share
 * the test flow state.
 */
export function useAffinityResult(testId?: number): AffinityResultState {
  const [state, setState] = useState<AffinityResultState>(() => ({
    affinity: null,
    status: getVisitorTokenCookie() ? 'loading' : 'empty',
  }))

  useEffect(() => {
    const token = getVisitorTokenCookie()
    if (!token) {
      return
    }

    let isMounted = true

    async function load(authToken: string) {
      setState((prev) => ({ ...prev, status: 'loading' }))
      try {
        const attempt = await getCurrentTestAttempt(authToken, testId)
        if (!isMounted) return

        if (!attempt || attempt.status !== 'completed') {
          setState({ affinity: null, status: 'empty' })
          return
        }

        const affinity = await getAffinity(authToken, attempt.test_id)
        if (!isMounted) return

        setState({ affinity, status: 'ready' })
      } catch {
        if (isMounted) setState({ affinity: null, status: 'error' })
      }
    }

    load(token)

    return () => {
      isMounted = false
    }
  }, [testId])

  return state
}
