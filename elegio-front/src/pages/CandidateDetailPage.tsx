import { Link, useParams } from 'react-router'
import { CandidateDetailHero } from '../features/candidates/components/CandidateDetailHero'
import { CandidateTroubles } from '../features/candidates/components/CandidateTroubles'
import { CategoryAveragesSection } from '../features/candidates/components/CategoryAveragesSection'
import { useCandidate } from '../features/candidates/hooks/useCandidate'
import { GovernmentPlansSection } from '../features/government-plans/components/GovernmentPlansSection'
import { useGovernmentPlans } from '../features/government-plans/hooks/useGovernmentPlans'
import { ROUTE_PATHS } from '../routes/paths'
import { NavBar } from '../features/home/components/NavBar'
import { Footer } from '../components/Footer'

export function CandidateDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { candidate, isLoading, error } = useCandidate(id)
  const {
    plans: governmentPlans,
    isLoading: isLoadingPlans,
    error: governmentPlansError,
  } = useGovernmentPlans(id)

  if (isLoading) {
    return (
      <div className="flex min-h-screen flex-col bg-surface text-ink">
        <NavBar />
        <main className="flex-grow">
          <div className="mx-auto max-w-3xl px-6 py-24 text-center">
            <p className="text-sm font-black uppercase tracking-[0.3em] text-clay">Cargando candidato…</p>
            <div className="mx-auto mt-6 h-2 w-48 animate-pulse rounded-full bg-coffee/10" />
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  if (error || !candidate) {
    return (
      <div className="flex min-h-screen flex-col bg-surface text-ink">
        <NavBar />
        <main className="flex-grow">
          <div className="mx-auto max-w-3xl px-6 py-24 text-center">
            <p className="text-sm font-black uppercase tracking-[0.3em] text-clay">Ups</p>
            <h1 className="mt-3 font-display text-4xl tracking-[-0.03em] text-ink">
              {error ?? 'No encontramos este candidato.'}
            </h1>
            <Link
              to={ROUTE_PATHS.home}
              className="mt-8 inline-flex rounded-full bg-coffee px-6 py-3 text-xs font-black uppercase tracking-[0.25em] text-white hover:bg-jade"
            >
              Volver al tarjetón
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />
      <main className="flex-grow">
        <CandidateDetailHero candidate={candidate} />

        <div className="mx-auto w-full max-w-7xl space-y-12 px-6 py-14 sm:px-10 lg:px-16">
          <CandidateTroubles troubles={candidate.troubles_questions} />
          <GovernmentPlansSection
            plans={governmentPlans}
            isLoading={isLoadingPlans}
            error={governmentPlansError}
          />
          <CategoryAveragesSection categories={candidate.category_averages} />
        </div>
      </main>
      <Footer />
    </div>
  )
}
