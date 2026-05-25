import type { Proposal } from '../types'
import { ProposalCard } from './ProposalCard'

type CategoryGroup = {
  categoryId: number
  categoryName: string
  proposals: Proposal[]
}

type CandidateGroup = {
  candidateId: number
  candidateName: string
  politicalGroup: string
  categories: CategoryGroup[]
}

type ProposalCategoryMapProps = {
  proposals: Proposal[]
}

function groupProposalsByCandidateAndCategory(proposals: Proposal[]): CandidateGroup[] {
  const candidates = new Map<number, CandidateGroup>()

  proposals.forEach((proposal) => {
    const candidateGroup = candidates.get(proposal.candidate.id) ?? {
      candidateId: proposal.candidate.id,
      candidateName: proposal.candidate.presidential_candidate,
      politicalGroup: proposal.candidate.political_group,
      categories: [],
    }

    let categoryGroup = candidateGroup.categories.find(
      (category) => category.categoryId === proposal.category.id,
    )

    if (!categoryGroup) {
      categoryGroup = {
        categoryId: proposal.category.id,
        categoryName: proposal.category.name,
        proposals: [],
      }
      candidateGroup.categories.push(categoryGroup)
    }

    categoryGroup.proposals.push(proposal)
    candidates.set(proposal.candidate.id, candidateGroup)
  })

  return Array.from(candidates.values()).map((candidate) => ({
    ...candidate,
    categories: candidate.categories.sort((a, b) =>
      a.categoryName.localeCompare(b.categoryName, 'es'),
    ),
  }))
}

export function ProposalCategoryMap({ proposals }: ProposalCategoryMapProps) {
  const candidateGroups = groupProposalsByCandidateAndCategory(proposals)

  return (
    <section className="mt-12">
      <div className="mb-6 max-w-3xl">
        <p className="text-sm font-black uppercase tracking-[0.3em] text-clay">
          Mapa de propuestas
        </p>
        <h2 className="mt-2 font-display text-3xl leading-tight tracking-[-0.04em] text-ink">
          Propuestas organizadas por candidato y categoría.
        </h2>
        <p className="mt-3 text-sm leading-6 text-muted">
          Una lectura más ordenada: primero la candidatura, después sus temas, y dentro
          de cada tema las propuestas asociadas.
        </p>
      </div>

      <div className="space-y-6">
        {candidateGroups.map((candidate) => (
          <article
            key={candidate.candidateId}
            className="rounded-[2rem] border border-coffee/10 bg-white/70 p-5 shadow-sm shadow-coffee/5"
          >
            <header className="flex flex-wrap items-end justify-between gap-3 border-b border-coffee/10 pb-4">
              <div>
                <h3 className="font-display text-2xl tracking-[-0.03em] text-ink">
                  {candidate.candidateName}
                </h3>
                <p className="text-sm font-semibold text-muted">{candidate.politicalGroup}</p>
              </div>
              <span className="rounded-full bg-clay/10 px-3 py-1 text-xs font-black uppercase tracking-[0.15em] text-clay">
                {candidate.categories.length} categorías
              </span>
            </header>

            <div className="mt-5 grid gap-4 lg:grid-cols-2">
              {candidate.categories.map((category) => (
                <section
                  key={category.categoryId}
                  className="rounded-3xl border border-coffee/10 bg-surface/60 p-4"
                >
                  <div className="mb-3 flex items-center justify-between gap-3">
                    <h4 className="font-black text-ink">{category.categoryName}</h4>
                    <span className="text-xs font-bold text-muted">
                      {category.proposals.length} propuestas
                    </span>
                  </div>

                  <div className="space-y-3">
                    {category.proposals.map((proposal) => (
                      <ProposalCard key={proposal.id} proposal={proposal} />
                    ))}
                  </div>
                </section>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
