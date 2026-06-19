export type TestType = 'POLITICAL_SPECTRUM' | 'PROGRAMMATIC_ALIGNMENT'

export type Test = {
  id: number
  name: string
  description: string | null
  image_url: string | null
  type: TestType | null
  created_at: string
}

export type TestListResponse = {
  items: Test[]
  total: number
  limit: number
  offset: number
}

export type TestAttempt = {
  id: number
  uuid: string
  visitor_id: number
  test_id: number
  status: 'in_progress' | 'completed' | 'abandoned' | 'timed_out'
  started_at: string
  finished_at: string | null
  created_at: string
}

export type Question = {
  id: number
  test_id: number
  title: string
  description: string | null
  type_question:
    | 'multiple_choice'
    | 'boolean'
    | 'only_option'
    | 'open_question'
    | 'video_emotion_slider'
  candidate_id: number | null
  video_url: string | null
  question_order: number
  is_active: boolean
  category: {
    id: number
    name: string
    weight: number
  } | null
  candidate: {
    id: number
    presidential_candidate: string
    vice_presidential_candidate: string
    political_group: string
    photo_of_political_group: string | null
    photo_president: string | null
    photo_vice_president: string | null
    political_spectrum: string | null
  } | null
  created_at: string
}

export type QuestionListResponse = {
  items: Question[]
  total: number
  limit: number
  offset: number
}

export type ResponseOption = {
  id: number
  question_id: number
  title: string
  value: number
  created_at: string
}

export type ResponseOptionListResponse = {
  items: ResponseOption[]
  total: number
  limit: number
  offset: number
}

export type AnswerCreateResponse = {
  answer: {
    id: number
    test_attempt_id: number
    question_id: number
    response_option_id: number | null
    boolean_answer: boolean | null
    open_text_answer: string | null
    emotion_answer: number | null
    response_time: number | null
    created_at: string
  }
  test_completed: boolean
  test_attempt_status: TestAttempt['status']
}

export type AnswerListResponse = {
  items: AnswerCreateResponse['answer'][]
  total: number
  limit: number
  offset: number
}

export type CandidateAffinity = {
  candidate_id: number
  presidential_candidate: string
  vice_presidential_candidate: string
  political_group: string
  political_spectrum: string | null
  photo_president: string | null
  photo_vice_president: string | null
  photo_of_political_group: string | null
  affinity: number
  distance: number
  categories_compared: number
}

export type AffinityResponse = {
  test_attempt_uuid: string
  user_averages: Array<{
    category_id: number
    category_name: string
    weight: number
    average: number
  }>
  candidates: CandidateAffinity[]
}
