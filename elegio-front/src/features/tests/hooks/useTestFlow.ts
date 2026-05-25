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
  clearTestTokenCookie,
  getTestTokenCookie,
  setTestTokenCookie,
} from '../utils/testTokenCookie'

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
  const [token, setToken] = useState<string | null>(() => getTestTokenCookie())
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

        const storedToken = getTestTokenCookie()
        if (!storedToken) {
          setActiveTest(response.items[0])
          setStatus('idle')
          return
        }

        const attempt = await getCurrentTestAttempt(storedToken)
        if (!isMounted) return

        const testFromAttempt =
          response.items.find((test) => test.id === attempt.test_id) ?? response.items[0]
        const [loadedQuestions, answers] = await Promise.all([
          getQuestionsByTest(attempt.test_id),
          getAnswers(storedToken),
        ])
        if (!isMounted) return

        const answeredByQuestion = mapAnswersByQuestion(answers)
        setActiveTest(testFromAttempt)
        setToken(storedToken)
        setQuestions(loadedQuestions)
        setSelectedOptions(answeredByQuestion)

        if (attempt.status === 'completed') {
          const result = await getAffinity(storedToken)
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
        clearTestTokenCookie()
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
      const [attempt, loadedQuestions] = await Promise.all([
        initializeTestAttempt(activeTest.id),
        getQuestionsByTest(activeTest.id),
      ])
      const questionOptions = await loadQuestionOptions(loadedQuestions)

      setTestTokenCookie(attempt.token)
      setToken(attempt.token)
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
    if (!token || !currentQuestion) return

    const responseOptionId = selectedOptions[currentQuestion.id]
    if (responseOptionId === undefined) return

    setStatus('submitting')
    setError(null)

    try {
      await createAnswer({
        token,
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

      const result = await getAffinity(token)
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
    startTest,
    submitCurrentAnswer,
  }
}
