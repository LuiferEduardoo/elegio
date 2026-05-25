export type SpectrumMarkerTone = 'candidate' | 'user'

type SpectrumMarkerProps = {
  /** Horizontal position along the track, 0–100. */
  position: number
  /** Who the marker belongs to, e.g. "Tú" / "Candidato". */
  label: string
  /** Raw average value, -1..1. */
  value: number
  tone: SpectrumMarkerTone
  /** Optional human-readable lean, e.g. the pole the value tends toward. */
  hint?: string
  /** Overrides the dot color (e.g. when plotting several candidates at once). */
  colorClass?: string
}

const toneDot: Record<SpectrumMarkerTone, string> = {
  candidate: 'bg-clay',
  user: 'bg-ink',
}

const formatAverage = (value: number) => `${value > 0 ? '+' : ''}${value.toFixed(2)}`

export function SpectrumMarker({
  position,
  label,
  value,
  tone,
  hint,
  colorClass,
}: SpectrumMarkerProps) {
  // Keep the tooltip inside the track: align it inward near the edges so it
  // never overflows the bar (and never the viewport).
  const translatePct = position <= 15 ? 0 : position >= 85 ? -100 : -50
  const description = `${label}: ${formatAverage(value)}${hint ? ` · ${hint}` : ''}`
  const dot = colorClass ?? toneDot[tone]

  return (
    <div
      className="group/marker absolute top-1/2 z-20 -translate-y-1/2 transition-[left] duration-500 ease-out"
      style={{ left: `${position}%` }}
    >
      <button
        type="button"
        aria-label={description}
        className={`block size-5 -translate-x-1/2 rounded-full border-2 border-white shadow-md shadow-coffee/30 outline-none transition-transform duration-200 hover:scale-125 focus-visible:scale-125 focus-visible:ring-2 focus-visible:ring-ink/40 ${dot}`}
      />
      <div
        role="tooltip"
        style={{ transform: `translateX(${translatePct}%)` }}
        className="pointer-events-none absolute bottom-[calc(100%+0.6rem)] left-0 z-30 hidden w-max max-w-[12rem] rounded-2xl bg-ink px-3 py-2 shadow-xl shadow-coffee/30 group-hover/marker:block group-focus-within/marker:block"
      >
        <p className="flex items-center gap-1.5 text-[0.55rem] font-black uppercase tracking-[0.2em] text-white/55">
          <span className={`size-2 rounded-full ${dot}`} aria-hidden="true" />
          {label}
        </p>
        <p className="mt-1 text-base font-black leading-none text-white">{formatAverage(value)}</p>
        {hint && (
          <p className="mt-1.5 text-[0.65rem] font-semibold leading-snug text-white/75">{hint}</p>
        )}
      </div>
    </div>
  )
}
