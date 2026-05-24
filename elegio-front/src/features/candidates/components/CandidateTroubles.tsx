type CandidateTroublesProps = {
  troubles: string
}

export function CandidateTroubles({ troubles }: CandidateTroublesProps) {
  if (!troubles?.trim()) {
    return null
  }

  return (
    <section className="rounded-[2rem] border border-coffee/15 bg-white p-8 shadow-sm shadow-coffee/5">
      <p className="text-xs font-black uppercase tracking-[0.3em] text-clay">Polémicas y cuestionamientos</p>
      <h2 className="mt-2 font-display text-3xl tracking-[-0.03em] text-ink">
        Lo que la prensa señaló.
      </h2>
      <p className="mt-5 text-base leading-7 text-ink/80">{troubles}</p>
    </section>
  )
}
