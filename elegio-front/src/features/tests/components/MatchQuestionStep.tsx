import { useCallback, useState } from 'react'
import type { TestFlowStatus } from '../hooks/useTestFlow'
import type { Question, ResponseOption } from '../types'
import { normalizeMojibake } from '../utils/text'
import { QuestionVideo } from './QuestionVideo'

type MatchQuestionStepProps = {
  question: Question
  options: ResponseOption[]
  selectedOptionId: number | undefined
  selectedEmotion: number | undefined
  currentIndex: number
  totalQuestions: number
  answeredCount: number
  canSubmit: boolean
  status: TestFlowStatus
  error: string | null
  onSelectOption: (questionId: number, optionId: number) => void
  onSelectEmotion: (questionId: number, value: number) => void
  onSubmit: () => void
}

const EMOTION_OPTIONS = [
  { value: -1, emoji: '😠', label: 'Me genera rechazo' },
  { value: 0, emoji: '😐', label: 'Me deja neutral' },
  { value: 1, emoji: '😊', label: 'Me genera empatía' },
]

/** Tints an option by the sign of its value: agree (jade) / neutral / against (clay). */
function optionTone(value: number, selected: boolean) {
  if (selected) {
    if (value > 0) return 'border-jade bg-jade text-white shadow-xl shadow-jade/25'
    if (value < 0) return 'border-clay bg-clay text-white shadow-xl shadow-clay/25'
    return 'border-coffee bg-coffee text-white shadow-xl shadow-coffee/20'
  }
  return 'border-coffee/10 bg-surface text-ink hover:border-clay/50 hover:bg-white'
}

