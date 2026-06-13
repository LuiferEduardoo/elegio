import { useCallback, useEffect, useRef, useState } from 'react'

import {
  CHAT_ERROR_MESSAGE,
  createChat,
  createVisitorToken,
  streamMessage,
} from '../api/chatApi'
import type { ChatMessage } from '../types'
import {
  loadChatId,
  loadMessages,
  saveChatId,
  saveMessages,
} from '../utils/chatStorage'
import {
  getVisitorTokenCookie,
  setVisitorTokenCookie,
} from '../utils/visitorTokenCookie'

const WELCOME_MESSAGE: ChatMessage = {
  id: 'welcome',
  role: 'assistant',
  content:
    '¡Hola! Soy Emma. Pregúntame por las propuestas de los candidatos y te ayudo a contrastar qué es real. ¿Qué quieres verificar?',
}

function createId(): string {
  return crypto.randomUUID()
}

export function useEmmaChat() {
  const [messages, setMessages] = useState<ChatMessage[]>(
    () => loadMessages() ?? [WELCOME_MESSAGE],
  )
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const tokenRef = useRef<string | null>(null)
  const chatIdRef = useRef<number | null>(loadChatId())

  // Typewriter reveal: the network fills `targetRef` (often in large chunks),
  // while a requestAnimationFrame loop copies it into the visible message a few
  // characters at a time, so the answer appears progressively word by word.
  const targetRef = useRef('')
  const shownRef = useRef('')
  const streamDoneRef = useRef(false)
  const activeIdRef = useRef<string | null>(null)
  const frameRef = useRef<number | null>(null)
  const revealRef = useRef<() => void>(() => {})

  const stopReveal = useCallback(() => {
    if (frameRef.current !== null) {
      cancelAnimationFrame(frameRef.current)
      frameRef.current = null
    }
  }, [])

  const reveal = useCallback(() => {
    const id = activeIdRef.current
    if (id === null) {
      frameRef.current = null
      return
    }

    const target = targetRef.current
    if (shownRef.current.length < target.length) {
      const remaining = target.length - shownRef.current.length
      const step = Math.max(2, Math.ceil(remaining / 10))
      shownRef.current = target.slice(0, shownRef.current.length + step)
      const next = shownRef.current
      setMessages((prev) =>
        prev.map((message) =>
          message.id === id ? { ...message, content: next } : message,
        ),
      )
    }

    const caughtUp = shownRef.current.length >= targetRef.current.length
    if (!caughtUp || !streamDoneRef.current) {
      frameRef.current = requestAnimationFrame(() => revealRef.current())
    } else {
      frameRef.current = null
      activeIdRef.current = null
      setIsStreaming(false)
    }
  }, [])

  useEffect(() => {
    revealRef.current = reveal
  }, [reveal])

  // Persist once a turn settles, so the typewriter's per-frame updates don't
  // thrash localStorage and only completed text is stored.
  useEffect(() => {
    if (!isStreaming) saveMessages(messages)
  }, [messages, isStreaming])

  const ensureSession = useCallback(async () => {
    if (!tokenRef.current) {
      const existing = getVisitorTokenCookie()
      tokenRef.current = existing ?? (await createVisitorToken())
      if (!existing) setVisitorTokenCookie(tokenRef.current)
    }
    if (chatIdRef.current === null) {
      const chat = await createChat(tokenRef.current)
      chatIdRef.current = chat.id
      saveChatId(chat.id)
    }
    return { token: tokenRef.current, chatId: chatIdRef.current }
  }, [])

  const sendMessage = useCallback(
    async (rawContent: string) => {
      const content = rawContent.trim()
      if (!content || isStreaming) return

      setError(null)
      setIsStreaming(true)

      const userMessage: ChatMessage = { id: createId(), role: 'user', content }
      const assistantId = createId()
      setMessages((prev) => [
        ...prev,
        userMessage,
        { id: assistantId, role: 'assistant', content: '' },
      ])

      targetRef.current = ''
      shownRef.current = ''
      streamDoneRef.current = false
      activeIdRef.current = assistantId
      stopReveal()
      frameRef.current = requestAnimationFrame(() => revealRef.current())

      try {
        const { token, chatId } = await ensureSession()
        await streamMessage(token, chatId, content, {
          onToken: (delta) => {
            targetRef.current += delta
          },
          onError: (detail) => {
            setError(detail)
          },
        })
      } catch {
        setError(CHAT_ERROR_MESSAGE)
      } finally {
        streamDoneRef.current = true
        if (targetRef.current.length === 0) {
          // Nothing came back (e.g. a server error event): drop the empty
          // assistant bubble and stop the reveal loop right away.
          stopReveal()
          activeIdRef.current = null
          setMessages((prev) => prev.filter((m) => m.id !== assistantId))
          setIsStreaming(false)
        }
      }
    },
    [ensureSession, isStreaming, stopReveal],
  )

  return { messages, isStreaming, error, sendMessage }
}
