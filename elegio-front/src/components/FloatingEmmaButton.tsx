import { useEffect, useState } from 'react'

import { ChatWindow } from '../features/chat/components/ChatWindow'
import { useEmmaChat } from '../features/chat/hooks/useEmmaChat'

const EMMA_MESSAGES = [
  'Evita la desinformación. Pregúntale a Emma y descubre qué es real en las propuestas de los candidatos.',
  'Que no te manipulen. Chatea con Emma, contrasta los datos y vota con la verdad.',
  'Protege tu voto de los mitos. Habla con Emma y verifica qué candidatos dicen la verdad.',
  '¿Información real o manipulación? Pregúntale a Emma y sal de dudas.',
  '¿Es real o engañoso? Verifícalo con Emma.',
  '¿Qué propuesta quieres verificar hoy? Pregúntale a Emma.',
]

const MESSAGE_INTERVAL_MS = 12000
const MESSAGE_EXIT_MS = 300

export function FloatingEmmaButton() {
  const [messageIndex, setMessageIndex] = useState(
    () => Math.floor(Math.random() * EMMA_MESSAGES.length),
  )
  const [isExiting, setIsExiting] = useState(false)
  const [showBubble, setShowBubble] = useState(true)
  const [isOpen, setIsOpen] = useState(false)
  const chat = useEmmaChat()

  useEffect(() => {
    if (!showBubble || isOpen) return

    const timer = setInterval(() => {
      setIsExiting(true)
    }, MESSAGE_INTERVAL_MS)

    return () => clearInterval(timer)
  }, [showBubble, isOpen])

  useEffect(() => {
    if (!isExiting) return

    const timer = setTimeout(() => {
      setMessageIndex((prev) => (prev + 1) % EMMA_MESSAGES.length)
      setIsExiting(false)
    }, MESSAGE_EXIT_MS)

    return () => clearTimeout(timer)
  }, [isExiting])

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      {isOpen ? (
        <ChatWindow
          onClose={() => setIsOpen(false)}
          messages={chat.messages}
          isStreaming={chat.isStreaming}
          error={chat.error}
          sendMessage={chat.sendMessage}
        />
      ) : (
        showBubble && (
          <div className="relative mr-1 max-w-xs animate-fade-in rounded-2xl rounded-br-sm bg-white px-4 py-3 text-sm text-ink shadow-xl ring-1 ring-black/5">
            <button
              type="button"
              aria-label="Cerrar mensaje"
              onClick={() => setShowBubble(false)}
              className="absolute -left-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full bg-white text-sm text-muted shadow ring-1 ring-black/5 transition-transform hover:scale-110"
            >
              ×
            </button>
            <p
              key={messageIndex}
              className={`leading-snug ${isExiting ? 'animate-message-out' : 'animate-message-swap'}`}
            >
              {EMMA_MESSAGES[messageIndex]}
            </p>
            <span className="absolute -bottom-1.5 right-5 h-3 w-3 rotate-45 bg-white" />
          </div>
        )
      )}

      <button
        type="button"
        aria-label={isOpen ? 'Cerrar asistente Emma' : 'Abrir asistente Emma'}
        onClick={() => setIsOpen((prev) => !prev)}
        className="group relative flex h-16 w-16 shrink-0 items-center justify-center overflow-hidden rounded-full shadow-lg transition-all duration-300 hover:scale-105 hover:shadow-[0_0_25px_4px_rgba(37,99,235,0.6)] focus:outline-none focus-visible:ring-4 focus-visible:ring-white/40"
        style={{ backgroundColor: '#2563eb' }}
      >
        <img
          src="/logo-emma.webp"
          alt="Emma"
          className="h-full w-full scale-[1.7] object-contain"
        />
        <span className="pointer-events-none absolute inset-0 -translate-x-full -skew-x-12 bg-gradient-to-r from-transparent via-white/50 to-transparent transition-transform duration-700 ease-out group-hover:translate-x-full" />
      </button>
    </div>
  )
}