export function MatchQuestionStep({
  question,
  options,
  selectedOptionId,
  selectedEmotion,
  currentIndex,
  totalQuestions,
  answeredCount,
  canSubmit,
  status,
  error,
  onSelectOption,
  onSelectEmotion,
  onSubmit,
}: MatchQuestionStepProps) {
  const progress = totalQuestions > 0 ? answeredCount / totalQuestions : 0
  const isLast = currentIndex === totalQuestions - 1
  const isEmotion = question.type_question === 'video_emotion_slider'
  const emotionValue = selectedEmotion ?? 0
  const activeEmotion =
    emotionValue <= -0.34
      ? EMOTION_OPTIONS[0]
      : emotionValue >= 0.34
        ? EMOTION_OPTIONS[2]
        : EMOTION_OPTIONS[1]
  const description = question.description ? normalizeMojibake(question.description) : null

  const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false)

  const handleAskEmma = useCallback(() => {
    const promptParts = [`Explícame esta pregunta del test electoral: ${normalizeMojibake(question.title)}`]
    if (question.category) {
      promptParts.push(`Categoría: ${normalizeMojibake(question.category.name)}`)
    }
    if (description) {
      promptParts.push(`Descripción: ${description}`)
    }
    promptParts.push('Trata de explicarla en lenguaje simple y sin sesgo político.')

    const event = new CustomEvent('emma:explain-question', {
      detail: {
        prompt: promptParts.join('\n\n'),
        questionId: question.id,
      },
    })

    window.dispatchEvent(event)
  }, [question, description])

  return (
    <section className="overflow-hidden rounded-2xl border border-coffee/10 bg-white shadow-2xl shadow-coffee/10 sm:rounded-[2.5rem]">
      {/* Progress header */}
      <div className="border-b border-coffee/10 bg-surface/60 px-4 py-3 sm:px-10 sm:py-5">
        <div className="flex items-center justify-between text-xs font-black uppercase tracking-[0.2em]">
          <span className="text-clay">
            Pregunta {currentIndex + 1} / {totalQuestions}
          </span>
          <span className="text-muted">{Math.round(progress * 100)}% completado</span>
        </div>
        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-coffee/10 sm:h-2">
          <div
            className="h-full rounded-full bg-gradient-to-r from-clay to-jade transition-all duration-500"
            style={{ width: `${progress * 100}%` }}
          />
        </div>
      </div>

      <div className="p-4 sm:p-10">
        {question.category && (
          <span className="inline-flex rounded-full border border-coffee/10 bg-white px-3 py-1 text-xs font-bold text-muted">
            {normalizeMojibake(question.category.name)}
          </span>
        )}

        <h2 className="mt-3 font-display text-xl leading-tight tracking-[-0.03em] text-ink sm:mt-5 sm:text-3xl">
          {normalizeMojibake(question.title)}
        </h2>

        {description && (
          <div className="mt-3 max-w-2xl sm:mt-4">
            <p
              className={`overflow-hidden text-sm leading-relaxed text-muted transition-all duration-300 ${
                !isDescriptionExpanded ? 'line-clamp-3 sm:line-clamp-none' : ''
              }`}
            >
              {description}
            </p>
            <button
              type="button"
              onClick={() => setIsDescriptionExpanded(!isDescriptionExpanded)}
              className="mt-1 text-xs font-bold text-clay hover:underline sm:hidden"
            >
              {isDescriptionExpanded ? 'Ver menos' : 'Ver más'}
            </button>
          </div>
        )}

        {question.video_url && (
          <div className="mt-4 sm:mt-6">
            <QuestionVideo url={question.video_url} />
          </div>
        )}

        <button
          type="button"
          onClick={handleAskEmma}
          className="group mt-4 inline-flex w-full items-center gap-3 rounded-2xl border border-jade/20 bg-gradient-to-r from-jade/10 via-surface to-clay/10 px-3.5 py-2.5 text-left transition hover:-translate-y-0.5 hover:border-jade/40 hover:shadow-lg hover:shadow-jade/15 sm:w-fit"
        >
          <span className="grid size-9 shrink-0 place-items-center rounded-full bg-gradient-to-br from-clay to-jade text-sm font-black text-white shadow-md shadow-jade/30 transition group-hover:rotate-12">
            ✦
          </span>
          <span className="min-w-0 flex-1">
            <span className="block text-sm font-black leading-tight text-ink">
              ¿No entendiste la pregunta?
            </span>
            <span className="block text-xs font-semibold text-muted">
              <span className="font-black text-jade">Emma</span> te la explica en simple
            </span>
          </span>
          <span className="shrink-0 text-jade transition group-hover:translate-x-0.5">→</span>
        </button>

        {isEmotion ? (
          <div className="mt-6 sm:mt-8">
            <div className="flex items-end justify-between px-1">
              {EMOTION_OPTIONS.map((emotion) => {
                const isActive = activeEmotion.value === emotion.value
                return (
                  <span
                    key={emotion.value}
                    className={`flex flex-col items-center gap-1 transition ${
                      isActive ? 'scale-110' : 'opacity-50'
                    }`}
                  >
                    <span className="text-2xl sm:text-3xl" aria-hidden="true">
                      {emotion.emoji}
                    </span>
                    <span className="text-[0.65rem] font-bold uppercase tracking-wide text-muted sm:text-xs">
                      {emotion.label}
                    </span>
                  </span>
                )
              })}
            </div>
            <input
              type="range"
              min={-1}
              max={1}
              step={0.01}
              value={emotionValue}
              onChange={(event) =>
                onSelectEmotion(question.id, Number(event.target.value))
              }
              aria-label="¿Qué te genera este video?"
              className="mt-4 w-full cursor-pointer accent-clay"
            />
            <p className="mt-4 text-center text-sm font-black text-ink">
              <span aria-hidden="true">{activeEmotion.emoji}</span> {activeEmotion.label}
            </p>
          </div>
        ) : (
          <div className="mt-5 grid gap-2 sm:mt-8 sm:gap-3">
            {options.map((option) => {
              const isSelected = selectedOptionId === option.id
              return (
                <button
                  key={option.id}
                  type="button"
                  onClick={() => onSelectOption(question.id, option.id)}
                  aria-pressed={isSelected}
                  className={`flex items-center justify-between rounded-xl border px-4 py-3 text-left transition sm:rounded-2xl sm:px-5 sm:py-4 ${optionTone(
                    option.value,
                    isSelected,
                  )}`}
                >
                  <span className="text-sm font-black sm:text-base">{normalizeMojibake(option.title)}</span>
                  <span
                    className={`grid size-4 shrink-0 place-items-center rounded-full border-2 sm:size-5 ${
                      isSelected ? 'border-white' : 'border-coffee/25'
                    }`}
                  >
                    {isSelected && <span className="size-1.5 rounded-full bg-white sm:size-2" />}
                  </span>
                </button>
              )
            })}
          </div>
        )}

        {error && <p className="mt-4 font-bold text-clay sm:mt-5">{error}</p>}

        <div className="mt-6 flex items-center justify-end sm:mt-8">
          <button
            type="button"
            onClick={onSubmit}
            disabled={!canSubmit || status === 'submitting'}
            className="w-full rounded-full bg-ink px-7 py-3 text-sm font-black uppercase tracking-[0.22em] text-white transition hover:bg-clay disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:py-3.5"
          >
            {status === 'submitting' ? 'Guardando…' : isLast ? 'Ver mi match →' : 'Siguiente →'}
          </button>
        </div>
      </div>
    </section>
  )
}
