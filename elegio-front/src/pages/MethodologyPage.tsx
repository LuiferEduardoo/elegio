import { NavBar } from '../features/home/components/NavBar'
import { Footer } from '../components/Footer'

type Step = {
  number: string
  title: string
  body: string
}

const STEPS: Step[] = [
  {
    number: '01',
    title: 'Recolección',
    body:
      'Leemos los planes de gobierno publicados oficialmente por cada candidatura y extraemos sus propuestas frase por frase. Cada propuesta queda vinculada a la fuente original (PDF, sitio oficial o pronunciamiento público) para que cualquiera pueda auditarla.',
  },
  {
    number: '02',
    title: 'Clasificación por categoría',
    body:
      'Cada propuesta se asigna a una categoría temática (economía, salud, seguridad, ambiente, etc.) con una rúbrica pública. La categoría define el eje sobre el cual la propuesta será posicionada en un rango de -1.0 a +1.0.',
  },
  {
    number: '03',
    title: 'Posicionamiento descriptivo',
    body:
      'Un modelo de lenguaje (Google Gemini) lee la propuesta junto con la rúbrica de su categoría y emite una puntuación, una explicación y un nivel de confianza. Cada puntuación queda etiquetada como "llm" y puede ser revisada o sustituida por revisión humana ("human") sin perder el historial.',
  },
  {
    number: '04',
    title: 'Búsqueda híbrida',
    body:
      'El buscador combina búsqueda semántica (embeddings multilingüe-e5-large sobre Qdrant) con búsqueda léxica (BM25). Los dos rankings se fusionan con Reciprocal Rank Fusion (RRF, k=60) para que un término exacto y una intención parecida pesen ambos.',
  },
  {
    number: '05',
    title: 'Test de afinidad',
    body:
      'El test compara tus respuestas con las posiciones agregadas de cada candidatura por categoría. No te dice por quién votar: te muestra qué tan cerca o lejos quedan las propuestas de cada fórmula respecto a tus posturas, ponderando por la importancia que vos diste a cada tema.',
  },
]

type Formula = {
  name: string
  expression: string
  usage: string
}

const FORMULAS: Formula[] = [
  {
    name: 'Promedio por categoría',
    expression: 'avg(c) = (Σ pᵢ) / N',
    usage:
      'Por cada candidato y cada categoría promediamos los axis_value (-1.0 / +1.0) de sus propuestas. Es lo que ves en las tarjetas: el "centro de masa" de su discurso en ese eje.',
  },
  {
    name: 'Embedding multilingüe',
    expression: 'e(t) = E(t) ∈ ℝ¹⁰²⁴',
    usage:
      'Cada propuesta y cada consulta se convierten en un vector de 1024 dimensiones usando multilingual-e5-large. Los vectores capturan significado, no solo palabras, así una búsqueda por "pensión" también encuentra "jubilación".',
  },
  {
    name: 'Similitud coseno',
    expression: 'cos(q, p) = (q · p) / (‖q‖ ‖p‖)',
    usage:
      'Qdrant ordena los chunks de propuestas por similitud coseno entre el embedding de tu consulta y los embeddings precalculados. Es la base del ranking semántico.',
  },
  {
    name: 'BM25',
    expression: 'score(d, q) = Σ IDF(t) · tf · (k₁+1) / (tf + k₁(1 − b + b·|d|/avgdl))',
    usage:
      'Ranking léxico clásico: premia documentos que contienen los términos exactos de la consulta, ajustando por frecuencia y longitud del documento. Usado en paralelo al semántico para no perder coincidencias literales.',
  },
  {
    name: 'Reciprocal Rank Fusion (RRF)',
    expression: 'score(p) = Σᵢ 1 / (k + rankᵢ(p)),  k = 60',
    usage:
      'Combinamos el ranking semántico y el léxico sumando 1/(60 + rango) en cada lista. El parámetro k=60 amortigua el peso de los rangos altos. Esto permite fusionar dos algoritmos con escalas distintas sin tener que calibrarlos.',
  },
  {
    name: 'Distancia de Manhattan ponderada (resultado del test)',
    expression:
      'd(u, c) = Σₖ wₖ · |uₖ − cₖ|\nafinidad(u, c) = 1 − d(u, c) / (2 · Σₖ wₖ)',
    usage:
      'Tu afinidad con cada candidato se calcula como la distancia de Manhattan ponderada entre tu vector de respuestas y el suyo, categoría por categoría. uₖ es tu posición promedio en la categoría k, cₖ la del candidato (promedio de sus postures) y wₖ el peso de esa categoría. Dividimos entre la distancia máxima posible (2·Σwₖ, porque cada eje vive en [−1, +1]) para que el resultado quede en [0, 1] y lo mostramos como porcentaje: 100% es coincidencia perfecta, 0% es oposición total. Elegimos Manhattan en vez de euclidiana para que cada categoría aporte de forma lineal, sin penalizar desproporcionadamente desacuerdos grandes en un solo eje.',
  },
]

