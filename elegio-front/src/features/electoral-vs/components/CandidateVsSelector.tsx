import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import { normalizeMojibake } from '../../../utils/text'
import type { Candidate } from '../../candidates/types'
import { MAX_SELECTED_CANDIDATES } from '../types'

type CandidateVsSelectorProps = {
  candidates: Candidate[]
  selectedCandidateIds: number[]
  onClear: () => void
  onToggle: (candidateId: number) => void
}

export function CandidateVsSelector({
  candidates,
  selectedCandidateIds,
  onClear,
  onToggle,
}: CandidateVsSelectorProps) {
  return (
    <section className="mt-8 rounded-[2rem] border border-coffee/10 bg-white p-5 shadow-sm shadow-coffee/5 sm:p-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.25em] text-clay">Paso 1</p>
          <h2 className="mt-1 font-display text-3xl tracking-[-0.04em] text-ink">
            Escogé máximo tres candidatos.
          </h2>
        </div>
        {selectedCandidateIds.length > 0 && (
          <button
            type="button"
            onClick={onClear}
            className="w-fit rounded-full border border-coffee/15 px-4 py-2 text-xs font-black uppercase tracking-[0.14em] text-clay transition hover:border-clay/40 hover:bg-clay/5"
          >
            Limpiar selección
          </button>
        )}
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-4">
        {candidates.map((candidate) => (
          <CandidateVsCard
            candidate={candidate}
            isDisabled={
              selectedCandidateIds.length >= MAX_SELECTED_CANDIDATES &&
              !selectedCandidateIds.includes(candidate.id)
            }
            isSelected={selectedCandidateIds.includes(candidate.id)}
            key={candidate.id}
            onToggle={onToggle}
          />
        ))}
      </div>
    </section>
  )
}

type CandidateVsCardProps = {
  candidate: Candidate
  isDisabled: boolean
  isSelected: boolean
  onToggle: (candidateId: number) => void
}

function CandidateVsCard({ candidate, isDisabled, isSelected, onToggle }: CandidateVsCardProps) {
  const name = normalizeMojibake(candidate.presidential_candidate)
  const politicalGroup = normalizeMojibake(candidate.political_group)
  const photo = candidate.photo_president || fallbackCandidateImage

  return (
    <button
      type="button"
      disabled={isDisabled}
      onClick={() => onToggle(candidate.id)}
      aria-pressed={isSelected}
      className={`group relative overflow-hidden rounded-[1.75rem] border p-3 text-left transition ${
        isSelected
          ? 'border-clay bg-clay text-white shadow-xl shadow-clay/20'
          : 'border-coffee/10 bg-surface text-ink hover:-translate-y-0.5 hover:border-clay/40 hover:bg-white hover:shadow-xl hover:shadow-coffee/10'
      } disabled:cursor-not-allowed disabled:opacity-40`}
    >
      {isSelected && (
        <span className="absolute right-3 top-3 rounded-full bg-white px-2 py-0.5 text-xs font-black text-clay">
          ✓
        </span>
      )}
      <img
        src={photo}
        alt={name}
        className="h-36 w-full rounded-[1.25rem] object-cover object-top sm:h-44"
        loading="lazy"
        onError={(event) => {
          event.currentTarget.onerror = null
          event.currentTarget.src = fallbackCandidateImage
        }}
      />
      <h3 className="mt-3 text-base font-black leading-tight">{name}</h3>
      <p className={`mt-1 text-xs font-semibold ${isSelected ? 'text-white/75' : 'text-muted'}`}>
        {politicalGroup}
      </p>
    </button>
  )
}
