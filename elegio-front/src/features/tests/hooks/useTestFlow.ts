import { useEffect, useMemo, useState } from 'react'
import {
  createAnswer,
  getAffinity,
  getAnswers,
  getAvailableTests,
  getCurrentTestAttempt,
  getQuestionsByTest,
  getResponseOptionsByQuestion,
  initializeTestAttempt,
} from '../api/testApi'
import type { AffinityResponse, Question, ResponseOption, Test } from '../types'
import {
  getOrCreateVisitorToken,
  getVisitorTokenCookie,
} from '../../../utils/visitorToken'
import { DEFAULT_TEST_ID } from '../../../config/api'

/** Picks the configured default test, falling back to the first one listed. */
function pickDefaultTest(tests: Test[]): Test {
  return tests.find((test) => test.id === DEFAULT_TEST_ID) ?? tests[0]
}

export type TestFlowStatus =
  | 'idle'
  | 'loading'
  | 'ready'
  | 'submitting'
  | 'finished'
  | 'error'

type OptionsByQuestionId = Record<number, ResponseOption[]>
type SelectedOptions = Record<number, number>

async function loadQuestionOptions(questions: Question[]): Promise<OptionsByQuestionId> {
  const entries = await Promise.all(
    questions.map(async (question) => [
      question.id,
      await getResponseOptionsByQuestion(question.id),
    ] as const),
  )

  return Object.fromEntries(entries)
}

function mapAnswersByQuestion(
  answers: Awaited<ReturnType<typeof getAnswers>>,
): SelectedOptions {
  return Object.fromEntries(
    answers.items
      .filter((answer) => answer.response_option_id !== null)
      .map((answer) => [answer.question_id, answer.response_option_id as number]),
  )
}

function getFirstUnansweredIndex(
  questions: Question[],
  selectedOptions: SelectedOptions,
): number {
  const index = questions.findIndex(
    (question) => selectedOptions[question.id] === undefined,
  )

  return index === -1 ? 0 : index
}

