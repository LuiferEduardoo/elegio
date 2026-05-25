import { normalizeMojibake } from '../../../utils/text'
import { getCoverageCopy, type CoverageMetric } from '../coverage'

type CoverageSummaryProps = {
  metrics: CoverageMetric[]
}

export function CoverageSummary({ metrics }: CoverageSummaryProps) {
  const richestMetric = metrics.reduce<CoverageMetric | null>((current, metric) => {
    if (!current || metric.count > current.count) return metric
    return current
  }, null)
  const hasImbalance = metrics.some(
    (metric) => richestMetric && richestMetric.count - metric.count >= 4,
  )

  return (
    <aside className="mt-6 overflow-hidden rounded-[2rem] border border-ink/10 bg-ink text-white shadow-xl shadow-ink/10">
      <div className="grid gap-0 lg:grid-cols-[minmax(0,0.95fr)_minmax(0,1.4fr)]">
        <div className="relative p-5 sm:p-6">
          <div className="absolute -left-16 -top-20 h-44 w-44 rounded-full bg-jade/20 blur-3xl" />
          <p className="relative text-xs font-black uppercase tracking-[0.25em] text-white/50">
            Mapa de cobertura
          </p>
          <h3 className="relative mt-2 font-display text-3xl leading-none tracking-[-0.05em]">
            No solo importa qué proponen, también cuánto cubren.
          </h3>
          <p className="relative mt-4 text-sm leading-6 text-white/65">
            Esta lectura deja visible si una candidatura trae músculo programático o si apenas tiene
            presencia en la categoría elegida.
          </p>

          <p className="relative mt-5 rounded-2xl border border-white/10 bg-white/10 p-4 text-sm font-bold leading-6 text-white/75">
            {hasImbalance
              ? 'Hay una brecha clara de cobertura: compará contenido, pero también el nivel de detalle.'
              : 'La cobertura está relativamente pareja: buen terreno para comparar propuesta contra propuesta.'}
          </p>
        </div>

        <div className="space-y-3 border-t border-white/10 p-5 sm:p-6 lg:border-l lg:border-t-0">
          {metrics.map((metric) => (
            <CoverageRow key={metric.candidate.id} metric={metric} />
          ))}
        </div>
      </div>
    </aside>
  )
}

function CoverageRow({ metric }: { metric: CoverageMetric }) {
  const name = normalizeMojibake(metric.candidate.presidential_candidate)
  const copy = getCoverageCopy(metric.tone)

  return (
    <div className="rounded-2xl bg-white/[0.07] p-4 ring-1 ring-white/10">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="truncate text-sm font-black text-white">{name}</p>
          <p className="mt-1 text-xs font-semibold text-white/55">{copy.summary}</p>
        </div>
        <span className={`shrink-0 rounded-full px-3 py-1 text-xs font-black ${copy.badgeClass}`}>
          {copy.label}
        </span>
      </div>

      <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/10">
        <div className={`h-full rounded-full ${copy.barClass}`} style={{ width: `${metric.percentage}%` }} />
      </div>
      <p className="mt-2 text-[0.68rem] font-black uppercase tracking-[0.18em] text-white/40">
        {metric.count} propuesta{metric.count === 1 ? '' : 's'} · {metric.percentage}% de la mayor
        cobertura
      </p>
    </div>
  )
}
