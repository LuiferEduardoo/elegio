import type { CategoryOption } from '../types'

type ElectoralVsHeroProps = {
  selectedCategory: CategoryOption | undefined
  selectedCount: number
}

export function ElectoralVsHero({ selectedCategory, selectedCount }: ElectoralVsHeroProps) {
  return (
    <header className="overflow-hidden rounded-[2.5rem] bg-ink p-6 text-white shadow-2xl shadow-coffee/20 sm:p-10 lg:p-12">
      <p className="text-xs font-black uppercase tracking-[0.3em] text-white/60">
        VS Electoral
      </p>
      <div className="mt-4 grid gap-6 lg:grid-cols-[minmax(0,1fr)_24rem] lg:items-end">
        <div>
          <h1 className="font-display text-5xl leading-[0.95] tracking-[-0.05em] sm:text-6xl">
            Compará propuestas cara a cara.
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-white/70">
            Elegí hasta tres candidaturas y una categoría del plan de gobierno. Te
            mostramos sus propuestas lado a lado para que compares con criterio, no con ruido.
          </p>
        </div>

        <div className="rounded-[2rem] border border-white/10 bg-white/10 p-5 backdrop-blur">
          <p className="text-xs font-black uppercase tracking-[0.22em] text-white/60">
            Estado de comparación
          </p>
          <div className="mt-4 grid grid-cols-2 gap-3">
            <StatusPill label="Candidatos" value={`${selectedCount}/3`} />
            <StatusPill label="Categoría" value={selectedCategory ? 'Lista' : 'Pendiente'} />
          </div>
        </div>
      </div>
    </header>
  )
}

function StatusPill({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-white/10 p-4">
      <p className="text-[0.6rem] font-black uppercase tracking-[0.2em] text-white/50">
        {label}
      </p>
      <p className="mt-1 text-2xl font-black text-white">{value}</p>
    </div>
  )
}
