const VISITOR_TOKEN_COOKIE = 'elegio_visitor_token'
const THIRTY_DAYS_IN_SECONDS = 60 * 60 * 24 * 30

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
