# Elegio — Frontend

Web client for [Elegio](../README.md): a non-partisan platform to explore 2026 presidential candidates, their proposals, and an affinity test. Built with Vite + React 19 and styled with Tailwind CSS v4. It talks to the [FastAPI backend](../api) over HTTP.

## 🚀 Tech stack

- **Vite 8** — build tool and dev server
- **React 19** + **TypeScript** — UI, with the **React Compiler** enabled (`babel-plugin-react-compiler`)
- **React Router 7** — client-side routing (`createBrowserRouter`)
- **Tailwind CSS v4** — styling (via `@tailwindcss/vite`)
- **axios** — HTTP client, configured once in [`src/config/api.ts`](src/config/api.ts)
- **react-markdown** — renders Emma's streamed assistant replies as Markdown
- **ESLint** — linting (`eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`)

## 📁 Project structure

```
elegio-front/
├── src/
│   ├── main.tsx              # Entry — mounts <App/> (RouterProvider)
│   ├── App.tsx               # RouterProvider with the app router
│   ├── config/
│   │   └── api.ts            # axios apiClient (baseURL from VITE_API_URL)
│   ├── routes/
│   │   ├── router.tsx        # Route table → pages, under RootLayout
│   │   └── paths.ts          # ROUTE_PATHS + buildCandidateDetailPath()
│   ├── pages/                # One component per route
│   ├── components/           # Shared UI (RootLayout, Footer, SpectrumMarker, FloatingEmmaButton)
│   ├── features/             # Feature modules (see below)
│   ├── utils/                # Cross-feature helpers (e.g. text.ts)
│   └── assets/
├── .env.example             # Documents VITE_API_URL
└── vite.config.ts
```

### Feature modules

Each feature under `src/features/<name>/` owns its slice and follows the same internal layout: `api/` (typed `apiClient` calls), `components/`, `hooks/`, `utils/`, and `types.ts`.

