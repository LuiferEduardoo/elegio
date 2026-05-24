import { createBrowserRouter } from 'react-router'
import { CandidateDetailPage } from '../pages/CandidateDetailPage'
import { HomePage } from '../pages/HomePage'
import { ProposalsPage } from '../pages/ProposalsPage'
import { ROUTE_PATHS } from './paths'

export const router = createBrowserRouter([
  {
    path: ROUTE_PATHS.home,
    element: <HomePage />,
  },
  {
    path: ROUTE_PATHS.proposals,
    element: <ProposalsPage />,
  },
  {
    path: ROUTE_PATHS.candidateDetail,
    element: <CandidateDetailPage />,
  },
])
