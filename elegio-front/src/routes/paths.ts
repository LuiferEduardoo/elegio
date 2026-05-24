export const ROUTE_PATHS = {
  home: '/',
  candidates: '/candidatos',
  candidateDetail: '/candidatos/:id',
  proposals: '/propuestas',
  methodology: '/metodologia',
  test: '/test',
  results: '/resultados',
  privacy: '/privacidad',
  cookies: '/cookies',
} as const

export const buildCandidateDetailPath = (id: number | string) => `/candidatos/${id}`