| Feature | Responsibility |
| ------- | -------------- |
| `home` | Landing page and shared `NavBar`. |
| `candidates` | Candidate list and detail, including per-category averages (raw `average` and rhetorical-weight `adjusted_average`). |
| `proposals` | Hybrid proposal search with candidate/category filters; state synced to the URL. |
| `electoral-vs` | Side-by-side candidate comparison by category; selection synced to the URL. |
| `government-plans` | Candidate government plan documents. |
| `tests` | Affinity test flow and results. |
| `chat` | Emma, the streaming chat assistant (see [Emma chatbot](#-emma-chatbot)). |

## 🧭 Routes

Defined in [`src/routes/paths.ts`](src/routes/paths.ts) and wired in [`src/routes/router.tsx`](src/routes/router.tsx); all render under `RootLayout`.

| Path | Page |
| ---- | ---- |
| `/` | `HomePage` |
| `/propuestas` | `ProposalsPage` |
| `/vs-electoral` | `ElectoralVsPage` |
| `/candidatos/:id` | `CandidateDetailPage` |
| `/metodologia` | `MethodologyPage` |
| `/test` | `TestPage` |
| `/resultados` | `ResultsPage` |
| `/privacidad` | `PrivacyPolicyPage` |
| `/cookies` | `CookiesPolicyPage` |

> **Shareable URLs.** `ProposalsPage` and `ElectoralVsPage` persist their filters in the query string via `useSearchParams` (`?q=`, `?candidates=1,2`, `?category=3`), so a search or comparison can be bookmarked and shared.

## 📦 Setup

### Prerequisites

- **Node.js 20+**
- The [API](../api) running and reachable (default `http://localhost:8000`).

### Install and configure

```bash
cd elegio-front
npm install
cp .env.example .env.local   # then edit VITE_API_URL if needed
```

### Run the dev server

```bash
npm run dev
```

Vite serves the app at `http://localhost:5173` by default.

## 🔧 Environment variables

Vite only exposes variables prefixed with `VITE_` to the client, and injects them at **build time** (not runtime) — set them before `npm run build`. See [.env.example](.env.example).

| Key | Default | Description |
| --- | ------- | ----------- |
| `VITE_API_URL` | `http://127.0.0.1:8000` | Base URL of the FastAPI backend, used by `apiClient`. |

## 🛠 Scripts

```bash
npm run dev       # Start the Vite dev server (HMR)
npm run build     # Type-check (tsc -b) and build for production into dist/
npm run preview   # Serve the production build locally
npm run lint      # Run ESLint
```

## 🔌 API integration

All requests go through the shared `apiClient` in [`src/config/api.ts`](src/config/api.ts) (axios instance with `baseURL = VITE_API_URL` and a 10s timeout). Feature `api/` modules call versioned endpoints under `/api/v1` and map errors to user-facing messages. Avoid `fetch`/bare `axios` in components — call a feature `api/` function instead.

### Auth flow (tests feature)

The affinity test uses an anonymous **visitor token** (no user accounts):

1. `createAuthToken()` posts the visitor/session metadata (language, timezone, screen, referer, …) to `POST /api/v1/auth/token` and receives a JWT bound to the visitor.
2. `initializeTestAttempt(testId, token)` calls `POST /api/v1/test-attempts/initialize` with the token as `Authorization: Bearer` to create the test attempt.
3. Protected calls (`/test-attempts`, `/answers`, `/answers/affinity`) send the same Bearer token; the API resolves the visitor's most recent attempt server-side.

The token is persisted in a cookie (`src/features/tests/utils/testTokenCookie.ts`) so an in-progress test survives a page reload.

## 🤖 Emma chatbot

Emma is the in-app assistant that helps visitors verify candidate proposals. It lives in [`src/features/chat/`](src/features/chat/) and is surfaced everywhere through [`src/components/FloatingEmmaButton.tsx`](src/components/FloatingEmmaButton.tsx), which `RootLayout` mounts on every route.

### UI

- A floating button (bottom-right, blue `#2563eb`, Emma logo at `/logo-emma.webp`) toggles the chat window.
- While closed, the button shows a rotating bubble of invitation messages (`EMMA_MESSAGES`), swapping every 12s; the bubble can be dismissed.
- The chat window ([`ChatWindow.tsx`](src/features/chat/components/ChatWindow.tsx)) supports a **fullscreen** mode. Open/fullscreen state is reflected in the URL via a `chat` query param (`?chat=open` / `?chat=full`), so the panel state is bookmarkable and survives back/forward navigation.
- Assistant messages are rendered as Markdown via `react-markdown`.

### Conversation flow

The chat reuses the anonymous **visitor token** described above, then streams replies over **Server-Sent Events (SSE)**. All of this is wrapped by the [`useEmmaChat`](src/features/chat/hooks/useEmmaChat.ts) hook, with the network layer in [`chatApi.ts`](src/features/chat/api/chatApi.ts):

1. **Visitor token** — `createVisitorToken()` posts visitor/session metadata to `POST /api/v1/auth/token` and returns a JWT. It is cached in the `elegio_visitor_token` cookie ([`visitorTokenCookie.ts`](src/features/chat/utils/visitorTokenCookie.ts), 30-day max-age) and reused on later visits.
2. **Create a chat** — `createChat(token)` calls `POST /api/v1/chats` with `Authorization: Bearer <token>` and returns the chat `id`.
3. **Stream a message** — `streamMessage(...)` `fetch`-es `POST /api/v1/chats/{id}/messages` with `Accept: text/event-stream` and reads the response body via a `ReadableStream` reader, parsing these SSE events:
   - `sources` — retrieved sources for the answer (`ChatSource[]`)
   - `token` — an incremental text delta
   - `title` — a generated chat title
   - `done` — turn finished (persisted server-side; nothing extra to render)
   - `error` — server-side error detail

`fetch` is used here (instead of the shared `apiClient`) because axios does not expose a streaming body — this is the documented exception to the "always use a feature `api/` function" rule.

### Typewriter reveal & cancellation

`useEmmaChat` buffers incoming `token` deltas into a target string and reveals it a few characters per `requestAnimationFrame`, so answers appear progressively even when the network delivers large chunks. `resetChat()` (new conversation) aborts any in-flight stream through an `AbortController`, clears state, and returns to the welcome message.

### Persistence

Messages and the active chat id are stored in `localStorage` (`elegio_chat_messages`, `elegio_chat_id`) via [`chatStorage.ts`](src/features/chat/utils/chatStorage.ts), so a conversation survives a reload. Writes happen once a turn settles (not per typewriter frame) to avoid thrashing storage. Storage failures (private mode, quota) degrade gracefully — the chat keeps working in memory.

## 🧹 Code style

- **Prettier** + **ESLint** for formatting and linting.
- **Conventional Commits** — `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`...
- Keep components in `components/`; colocate data fetching in the feature's `api/` and `hooks/`.
