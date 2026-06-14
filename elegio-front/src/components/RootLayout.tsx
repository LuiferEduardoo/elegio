import { useEffect } from 'react'
import { Outlet, useLocation } from 'react-router'
import { FloatingEmmaButton } from './FloatingEmmaButton'
import { AnalyticsTracker } from '../features/analytics/components/AnalyticsTracker'

export function RootLayout() {
  const { pathname } = useLocation()

  useEffect(() => {
    // Cuando cambia la ruta, hacemos scroll suave hacia arriba
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }, [pathname])

  return (
    <>
      <AnalyticsTracker />
      <Outlet />
      <FloatingEmmaButton />
    </>
  )
}
