import { apiClient } from '../../../config/api'
import type { Candidate } from '../types'

const CANDIDATE_ERROR_MESSAGE =
  'No pudimos cargar el candidato. Revisá que la API esté corriendo.'

export async function getCandidate(id: number | string): Promise<Candidate> {
  try {
    const response = await apiClient.get<Candidate>(`/api/v1/candidates/${id}`)
    return response.data
  } catch (error) {
    throw new Error(CANDIDATE_ERROR_MESSAGE, { cause: error })
  }
}
