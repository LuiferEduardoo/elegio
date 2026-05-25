import fallbackCandidateImage from '../../../assets/candidate-fallback.svg'
import { normalizeMojibake } from '../../../utils/text'
import type { Candidate } from '../../candidates/types'

type ProposalCandidatePickerProps = {
  candidates: Candidate[]
  selectedCandidateIds: number[]
  onToggleCandidate: (candidateId: number) => void
  onClearCandidates: () => void
}

export function ProposalCandidatePicker({
  candidates,
  selectedCandidateIds,
  onToggleCandidate,
  onClearCandidates,
}: ProposalCandidatePickerProps) {
  if (candidates.length === 0) return null

  const selectedCount = selectedCandidateIds.length

  return (
    <section className="mt-8 rounded-[2rem] border border-coffee/10 bg-white/75 p-4 shadow-sm shadow-coffee/5 backdrop-blur sm:p-5">
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.25em] text-clay">
            Elegí candidaturas
          </p>
          <h2 className="mt-1 font-display text-2xl tracking-[-0.03em] text-ink">
            Seleccioná una o varias caras.
          </h2>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-jade/10 px-3 py-1.5 text-xs font-black uppercase tracking-[0.14em] text-jade">
            {selectedCount === 0
              ? 'Sin filtro de candidatura'
              : `${selectedCount} ${selectedCount === 1 ? 'seleccionado' : 'seleccionados'}`}
          </span>
          {selectedCount > 0 && (
            <button
              type="button"
              onClick={onClearCandidates}
              className="rounded-full border border-coffee/15 bg-white px-3 py-1.5 text-xs font-black uppercase tracking-[0.14em] text-clay transition hover:border-clay/40 hover:bg-clay/5"
            >
              Quitar filtro
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
        {candidates.map((candidate) => {
          const isSelected = selectedCandidateIds.includes(candidate.id)
          const photo = candidate.photo_president || fallbackCandidateImage
          const presidentialCandidate = normalizeMojibake(candidate.presidential_candidate)
          const politicalGroup = normalizeMojibake(candidate.political_group)

          return (
            <button
              key={candidate.id}
              type="button"
              onClick={() => onToggleCandidate(candidate.id)}
              aria-pressed={isSelected}
              className={`group relative overflow-hidden rounded-3xl border p-3 text-left transition duration-300 ${
                isSelected
                  ? 'border-clay bg-clay text-white shadow-xl shadow-clay/20'
                  : 'border-coffee/10 bg-surface text-ink hover:-translate-y-0.5 hover:border-clay/40 hover:bg-white'
              }`}
            >
              <div className="flex flex-col items-center text-center sm:flex-row sm:text-left">
                <img
                  src={photo}
                  alt={presidentialCandidate}
                  className={`size-20 shrink-0 rounded-2xl border object-cover object-top transition sm:size-16 ${
                    isSelected ? 'border-white/30' : 'border-coffee/10'
                  }`}
                  loading="lazy"
                  onError={(event) => {
                    event.currentTarget.onerror = null
                    event.currentTarget.src = fallbackCandidateImage
                  }}
                />

                <span className="mt-3 min-w-0 sm:ml-3 sm:mt-0">
                  <span className="block text-sm font-black leading-tight">
                    {presidentialCandidate}
                  </span>
                  <span
                    className={`mt-1 block text-xs font-semibold leading-tight ${
                      isSelected ? 'text-white/75' : 'text-muted'
                    }`}
                  >
                    {politicalGroup}
                  </span>
                </span>
              </div>

              {isSelected && (
                <span className="absolute right-3 top-3 rounded-full bg-white px-2 py-0.5 text-xs font-black text-clay">
                  ✓
                </span>
              )}
            </button>
          )
        })}
      </div>
    </section>
  )
}
