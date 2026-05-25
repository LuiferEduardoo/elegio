type ProposalPaginationProps = {
  currentPage: number
  pageSize: number
  totalItems: number
  onPageChange: (page: number) => void
}

export function ProposalPagination({
  currentPage,
  pageSize,
  totalItems,
  onPageChange,
}: ProposalPaginationProps) {
  const totalPages = Math.ceil(totalItems / pageSize)
  if (totalPages <= 1) return null

  return (
    <nav
      className="mt-8 flex flex-col gap-3 rounded-3xl border border-coffee/10 bg-white/75 p-3 shadow-sm shadow-coffee/5 sm:flex-row sm:items-center sm:justify-between"
      aria-label="Paginación de propuestas"
    >
      <p className="text-center text-sm font-bold text-muted sm:text-left">
        Página {currentPage} de {totalPages}
      </p>

      <div className="grid grid-cols-2 gap-2 sm:flex sm:items-center">
        <button
          type="button"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="rounded-full border border-coffee/15 bg-surface px-4 py-2 text-sm font-black text-ink transition hover:border-clay/40 hover:bg-white disabled:cursor-not-allowed disabled:opacity-40"
        >
          Anterior
        </button>
        <button
          type="button"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="rounded-full bg-ink px-4 py-2 text-sm font-black text-white transition hover:bg-clay disabled:cursor-not-allowed disabled:opacity-40"
        >
          Siguiente
        </button>
      </div>
    </nav>
  )
}
