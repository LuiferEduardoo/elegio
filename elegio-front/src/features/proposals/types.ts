export type ProposalCategory = {
  id: number
  name: string
  weight: number
}

export type ProposalCandidate = {
  id: number
  presidential_candidate: string
  vice_presidential_candidate: string
  political_group: string
  political_spectrum: string | null
  photo_president: string | null
  photo_vice_president: string | null
  photo_of_political_group: string | null
}

export type ProposalTagging = {
  id: number
  name: string
}

export type ProposalSource = {
  id: number
  url: string
}

export type ProposalHit = {
  proposal_id: number
  title: string
  summary: string | null
  candidate: ProposalCandidate
  category: ProposalCategory
  taggings: ProposalTagging[]
  sources: ProposalSource[]
  score: number
  semantic_rank: number | null
  semantic_score: number | null
  lexical_rank: number | null
  lexical_score: number | null
  excerpt: string | null
}

export type ProposalSearchResponse = {
  query: string
  total: number
  items: ProposalHit[]
}
