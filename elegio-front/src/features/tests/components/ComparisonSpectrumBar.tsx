import { SpectrumMarker } from '../../../components/SpectrumMarker'
import { normalizeMojibake } from '../../../utils/text'
import type { CategoryAverage } from '../../candidates/types'

type ComparisonSpectrumBarProps = {
  category: CategoryAverage
  userAverage?: number
}

const clampAverage = (value: number) => Math.max(-1, Math.min(1, value))

const toPosition = (value: number) => ((clampAverage(value) + 1) / 2) * 100

const formatAverage = (value: number) => `${value > 0 ? '+' : ''}${value.toFixed(2)}`

export function ComparisonSpectrumBar({ category, userAverage }: ComparisonSpectrumBarProps) {
  const candidate = clampAverage(category.average)
  const hasUser = userAverage !== undefined
  const user = hasUser ? clampAverage(userAverage) : 0
  const gap = hasUser ? Math.abs(candidate - user) : 0

  const negativePole = normalizeMojibake(category.negative_pole_name)
  const positivePole = normalizeMojibake(category.positive_pole_name)
  const leanHint = (value: number) =>
    value >= 0.15 ? positivePole : value <= -0.15 ? negativePole : 'Postura neutral'

  return (
    <article className="min-w-0 rounded-3xl border border-coffee/10 bg-white p-4 shadow-sm shadow-coffee/5 sm:p-5">
      <header className="flex flex-wrap items-center justify-between gap-2">
        <p className="min-w-0 flex-1 truncate text-xs font-black uppercase tracking-[0.3em] text-clay">
          {normalizeMojibake(category.category_name)}
        </p>
        <span className="shrink-0 rounded-full bg-surface px-3 py-1 text-[0.65rem] font-black uppercase tracking-[0.25em] text-coffee">
          Peso {Math.round(category.weight * 100)}%
        </span>
      </header>

      <div className="mt-6">
        <div className="relative mx-3 h-4 rounded-full bg-gradient-to-r from-coffee/15 via-coffee/5 to-jade/20 sm:mx-2.5 sm:h-3">
          <div className="absolute inset-y-0 left-1/2 w-px bg-coffee/30" aria-hidden="true" />
          {hasUser && (
            <SpectrumMarker
              position={toPosition(user)}
              value={user}
              label="Tú"
              tone="user"
              hint={leanHint(user)}
            />
          )}
          <SpectrumMarker
            position={toPosition(candidate)}
            value={candidate}
            label="Candidato"
            tone="candidate"
            hint={leanHint(candidate)}
          />
        </div>

        <div className="mt-5 grid gap-2 text-[0.65rem] font-black uppercase tracking-[0.16em] sm:flex sm:flex-wrap sm:items-center sm:gap-x-5">
          {hasUser && (
            <span className="flex items-center gap-2 text-ink">
              <span className="size-3 rounded-full bg-ink" aria-hidden="true" /> Tú{' '}
              {formatAverage(user)}
            </span>
          )}
          <span className="flex items-center gap-2 text-clay">
            <span className="size-3 rounded-full bg-clay" aria-hidden="true" /> Candidato{' '}
            {formatAverage(candidate)}
          </span>
          {hasUser && <span className="text-muted">Distancia {gap.toFixed(2)}</span>}
        </div>

        <div className="mt-4 flex items-start justify-between gap-3 text-[0.55rem] font-black uppercase tracking-[0.13em] sm:text-[0.6rem] sm:tracking-[0.2em]">
          <span className="min-w-0 max-w-[46%] truncate text-coffee">
            ◀ {normalizeMojibake(category.negative_pole_name)}
          </span>
          <span className="min-w-0 max-w-[46%] truncate text-right text-jade">
            {normalizeMojibake(category.positive_pole_name)} ▶
          </span>
        </div>
      </div>
    </article>
  )
}
