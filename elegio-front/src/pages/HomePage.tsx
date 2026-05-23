import { CandidateGrid } from '../features/candidates/components/CandidateGrid'
import { useCandidates } from '../features/candidates/hooks/useCandidates'
import { HeroSection } from '../features/home/components/HeroSection'

export function HomePage() {
  const { candidates, isLoading, error } = useCandidates()

  return (
    <main className="min-h-screen bg-surface text-ink">
      <HeroSection candidateCount={candidates.length} />
      <CandidateGrid candidates={candidates} error={error} isLoading={isLoading} />
    </main>
  )
}
