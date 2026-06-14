import { API_BASE_URL, apiClient } from '../../../config/api'
import type { ChatRead, ChatSource, StreamHandlers } from '../types'

export const CHAT_ERROR_MESSAGE =
  'No pudimos conectar con Emma.'

export async function createChat(token: string): Promise<ChatRead> {
  const response = await apiClient.post<ChatRead>(
    '/api/v1/chats',
    {},
    { headers: { Authorization: `Bearer ${token}` } },
  )
  return response.data
}

function dispatchEvent(rawEvent: string, handlers: StreamHandlers): void {
  let eventName = 'message'
  const dataLines: string[] = []

  for (const line of rawEvent.split('\n')) {
    if (line.startsWith('event:')) {
      eventName = line.slice('event:'.length).trim()
    } else if (line.startsWith('data:')) {
      dataLines.push(line.slice('data:'.length).trim())
    }
  }

  if (dataLines.length === 0) return

  const data = JSON.parse(dataLines.join('\n'))

  switch (eventName) {
    case 'sources':
      handlers.onSources?.(data as ChatSource[])
      break
    case 'token':
      handlers.onToken(data.delta as string)
      break
    case 'title':
      handlers.onTitle?.(data.title as string)
      break
    case 'error':
      handlers.onError(data.detail as string)
      break
    // 'done' carries the persisted messages; the UI already has the
    // streamed text, so there is nothing extra to render.
    default:
      break
  }
}

export async function streamMessage(
  token: string,
  chatId: number,
  content: string,
  handlers: StreamHandlers,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/v1/chats/${chatId}/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'text/event-stream',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ content }),
    signal,
  })

  if (!response.ok || !response.body) {
    throw new Error(CHAT_ERROR_MESSAGE)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, '\n')
    const events = buffer.split('\n\n')
    buffer = events.pop() ?? ''

    for (const rawEvent of events) {
      if (rawEvent.trim()) dispatchEvent(rawEvent, handlers)
    }
  }

  if (buffer.trim()) dispatchEvent(buffer, handlers)
}
