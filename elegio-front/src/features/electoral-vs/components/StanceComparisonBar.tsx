import { SpectrumMarker } from '../../../components/SpectrumMarker'
import { normalizeMojibake } from '../../../utils/text'
import type { Candidate } from '../../candidates/types'

const MARKER_COLORS = ['bg-ink', 'bg-clay', 'bg-jade']

type StanceComparisonBarProps = {
  selectedCandidates: Candidate[]
  categoryId: number
  categoryName: string
}

const clampAverage = (value: number) => Math.max(-1, Math.min(1, value))

const toPosition = (value: number) => ((clampAverage(value) + 1) / 2) * 100

const formatAverage = (value: number) => `${value > 0 ? '+' : ''}${value.toFixed(2)}`

export function StanceComparisonBar({
  selectedCandidates,
  categoryId,
  categoryName,
}: StanceComparisonBarProps) {
  const entries = selectedCandidates.map((candidate, index) => ({
    candidate,
    average: candidate.category_averages.find((item) => item.category_id === categoryId),
    color: MARKER_COLORS[index % MARKER_COLORS.length],
  }))

  const withStance = entries.flatMap((entry) =>
    entry.average ? [{ candidate: entry.candidate, average: entry.average, color: entry.color }] : [],
  )
  const withoutStance = entries.filter((entry) => !entry.average)

  if (withStance.length === 0) return null

  const negativePole = normalizeMojibake(withStance[0].average.negative_pole_name)
  const positivePole = normalizeMojibake(withStance[0].average.positive_pole_name)
  const leanHint = (value: number) =>
    value >= 0.15 ? positivePole : value <= -0.15 ? negativePole : 'Postura neutral'

  return (
    <section className="mt-8 rounded-[2.5rem] border border-coffee/10 bg-white p-5 shadow-2xl shadow-coffee/10 sm:p-6 lg:p-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.25em] text-clay">Postura cara a cara</p>
          <h2 className="mt-1 font-display text-3xl tracking-[-0.04em] text-ink">{categoryName}</h2>
        </div>
        <p className="max-w-sm text-sm leading-6 text-muted">
          Dónde se para cada candidato en esta categoría, de un vistazo. Pasá el cursor sobre cada
          punto para ver el detalle.
        </p>
      </div>

      <div className="mt-9 px-3">
        <div className="relative h-3 rounded-full bg-gradient-to-r from-coffee/15 via-coffee/5 to-jade/20">
          <div className="absolute inset-y-0 left-1/2 w-px bg-coffee/30" aria-hidden="true" />
          {withStance.map(({ candidate, average, color }) => (
            <SpectrumMarker
              key={candidate.id}
              position={toPosition(average.average)}
              value={average.average}
              label={normalizeMojibake(candidate.presidential_candidate)}
              tone="candidate"
              colorClass={color}
              hint={leanHint(average.average)}
            />
          ))}
        </div>

        <div className="mt-4 flex items-start justify-between gap-3 text-[0.6rem] font-black uppercase tracking-[0.2em]">
          <span className="min-w-0 max-w-[45%] truncate text-coffee">◀ {negativePole}</span>
          <span className="min-w-0 max-w-[45%] truncate text-right text-jade">{positivePole} ▶</span>
        </div>
      </div>

      <div className="mt-7 flex flex-wrap gap-x-5 gap-y-3 border-t border-coffee/10 pt-5">
        {withStance.map(({ candidate, average, color }) => (
          <span key={candidate.id} className="flex items-center gap-2 text-sm font-black text-ink">
            <span className={`size-3 rounded-full ${color}`} aria-hidden="true" />
            <span className="max-w-[12rem] truncate">
              {normalizeMojibake(candidate.presidential_candidate)}
            </span>
            <span className="text-muted">{formatAverage(average.average)}</span>
          </span>
        ))}
      </div>

      {withoutStance.length > 0 && (
        <p className="mt-4 text-xs font-semibold leading-5 text-muted">
          Sin postura registrada en esta categoría:{' '}
          {withoutStance
            .map((entry) => normalizeMojibake(entry.candidate.presidential_candidate))
            .join(', ')}
          .
        </p>
      )}
    </section>
  )
}
