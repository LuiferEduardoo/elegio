import { createBrowserRouter } from 'react-router'
import { HomePage } from '../pages/HomePage'
import { ROUTE_PATHS } from './paths'

export const router = createBrowserRouter([
  {
    path: ROUTE_PATHS.home,
    element: <HomePage />,
  },
])
