import type { TestFlowStatus } from '../hooks/useTestFlow'
import type { Test } from '../types'
import { normalizeMojibake } from '../utils/text'

type TestIntroPanelProps = {
  activeTest: Test | null
  error: string | null
  status: TestFlowStatus
  testCount: number
  onStart: () => void
}

export function TestIntroPanel({
  activeTest,
  error,
  status,
  testCount,
  onStart,
}: TestIntroPanelProps) {
  const testName = activeTest ? normalizeMojibake(activeTest.name) : 'Preparando el test...'

  return (
    <div className="flex min-h-[28rem] flex-col justify-center">
      <p className="text-sm font-black uppercase tracking-[0.25em] text-clay">
        {testCount} test{testCount === 1 ? '' : 's'} disponible{testCount === 1 ? '' : 's'}
      </p>
      <h2 className="mt-4 font-display text-3xl tracking-[-0.03em] sm:text-4xl">
        {testName}
      </h2>
      <p className="mt-4 max-w-xl leading-7 text-muted">
        Al iniciar guardamos un token temporal en cookies para asociar tus respuestas con
        este intento. Si ya terminaste, esta página abre tus resultados directamente.
      </p>

      {error && <p className="mt-6 rounded-2xl bg-clay p-4 font-bold text-white">{error}</p>}

      <button
        type="button"
        onClick={onStart}
        disabled={!activeTest || status === 'loading'}
        className="mt-8 inline-flex w-fit items-center justify-center rounded-full bg-ink px-6 py-3 text-sm font-black uppercase tracking-[0.22em] text-white transition hover:bg-clay disabled:cursor-not-allowed disabled:opacity-50"
      >
        {status === 'loading' ? 'Cargando...' : 'Empezar test'}
      </button>
    </div>
  )
}
