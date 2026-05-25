import { useEffect, useState } from 'react'
import { getAffinity, getCurrentTestAttempt } from '../api/testApi'
import type { AffinityResponse } from '../types'
import { getTestTokenCookie } from '../utils/testTokenCookie'

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
export function useAffinityResult(): AffinityResultState {
  const [state, setState] = useState<AffinityResultState>(() => ({
    affinity: null,
    status: getTestTokenCookie() ? 'loading' : 'empty',
  }))

  useEffect(() => {
    const token = getTestTokenCookie()
    if (!token) return

    let isMounted = true

    async function load(authToken: string) {
      try {
        const attempt = await getCurrentTestAttempt(authToken)
        if (!isMounted) return

        if (attempt.status !== 'completed') {
          setState({ affinity: null, status: 'empty' })
          return
        }

        const affinity = await getAffinity(authToken)
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
  }, [])

  return state
}
