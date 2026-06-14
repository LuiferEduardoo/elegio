import { useEffect, useRef } from 'react'
import { useLocation } from 'react-router'

import { trackEvent } from '../api/trackEvent'

const SCROLL_MILESTONES = [25, 50, 75, 100]
const INTERACTIVE_SELECTOR = 'a, button, [role="button"], input, [data-track]'

function truncate(value: string | null | undefined, max: number): string | undefined {
  if (!value) return undefined
  const trimmed = value.replace(/\s+/g, ' ').trim()
  if (!trimmed) return undefined
  return trimmed.length > max ? trimmed.slice(0, max) : trimmed
}

function pageInfo() {
  return {
    page_url: window.location.href,
    page_path: truncate(window.location.pathname, 500),
    page_title: truncate(document.title, 255),
  }
}

export function AnalyticsTracker() {
  const { pathname } = useLocation()
  const reachedMilestones = useRef<Set<number>>(new Set())

  // Page view on every route change (including the first render).
  useEffect(() => {
    reachedMilestones.current = new Set()
    trackEvent({ event_type: 'page_view', ...pageInfo() })
  }, [pathname])

  // Clicks on interactive elements.
  useEffect(() => {
    const handleClick = (event: MouseEvent) => {
      const target = event.target as Element | null
      const element = target?.closest<HTMLElement>(INTERACTIVE_SELECTOR)
      if (!element) return

      trackEvent({
        event_type: 'click',
        event_name: truncate(element.getAttribute('data-track'), 100),
        element_tag: truncate(element.tagName.toLowerCase(), 50),
        element_id: truncate(element.id, 255),
        element_class: truncate(element.className, 255),
        element_text: truncate(
          element.textContent ?? element.getAttribute('aria-label'),
          500,
        ),
        ...pageInfo(),
      })
    }

    document.addEventListener('click', handleClick, { capture: true })
    return () => document.removeEventListener('click', handleClick, { capture: true })
  }, [])

  // Scroll depth milestones (each reported once per page).
  useEffect(() => {
    let ticking = false

    const measure = () => {
      ticking = false
      const scrollable = document.documentElement.scrollHeight - window.innerHeight
      if (scrollable <= 0) return
      const depth = Math.min(100, Math.round((window.scrollY / scrollable) * 100))

      for (const milestone of SCROLL_MILESTONES) {
        if (depth >= milestone && !reachedMilestones.current.has(milestone)) {
          reachedMilestones.current.add(milestone)
          trackEvent({
            event_type: 'scroll',
            event_name: `depth_${milestone}`,
            scroll_depth: milestone,
            ...pageInfo(),
          })
        }
      }
    }

    const handleScroll = () => {
      if (ticking) return
      ticking = true
      window.requestAnimationFrame(measure)
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return null
}
