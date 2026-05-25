import type { Candidate } from '../candidates/types'
import type { Proposal } from '../proposals/types'

export type CoverageTone = 'empty' | 'thin' | 'steady' | 'deep'

export type CoverageMetric = {
  candidate: Candidate
  count: number
  percentage: number
  tone: CoverageTone
}

export type CoverageCopy = {
  label: string
  summary: string
  detail: string
  badgeClass: string
  lightBadgeClass: string
  barClass: string
  lightBarClass: string
}

export function buildCoverageMetrics(
  candidates: Candidate[],
  proposalsByCandidate: Record<number, Proposal[]>,
): CoverageMetric[] {
  const proposalCounts = candidates.map(
    (candidate) => proposalsByCandidate[candidate.id]?.length ?? 0,
  )
  const maxCount = Math.max(...proposalCounts, 0)

  return candidates.map((candidate, index) => {
    const count = proposalCounts[index]
    const percentage = maxCount === 0 ? 0 : Math.max(8, Math.round((count / maxCount) * 100))

    return {
      candidate,
      count,
      percentage,
      tone: getCoverageTone(count, percentage),
    }
  })
}

export function getCoverageTone(count: number, percentage: number): CoverageTone {
  if (count === 0) return 'empty'
  if (count <= 2 || percentage < 35) return 'thin'
  if (count <= 5 || percentage < 75) return 'steady'
  return 'deep'
}

export function getCoverageCopy(tone: CoverageTone): CoverageCopy {
  const copies: Record<CoverageTone, CoverageCopy> = {
    empty: {
      label: 'Sin cobertura',
      summary: 'No hay material comparable.',
      detail:
        'No hay propuestas encontradas: conviene leer esto como ausencia de evidencia programática.',
      badgeClass: 'bg-clay/25 text-clay',
      lightBadgeClass: 'bg-clay/10 text-clay',
      barClass: 'bg-clay',
      lightBarClass: 'bg-clay',
    },
    thin: {
      label: 'Cobertura baja',
      summary: 'Pocas señales; compará con cuidado.',
      detail:
        'Hay propuestas, pero el volumen es bajo frente al resto. Sirve como pista, no como mapa completo.',
      badgeClass: 'bg-sand/20 text-sand',
      lightBadgeClass: 'bg-sand/30 text-clay',
      barClass: 'bg-sand',
      lightBarClass: 'bg-clay',
    },
    steady: {
      label: 'Cobertura media',
      summary: 'Hay base suficiente para contrastar.',
      detail:
        'La categoría tiene contenido razonable: podés comparar prioridades y enfoque con bastante confianza.',
      badgeClass: 'bg-white/15 text-white',
      lightBadgeClass: 'bg-coffee/10 text-ink',
      barClass: 'bg-white',
      lightBarClass: 'bg-ink',
    },
    deep: {
      label: 'Cobertura alta',
      summary: 'Mucho material programático.',
      detail:
        'Acá hay densidad: no mires solo cantidad, buscá consistencia entre las propuestas.',
      badgeClass: 'bg-jade/25 text-jade',
      lightBadgeClass: 'bg-jade/10 text-jade',
      barClass: 'bg-jade',
      lightBarClass: 'bg-jade',
    },
  }

  return copies[tone]
}
