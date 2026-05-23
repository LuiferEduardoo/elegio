import { formatAxisValue } from '../utils/candidateInsights'
import type { CategoryAverage } from '../types'

type CandidateMetricProps = {
  category: CategoryAverage
}

export function CandidateMetric({ category }: CandidateMetricProps) {
  return (
    <li className="rounded-2xl border border-coffee/10 bg-white p-3 shadow-sm shadow-coffee/5">
      <div className="flex items-center justify-between gap-3 text-sm font-bold text-ink">
        <span>{category.category_name}</span>
        <span className="text-clay">{formatAxisValue(category.average)}</span>
      </div>
      <div className="mt-2 h-2 overflow-hidden rounded-full bg-coffee/10">
        <div
          className="h-full rounded-full bg-gradient-to-r from-clay via-gold to-jade"
          style={{ width: `${Math.min(Math.abs(category.average) * 100, 100)}%` }}
        />
      </div>
      <p className="mt-2 text-xs text-muted">{category.proposals_count} propuestas</p>
    </li>
  )
}
