import { apiClient } from '../../../config/api'
import { getOrCreateVisitorToken } from '../../../utils/visitorToken'

export type EventPayload = {
  event_type: string
  event_name?: string
  page_url?: string
  page_path?: string
  page_title?: string
  element_tag?: string
  element_id?: string
  element_class?: string
  element_text?: string
  scroll_depth?: number
  duration_ms?: number
  properties?: Record<string, unknown>
}

/**
 * Sends a usage event to the backend. Fire-and-forget: analytics must never
 * surface errors or block the UI, so failures are swallowed.
 */
export async function trackEvent(payload: EventPayload): Promise<void> {
  try {
    const token = await getOrCreateVisitorToken()
    await apiClient.post('/api/v1/events', payload, {
      headers: { Authorization: `Bearer ${token}` },
    })
  } catch {
    // Ignore — tracking is best-effort.
  }
}
