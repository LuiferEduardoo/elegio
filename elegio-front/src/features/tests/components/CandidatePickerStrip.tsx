import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import { normalizeMojibake } from '../../../utils/text'
import type { CandidateAffinity } from '../types'
import { formatPercent } from '../utils/text'

type CandidatePickerStripProps = {
  candidates: CandidateAffinity[]
  selectedId: number | undefined
  onSelect: (candidateId: number) => void
}

export function CandidatePickerStrip({ candidates, selectedId, onSelect }: CandidatePickerStripProps) {
  return (
    <div className="mt-6 max-w-full overflow-x-auto pb-2 [-webkit-overflow-scrolling:touch] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden md:overflow-visible">
      <div className="grid auto-cols-[minmax(16rem,1fr)] grid-flow-col gap-3 pr-4 md:grid-flow-row md:grid-cols-2 md:pr-0 xl:grid-cols-3">
        {candidates.map((candidateOption) => {
          const isActive = candidateOption.candidate_id === selectedId
          return (
            <button
              key={candidateOption.candidate_id}
              type="button"
              onClick={() => onSelect(candidateOption.candidate_id)}
              aria-pressed={isActive}
              className={`group flex min-w-0 items-center gap-3 rounded-[1.5rem] border px-3 py-3 text-left transition ${
                isActive
                  ? 'border-ink bg-ink text-white shadow-xl shadow-ink/10'
                  : 'border-coffee/15 bg-white hover:-translate-y-0.5 hover:border-clay/40 hover:shadow-xl hover:shadow-coffee/10'
              }`}
            >
              <img
                src={candidateOption.photo_president || fallbackCandidateImage}
                alt=""
                className="size-12 shrink-0 rounded-2xl object-cover object-top"
              />
              <span className="min-w-0 flex-1">
                <span className="block truncate text-sm font-black">
                  {normalizeMojibake(candidateOption.presidential_candidate)}
                </span>
                <span
                  className={`block text-xs font-bold ${isActive ? 'text-white/70' : 'text-jade'}`}
                >
                  {formatPercent(candidateOption.affinity)} afinidad
                </span>
              </span>
              <span
                className={`flex size-8 shrink-0 items-center justify-center rounded-full text-xs font-black transition ${
                  isActive
                    ? 'bg-white text-ink'
                    : 'bg-surface text-muted group-hover:bg-clay group-hover:text-white'
                }`}
              >
                →
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
