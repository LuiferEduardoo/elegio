type TestProgressPanelProps = {
  answeredCount: number
  progress: number
  totalQuestions: number
}

export function TestProgressPanel({
  answeredCount,
  progress,
  totalQuestions,
}: TestProgressPanelProps) {
  return (
    <aside className="relative isolate flex min-h-[24rem] flex-col justify-between bg-coffee p-8 text-white sm:p-10">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_20%_20%,rgba(125,211,252,0.35),transparent_20rem),radial-gradient(circle_at_80%_0%,rgba(37,99,235,0.4),transparent_22rem)]" />
      <div>
        <p className="text-xs font-black uppercase tracking-[0.35em] text-gold">
          Test de afinidad
        </p>
        <h1 className="mt-5 font-display text-4xl leading-[1.02] tracking-[-0.04em] sm:text-5xl">
          Votá con menos ruido y más criterio.
        </h1>
        <p className="mt-5 max-w-md text-base leading-7 text-white/75">
          Respondé preguntas por categoría y comparamos tus posiciones con las propuestas
          analizadas de cada candidato.
        </p>
      </div>

      <div className="mt-10 rounded-[2rem] border border-white/15 bg-white/10 p-5 backdrop-blur">
        <div className="flex items-center justify-between text-sm font-bold text-white/80">
          <span>Progreso</span>
          <span>
            {answeredCount}/{totalQuestions || 0}
          </span>
        </div>
        <div className="mt-3 h-3 overflow-hidden rounded-full bg-white/15">
          <div
            className="h-full rounded-full bg-gold transition-all duration-500"
            style={{ width: `${progress * 100}%` }}
          />
        </div>
      </div>
    </aside>
  )
}
