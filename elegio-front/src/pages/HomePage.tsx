import { CandidateGrid } from '../features/candidates/components/CandidateGrid'
import { useCandidates } from '../features/candidates/hooks/useCandidates'
import { HeroSection } from '../features/home/components/HeroSection'
import { NavBar } from '../features/home/components/NavBar'

export function HomePage() {
  const { candidates, isLoading, error } = useCandidates()

  return (
    <div className="min-h-screen bg-surface text-ink">
      <NavBar />
      <main>
        <HeroSection candidateCount={candidates.length} />
        <CandidateGrid candidates={candidates} error={error} isLoading={isLoading} />
      </main>
    </div>
  )
}
