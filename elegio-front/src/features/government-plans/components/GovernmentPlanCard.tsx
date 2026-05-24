import type { GovernmentPlan } from '../types'
import { formatPublishedDate, getHostname, isPdfUrl } from '../utils/planMetadata'

type GovernmentPlanCardProps = {
  plan: GovernmentPlan
}

export function GovernmentPlanCard({ plan }: GovernmentPlanCardProps) {
  const isPdf = isPdfUrl(plan.url)
  const host = getHostname(plan.url)

  return (
    <article className="flex flex-col gap-5 rounded-3xl border border-coffee/10 bg-white p-6 shadow-sm shadow-coffee/5 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-start gap-4">
        <span
          className="flex size-12 shrink-0 items-center justify-center rounded-2xl bg-jade/10 text-sm font-black uppercase tracking-[0.2em] text-jade"
          aria-hidden="true"
        >
          {isPdf ? 'PDF' : 'WEB'}
        </span>
        <div>
          <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">
            Documento oficial
          </p>
          <p className="mt-1 text-base font-bold text-ink">{host}</p>
          <p className="mt-1 text-sm text-muted">
            Publicado el {formatPublishedDate(plan.created_at)}
          </p>
        </div>
      </div>

      <a
        href={plan.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center justify-center gap-2 rounded-full bg-coffee px-5 py-3 text-xs font-black uppercase tracking-[0.25em] text-white transition hover:bg-jade focus:outline-none focus:ring-2 focus:ring-jade/40"
      >
        {isPdf ? 'Abrir PDF' : 'Ver documento'} ↗
      </a>
    </article>
  )
}
