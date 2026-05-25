import type { CategoryOption } from '../types'

type CategoryVsSelectorProps = {
  categories: CategoryOption[]
  selectedCategoryId: number | undefined
  onSelectCategory: (categoryId: number) => void
}

export function CategoryVsSelector({
  categories,
  selectedCategoryId,
  onSelectCategory,
}: CategoryVsSelectorProps) {
  return (
    <section className="mt-8 rounded-[2rem] border border-coffee/10 bg-white p-5 shadow-sm shadow-coffee/5 sm:p-6">
      <p className="text-xs font-black uppercase tracking-[0.25em] text-clay">Paso 2</p>
      <h2 className="mt-1 font-display text-3xl tracking-[-0.04em] text-ink">
        Elegí una categoría del plan de gobierno.
      </h2>

      <div className="mt-5 flex gap-2 overflow-x-auto pb-2 sm:flex-wrap sm:overflow-visible">
        {categories.map((category) => {
          const isSelected = category.id === selectedCategoryId
          return (
            <button
              key={category.id}
              type="button"
              onClick={() => onSelectCategory(category.id)}
              className={`shrink-0 rounded-full px-4 py-2 text-sm font-black transition ${
                isSelected
                  ? 'bg-ink text-white shadow-lg shadow-ink/10'
                  : 'border border-coffee/15 bg-surface text-ink hover:border-clay/40 hover:bg-white'
              }`}
            >
              {category.name}
            </button>
          )
        })}
      </div>
    </section>
  )
}
