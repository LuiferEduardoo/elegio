import { useEffect } from 'react'
import { Outlet, useLocation } from 'react-router'

export function RootLayout() {
  const { pathname } = useLocation()

  useEffect(() => {
    // Cuando cambia la ruta, hacemos scroll suave hacia arriba
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }, [pathname])

  return <Outlet />
}
