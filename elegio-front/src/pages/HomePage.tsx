import { CandidateGrid } from '../features/candidates/components/CandidateGrid'
import { useCandidates } from '../features/candidates/hooks/useCandidates'
import { HeroSection } from '../features/home/components/HeroSection'
import { NavBar } from '../features/home/components/NavBar'
import { Footer } from '../components/Footer'

export function HomePage() {
  const { candidates, isLoading, error } = useCandidates()

  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />
      <main className="flex-grow">
        <HeroSection
          candidateCount={candidates.filter((c) => c.is_in_the_second_round).length}
        />
        <CandidateGrid candidates={candidates} error={error} isLoading={isLoading} />
      </main>
      <Footer />
    </div>
  )
}
