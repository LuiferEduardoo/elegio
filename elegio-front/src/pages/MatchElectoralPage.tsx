import { Link } from 'react-router'
import { Footer } from '../components/Footer'
import { NavBar } from '../features/home/components/NavBar'
import { AffinityBarChart } from '../features/tests/components/charts/AffinityBarChart'
import { CategoryPostureChart } from '../features/tests/components/charts/CategoryPostureChart'
import { MatchScoreGauge } from '../features/tests/components/charts/MatchScoreGauge'
import { MatchVersus } from '../features/tests/components/charts/MatchVersus'
import { MatchQuestionStep } from '../features/tests/components/MatchQuestionStep'
import { MatchTestIntro } from '../features/tests/components/MatchTestIntro'
import { useTestFlow } from '../features/tests/hooks/useTestFlow'
import type { AffinityResponse } from '../features/tests/types'
import { normalizeMojibake } from '../features/tests/utils/text'
import { buildCandidateDetailPath, ROUTE_PATHS } from '../routes/paths'

export function MatchElectoralPage() {
  const testFlow = useTestFlow()
  const { status } = testFlow

  const showIntro = status === 'idle' || status === 'loading' || status === 'error'
  const showQuestion =
    (status === 'ready' || status === 'submitting') && testFlow.currentQuestion
  const showResults = status === 'finished' && testFlow.affinity

  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />
      <main className="flex-grow overflow-x-hidden">
        <div className="mx-auto w-full max-w-6xl px-3 py-4 sm:px-10 sm:py-14 lg:px-16">
          {showIntro && (
            <MatchTestIntro
              activeTest={testFlow.activeTest}
              status={testFlow.status}
              error={testFlow.error}
              tests={testFlow.tests}
              onStart={testFlow.startTest}
              onSelectTest={testFlow.selectTest}
            />
          )}

          {showQuestion && testFlow.currentQuestion && (
            <MatchQuestionStep
              question={testFlow.currentQuestion}
              options={testFlow.currentOptions}
              selectedOptionId={testFlow.selectedOptions[testFlow.currentQuestion.id]}
              currentIndex={testFlow.currentIndex}
              totalQuestions={testFlow.questions.length}
              answeredCount={testFlow.answeredCount}
              canSubmit={testFlow.canSubmitCurrentQuestion}
              status={testFlow.status}
              error={testFlow.error}
              onSelectOption={testFlow.selectOption}
              onSubmit={testFlow.submitCurrentAnswer}
            />
          )}

          {showResults && testFlow.affinity && testFlow.affinity.candidates.length > 0 && (
            <MatchContent affinity={testFlow.affinity} />
          )}

          {showResults && testFlow.affinity && testFlow.affinity.candidates.length === 0 && (
            <div className="mx-auto max-w-xl py-16 text-center">
              <h1 className="font-display text-3xl tracking-[-0.03em] text-ink">
                No pudimos calcular tu match.
              </h1>
              <p className="mt-4 text-sm leading-6 text-muted">
                No encontramos propuestas suficientes para comparar. Reintentá el test.
              </p>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  )
}

function MatchContent({ affinity }: { affinity: AffinityResponse }) {
  const candidates = affinity.candidates
  const [winner, runnerUp] = candidates
  const winnerName = normalizeMojibake(winner.presidential_candidate)
  const winnerGroup = normalizeMojibake(winner.political_group)

  return (
    <>
      <header className="max-w-2xl">
        <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">Match electoral ✦</p>
        <h1 className="mt-3 font-display text-3xl tracking-[-0.04em] sm:text-4xl lg:text-5xl">
          Tu cara a cara definitivo
        </h1>
        <p className="mt-4 text-sm leading-6 text-muted">
          Comparamos tus respuestas con las propuestas de cada finalista. Acá está con quién hacés
          match y cómo se reparte tu afinidad, tema por tema.
        </p>
      </header>

      {/* Hero: winner gauge + versus */}
      <section className="mt-8 grid gap-4 sm:mt-10 sm:gap-6 lg:grid-cols-[minmax(0,0.85fr)_minmax(0,1.15fr)]">
        <article className="relative overflow-hidden rounded-[1.75rem] bg-ink p-4 text-white shadow-2xl shadow-coffee/15 sm:rounded-[2.5rem] sm:p-9">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_25%_15%,rgba(201,138,94,0.35),transparent_30%),radial-gradient(circle_at_85%_0%,rgba(107,183,162,0.32),transparent_28%)]" />
          <div className="relative z-10">
            <p className="text-xs font-black uppercase tracking-[0.28em] text-white/65">
              Tu mayor match
            </p>
            <div className="mt-5 flex justify-center overflow-hidden rounded-[1.5rem] bg-white/95 px-3 py-4 text-ink sm:mt-6 sm:rounded-[2rem] sm:p-5">
              <MatchScoreGauge value={winner.affinity} />
            </div>
            <h2 className="mt-5 font-display text-2xl leading-[0.98] tracking-[-0.04em] sm:mt-6 sm:text-3xl">
              {winnerName}
            </h2>
            <p className="mt-2 text-sm font-semibold text-white/75">{winnerGroup}</p>
            <Link
              to={buildCandidateDetailPath(winner.candidate_id)}
              className="mt-6 inline-flex w-fit rounded-full bg-white px-4 py-3 text-[0.65rem] font-black uppercase tracking-[0.18em] text-ink transition hover:bg-jade hover:text-white sm:px-5 sm:text-xs sm:tracking-[0.2em]"
            >
              Ver candidato →
            </Link>
          </div>
        </article>

        <div className="flex flex-col gap-6">
          {runnerUp && (
            <article className="rounded-[2rem] border border-coffee/10 bg-white p-5 shadow-xl shadow-coffee/5 sm:rounded-[2.5rem] sm:p-9">
              <p className="mb-5 text-xs font-black uppercase tracking-[0.28em] text-clay">
                Cara a cara
              </p>
              <MatchVersus left={winner} right={runnerUp} />
            </article>
          )}

          <article className="rounded-[2rem] border border-coffee/10 bg-white p-5 shadow-xl shadow-coffee/5 sm:rounded-[2.5rem] sm:p-9">
            <p className="mb-5 text-xs font-black uppercase tracking-[0.28em] text-clay">
              Ranking de afinidad
            </p>
            <AffinityBarChart candidates={candidates} />
          </article>
        </div>
      </section>

      {/* Category posture chart */}
      {affinity.user_averages.length > 0 && (
        <section className="mt-6 rounded-[2rem] border border-coffee/10 bg-white p-5 shadow-xl shadow-coffee/5 sm:rounded-[2.5rem] sm:p-9">
          <div className="mb-6 max-w-xl">
            <p className="text-xs font-black uppercase tracking-[0.28em] text-clay">
              Tu postura por tema
            </p>
            <h3 className="mt-2 font-display text-2xl tracking-[-0.03em] text-ink sm:text-3xl">
              Hacia dónde te inclinaste
            </h3>
          </div>
          <CategoryPostureChart categories={affinity.user_averages} />
        </section>
      )}

      <div className="mt-8 text-center">
        <Link
          to={ROUTE_PATHS.results}
          className="inline-flex rounded-full border border-coffee/20 px-6 py-3 text-xs font-black uppercase tracking-[0.25em] text-ink transition hover:bg-coffee/5"
        >
          Ver resultados completos →
        </Link>
      </div>
    </>
  )
}
