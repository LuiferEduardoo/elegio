import { apiClient } from '../../../config/api'
import type { ProposalListResponse } from '../types'

const PROPOSALS_ERROR_MESSAGE =
  'No pudimos cargar las propuestas. Revisá que la API esté corriendo.'

export type GetProposalsOptions = {
  candidateId?: number
  categoryId?: number
  limit?: number
  offset?: number
}

export async function getProposals({
  candidateId,
  categoryId,
  limit = 100,
  offset = 0,
}: GetProposalsOptions = {}): Promise<ProposalListResponse> {
  try {
    const response = await apiClient.get<ProposalListResponse>('/api/v1/proposals', {
      params: {
        limit,
        offset,
        candidate_id: candidateId,
        category_id: categoryId,
      },
    })

    return response.data
  } catch (error) {
    throw new Error(PROPOSALS_ERROR_MESSAGE, { cause: error })
  }
}
