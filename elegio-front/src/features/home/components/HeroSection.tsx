type HeroSectionProps = {
  candidateCount: number
}

export function HeroSection({ candidateCount }: HeroSectionProps) {
  return (
    <section className="relative isolate overflow-hidden px-6 py-16 sm:px-10 lg:px-16">
      <div className="absolute inset-x-6 bottom-0 -z-10 h-px bg-gradient-to-r from-transparent via-coffee/15 to-transparent" />

      <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[1.1fr_.9fr] lg:items-end">
        <div className="max-w-3xl">
          <p className="mb-5 inline-flex rounded-full border border-coffee/10 bg-white px-4 py-2 text-sm font-semibold text-coffee shadow-sm shadow-coffee/5">
            Elecciones presidenciales Colombia 2026
          </p>
          <h1 className="font-display text-5xl leading-[.95] tracking-[-0.05em] text-ink sm:text-7xl">
            Elegí con evidencia, no con ruido.
          </h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-muted">
            Elegio reúne candidatos, propuestas, planes de gobierno y un test de
            afinidad para ayudarte a comparar posturas antes de votar.
          </p>
        </div>

        <div className="rounded-[2rem] border border-coffee/10 bg-white/90 p-6 shadow-2xl shadow-coffee/10 backdrop-blur">
          <p className="text-sm font-black uppercase tracking-[0.35em] text-jade">Mapa electoral</p>
          <strong className="mt-4 block text-6xl font-black text-coffee">{candidateCount || '—'}</strong>
          <p className="mt-3 text-balance text-lg text-muted">
            candidaturas listas para explorar con sus tendencias por categoría.
          </p>
        </div>
      </div>
    </section>
  )
}
