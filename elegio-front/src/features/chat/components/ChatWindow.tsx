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
  const scrollRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

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
    <div className="flex h-[32rem] max-h-[70vh] w-[22rem] max-w-[calc(100vw-3rem)] animate-fade-in flex-col overflow-hidden rounded-2xl bg-white shadow-2xl ring-1 ring-black/10">
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
          aria-label="Cerrar chat"
          onClick={onClose}
          className="flex h-8 w-8 items-center justify-center rounded-full text-lg text-white/90 transition-colors hover:bg-white/15"
        >
          ×
        </button>
      </header>

      <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto bg-surface px-4 py-4">
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

      <div className="flex items-end gap-2 border-t border-black/5 bg-white px-3 py-3">
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
