import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import { normalizeMojibake } from '../../../utils/text'
import type { Candidate } from '../../candidates/types'
import { MAX_SELECTED_CANDIDATES, type CategoryOption } from '../types'

type StickySelectionBarProps = {
  selectedCandidates: Candidate[]
  selectedCategory: CategoryOption | undefined
  onToggle: (candidateId: number) => void
  onClear: () => void
}

export function StickySelectionBar({
  selectedCandidates,
  selectedCategory,
  onToggle,
  onClear,
}: StickySelectionBarProps) {
  if (selectedCandidates.length === 0) return null

  return (
    <div className="sticky top-20 z-20 -mx-6 mb-2 border-b border-coffee/10 bg-surface/90 px-6 py-3 backdrop-blur sm:-mx-10 sm:px-10 lg:-mx-16 lg:px-16">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-3">
        <span className="rounded-full bg-coffee/10 px-2.5 py-1 text-[0.65rem] font-black uppercase tracking-[0.2em] text-coffee">
          {selectedCandidates.length}/{MAX_SELECTED_CANDIDATES}
        </span>

        <div className="flex flex-wrap gap-2">
          {selectedCandidates.map((candidate) => {
            const name = normalizeMojibake(candidate.presidential_candidate)
            return (
              <button
                key={candidate.id}
                type="button"
                onClick={() => onToggle(candidate.id)}
                title={`Quitar ${name}`}
                aria-label={`Quitar ${name}`}
                className="group flex items-center gap-2 rounded-full border border-coffee/15 bg-white py-1 pl-1 pr-3 transition hover:border-clay/40 hover:bg-clay/5"
              >
                <img
                  src={candidate.photo_president || fallbackCandidateImage}
                  alt=""
                  className="size-7 rounded-full object-cover object-top"
                  onError={(event) => {
                    event.currentTarget.onerror = null
                    event.currentTarget.src = fallbackCandidateImage
                  }}
                />
                <span className="max-w-[8rem] truncate text-xs font-black text-ink">{name}</span>
                <span className="text-sm font-black leading-none text-muted group-hover:text-clay">
                  ×
                </span>
              </button>
            )
          })}
        </div>

        <div className="ml-auto flex items-center gap-3">
          <span
            className={`rounded-full px-3 py-1 text-xs font-black ${
              selectedCategory ? 'bg-ink text-white' : 'bg-coffee/10 text-muted'
            }`}
          >
            {selectedCategory ? selectedCategory.name : 'Elegí categoría'}
          </span>
          <button
            type="button"
            onClick={onClear}
            className="text-xs font-black uppercase tracking-[0.14em] text-clay underline-offset-4 hover:underline"
          >
            Limpiar
          </button>
        </div>
      </div>
    </div>
  )
}
