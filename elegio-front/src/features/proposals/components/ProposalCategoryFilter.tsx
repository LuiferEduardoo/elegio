type ProposalCategoryFilterProps = {
  categories: Array<{ id: number; name: string }>
  selectedCategoryId: number | undefined
  onSelectCategory: (categoryId: number | undefined) => void
}

export function ProposalCategoryFilter({
  categories,
  selectedCategoryId,
  onSelectCategory,
}: ProposalCategoryFilterProps) {
  return (
    <section className="mt-4 rounded-[2rem] border border-coffee/10 bg-white/70 p-4 shadow-sm shadow-coffee/5 sm:p-5">
      <div className="mb-3 flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.25em] text-clay">
            Categoría
          </p>
          <h2 className="font-display text-xl tracking-[-0.03em] text-ink">
            Afiná el tema sin perder contexto.
          </h2>
        </div>
        {selectedCategoryId !== undefined && (
          <button
            type="button"
            onClick={() => onSelectCategory(undefined)}
            className="w-fit rounded-full border border-coffee/15 bg-white px-3 py-1.5 text-xs font-black uppercase tracking-[0.14em] text-clay transition hover:border-clay/40 hover:bg-clay/5"
          >
            Quitar categoría
          </button>
        )}
      </div>

      <div className="flex gap-2 overflow-x-auto pb-1 sm:flex-wrap sm:overflow-visible">
        <button
          type="button"
          onClick={() => onSelectCategory(undefined)}
          className="shrink-0 rounded-full border border-coffee/15 bg-white px-4 py-2 text-sm font-black text-muted transition hover:border-clay/40 hover:bg-clay/5 hover:text-clay"
        >
          Sin filtro
        </button>

        {categories.map((category) => {
          const isSelected = category.id === selectedCategoryId

          return (
            <button
              key={category.id}
              type="button"
              onClick={() => onSelectCategory(category.id)}
              className={`shrink-0 rounded-full px-4 py-2 text-sm font-black transition ${
                isSelected
                  ? 'bg-clay text-white shadow-lg shadow-clay/20'
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
