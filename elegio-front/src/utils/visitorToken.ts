import { apiClient } from '../config/api'

const VISITOR_TOKEN_COOKIE = 'elegio_visitor_token'
const THIRTY_DAYS_IN_SECONDS = 60 * 60 * 24 * 30

type AuthTokenResponse = {
  token: string
  visitor_id: number
}

export function getVisitorTokenCookie(): string | null {
  const tokenCookie = document.cookie
    .split('; ')
    .find((cookie) => cookie.startsWith(`${VISITOR_TOKEN_COOKIE}=`))

  if (!tokenCookie) return null

  return decodeURIComponent(tokenCookie.split('=').slice(1).join('='))
}

export function setVisitorTokenCookie(token: string): void {
  document.cookie = `${VISITOR_TOKEN_COOKIE}=${encodeURIComponent(
    token,
  )}; Max-Age=${THIRTY_DAYS_IN_SECONDS}; Path=/; SameSite=Lax`
}

export async function createVisitorToken(): Promise<string> {
  const response = await apiClient.post<AuthTokenResponse>('/api/v1/auth/token', {
    visitor: {
      primary_language: navigator.language,
      languages: navigator.languages ? Array.from(navigator.languages) : undefined,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      consent_given: true,
      screen_width: window.screen.width,
      screen_height: window.screen.height,
      pixel_ratio: window.devicePixelRatio,
    },
    session: {
      landing_page: window.location.pathname,
      referer: document.referrer || undefined,
      viewport_width: window.innerWidth,
      viewport_height: window.innerHeight,
    },
  })
  return response.data.token
}

/** Returns the cached visitor token, minting and persisting one if needed. */
export async function getOrCreateVisitorToken(): Promise<string> {
  const existing = getVisitorTokenCookie()
  if (existing) return existing

  const token = await createVisitorToken()
  setVisitorTokenCookie(token)
  return token
}
