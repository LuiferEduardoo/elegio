import axios from 'axios'

export const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'

/**
 * Test that drives the default experience (the test flow at /test and the
 * /match-electoral results). Defaults to the segunda-vuelta test (id 4); can be
 * overridden per environment via VITE_DEFAULT_TEST_ID.
 */
export const DEFAULT_TEST_ID = Number(import.meta.env.VITE_DEFAULT_TEST_ID ?? 4)

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10_000,
})
