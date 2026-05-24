export type GovernmentPlanCandidate = {
  id: number
  presidential_candidate: string
  vice_presidential_candidate: string
  political_group: string
  political_spectrum: string
  photo_president: string
  photo_vice_president: string
  photo_of_political_group: string
}

export type GovernmentPlan = {
  id: number
  url: string
  candidate: GovernmentPlanCandidate
  created_at: string
}

export type GovernmentPlansResponse = {
  items: GovernmentPlan[]
  total: number
  limit: number
  offset: number
}
