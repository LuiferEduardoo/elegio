import { SpectrumMarker } from '../../../components/SpectrumMarker'
import { normalizeMojibake } from '../../../utils/text'
import type { CategoryAverage } from '../types'

type CategorySpectrumBarProps = {
  category: CategoryAverage
  userAverage?: number | null
}

const clampAverage = (value: number) => Math.max(-1, Math.min(1, value))

const toPosition = (value: number) => ((clampAverage(value) + 1) / 2) * 100

const formatWeight = (weight: number) => `${Math.round(weight * 100)}%`

const formatAverage = (value: number) => {
  const sign = value > 0 ? '+' : ''
  return `${sign}${value.toFixed(2)}`
}

export function CategorySpectrumBar({ category, userAverage }: CategorySpectrumBarProps) {
  const average = clampAverage(category.adjusted_average)
  const leansPositive = average > 0
  const leansNegative = average < 0

  const isComparing = userAverage !== undefined && userAverage !== null
  const user = isComparing ? clampAverage(userAverage) : 0
  const gap = isComparing ? Math.abs(average - user) : 0

  const negativePole = normalizeMojibake(category.negative_pole_name)
  const positivePole = normalizeMojibake(category.positive_pole_name)
  const leanHint = (value: number) =>
    value >= 0.15 ? positivePole : value <= -0.15 ? negativePole : 'Postura neutral'

  return (
    <article className="rounded-3xl border border-coffee/10 bg-white p-6 shadow-sm shadow-coffee/5">
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">
            {normalizeMojibake(category.category_name)}
          </p>
          <p className="mt-1 text-sm text-muted">
            {category.proposals_count} propuesta{category.proposals_count === 1 ? '' : 's'} analizada
            {category.proposals_count === 1 ? '' : 's'}
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <span className="rounded-full bg-surface px-3 py-1 text-[0.65rem] font-black uppercase tracking-[0.25em] text-coffee">
            Peso {formatWeight(category.weight)}
          </span>
          {!isComparing && (
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
          )}
        </div>
      </header>

      <div className="mt-6">
        <div className="relative h-3 rounded-full bg-gradient-to-r from-coffee/15 via-coffee/5 to-jade/20">
          <div className="absolute inset-y-0 left-1/2 w-px bg-coffee/30" aria-hidden="true" />
          {isComparing && (
            <SpectrumMarker
              position={toPosition(user)}
              value={user}
              label="Tú"
              tone="user"
              hint={leanHint(user)}
            />
          )}
          <SpectrumMarker
            position={toPosition(average)}
            value={average}
            label="Candidato"
            tone="candidate"
            hint={leanHint(average)}
          />
        </div>

        {isComparing && (
          <div className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-2 text-[0.7rem] font-black uppercase tracking-[0.2em]">
            <span className="flex items-center gap-2 text-ink">
              <span className="size-3 rounded-full bg-ink" aria-hidden="true" /> Tú {formatAverage(user)}
            </span>
            <span className="flex items-center gap-2 text-clay">
              <span className="size-3 rounded-full bg-clay" aria-hidden="true" /> Candidato{' '}
              {formatAverage(average)}
            </span>
            <span className="text-muted">Distancia {gap.toFixed(2)}</span>
          </div>
        )}

        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <div
            className={`rounded-2xl border p-4 transition ${
              leansNegative ? 'border-coffee/40 bg-coffee/5' : 'border-coffee/10 bg-surface/60'
            }`}
          >
            <p className="text-[0.65rem] font-black uppercase tracking-[0.25em] text-coffee">
              ◀ {negativePole}
            </p>
            <p className="mt-2 text-sm leading-5 text-ink/80">
              {normalizeMojibake(category.negative_pole_description)}
            </p>
          </div>
          <div
            className={`rounded-2xl border p-4 transition ${
              leansPositive ? 'border-jade/50 bg-jade/5' : 'border-coffee/10 bg-surface/60'
            }`}
          >
            <p className="text-[0.65rem] font-black uppercase tracking-[0.25em] text-jade">
              {positivePole} ▶
            </p>
            <p className="mt-2 text-sm leading-5 text-ink/80">
              {normalizeMojibake(category.positive_pole_description)}
            </p>
          </div>
        </div>
      </div>
    </article>
  )
}
