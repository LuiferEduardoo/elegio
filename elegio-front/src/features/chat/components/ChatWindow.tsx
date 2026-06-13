import { useEffect, useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'

import type { ChatMessage } from '../types'

type ChatWindowProps = {
  onClose: () => void
  messages: ChatMessage[]
  isStreaming: boolean
  error: string | null
  sendMessage: (content: string) => void
}

export function ChatWindow({
  onClose,
  messages,
  isStreaming,
  error,
  sendMessage,
}: ChatWindowProps) {
  const [input, setInput] = useState('')
  const [isFullscreen, setIsFullscreen] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    inputRef.current?.focus({ preventScroll: true })
  }, [])

  // While fullscreen, lock the underlying page so its scrollbar doesn't show
  // (and scroll) behind the overlay.
  useEffect(() => {
    if (!isFullscreen) return
    const previous = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = previous
    }
  }, [isFullscreen])

  const handleSubmit = () => {
    const content = input.trim()
    if (!content || isStreaming) return
    void sendMessage(content)
    setInput('')
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div
      className={`flex animate-fade-in flex-col overflow-hidden bg-white shadow-2xl ring-1 ring-black/10 ${
        isFullscreen
          ? 'fixed inset-0 z-50 rounded-none'
          : 'h-[32rem] max-h-[70vh] w-[25rem] max-w-[calc(100vw-3rem)] rounded-2xl'
      }`}
    >
      <header
        className="flex items-center gap-3 px-4 py-3 text-white"
        style={{ backgroundColor: '#2563eb' }}
      >
        <span className="flex h-9 w-9 items-center justify-center overflow-hidden rounded-full bg-white/15">
          <img src="/logo-emma.webp" alt="Emma" className="h-full w-full scale-[1.7] object-contain" />
        </span>
        <div className="flex-1 leading-tight">
          <p className="font-semibold">Emma</p>
          <p className="text-xs text-white/80">Verifica las propuestas</p>
        </div>
        <button
          type="button"
          aria-label={isFullscreen ? 'Salir de pantalla completa' : 'Pantalla completa'}
          onClick={() => setIsFullscreen((prev) => !prev)}
          className="flex h-8 w-8 items-center justify-center rounded-full text-white/90 transition-colors hover:bg-white/15"
        >
          <svg viewBox="0 0 24 24" fill="none" className="h-4 w-4" aria-hidden="true">
            {isFullscreen ? (
              <path
                d="M9 4v3a2 2 0 01-2 2H4m16 0h-3a2 2 0 01-2-2V4M4 15h3a2 2 0 012 2v3m6 0v-3a2 2 0 012-2h3"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            ) : (
              <path
                d="M4 9V6a2 2 0 012-2h3m6 0h3a2 2 0 012 2v3m0 6v3a2 2 0 01-2 2h-3m-6 0H6a2 2 0 01-2-2v-3"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            )}
          </svg>
        </button>
        <button
          type="button"
          aria-label="Cerrar chat"
          onClick={onClose}
          className="flex h-8 w-8 items-center justify-center rounded-full text-white/90 transition-colors hover:bg-white/15"
        >
          <svg viewBox="0 0 24 24" fill="none" className="h-4 w-4" aria-hidden="true">
            <path
              d="M6 6l12 12M18 6L6 18"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </header>

      <div ref={scrollRef} className="flex-1 overflow-y-auto bg-surface px-4 py-4">
        <div className={`space-y-3 ${isFullscreen ? 'mx-auto w-full max-w-3xl' : ''}`}>
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-3 py-2 text-sm leading-snug ${
                  message.role === 'user'
                    ? 'whitespace-pre-wrap rounded-br-sm text-white'
                    : 'chat-markdown rounded-bl-sm bg-white text-ink ring-1 ring-black/5'
                }`}
                style={message.role === 'user' ? { backgroundColor: '#2563eb' } : undefined}
              >
                {message.role === 'user' ? (
                  message.content
                ) : message.content ? (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                ) : (
                  isStreaming && '…'
                )}
              </div>
            </div>
          ))}
          {error && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-xs text-red-600">{error}</p>
          )}
        </div>
      </div>

      <div
        className={`flex items-end gap-2 border-t border-black/5 bg-white px-3 py-3 ${
          isFullscreen ? 'mx-auto w-full max-w-3xl' : ''
        }`}
      >
        <textarea
          ref={inputRef}
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder="Escribe tu pregunta…"
          className="max-h-28 flex-1 resize-none rounded-xl bg-surface px-3 py-2 text-sm text-ink outline-none ring-1 ring-black/10 focus:ring-2 focus:ring-clay"
        />
        <button
          type="button"
          aria-label="Enviar mensaje"
          onClick={handleSubmit}
          disabled={!input.trim() || isStreaming}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-white transition-opacity disabled:opacity-40"
          style={{ backgroundColor: '#2563eb' }}
        >
          <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5">
            <path
              d="M3.4 20.4l17.45-7.48a1 1 0 000-1.84L3.4 3.6a.5.5 0 00-.7.58L4.5 11 13 12l-8.5 1-1.8 6.82a.5.5 0 00.7.58z"
              fill="currentColor"
            />
          </svg>
        </button>
      </div>
    </div>
  )
}
