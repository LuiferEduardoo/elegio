import type { CategoryAverage } from '../types'

type CategorySpectrumBarProps = {
  category: CategoryAverage
}

const clampAverage = (value: number) => Math.max(-1, Math.min(1, value))

const formatWeight = (weight: number) => `${Math.round(weight * 100)}%`

const formatAverage = (value: number) => {
  const sign = value > 0 ? '+' : ''
  return `${sign}${value.toFixed(2)}`
}

export function CategorySpectrumBar({ category }: CategorySpectrumBarProps) {
  const average = clampAverage(category.average)
  const markerPosition = ((average + 1) / 2) * 100
  const leansPositive = average > 0
  const leansNegative = average < 0

  return (
    <article className="rounded-3xl border border-coffee/10 bg-white p-6 shadow-sm shadow-coffee/5">
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">
            {category.category_name}
          </p>
          <p className="mt-1 text-sm text-muted">
            {category.proposals_count} propuesta{category.proposals_count === 1 ? '' : 's'} analizada
            {category.proposals_count === 1 ? '' : 's'}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-surface px-3 py-1 text-[0.65rem] font-black uppercase tracking-[0.25em] text-coffee">
            Peso {formatWeight(category.weight)}
          </span>
          <span
            className={`rounded-full px-3 py-1 text-[0.65rem] font-black uppercase tracking-[0.25em] ${
              leansPositive
                ? 'bg-jade text-white'
                : leansNegative
                  ? 'bg-coffee text-white'
                  : 'bg-coffee/10 text-coffee'
            }`}
          >
            {formatAverage(average)}
          </span>
        </div>
      </header>

      <div className="mt-6">
        <div className="relative h-3 rounded-full bg-gradient-to-r from-coffee/15 via-coffee/5 to-jade/20">
          <div className="absolute inset-y-0 left-1/2 w-px bg-coffee/30" aria-hidden="true" />
          <div
            className="absolute top-1/2 size-5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-clay shadow-md shadow-coffee/30 transition-all"
            style={{ left: `${markerPosition}%` }}
            aria-hidden="true"
          />
        </div>

        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <div
            className={`rounded-2xl border p-4 transition ${
              leansNegative ? 'border-coffee/40 bg-coffee/5' : 'border-coffee/10 bg-surface/60'
            }`}
          >
            <p className="text-[0.65rem] font-black uppercase tracking-[0.25em] text-coffee">
              ◀ {category.negative_pole_name}
            </p>
            <p className="mt-2 text-sm leading-5 text-ink/80">
              {category.negative_pole_description}
            </p>
          </div>
          <div
            className={`rounded-2xl border p-4 transition ${
              leansPositive ? 'border-jade/50 bg-jade/5' : 'border-coffee/10 bg-surface/60'
            }`}
          >
            <p className="text-[0.65rem] font-black uppercase tracking-[0.25em] text-jade">
              {category.positive_pole_name} ▶
            </p>
            <p className="mt-2 text-sm leading-5 text-ink/80">
              {category.positive_pole_description}
            </p>
          </div>
        </div>
      </div>
    </article>
  )
}
