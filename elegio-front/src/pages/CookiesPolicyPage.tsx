import { NavBar } from '../features/home/components/NavBar'
import { Footer } from '../components/Footer'

export function CookiesPolicyPage() {
  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />

      <main className="mx-auto w-full max-w-3xl flex-grow px-6 py-16 sm:px-10 lg:px-16">
        <header className="mb-12">
          <p className="text-sm font-black uppercase tracking-[0.3em] text-clay">
            Legal
          </p>
          <h1 className="mt-3 font-display text-4xl leading-[1.05] tracking-[-0.04em] text-ink sm:text-5xl">
            Política de Cookies
          </h1>
        </header>

        <article className="max-w-none text-muted">
          <p className="text-base leading-7">
            Esta Política de Cookies explica qué son las cookies y cómo las usamos en Elegio. 
            Nuestro objetivo es recopilar la menor cantidad de información posible. Por ello, solo utilizamos cookies estrictamente necesarias para que la herramienta principal funcione correctamente.
          </p>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            1. ¿Qué son las cookies?
          </h2>
          <p className="mt-4 text-base leading-7">
            Una cookie es un pequeño archivo de texto que un sitio web guarda en tu ordenador o dispositivo móvil cuando lo visitas. Permiten que el sitio web recuerde tus acciones y preferencias durante un período de tiempo.
          </p>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            2. ¿Qué tipo de cookies utilizamos?
          </h2>
          <p className="mt-4 text-base leading-7">
            En Elegio <strong className="text-ink">no usamos cookies de rastreo, de terceros ni con fines publicitarios.</strong> 
            Únicamente utilizamos una cookie técnica y estrictamente necesaria:
          </p>
          
          <div className="mt-6 overflow-hidden rounded-2xl border border-coffee/10 bg-white shadow-sm">
            <table className="w-full text-left text-sm">
              <thead className="bg-surface/50 font-bold text-ink border-b border-coffee/10">
                <tr>
                  <th className="px-4 py-3">Nombre de la Cookie</th>
                  <th className="px-4 py-3">Propósito</th>
                  <th className="px-4 py-3">Duración</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-coffee/10 text-muted">
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">elegio_test_token</td>
                  <td className="px-4 py-3">
                    Identificador anónimo temporal. Se utiliza exclusivamente para guardar el progreso de tu "Match electoral" (el test) y poder calcular tus resultados finales. 
                    Sin esta cookie, perderías tu progreso en el test al recargar la página.
                  </td>
                  <td className="px-4 py-3">1 mes</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            3. Cómo gestionar las cookies
          </h2>
          <p className="mt-4 text-base leading-7">
            Dado que la única cookie que utilizamos es estrictamente necesaria para el funcionamiento del test de afinidad, no requiere de consentimiento previo según las normativas de privacidad (como el RGPD o leyes locales). Sin embargo, siempre puedes configurar tu navegador para bloquearla. Ten en cuenta que si la bloqueas, no podrás realizar el "Match electoral" correctamente.
          </p>
          
          <p className="mt-4 text-base leading-7">
            Si deseas eliminar la cookie en cualquier momento, puedes hacerlo desde las opciones de privacidad y seguridad de los ajustes de tu navegador, o simplemente completando el test, tras lo cual la aplicación suele limpiar la sesión de forma automática.
          </p>
        </article>
      </main>

      <Footer />
    </div>
  )
}
