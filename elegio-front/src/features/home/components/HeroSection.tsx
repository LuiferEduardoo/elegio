import { useEffect, useState } from 'react'

type HeroSectionProps = {
  candidateCount: number
}

const SECOND_ROUND_DATE = new Date('2026-06-21T08:00:00-05:00')

type TimeLeft = { days: number; hours: number; minutes: number; seconds: number }

function calculateTimeLeft(): TimeLeft | null {
  const diff = SECOND_ROUND_DATE.getTime() - Date.now()
  if (diff <= 0) return null
  return {
    days: Math.floor(diff / (1000 * 60 * 60 * 24)),
    hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((diff / (1000 * 60)) % 60),
    seconds: Math.floor((diff / 1000) % 60),
  }
}

export function HeroSection({ candidateCount }: HeroSectionProps) {
  const [timeLeft, setTimeLeft] = useState<TimeLeft | null>(calculateTimeLeft)

  useEffect(() => {
    const id = setInterval(() => setTimeLeft(calculateTimeLeft()), 1000)
    return () => clearInterval(id)
  }, [])

  return (
    <section className="relative isolate overflow-hidden px-6 py-16 sm:px-10 lg:px-16">
      <div className="absolute inset-x-6 bottom-0 -z-10 h-px bg-gradient-to-r from-transparent via-coffee/15 to-transparent" />

      <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[1.1fr_.9fr] lg:items-center">
        <div className="max-w-3xl">
          <p className="mb-5 inline-flex rounded-full border border-coffee/10 bg-white px-4 py-2 text-sm font-semibold text-coffee shadow-sm shadow-coffee/5">
            Segunda vuelta presidencial · Colombia 2026
          </p>
          <h1 className="font-display text-5xl leading-[.95] tracking-[-0.05em] text-ink sm:text-7xl">
            Elegí con evidencia, no con ruido.
          </h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-muted">
            Elegio reúne candidatos, propuestas, planes de gobierno y un test de
            afinidad para ayudarte a comparar posturas antes de votar.
          </p>
        </div>

        <div className="grid gap-5">

          <div className="rounded-[2rem] border border-coffee/10 bg-white/90 p-6 shadow-2xl shadow-coffee/10 backdrop-blur">
            <p className="text-sm font-black uppercase tracking-[0.35em] text-jade">Mapa electoral</p>
            <strong className="mt-4 block text-6xl font-black text-coffee">{candidateCount || '—'}</strong>
            <p className="mt-3 text-balance text-lg text-muted">
              candidaturas en segunda vuelta para comparar con sus tendencias por categoría.
            </p>
          </div>
          <div className="rounded-[2rem] border border-coffee/10 bg-white/90 p-6 shadow-2xl shadow-coffee/10 backdrop-blur">
            {timeLeft ? (
              <>
                <p className="text-sm font-black uppercase tracking-[0.35em] text-clay">Cuenta regresiva</p>
                <div className="mt-4 grid grid-cols-4 gap-2 sm:gap-3">
                  <TimeBlock value={timeLeft.days} label="Días" />
                  <TimeBlock value={timeLeft.hours} label="Horas" />
                  <TimeBlock value={timeLeft.minutes} label="Min" />
                  <TimeBlock value={timeLeft.seconds} label="Seg" />
                </div>
                <p className="mt-4 text-balance text-base text-muted">
                  Para la segunda vuelta.
                </p>
              </>
            ) : (
              <>
                <p className="text-sm font-black uppercase tracking-[0.35em] text-clay">Hoy es el día</p>
                <p className="mt-4 font-display text-2xl leading-tight tracking-[-0.02em] text-ink">
                  Hoy es la segunda vuelta, recuerda que las urnas cierran a las 4 p.m.
                </p>
              </>
            )}
          </div>
        </div>

      </div>
    </section>
  )
}

function TimeBlock({ value, label }: { value: number; label: string }) {
  return (
    <div className="rounded-2xl border border-coffee/10 bg-coffee/5 p-3 text-center">
      <strong className="block font-display text-3xl font-black tabular-nums text-coffee sm:text-4xl">
        {value.toString().padStart(2, '0')}
      </strong>
      <span className="mt-1 block text-[0.65rem] font-bold uppercase tracking-[0.2em] text-muted">
        {label}
      </span>
    </div>
  )
}
