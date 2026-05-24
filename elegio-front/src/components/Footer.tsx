import { Link } from 'react-router'

export function Footer() {
  return (
    <footer className="mt-auto border-t border-coffee/10 bg-surface/50 pb-12 pt-16">
      <div className="mx-auto max-w-7xl px-6 sm:px-10 lg:px-16">
        <div className="grid grid-cols-1 gap-12 md:grid-cols-[2fr_1fr_1fr] md:gap-8">
          {/* Columna 1: Marca y Créditos */}
          <div className="flex flex-col items-center md:items-start max-w-sm mx-auto md:mx-0">
            <Link to="/" className="flex items-center gap-3" aria-label="Elegio - Inicio">
              <img 
                src="/elegio-logo.svg" 
                alt="Logo Elegio" 
                className="h-10 w-auto opacity-50 grayscale transition-all hover:opacity-80" 
              />
            </Link>
            <p className="mt-4 text-center text-sm text-muted md:text-left">
              Fomentando el voto informado mediante el análisis de propuestas y planes de gobierno.
            </p>
            <p className="mt-6 text-center text-sm text-muted md:text-left">
              Creado con amor por:{' '}
              <a 
                href="https://www.linkedin.com/in/luifereduardoo/" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="font-semibold text-ink transition-colors hover:text-clay underline underline-offset-2 decoration-coffee/20 hover:decoration-clay"
              >
                Luifer Ortega
              </a>
              {' '}Y{' '}
              <a 
                href="https://www.linkedin.com/in/emerson-roncancio/" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="font-semibold text-ink transition-colors hover:text-clay underline underline-offset-2 decoration-coffee/20 hover:decoration-clay"
              >
                Emerson Roncancio
              </a>
            </p>
          </div>
          
          {/* Columna 2: Navegación */}
          <div className="flex flex-col items-center md:items-start">
            <h3 className="font-display text-base font-bold tracking-tight text-ink">Navegación</h3>
            <nav className="mt-4 flex flex-col gap-3 text-center md:text-left">
              <Link to="/" className="text-sm font-semibold text-muted transition hover:text-ink">
                Inicio
              </Link>
              <Link to="/propuestas" className="text-sm font-semibold text-muted transition hover:text-ink">
                Propuestas
              </Link>
              <Link to="/test" className="text-sm font-semibold text-muted transition hover:text-ink">
                Match electoral
              </Link>
              <Link to="/metodologia" className="text-sm font-semibold text-muted transition hover:text-ink">
                Metodología
              </Link>
            </nav>
          </div>

          {/* Columna 3: Legal y Contacto */}
          <div className="flex flex-col items-center md:items-start">
            <h3 className="font-display text-base font-bold tracking-tight text-ink">Legal y Contacto</h3>
            <nav className="mt-4 flex flex-col gap-3 text-center md:text-left">
              <Link to="/privacidad" className="text-sm font-semibold text-muted transition hover:text-ink">
                Política de privacidad
              </Link>
              <Link to="/cookies" className="text-sm font-semibold text-muted transition hover:text-ink">
                Política de cookies
              </Link>
            </nav>
          </div>
        </div>
        
        <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-coffee/10 pt-8 sm:flex-row text-xs text-muted/70">
          <p>© {new Date().getFullYear()} Elegio. Todos los derechos reservados.</p>
          <div className="flex items-center gap-4">
            <span>Proyecto de código abierto</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
