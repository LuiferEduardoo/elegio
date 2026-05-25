import { NavBar } from '../features/home/components/NavBar'
import { QuestionStep } from '../features/tests/components/QuestionStep'
import { TestIntroPanel } from '../features/tests/components/TestIntroPanel'
import { TestProgressPanel } from '../features/tests/components/TestProgressPanel'
import { TestResultsPanel } from '../features/tests/components/TestResultsPanel'
import { useTestFlow } from '../features/tests/hooks/useTestFlow'

export function TestPage() {
  const testFlow = useTestFlow()
  const shouldShowIntro = ['idle', 'loading', 'error'].includes(testFlow.status)
  const shouldShowQuestion =
    ['ready', 'submitting'].includes(testFlow.status) && testFlow.currentQuestion
  const shouldShowResults = testFlow.status === 'finished'

  return (
    <div className="min-h-screen bg-surface text-ink">
      <NavBar />

      <main className="mx-auto max-w-6xl px-6 py-14 sm:px-10 lg:px-16">
        <section className="overflow-hidden rounded-[2.5rem] border border-coffee/10 bg-white shadow-2xl shadow-coffee/10">
          <div className="grid min-w-0 gap-0 lg:grid-cols-[0.9fr_minmax(0,1.1fr)]">
            <TestProgressPanel
              answeredCount={testFlow.answeredCount}
              progress={testFlow.progress}
              totalQuestions={testFlow.questions.length}
            />

            <section className="min-w-0 p-5 sm:p-8 lg:p-10">
              {shouldShowIntro && (
                <TestIntroPanel
                  activeTest={testFlow.activeTest}
                  error={testFlow.error}
                  status={testFlow.status}
                  testCount={testFlow.tests.length}
                  onStart={testFlow.startTest}
                />
              )}

              {shouldShowQuestion && testFlow.currentQuestion && (
                <QuestionStep
                  canSubmit={testFlow.canSubmitCurrentQuestion}
                  currentIndex={testFlow.currentIndex}
                  error={testFlow.error}
                  options={testFlow.currentOptions}
                  question={testFlow.currentQuestion}
                  selectedOptionId={
                    testFlow.selectedOptions[testFlow.currentQuestion.id]
                  }
                  status={testFlow.status}
                  totalQuestions={testFlow.questions.length}
                  onSelectOption={testFlow.selectOption}
                  onSubmit={testFlow.submitCurrentAnswer}
                />
              )}

              {shouldShowResults && testFlow.affinity && (
                <TestResultsPanel affinity={testFlow.affinity} />
              )}
            </section>
          </div>
        </section>
      </main>
    </div>
  )
}
