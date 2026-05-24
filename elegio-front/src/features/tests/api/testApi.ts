import { apiClient } from '../../../config/api'
import type {
  AffinityResponse,
  AnswerCreateResponse,
  AnswerListResponse,
  InitializeTestResponse,
  Question,
  QuestionListResponse,
  ResponseOption,
  ResponseOptionListResponse,
  TestListResponse,
} from '../types'

const TEST_ERROR_MESSAGE = 'No pudimos cargar el test. Revisá que la API esté corriendo.'
const AUTH_ERROR_MESSAGE = 'No pudimos guardar tu respuesta. Volvé a iniciar el test.'

export async function getAvailableTests(): Promise<TestListResponse> {
  try {
    const response = await apiClient.get<TestListResponse>('/api/v1/tests', {
      params: { limit: 10 },
    })
    return response.data
  } catch (error) {
    throw new Error(TEST_ERROR_MESSAGE, { cause: error })
  }
}

export async function initializeTestAttempt(testId: number): Promise<InitializeTestResponse> {
  try {
    const response = await apiClient.post<InitializeTestResponse>(
      '/api/v1/test-attempts/initialize',
      {
        test_id: testId,
        visitor: {
          primary_language: navigator.language,
          languages: navigator.languages ? Array.from(navigator.languages) : undefined,
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
          consent_given: true,
          screen_width: window.screen.width,
          screen_height: window.screen.height,
          pixel_ratio: window.devicePixelRatio,
        },
        session: {
          landing_page: window.location.pathname,
          referer: document.referrer || undefined,
          viewport_width: window.innerWidth,
          viewport_height: window.innerHeight,
        },
      },
    )
    return response.data
  } catch (error) {
    throw new Error(TEST_ERROR_MESSAGE, { cause: error })
  }
}

export async function getCurrentTestAttempt(token: string): Promise<InitializeTestResponse['test_attempt']> {
  try {
    const response = await apiClient.get<InitializeTestResponse['test_attempt']>(
      '/api/v1/test-attempts',
      { headers: { Authorization: `Bearer ${token}` } },
    )
    return response.data
  } catch (error) {
    throw new Error(AUTH_ERROR_MESSAGE, { cause: error })
  }
}

export async function getAnswers(token: string): Promise<AnswerListResponse> {
  try {
    const response = await apiClient.get<AnswerListResponse>('/api/v1/answers', {
      params: { limit: 100 },
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data
  } catch (error) {
    throw new Error(AUTH_ERROR_MESSAGE, { cause: error })
  }
}

export async function getQuestionsByTest(testId: number): Promise<Question[]> {
  try {
    const response = await apiClient.get<QuestionListResponse>(
      `/api/v1/questions/by-test/${testId}`,
      { params: { limit: 100 } },
    )
    return response.data.items
      .filter((question) => question.is_active)
      .sort((a, b) => a.question_order - b.question_order || a.id - b.id)
  } catch (error) {
    throw new Error(TEST_ERROR_MESSAGE, { cause: error })
  }
}

export async function getResponseOptionsByQuestion(
  questionId: number,
): Promise<ResponseOption[]> {
  try {
    const response = await apiClient.get<ResponseOptionListResponse>(
      `/api/v1/response-options/question/${questionId}`,
      { params: { limit: 10 } },
    )
    return response.data.items
  } catch (error) {
    throw new Error(TEST_ERROR_MESSAGE, { cause: error })
  }
}

export async function createAnswer({
  token,
  questionId,
  responseOptionId,
  responseTime,
}: {
  token: string
  questionId: number
  responseOptionId: number
  responseTime: number
}): Promise<AnswerCreateResponse> {
  try {
    const response = await apiClient.post<AnswerCreateResponse>(
      '/api/v1/answers',
      {
        question_id: questionId,
        response_option_id: responseOptionId,
        response_time: responseTime,
      },
      { headers: { Authorization: `Bearer ${token}` } },
    )
    return response.data
  } catch (error) {
    throw new Error(AUTH_ERROR_MESSAGE, { cause: error })
  }
}

export async function getAffinity(token: string): Promise<AffinityResponse> {
  try {
    const response = await apiClient.get<AffinityResponse>('/api/v1/answers/affinity', {
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data
  } catch (error) {
    throw new Error(AUTH_ERROR_MESSAGE, { cause: error })
  }
}
