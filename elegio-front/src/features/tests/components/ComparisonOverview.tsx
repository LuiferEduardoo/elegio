import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import { formatPercent } from '../utils/text'

type ComparisonOverviewProps = {
  affinity: number
  categoriesCompared: number
  distance: number
  name: string
  photo: string | null
  politicalGroup: string
}

export function ComparisonOverview({
  affinity,
  categoriesCompared,
  distance,
  name,
  photo,
  politicalGroup,
}: ComparisonOverviewProps) {
  const affinityPercent = formatPercent(affinity)
  const closeness = affinity >= 0.85 ? 'Muy cerca' : affinity >= 0.7 ? 'Cerca' : 'Distante'

  return (
    <div className="mt-8 overflow-hidden rounded-[2.5rem] border border-ink/10 bg-white shadow-2xl shadow-coffee/10">
      <div className="grid gap-0 lg:grid-cols-[minmax(0,1fr)_minmax(20rem,0.65fr)]">
        <div className="relative min-w-0 p-5 sm:p-7">
          <div className="absolute right-4 top-4 hidden rounded-full bg-surface px-4 py-2 text-xs font-black uppercase tracking-[0.18em] text-muted sm:block">
            {closeness}
          </div>
          <div className="flex min-w-0 flex-col gap-5 sm:flex-row sm:items-center">
            <img
              src={photo || fallbackCandidateImage}
              alt=""
              className="h-28 w-24 rounded-[1.75rem] object-cover object-top shadow-xl shadow-coffee/15"
              loading="lazy"
              onError={(event) => {
                event.currentTarget.onerror = null
                event.currentTarget.src = fallbackCandidateImage
              }}
            />
            <div className="min-w-0">
              <p className="text-[0.65rem] font-black uppercase tracking-[0.25em] text-clay">
                Comparando con
              </p>
              <h4 className="mt-2 text-3xl font-black leading-none tracking-[-0.04em] text-ink">
                {name}
              </h4>
              <p className="mt-2 text-sm font-semibold text-muted">{politicalGroup}</p>
            </div>
          </div>

          <p className="mt-5 max-w-2xl text-sm font-semibold leading-6 text-muted">
            Esta lectura cruza tu mapa de respuestas contra el promedio del candidato por categoría.
            Sin barras decorativas: foco en señales claras y comparación real.
          </p>
        </div>

        <div className="grid gap-3 border-t border-coffee/10 bg-surface p-5 sm:grid-cols-3 sm:p-7 lg:grid-cols-1 lg:border-l lg:border-t-0">
          <Metric label="Afinidad" value={affinityPercent} accent helper="Coincidencia global" />
          <Metric label="Distancia" value={distance.toFixed(2)} helper="Menor es más cerca" />
          <Metric label="Categorías" value={String(categoriesCompared)} helper="Ejes comparados" />
        </div>
      </div>
    </div>
  )
}

type MetricProps = {
  label: string
  value: string
  accent?: boolean
  helper: string
}

function Metric({ label, value, accent = false, helper }: MetricProps) {
  return (
    <div className="rounded-[1.5rem] border border-coffee/10 bg-white p-4 shadow-sm shadow-coffee/5">
      <p className="text-[0.6rem] font-black uppercase tracking-[0.2em] text-muted">{label}</p>
      <p className={`mt-1 text-3xl font-black tracking-[-0.04em] ${accent ? 'text-jade' : 'text-ink'}`}>
        {value}
      </p>
      <p className="mt-1 text-xs font-semibold text-muted">{helper}</p>
    </div>
  )
}
