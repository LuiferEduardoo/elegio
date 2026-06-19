/**
 * Scrolls the window to the top with a gentle, eased animation over `duration`
 * ms (slower than the browser's native `behavior: 'smooth'`). Honors the user's
 * reduced-motion preference by jumping instantly.
 */
export function smoothScrollToTop(duration = 900): void {
  const start = window.scrollY
  if (start <= 0) return

  const prefersReducedMotion = window.matchMedia?.(
    '(prefers-reduced-motion: reduce)',
  ).matches
  if (prefersReducedMotion) {
    window.scrollTo(0, 0)
    return
  }

  const startTime = performance.now()
  const easeInOutQuad = (t: number) =>
    t < 0.5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2

  function step(now: number) {
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1)
    window.scrollTo(0, start * (1 - easeInOutQuad(progress)))
    if (progress < 1) requestAnimationFrame(step)
  }

  requestAnimationFrame(step)
}
