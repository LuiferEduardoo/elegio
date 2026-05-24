import type { CategoryAverage } from '../types'
import { CategorySpectrumBar } from './CategorySpectrumBar'

type CategoryAveragesSectionProps = {
  categories: CategoryAverage[]
}

export function CategoryAveragesSection({ categories }: CategoryAveragesSectionProps) {
  const sorted = [...categories].sort((a, b) => b.weight - a.weight)

  return (
    <section>
      <div className="mb-8 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">Posiciones por categoría</p>
          <h2 className="mt-2 font-display text-3xl tracking-[-0.03em] text-ink">
            Dónde se para el candidato.
          </h2>
        </div>
        <p className="max-w-md text-sm leading-6 text-muted">
          Cada barra muestra el promedio de sus propuestas entre dos polos. Cuanto más cerca de un extremo, más marcada la postura.
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        {sorted.map((category) => (
          <CategorySpectrumBar category={category} key={category.category_id} />
        ))}
      </div>
    </section>
  )
}
