export type CategoryAverage = {
  category_id: number
  category_name: string
  weight: number
  negative_pole_name: string
  negative_pole_description: string
  positive_pole_name: string
  positive_pole_description: string
  average: number
  rhetorical_weight: number | null
  editorial_justification: string | null
  adjusted_average: number
  proposals_count: number
}

export type Candidate = {
  id: number
  presidential_candidate: string
  vice_presidential_candidate: string
  political_group: string
  photo_of_political_group: string
  photo_president: string
  photo_vice_president: string
  troubles_questions: string
  political_spectrum: string
  created_at: string
  category_averages: CategoryAverage[]
}

export type CandidatesResponse = {
  items: Candidate[]
  total: number
  limit: number
  offset: number
}
