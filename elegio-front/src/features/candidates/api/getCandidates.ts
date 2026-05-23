import { apiClient } from '../../../config/api'
import type { CandidatesResponse } from '../types'

const CANDIDATES_ERROR_MESSAGE =
  'No pudimos cargar los candidatos. Revisá que la API esté corriendo.'

export async function getCandidates(): Promise<CandidatesResponse> {
  try {
    const response = await apiClient.get<CandidatesResponse>('/api/v1/candidates', {
      params: { limit: 100 },
    })

    return response.data
  } catch (error) {
    throw new Error(CANDIDATES_ERROR_MESSAGE, { cause: error })
  }
}
