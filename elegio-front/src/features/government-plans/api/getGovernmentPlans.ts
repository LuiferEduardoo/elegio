import { apiClient } from '../../../config/api'
import type { GovernmentPlansResponse } from '../types'

const GOVERNMENT_PLANS_ERROR_MESSAGE =
  'No pudimos cargar el plan de gobierno. Revisá que la API esté corriendo.'

export async function getGovernmentPlans(
  candidateId: number | string,
): Promise<GovernmentPlansResponse> {
  try {
    const response = await apiClient.get<GovernmentPlansResponse>(
      `/api/v1/government-plans/${candidateId}`,
    )
    return response.data
  } catch (error) {
    throw new Error(GOVERNMENT_PLANS_ERROR_MESSAGE, { cause: error })
  }
}
