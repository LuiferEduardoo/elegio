import { useState } from 'react'

import type { TestFlowStatus, TestIntroStats } from '../hooks/useTestFlow'
import type { Test } from '../types'
import { normalizeMojibake } from '../utils/text'

type MatchTestIntroProps = {
  activeTest: Test | null
  status: TestFlowStatus
  error: string | null
  tests: Test[]
  stats: TestIntroStats | null
  onStart: () => void
  onSelectTest: (testId: number) => void
}

/**
 * Landing/intro for the match-electoral experience. Shows the default test
 * (segunda vuelta) with its cover image and invites the visitor to start.
 */
export function MatchTestIntro({
  activeTest,
  status,
  error,
  tests,
  stats,
  onStart,
  onSelectTest,
}: MatchTestIntroProps) {
  const name = activeTest ? normalizeMojibake(activeTest.name) : 'Preparando el cara a cara…'
  const description = activeTest?.description ? normalizeMojibake(activeTest.description) : null
  const isLoading = status === 'loading'
  const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false)

  return (
    <section className="overflow-hidden rounded-[1.25rem] border border-coffee/10 bg-white shadow-2xl shadow-coffee/10 sm:rounded-[2.5rem]">
      <div className="grid min-w-0 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
        <div className="order-2 flex flex-col justify-center p-4 sm:p-10 lg:order-1 lg:p-12">
          <p className="text-[0.62rem] font-black uppercase tracking-[0.18em] text-clay sm:text-xs sm:tracking-[0.3em]">
            Match electoral ✦ · Segunda vuelta
          </p>
          <h1 className="mt-2 font-display text-2xl leading-[1.02] tracking-[-0.04em] sm:mt-4 sm:text-4xl lg:text-5xl">
            {name}
          </h1>
          {description && (
            <div className="mt-3 max-w-xl sm:mt-5">
              <p
                className={`text-sm leading-6 text-muted sm:leading-7 ${
                  isDescriptionExpanded ? '' : 'line-clamp-4 sm:line-clamp-none'
                }`}
              >
                {description}
              </p>
              <button
                type="button"
                onClick={() => setIsDescriptionExpanded((expanded) => !expanded)}
                className="mt-1 text-xs font-black uppercase tracking-[0.14em] text-clay sm:hidden"
              >
                {isDescriptionExpanded ? 'Ver menos' : 'Ver más'}
              </button>
            </div>
          )}

          {stats && (
            <ul className="mt-4 flex flex-wrap gap-1.5 text-[0.68rem] font-bold text-ink sm:mt-7 sm:gap-2.5 sm:text-xs">
              <li className="rounded-full bg-jade/10 px-3 py-1.5 text-jade sm:px-3.5 sm:py-2">
                {stats.questions} {stats.questions === 1 ? 'pregunta' : 'preguntas'}
              </li>
              {stats.finalists > 0 && (
                <li className="rounded-full bg-clay/10 px-3 py-1.5 text-clay sm:px-3.5 sm:py-2">
                  {stats.finalists} {stats.finalists === 1 ? 'finalista' : 'finalistas'}
                </li>
              )}
              <li className="rounded-full bg-coffee/10 px-3 py-1.5 text-coffee sm:px-3.5 sm:py-2">
                ~{stats.minutes} min
              </li>
            </ul>
          )}

          {error && (
            <p className="mt-6 rounded-2xl bg-clay px-4 py-3 text-sm font-bold text-white">{error}</p>
          )}

          <button
            type="button"
            onClick={onStart}
            disabled={!activeTest || isLoading}
            className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-full bg-ink px-5 py-3 text-xs font-black uppercase tracking-[0.18em] text-white transition hover:bg-clay disabled:cursor-not-allowed disabled:opacity-50 sm:mt-8 sm:w-fit sm:px-7 sm:py-3.5 sm:text-sm sm:tracking-[0.22em]"
          >
            {isLoading ? 'Cargando…' : 'Empezar el cara a cara →'}
          </button>

          {tests.length > 1 && (
            <div className="mt-3 flex flex-wrap items-center gap-1.5 sm:mt-4 sm:gap-2">
              <span className="text-[0.65rem] font-bold uppercase tracking-[0.15em] text-muted sm:text-xs">
                Cambiar test:
              </span>
              {tests.map((test) => (
                <button
                  key={test.id}
                  type="button"
                  onClick={() => onSelectTest(test.id)}
                  disabled={activeTest?.id === test.id || isLoading}
                  className={`rounded-full px-2.5 py-1 text-[0.65rem] font-bold transition sm:px-3 sm:py-1.5 sm:text-xs ${
                    activeTest?.id === test.id
                      ? 'bg-ink text-white'
                      : 'bg-coffee/10 text-coffee hover:bg-coffee/15'
                  }`}
                >
                  {normalizeMojibake(test.name)}
                </button>
              ))}
            </div>
          )}

          <p className="mt-4 hidden text-xs leading-5 text-muted sm:block">
            Guardamos un token temporal en cookies para asociar tus respuestas con este intento.
          </p>
        </div>

        <div className="relative order-1 min-h-[9rem] bg-ink sm:min-h-[16rem] lg:order-2 lg:min-h-full">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(201,138,94,0.4),transparent_35%),radial-gradient(circle_at_80%_10%,rgba(107,183,162,0.38),transparent_32%)]" />
          {activeTest?.image_url && (
            <img
              src={activeTest.image_url}
              alt={name}
              className="absolute inset-0 h-full w-full object-cover opacity-80 mix-blend-luminosity"
              loading="lazy"
            />
          )}
          <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink/90 to-transparent p-4 sm:p-10">
            <p className="font-display text-base italic leading-tight tracking-[-0.03em] text-white sm:text-2xl">
              Poné sus propuestas bajo la lupa.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
