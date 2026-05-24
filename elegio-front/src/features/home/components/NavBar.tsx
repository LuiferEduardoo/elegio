import { useEffect, useState } from 'react'
import { Link } from 'react-router'

const NAV_LINKS = [
  { href: '/', label: 'Inicio' },
  { href: '/propuestas', label: 'Propuestas' },
  { href: '/metodologia', label: 'Metodología' },
]

export function NavBar() {
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    if (!isOpen) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsOpen(false)
    }
    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    document.addEventListener('keydown', onKey)
    return () => {
      document.body.style.overflow = previousOverflow
      document.removeEventListener('keydown', onKey)
    }
  }, [isOpen])

  return (
    <>
      <header className="sticky top-0 z-30 border-b border-coffee/10 bg-white/85 backdrop-blur">
        <nav className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4 sm:px-10 lg:px-16">
        <Link to="/" className="flex items-center gap-3" aria-label="Elegio - Inicio">
          <img src="/elegio-logo.svg" alt="" className="h-12 w-auto" />
        </Link>

        <div className="flex items-center gap-7">
          <ul className="hidden items-center gap-7 md:flex">
            {NAV_LINKS.map((link) => (
              <li key={link.href}>
                <Link
                  to={link.href}
                  className="text-sm font-semibold text-muted transition hover:text-ink"
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>

          <a
            href="#afinidad"
            className="inline-flex items-center rounded-full bg-ink px-4 py-2 text-sm font-bold text-white transition hover:bg-clay focus:outline-none focus-visible:ring-2 focus-visible:ring-clay focus-visible:ring-offset-2"
          >
            Hacer test
          </a>

          <button
            type="button"
            onClick={() => setIsOpen(true)}
            aria-label="Abrir menú"
            aria-expanded={isOpen}
            aria-controls="mobile-menu"
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-coffee/10 text-ink transition hover:bg-coffee/5 focus:outline-none focus-visible:ring-2 focus-visible:ring-clay md:hidden"
          >
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="4" y1="7" x2="20" y2="7" />
              <line x1="4" y1="12" x2="20" y2="12" />
              <line x1="4" y1="17" x2="20" y2="17" />
            </svg>
          </button>
        </div>
        </nav>
      </header>

      <div
        onClick={() => setIsOpen(false)}
        aria-hidden="true"
        className={`fixed inset-0 z-40 bg-ink/40 backdrop-blur-sm transition-opacity duration-300 md:hidden ${
          isOpen ? 'opacity-100' : 'pointer-events-none opacity-0'
        }`}
      />

      <aside
        id="mobile-menu"
        aria-hidden={!isOpen}
        className={`fixed inset-y-0 right-0 z-50 flex w-72 max-w-[80vw] flex-col bg-white shadow-2xl shadow-coffee/20 transition-transform duration-300 ease-out md:hidden ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between border-b border-coffee/10 px-6 py-4">
          <span className="font-display text-lg tracking-[-0.02em] text-ink"></span>
          <button
            type="button"
            onClick={() => setIsOpen(false)}
            aria-label="Cerrar menú"
            className="inline-flex h-9 w-9 items-center justify-center rounded-full text-ink transition hover:bg-coffee/5 focus:outline-none focus-visible:ring-2 focus-visible:ring-clay"
          >
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="6" y1="6" x2="18" y2="18" />
              <line x1="18" y1="6" x2="6" y2="18" />
            </svg>
          </button>
        </div>

        <ul className="flex flex-col gap-1 px-3 py-4">
          {NAV_LINKS.map((link) => (
            <li key={link.href}>
              <Link
                to={link.href}
                onClick={() => setIsOpen(false)}
                className="block rounded-2xl px-4 py-3 text-base font-semibold text-ink transition hover:bg-coffee/5"
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </aside>
    </>
  )
}
