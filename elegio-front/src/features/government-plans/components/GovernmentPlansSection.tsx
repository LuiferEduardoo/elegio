import type { GovernmentPlan } from '../types'
import { GovernmentPlanCard } from './GovernmentPlanCard'

type GovernmentPlansSectionProps = {
  plans: GovernmentPlan[]
  isLoading: boolean
  error: string | null
}

export function GovernmentPlansSection({ plans, isLoading, error }: GovernmentPlansSectionProps) {
  return (
    <section className="rounded-[2rem] border border-coffee/10 bg-white/70 p-8 shadow-sm shadow-coffee/5 backdrop-blur">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">Plan de gobierno</p>
          <h2 className="mt-2 font-display text-3xl tracking-[-0.03em] text-ink">
            La propuesta oficial.
          </h2>
        </div>
        <p className="max-w-md text-sm leading-6 text-muted">
          Acá podés consultar el documento original publicado por la campaña.
        </p>
      </div>

      {isLoading && (
        <p className="rounded-3xl border border-coffee/10 bg-surface/60 p-6 text-sm text-muted">
          Cargando plan de gobierno…
        </p>
      )}

      {!isLoading && error && (
        <p className="rounded-3xl bg-clay p-6 text-sm font-bold text-white">{error}</p>
      )}

      {!isLoading && !error && plans.length === 0 && (
        <p className="rounded-3xl border border-dashed border-coffee/20 bg-surface/40 p-6 text-sm text-muted">
          Este candidato todavía no tiene un plan de gobierno publicado.
        </p>
      )}

      {!isLoading && !error && plans.length > 0 && (
        <div className="grid gap-4">
          {plans.map((plan) => (
            <GovernmentPlanCard key={plan.id} plan={plan} />
          ))}
        </div>
      )}
    </section>
  )
}
