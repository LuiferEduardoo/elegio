import { useMemo } from 'react'
import { Link } from 'react-router'
import { Footer } from '../components/Footer'
import { NavBar } from '../features/home/components/NavBar'
import { AffinityResultsSection } from '../features/tests/components/AffinityResultsSection'
import { CandidateComparison } from '../features/tests/components/CandidateComparison'
import { useAffinityResult } from '../features/tests/hooks/useAffinityResult'
import { ROUTE_PATHS } from '../routes/paths'

export function ResultsPage() {
  const { affinity, status } = useAffinityResult()

  const userAverages = useMemo(
    () =>
      affinity
        ? Object.fromEntries(
            affinity.user_averages.map((category) => [category.category_id, category.average]),
          )
        : {},
    [affinity],
  )

  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />
      <main className="flex-grow">
        <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-10 sm:py-14 lg:px-16">
          {status === 'loading' && <ResultsMessage title="Cargando tus resultados…" />}

          {status === 'empty' && (
            <ResultsMessage
              eyebrow="Todavía nada"
              title="Aún no completaste el test."
              description="Hacé el test para descubrir con qué candidatos tenés más afinidad y comparar tu postura categoría por categoría."
              actionLabel="Hacer el test →"
              actionTo={ROUTE_PATHS.test}
            />
          )}

          {status === 'error' && (
            <ResultsMessage
              eyebrow="Ups"
              title="No pudimos cargar tus resultados."
              description="Volvé a intentarlo en un momento o reiniciá el test."
              actionLabel="Ir al test →"
              actionTo={ROUTE_PATHS.test}
            />
          )}

          {status === 'ready' && affinity && (
            <>
              <header className="max-w-2xl">
                <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">
                  Tus resultados
                </p>
                <h1 className="mt-3 font-display text-3xl tracking-[-0.04em] sm:text-4xl lg:text-5xl">
                  Tu mapa político completo
                </h1>
                <p className="mt-4 text-sm leading-6 text-muted">
                  Acá tenés el ranking de afinidad y la comparativa de tu postura frente a cada
                  candidato, categoría por categoría.
                </p>
              </header>

              <AffinityResultsSection candidates={affinity.candidates} />

              <CandidateComparison candidates={affinity.candidates} userAverages={userAverages} />
            </>
          )}
        </div>
      </main>
      <Footer />
    </div>
  )
}

type ResultsMessageProps = {
  eyebrow?: string
  title: string
  description?: string
  actionLabel?: string
  actionTo?: string
}

function ResultsMessage({ eyebrow, title, description, actionLabel, actionTo }: ResultsMessageProps) {
  return (
    <div className="mx-auto max-w-xl py-16 text-center">
      {eyebrow && (
        <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">{eyebrow}</p>
      )}
      <h1 className="mt-3 font-display text-3xl tracking-[-0.03em] text-ink sm:text-4xl">{title}</h1>
      {description && <p className="mt-4 text-sm leading-6 text-muted">{description}</p>}
      {actionLabel && actionTo && (
        <Link
          to={actionTo}
          className="mt-8 inline-flex rounded-full bg-coffee px-6 py-3 text-xs font-black uppercase tracking-[0.25em] text-white transition hover:bg-jade"
        >
          {actionLabel}
        </Link>
      )}
    </div>
  )
}
