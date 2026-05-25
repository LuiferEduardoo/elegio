import type { TestFlowStatus } from '../hooks/useTestFlow'
import type { Question, ResponseOption } from '../types'
import { normalizeMojibake } from '../utils/text'

type QuestionStepProps = {
  canSubmit: boolean
  currentIndex: number
  error: string | null
  options: ResponseOption[]
  question: Question
  selectedOptionId: number | undefined
  status: TestFlowStatus
  totalQuestions: number
  onSelectOption: (questionId: number, optionId: number) => void
  onSubmit: () => void
}

export function QuestionStep({
  canSubmit,
  currentIndex,
  error,
  options,
  question,
  selectedOptionId,
  status,
  totalQuestions,
  onSelectOption,
  onSubmit,
}: QuestionStepProps) {
  return (
    <div className="min-h-[28rem]">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <span className="rounded-full bg-jade/10 px-4 py-2 text-xs font-black uppercase tracking-[0.2em] text-jade">
          Pregunta {currentIndex + 1} de {totalQuestions}
        </span>
        {question.category && (
          <span className="rounded-full border border-coffee/10 px-4 py-2 text-xs font-bold text-muted">
            {normalizeMojibake(question.category.name)}
          </span>
        )}
      </div>

      <h2 className="mt-8 text-3xl font-black leading-tight tracking-[-0.03em] text-ink">
        {normalizeMojibake(question.title)}
      </h2>

      <div className="mt-8 grid gap-3">
        {options.map((option) => {
          const isSelected = selectedOptionId === option.id

          return (
            <button
              key={option.id}
              type="button"
              onClick={() => onSelectOption(question.id, option.id)}
              className={`rounded-3xl border px-5 py-4 text-left transition ${
                isSelected
                  ? 'border-clay bg-clay text-white shadow-xl shadow-clay/20'
                  : 'border-coffee/10 bg-surface text-ink hover:border-clay/50 hover:bg-white'
              }`}
            >
              <span className="block text-base font-black">
                {normalizeMojibake(option.title)}
              </span>
            </button>
          )
        })}
      </div>

      {error && <p className="mt-5 font-bold text-clay">{error}</p>}

      <div className="mt-8 flex flex-wrap items-center justify-between gap-3">
        <span className="text-sm font-bold text-muted">
          Tus respuestas quedan asociadas a este intento.
        </span>
        <button
          type="button"
          onClick={onSubmit}
          disabled={!canSubmit || status === 'submitting'}
          className="rounded-full bg-ink px-6 py-3 text-sm font-black uppercase tracking-[0.22em] text-white transition hover:bg-clay disabled:cursor-not-allowed disabled:opacity-50"
        >
          {status === 'submitting'
            ? 'Guardando...'
            : currentIndex === totalQuestions - 1
              ? 'Ver resultados'
              : 'Siguiente'}
        </button>
      </div>
    </div>
  )
}
