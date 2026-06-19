import { useEffect, useState } from 'react'
import { getAffinity, getCurrentTestAttempt } from '../api/testApi'
import type { AffinityResponse, CandidateAffinity } from '../types'
import { getVisitorTokenCookie } from '../../../utils/visitorToken'

export type AffinityResultStatus = 'loading' | 'ready' | 'empty' | 'error'

type AffinityResultState = {
  affinity: AffinityResponse | null
  status: AffinityResultStatus
}

/**
 * Processes affinity results to apply electoral rules:
 * 1. If the highest affinity candidate is <= 10% (0.1), prepends "Voto en Blanco" with 100% affinity.
 * 2. If BOTH of the top two candidates have >= 90% (0.9) affinity OR both have exactly 50% (0.5) affinity, 
 *    changes both of their affinities to 50% (0.5), and prepends an "Indeciso" candidate with "Inconsistencias ideológicas" and 50% (0.5) affinity.
 */
export function processAffinity(affinity: AffinityResponse | null): AffinityResponse | null {
  if (!affinity || !affinity.candidates || affinity.candidates.length === 0) {
    return affinity
  }

  const realCandidates = affinity.candidates.filter((c) => c.candidate_id >= 0)
  if (realCandidates.length === 0) {
    return affinity
  }

  // Rule 1: Max match <= 10% (0.1) among real candidates
  const maxAffinity = realCandidates[0].affinity
  if (maxAffinity <= 0.1) {
    const blankVoteCandidate: CandidateAffinity = {
      candidate_id: -1,
      presidential_candidate: 'Voto en Blanco',
      vice_presidential_candidate: '',
      political_group: 'Ningún partido',
      political_spectrum: null,
      photo_president: null,
      photo_vice_president: null,
      photo_of_political_group: null,
      affinity: 1.0, // 100%
      distance: 0,
      categories_compared: 0,
    }
    return {
      ...affinity,
      candidates: [blankVoteCandidate, ...realCandidates],
    }
  }

  // Rule 2: Top two candidates both have >= 90% (0.9) affinity OR both have exactly 50% (0.5) affinity
  if (realCandidates.length >= 2) {
    const firstAffinity = realCandidates[0].affinity
    const secondAffinity = realCandidates[1].affinity

    const isOver90Percent = firstAffinity >= 0.9 && secondAffinity >= 0.9
    const isExactly50Percent = Math.abs(firstAffinity - 0.5) < 0.001 && Math.abs(secondAffinity - 0.5) < 0.001

    if (isOver90Percent) {
      const undecidedCandidate: CandidateAffinity = {
        candidate_id: -2,
        presidential_candidate: 'Indeciso',
        vice_presidential_candidate: '',
        political_group: 'Inconsistencias ideológicas',
        political_spectrum: null,
        photo_president: null,
        photo_vice_president: null,
        photo_of_political_group: null,
        affinity: firstAffinity, // Keep original high percentage as the display match
        distance: 0,
        categories_compared: 0,
      }
      return {
        ...affinity,
        candidates: [undecidedCandidate, ...realCandidates],
      }
    }

    if (isExactly50Percent) {
      const undecidedCandidate: CandidateAffinity = {
        candidate_id: -2,
        presidential_candidate: 'Indeciso',
        vice_presidential_candidate: '',
        political_group: 'Indeciso',
        political_spectrum: null,
        photo_president: null,
        photo_vice_president: null,
        photo_of_political_group: null,
        affinity: 0.5,
        distance: 0,
        categories_compared: 0,
      }
      return {
        ...affinity,
        candidates: [undecidedCandidate, ...realCandidates],
      }
    }
  }

  return {
    ...affinity,
    candidates: realCandidates,
  }
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

        setState({ affinity: processAffinity(affinity), status: 'ready' })
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
