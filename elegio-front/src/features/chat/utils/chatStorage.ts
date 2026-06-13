import type { ChatMessage } from '../types'

const MESSAGES_KEY = 'elegio_chat_messages'
const CHAT_ID_KEY = 'elegio_chat_id'

export function loadMessages(): ChatMessage[] | null {
  try {
    const raw = localStorage.getItem(MESSAGES_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? (parsed as ChatMessage[]) : null
  } catch {
    return null
  }
}

export function saveMessages(messages: ChatMessage[]): void {
  try {
    localStorage.setItem(MESSAGES_KEY, JSON.stringify(messages))
  } catch {
    // Storage may be unavailable (private mode, quota); the chat still works
    // in memory, it just won't survive a reload.
  }
}

export function loadChatId(): number | null {
  try {
    const raw = localStorage.getItem(CHAT_ID_KEY)
    return raw ? Number(raw) || null : null
  } catch {
    return null
  }
}

export function saveChatId(chatId: number): void {
  try {
    localStorage.setItem(CHAT_ID_KEY, String(chatId))
  } catch {
    // See saveMessages.
  }
}

export function clearStoredChat(): void {
  try {
    localStorage.removeItem(MESSAGES_KEY)
    localStorage.removeItem(CHAT_ID_KEY)
  } catch {
    // See saveMessages.
  }
}
