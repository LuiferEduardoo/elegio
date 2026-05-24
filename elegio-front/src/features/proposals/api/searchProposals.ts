import { apiClient } from '../../../config/api'
import type { ProposalSearchResponse } from '../types'

const SEARCH_ERROR_MESSAGE =
  'No pudimos buscar propuestas. Revisá que la API esté corriendo.'

export type SearchProposalsOptions = {
  candidateId?: number
  categoryId?: number
  limit?: number
}

export async function searchProposals(
  query: string,
  { candidateId, categoryId, limit = 20 }: SearchProposalsOptions = {},
): Promise<ProposalSearchResponse> {
  try {
    const response = await apiClient.get<ProposalSearchResponse>(
      '/api/v1/search/proposals',
      {
        params: {
          q: query,
          limit,
          candidate_id: candidateId,
          category_id: categoryId,
        },
      },
    )
    return response.data
  } catch (error) {
    throw new Error(SEARCH_ERROR_MESSAGE, { cause: error })
  }
}
