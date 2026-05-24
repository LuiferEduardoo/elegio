import { apiClient } from '../../../config/api'
import type { ProposalSearchResponse } from '../types'

const SEARCH_ERROR_MESSAGE =
  'No pudimos buscar propuestas. Revisá que la API esté corriendo.'

export async function searchProposals(
  query: string,
  limit = 20,
): Promise<ProposalSearchResponse> {
  try {
    const response = await apiClient.get<ProposalSearchResponse>(
      '/api/v1/search/proposals',
      { params: { q: query, limit } },
    )
    return response.data
  } catch (error) {
    throw new Error(SEARCH_ERROR_MESSAGE, { cause: error })
  }
}