const PRINCIPLES: { title: string; body: string }[] = [
  {
    title: 'Trazabilidad',
    body:
      'Cada cifra, posición o resumen tiene una fuente vinculada. Si no podemos vincularla, no la publicamos.',
  },
  {
    title: 'Descriptivo, no prescriptivo',
    body:
      'Los ejes -1.0/+1.0 describen la dirección de la propuesta dentro de su categoría. No son "bueno" o "malo".',
  },
  {
    title: 'Reversibilidad',
    body:
      'Las posturas generadas por IA pueden ser sobrescritas por revisión humana, manteniendo el historial completo.',
  },
  {
    title: 'Open data',
    body:
      'El código del API, el frontend y el pipeline de análisis están abiertos para inspección y crítica.',
  },
]

export function MethodologyPage() {
  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />

      <main className="mx-auto w-full max-w-4xl flex-grow px-6 py-16 sm:px-10 lg:px-16">

        <header className="mb-14">
          <p className="text-sm font-black uppercase tracking-[0.3em] text-clay">
            Metodología
          </p>
          <h1 className="mt-3 font-display text-4xl leading-[1.05] tracking-[-0.04em] text-ink sm:text-5xl">
            Cómo construimos Elegio.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-muted">
            Elegio no es una opinión: es un pipeline auditable que convierte planes de
            gobierno en datos comparables. Acá explicamos cada paso, sus límites y por
            qué tomamos cada decisión.
          </p>
        </header>

        <section aria-labelledby="pipeline" className="mb-16">
          <h2 id="pipeline" className="font-display text-2xl tracking-[-0.03em] text-ink">
            El pipeline, paso a paso
          </h2>
          <ol className="mt-6 flex flex-col gap-4">
            {STEPS.map((step) => (
              <li
                key={step.number}
                className="rounded-3xl border border-coffee/10 bg-white p-6 shadow-sm shadow-coffee/5"
              >
                <div className="flex items-baseline gap-4">
                  <span className="font-display text-3xl font-black tabular-nums text-clay">
                    {step.number}
                  </span>
                  <h3 className="font-display text-xl tracking-[-0.02em] text-ink">
                    {step.title}
                  </h3>
                </div>
                <p className="mt-3 text-sm leading-7 text-muted">{step.body}</p>
              </li>
            ))}
          </ol>
        </section>

        <section aria-labelledby="formulas" className="mb-16">
          <h2 id="formulas" className="font-display text-2xl tracking-[-0.03em] text-ink">
            Funciones matemáticas que usamos
          </h2>
          <p className="mt-3 max-w-2xl text-sm leading-7 text-muted">
            Las fórmulas que están detrás del posicionamiento, la búsqueda y los
            promedios. Las dejamos explícitas para que cualquiera pueda auditar o
            cuestionar el resultado.
          </p>
          <ul className="mt-6 flex flex-col gap-4">
            {FORMULAS.map((formula) => (
              <li
                key={formula.name}
                className="rounded-3xl border border-coffee/10 bg-white p-6 shadow-sm shadow-coffee/5"
              >
                <h3 className="font-display text-lg tracking-[-0.02em] text-ink">
                  {formula.name}
                </h3>
                <pre className="mt-3 overflow-x-auto rounded-2xl border border-coffee/10 bg-surface/70 px-4 py-3 font-mono text-sm leading-6 text-coffee">
                  {formula.expression}
                </pre>
                <p className="mt-3 text-sm leading-7 text-muted">{formula.usage}</p>
              </li>
            ))}
          </ul>
        </section>

        <section aria-labelledby="principles" className="mb-16">
          <h2
            id="principles"
            className="font-display text-2xl tracking-[-0.03em] text-ink"
          >
            Principios
          </h2>
          <ul className="mt-6 grid gap-4 sm:grid-cols-2">
            {PRINCIPLES.map((principle) => (
              <li
                key={principle.title}
                className="rounded-3xl border border-coffee/10 bg-white p-6 shadow-sm shadow-coffee/5"
              >
                <h3 className="text-sm font-bold uppercase tracking-[0.2em] text-jade">
                  {principle.title}
                </h3>
                <p className="mt-3 text-sm leading-7 text-muted">{principle.body}</p>
              </li>
            ))}
          </ul>
        </section>

        <section
          aria-labelledby="limits"
          className="rounded-[2rem] border border-coffee/10 bg-white p-8 shadow-sm shadow-coffee/5"
        >
          <h2 id="limits" className="font-display text-2xl tracking-[-0.03em] text-ink">
            Lo que Elegio no es
          </h2>
          <ul className="mt-4 flex flex-col gap-3 text-sm leading-7 text-muted">
            <li>
              <strong className="font-bold text-ink">No es una recomendación de voto.</strong>{' '}
              Los resultados del test son una comparación entre tus respuestas y las
              propuestas, no un consejo electoral.
            </li>
            <li>
              <strong className="font-bold text-ink">No es un fact-check.</strong> Posicionamos lo que dicen los planes; no
              evaluamos su viabilidad fiscal, jurídica o técnica.
            </li>
            <li>
              <strong className="font-bold text-ink">No reemplaza la lectura directa.</strong>{' '}
              Cada propuesta enlaza a su fuente: usá la herramienta para llegar más
              rápido al plan, no para reemplazarlo.
            </li>
          </ul>
        </section>
      </main>
      <Footer />
    </div>
  )
}