export function useTestFlow() {
  const [tests, setTests] = useState<Test[]>([])
  const [activeTest, setActiveTest] = useState<Test | null>(null)
  const [questions, setQuestions] = useState<Question[]>([])
  const [optionsByQuestionId, setOptionsByQuestionId] = useState<OptionsByQuestionId>({})
  const [selectedOptions, setSelectedOptions] = useState<SelectedOptions>({})
  const [currentIndex, setCurrentIndex] = useState(0)
  const [token, setToken] = useState<string | null>(() => getVisitorTokenCookie())
  const [testAttemptId, setTestAttemptId] = useState<number | null>(null)
  const [status, setStatus] = useState<TestFlowStatus>('loading')
  const [error, setError] = useState<string | null>(null)
  const [questionStartedAt, setQuestionStartedAt] = useState(() => Date.now())
  const [affinity, setAffinity] = useState<AffinityResponse | null>(null)

  useEffect(() => {
    let isMounted = true

    async function loadTestState() {
      try {
        const response = await getAvailableTests()
        if (!isMounted) return

        setTests(response.items)
        if (response.items.length === 0) {
          setError('No hay tests disponibles por ahora.')
          setStatus('error')
          return
        }

        const candidateTest = pickDefaultTest(response.items)
        const storedToken = getVisitorTokenCookie()
        if (!storedToken) {
          setActiveTest(candidateTest)
          setStatus('idle')
          return
        }

        const attempt = await getCurrentTestAttempt(storedToken, candidateTest.id)
        if (!isMounted) return

        if (!attempt) {
          // The visitor token exists (chat/analytics) but no test was started yet.
          setActiveTest(candidateTest)
          setStatus('idle')
          return
        }

        const testFromAttempt =
          response.items.find((test) => test.id === attempt.test_id) ?? response.items[0]
        const [loadedQuestions, answers] = await Promise.all([
          getQuestionsByTest(attempt.test_id),
          getAnswers(storedToken, attempt.test_id),
        ])
        if (!isMounted) return

        const answeredByQuestion = mapAnswersByQuestion(answers)
        setActiveTest(testFromAttempt)
        setToken(storedToken)
        setTestAttemptId(attempt.id)
        setQuestions(loadedQuestions)
        setSelectedOptions(answeredByQuestion)

        if (attempt.status === 'completed') {
          const result = await getAffinity(storedToken, attempt.test_id)
          if (!isMounted) return
          setAffinity(result)
          setCurrentIndex(Math.max(loadedQuestions.length - 1, 0))
          setStatus('finished')
          return
        }

        const questionOptions = await loadQuestionOptions(loadedQuestions)
        if (!isMounted) return

        setOptionsByQuestionId(questionOptions)
        setCurrentIndex(getFirstUnansweredIndex(loadedQuestions, answeredByQuestion))
        setQuestionStartedAt(Date.now())
        setStatus('ready')
      } catch (loadError) {
        if (!isMounted) return
        // Keep the shared visitor token (also used by the chat and analytics);
        // just drop the local reference so the user can start over.
        setToken(null)
        setError(loadError instanceof Error ? loadError.message : 'No pudimos cargar el test.')
        setStatus('error')
      }
    }

    loadTestState()

    return () => {
      isMounted = false
    }
  }, [])

  const currentQuestion = questions[currentIndex]
  const currentOptions = currentQuestion ? optionsByQuestionId[currentQuestion.id] ?? [] : []
  const answeredCount = Object.keys(selectedOptions).length
  const progress = questions.length > 0 ? answeredCount / questions.length : 0
  const canSubmitCurrentQuestion =
    currentQuestion !== undefined && selectedOptions[currentQuestion.id] !== undefined
  const topCandidates = useMemo(
    () => affinity?.candidates.slice(0, 5) ?? [],
    [affinity],
  )

  async function startTest() {
    if (!activeTest) return

    setStatus('loading')
    setError(null)
    setAffinity(null)
    setSelectedOptions({})
    setCurrentIndex(0)

    try {
      const authToken = await getOrCreateVisitorToken()
      const [attempt, loadedQuestions] = await Promise.all([
        initializeTestAttempt(activeTest.id, authToken),
        getQuestionsByTest(activeTest.id),
      ])
      const questionOptions = await loadQuestionOptions(loadedQuestions)

      setToken(authToken)
      setTestAttemptId(attempt.id)
      setQuestions(loadedQuestions)
      setOptionsByQuestionId(questionOptions)
      setQuestionStartedAt(Date.now())
      setStatus('ready')
    } catch (startError) {
      setError(startError instanceof Error ? startError.message : 'No pudimos iniciar el test.')
      setStatus('error')
    }
  }

  async function submitCurrentAnswer() {
    if (!token || !testAttemptId || !activeTest || !currentQuestion) return

    const responseOptionId = selectedOptions[currentQuestion.id]
    if (responseOptionId === undefined) return

    setStatus('submitting')
    setError(null)

    try {
      await createAnswer({
        token,
        testAttemptId,
        questionId: currentQuestion.id,
        responseOptionId,
        responseTime: Date.now() - questionStartedAt,
      })

      if (currentIndex < questions.length - 1) {
        setCurrentIndex((index) => index + 1)
        setQuestionStartedAt(Date.now())
        setStatus('ready')
        return
      }

      const result = await getAffinity(token, activeTest.id)
      setAffinity(result)
      setStatus('finished')
    } catch (submitError) {
      setError(
        submitError instanceof Error ? submitError.message : 'No pudimos guardar tu respuesta.',
      )
      setStatus('ready')
    }
  }

  function selectOption(questionId: number, optionId: number) {
    setSelectedOptions((selected) => ({ ...selected, [questionId]: optionId }))
  }

  async function selectTest(testId: number) {
    const targetTest = tests.find(t => t.id === testId)
    if (!targetTest) return

    // Reset all test local state completely
    setQuestions([])
    setOptionsByQuestionId({})
    setSelectedOptions({})
    setCurrentIndex(0)
    setTestAttemptId(null)
    setAffinity(null)
    setError(null)

    setActiveTest(targetTest)
    const storedToken = getVisitorTokenCookie()
    if (!storedToken) {
      setStatus('idle')
      return
    }

    try {
      const attempt = await getCurrentTestAttempt(storedToken, testId)
      if (!attempt) {
        setStatus('idle')
        return
      }

      const [loadedQuestions, answers] = await Promise.all([
        getQuestionsByTest(testId),
        getAnswers(storedToken, testId),
      ])

      const answeredByQuestion = mapAnswersByQuestion(answers)
      setTestAttemptId(attempt.id)
      setQuestions(loadedQuestions)
      setSelectedOptions(answeredByQuestion)

      if (attempt.status === 'completed') {
        const result = await getAffinity(storedToken, testId)
        setAffinity(result)
        setCurrentIndex(Math.max(loadedQuestions.length - 1, 0))
        setStatus('finished')
        return
      }

      const questionOptions = await loadQuestionOptions(loadedQuestions)
      setOptionsByQuestionId(questionOptions)
      setCurrentIndex(getFirstUnansweredIndex(loadedQuestions, answeredByQuestion))
      setQuestionStartedAt(Date.now())
      setStatus('ready')
    } catch {
      setStatus('idle')
    }
  }

  return {
    activeTest,
    affinity,
    answeredCount,
    canSubmitCurrentQuestion,
    currentIndex,
    currentOptions,
    currentQuestion,
    error,
    progress,
    questions,
    selectedOptions,
    status,
    tests,
    topCandidates,
    selectOption,
    selectTest,
    startTest,
    submitCurrentAnswer,
  }
}
