// const NAV_LINKS = [
//   { href: '#inicio', label: 'Inicio' },
//   { href: '#candidatos', label: 'Candidatos' },
//   { href: '#propuestas', label: 'Propuestas' },
//   { href: '#afinidad', label: 'Test de afinidad' },
// ]

export function NavBar() {
  return (
    <header className="sticky top-0 z-50 border-b border-coffee/10 bg-white/85 backdrop-blur">
      <nav className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4 sm:px-10 lg:px-16">
        <a href="/" className="flex items-center gap-3" aria-label="Elegio - Inicio">
          <img src="/elegio-logo.svg" alt="" className="h-12 w-auto" />
        </a>

        {/* <ul className="hidden items-center gap-7 md:flex">
          {NAV_LINKS.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="text-sm font-semibold text-muted transition hover:text-ink"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul> */}

        <a
          href="#afinidad"
          className="inline-flex items-center rounded-full bg-ink px-4 py-2 text-sm font-bold text-white transition hover:bg-clay focus:outline-none focus-visible:ring-2 focus-visible:ring-clay focus-visible:ring-offset-2"
        >
          Hacer test
        </a>
      </nav>
    </header>
  )
}
