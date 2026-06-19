import { useEffect, useState } from 'react'
import { normalizeMojibake } from '../../utils/text'
import type { AffinityResponse } from '../../types'

type CategoryPostureChartProps = {
  categories: AffinityResponse['user_averages']
}

/**
 * Diverging bar chart of the visitor's average posture per category. Values are
 * clamped to [-1, 1]: bars grow left (en contra) or right (a favor) from a
 * central axis, so the user can read where they leaned topic by topic.
 */
export function CategoryPostureChart({ categories }: CategoryPostureChartProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    const frame = requestAnimationFrame(() => setMounted(true))
    return () => cancelAnimationFrame(frame)
  }, [])

  if (categories.length === 0) return null

  const sorted = [...categories].sort((a, b) => b.average - a.average)

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between text-[0.65rem] font-black uppercase tracking-[0.2em] text-muted">
        <span>En contra</span>
        <span>Neutral</span>
        <span>A favor</span>
      </div>
      <ul className="flex flex-col gap-2.5">
        {sorted.map((category, index) => {
          const value = Math.max(-1, Math.min(1, category.average))
          const half = Math.abs(value) * 50
          const positive = value >= 0

          return (
            <li
              key={category.category_id}
              className="flex flex-col gap-1.5 sm:flex-row sm:items-center sm:gap-3"
            >
              <span className="text-xs font-bold text-ink sm:w-36 sm:shrink-0 sm:truncate sm:text-right">
                {normalizeMojibake(category.category_name)}
              </span>
              <div className="relative h-6 w-full rounded-lg bg-coffee/5 sm:flex-1">
                <div className="absolute inset-y-0 left-1/2 w-px bg-coffee/20" />
                <div
                  className={`absolute inset-y-1 rounded-md ${
                    positive ? 'bg-jade/80' : 'bg-clay/80'
                  }`}
                  style={{
                    left: positive ? '50%' : `${50 - half}%`,
                    width: mounted ? `${half}%` : '0%',
                    transition: 'width 0.8s cubic-bezier(0.22, 1, 0.36, 1), left 0.8s cubic-bezier(0.22, 1, 0.36, 1)',
                    transitionDelay: `${index * 60}ms`,
                  }}
                />
              </div>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
