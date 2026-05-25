import { createBrowserRouter } from 'react-router'
import { CandidateDetailPage } from '../pages/CandidateDetailPage'
import { ElectoralVsPage } from '../pages/ElectoralVsPage'
import { HomePage } from '../pages/HomePage'
import { MethodologyPage } from '../pages/MethodologyPage'
import { ProposalsPage } from '../pages/ProposalsPage'
import { ResultsPage } from '../pages/ResultsPage'
import { TestPage } from '../pages/TestPage'
import { PrivacyPolicyPage } from '../pages/PrivacyPolicyPage'
import { CookiesPolicyPage } from '../pages/CookiesPolicyPage'
import { RootLayout } from '../components/RootLayout'
import { ROUTE_PATHS } from './paths'

export const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      {
        path: ROUTE_PATHS.home,
        element: <HomePage />,
      },
      {
        path: ROUTE_PATHS.proposals,
        element: <ProposalsPage />,
      },
      {
        path: ROUTE_PATHS.electoralVs,
        element: <ElectoralVsPage />,
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
      {
        path: ROUTE_PATHS.results,
        element: <ResultsPage />,
      },
      {
        path: ROUTE_PATHS.privacy,
        element: <PrivacyPolicyPage />,
      },
      {
        path: ROUTE_PATHS.cookies,
        element: <CookiesPolicyPage />,
      },
    ],
  },
])
