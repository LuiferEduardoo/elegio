import { NavBar } from '../features/home/components/NavBar'
import { Footer } from '../components/Footer'

export function PrivacyPolicyPage() {
  return (
    <div className="flex min-h-screen flex-col bg-surface text-ink">
      <NavBar />

      <main className="mx-auto w-full max-w-3xl flex-grow px-6 py-16 sm:px-10 lg:px-16">
        <header className="mb-12">
          <p className="text-sm font-black uppercase tracking-[0.3em] text-clay">
            Legal
          </p>
          <h1 className="mt-3 font-display text-4xl leading-[1.05] tracking-[-0.04em] text-ink sm:text-5xl">
            Política de Privacidad
          </h1>
          <p className="mt-4 text-base leading-7 text-muted">
            Última actualización: {new Date().toLocaleDateString('es-ES', { month: 'long', year: 'numeric' })}
          </p>
        </header>

        <article className="max-w-none text-muted">
          <p className="text-base leading-7">
            En Elegio creemos en la transparencia total, no solo en la política, sino también en cómo manejamos los datos de nuestros usuarios. Esta Política de Privacidad explica qué información recopilamos, cómo la usamos y los derechos que tienes sobre ella. 
            <strong className="text-ink"> Resumen: no recopilamos datos personales identificables y tus respuestas son anónimas.</strong>
          </p>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            1. Información que recopilamos
          </h2>
          <p className="mt-4 text-base leading-7">
            Cuando utilizas nuestra plataforma (la herramienta del "Match electoral" o el asistente Emma), recopilamos la siguiente información técnica y de uso:
          </p>
          <ul className="mt-4 flex flex-col gap-2 pl-5 list-disc text-base leading-7">
            <li><strong className="text-ink">Respuestas del test:</strong> Las opciones que seleccionas en cada pregunta de afinidad política.</li>
            <li><strong className="text-ink">Conversaciones con Emma:</strong> Si usas el asistente, guardamos los mensajes que escribes y las respuestas que genera, asociados únicamente a tu token anónimo, para mantener el contexto de la conversación. Por eso te recomendamos no compartir datos personales o sensibles en el chat.</li>
            <li><strong className="text-ink">Métricas de uso:</strong> El tiempo que tardas en responder cada pregunta (para análisis estadístico y detección de bots).</li>
            <li><strong className="text-ink">Tokens de sesión:</strong> Un identificador alfanumérico anónimo (guardado en una cookie) que nos permite vincular tus respuestas y conversaciones temporalmente para calcular tu resultado final, mantener tu chat y permitirte reanudar el test o la conversación si cierras la página.</li>
            <li><strong className="text-ink">Datos de registro estándar:</strong> Como la mayoría de los sitios web, nuestros servidores pueden registrar tu dirección IP (solo temporalmente para prevención de ataques DDoS y límite de peticiones), tipo de navegador y páginas visitadas.</li>
          </ul>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            2. Lo que NO recopilamos
          </h2>
          <p className="mt-4 text-base leading-7">
            Para garantizar tu privacidad y libertad ideológica:
          </p>
          <ul className="mt-4 flex flex-col gap-2 pl-5 list-disc text-base leading-7">
            <li><strong className="text-ink">No te pedimos registrarte:</strong> No recolectamos tu nombre, correo electrónico, ni números de teléfono.</li>
            <li><strong className="text-ink">No creamos perfiles publicitarios:</strong> Tus datos de afinidad política no se venden ni se comparten con redes de anuncios, partidos políticos o terceros.</li>
          </ul>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            3. Uso de la información
          </h2>
          <p className="mt-4 text-base leading-7">
            Los datos anónimos que recogemos se utilizan exclusivamente para:
          </p>
          <ul className="mt-4 flex flex-col gap-2 pl-5 list-disc text-base leading-7">
            <li>Calcular matemáticamente tu afinidad con las propuestas de cada candidatura.</li>
            <li>Generar las respuestas del asistente Emma a partir de tus preguntas y de las fuentes recuperadas.</li>
            <li>Mejorar la herramienta (por ejemplo, analizar si una pregunta es muy confusa basada en el tiempo de respuesta).</li>
            <li>Generar estadísticas agregadas y completamente anónimas sobre las tendencias generales de los usuarios (ej. "El 40% de los usuarios está a favor de la medida X"), sin que se pueda identificar a ningún individuo.</li>
          </ul>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            4. Retención de los datos
          </h2>
          <p className="mt-4 text-base leading-7">
            Tus respuestas y conversaciones se almacenan en nuestra base de datos asociadas únicamente a un token aleatorio. Como no existe manera de vincular este token con tu identidad real, los datos se consideran agregados y anónimos desde el momento de su captura.
          </p>
          <p className="mt-4 text-base leading-7">
            Además, tu historial de chat con Emma se guarda en el almacenamiento local de tu navegador para que la conversación sobreviva a una recarga. Puedes borrarlo en cualquier momento desde el propio chat (botón de "nueva conversación") o limpiando los datos de navegación de tu dispositivo.
          </p>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            5. Servicios de terceros e inteligencia artificial
          </h2>
          <p className="mt-4 text-base leading-7">
            El asistente Emma se apoya en modelos de inteligencia artificial de Google (Gemini). Para generar una respuesta, el texto de tu pregunta y los fragmentos de fuentes recuperados se envían a Google como proveedor de procesamiento. No enviamos tu token ni ningún dato que te identifique; aun así, evita compartir información personal o sensible en el chat, ya que su contenido se procesa fuera de nuestros servidores.
          </p>

          <h2 className="mt-10 font-display text-2xl tracking-[-0.03em] text-ink">
            6. Contacto
          </h2>
          <p className="mt-4 text-base leading-7">
            Elegio es un proyecto de código abierto. Si tienes dudas, sugerencias o preocupaciones sobre cómo manejamos la privacidad de esta plataforma, puedes contactarnos a través de:{' '}
            <a href="mailto:contacto@elegio.luifereduardoo.com" className="font-semibold text-clay transition hover:text-jade">
              contacto@elegio.luifereduardoo.com
            </a>
          </p>
        </article>
      </main>

      <Footer />
    </div>
  )
}
