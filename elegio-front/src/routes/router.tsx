import { createBrowserRouter } from 'react-router'
import { CandidateDetailPage } from '../pages/CandidateDetailPage'
import { HomePage } from '../pages/HomePage'
import { MethodologyPage } from '../pages/MethodologyPage'
import { ProposalsPage } from '../pages/ProposalsPage'
import { TestPage } from '../pages/TestPage'
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
  {
    path: ROUTE_PATHS.methodology,
    element: <MethodologyPage />,
  },
  {
    path: ROUTE_PATHS.test,
    element: <TestPage />,
  },
])
