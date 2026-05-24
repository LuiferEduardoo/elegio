export const ROUTE_PATHS = {
  home: '/',
  candidates: '/candidatos',
  candidateDetail: '/candidatos/:id',
  proposals: '/propuestas',
  test: '/test',
  results: '/resultados',
} as const

export const buildCandidateDetailPath = (id: number | string) => `/candidatos/${id}`
