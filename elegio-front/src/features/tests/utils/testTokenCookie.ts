const TEST_TOKEN_COOKIE = 'elegio_test_token'
const THIRTY_DAYS_IN_SECONDS = 60 * 60 * 24 * 30

export function getTestTokenCookie(): string | null {
  const tokenCookie = document.cookie
    .split('; ')
    .find((cookie) => cookie.startsWith(`${TEST_TOKEN_COOKIE}=`))

  if (!tokenCookie) return null

  return decodeURIComponent(tokenCookie.split('=').slice(1).join('='))
}

export function setTestTokenCookie(token: string): void {
  document.cookie = `${TEST_TOKEN_COOKIE}=${encodeURIComponent(
    token,
  )}; Max-Age=${THIRTY_DAYS_IN_SECONDS}; Path=/; SameSite=Lax`
}

export function clearTestTokenCookie(): void {
  document.cookie = `${TEST_TOKEN_COOKIE}=; Max-Age=0; Path=/; SameSite=Lax`
}
