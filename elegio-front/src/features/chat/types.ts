export type ChatRole = 'user' | 'assistant'

export type ChatMessage = {
  id: string
  role: ChatRole
  content: string
}

export type ChatRead = {
  id: number
  title: string
  is_active: boolean
  created_at: string
}

export type ChatSource = {
  ref: number
  collection: string | null
  score: number | null
  candidate_id: number | null
  candidate_name: string | null
  title: string | null
  url: string | null
}

export type StreamHandlers = {
  onSources?: (sources: ChatSource[]) => void
  onToken: (delta: string) => void
  onTitle?: (title: string) => void
  onError: (detail: string) => void
}
