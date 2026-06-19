import axios from 'axios'

import { apiClient } from '../../../config/api'
import type {
  AffinityResponse,
  AnswerCreateResponse,
  AnswerListResponse,
  Question,
  QuestionListResponse,
  ResponseOption,
  ResponseOptionListResponse,
  TestAttempt,
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

export async function initializeTestAttempt(
  testId: number,
  token: string,
): Promise<TestAttempt> {
  try {
    const response = await apiClient.post<TestAttempt>(
      '/api/v1/test-attempts/initialize',
      { test_id: testId },
      { headers: { Authorization: `Bearer ${token}` } },
    )
    return response.data
  } catch (error) {
    throw new Error(TEST_ERROR_MESSAGE, { cause: error })
  }
}

export async function getCurrentTestAttempt(
  token: string,
  testId?: number,
): Promise<TestAttempt | null> {
  try {
    const response = await apiClient.get<TestAttempt>(
      '/api/v1/test-attempts',
      {
        params: testId !== undefined ? { test_id: testId } : undefined,
        headers: { Authorization: `Bearer ${token}` },
      },
    )
    return response.data
  } catch (error) {
    // A visitor token can exist (from the chat or analytics) without any test
    // attempt yet: a 404 just means the test hasn't been started.
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      return null
    }
    throw new Error(AUTH_ERROR_MESSAGE, { cause: error })
  }
}

export async function getAnswers(
  token: string,
  testId: number,
): Promise<AnswerListResponse> {
  try {
    const response = await apiClient.get<AnswerListResponse>(
      `/api/v1/answers/${testId}`,
      {
        params: { limit: 100 },
        headers: { Authorization: `Bearer ${token}` },
      },
    )
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
  testAttemptId,
  questionId,
  responseOptionId,
  emotionAnswer,
  responseTime,
}: {
  token: string
  testAttemptId: number
  questionId: number
  responseOptionId?: number
  emotionAnswer?: number
  responseTime: number
}): Promise<AnswerCreateResponse> {
  try {
    const response = await apiClient.post<AnswerCreateResponse>(
      `/api/v1/answers/${testAttemptId}`,
      {
        question_id: questionId,
        response_option_id: responseOptionId ?? null,
        emotion_answer: emotionAnswer ?? null,
        response_time: responseTime,
      },
      { headers: { Authorization: `Bearer ${token}` } },
    )
    return response.data
  } catch (error) {
    throw new Error(AUTH_ERROR_MESSAGE, { cause: error })
  }
}

export async function getAffinity(
  token: string,
  testId: number,
): Promise<AffinityResponse> {
  try {
    const response = await apiClient.get<AffinityResponse>(
      `/api/v1/answers/affinity/${testId}`,
      { headers: { Authorization: `Bearer ${token}` } },
    )
    return response.data
  } catch (error) {
    throw new Error(AUTH_ERROR_MESSAGE, { cause: error })
  }
}
