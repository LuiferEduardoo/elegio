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
│   ├── utils/                # Cross-feature helpers (visitorToken.ts, smoothScroll.ts, text.ts)
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
| `tests` | Affinity test flows and results — both the classic `/test` and the `/match-electoral` match flow with video questions (see [Tests & Match electoral](#-tests--match-electoral)). |
| `chat` | Emma, the streaming chat assistant (see [Emma chatbot](#-emma-chatbot)). |
| `analytics` | Anonymous usage tracking — page views, clicks and scroll depth posted to `/api/v1/events` (see [Analytics](#-analytics)). |

> Cross-feature helpers (the shared visitor token, smooth-scroll, text utilities) live in [`src/utils/`](src/utils/) so the test, chat and analytics features can all reuse them — see [Visitor token](#-visitor-token).

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
| `/match-electoral` | `MatchElectoralPage` |
| `/resultados` | `ResultsPage` |
| `/privacidad` | `PrivacyPolicyPage` |
| `/cookies` | `CookiesPolicyPage` |

> `ROUTE_PATHS` also defines `/candidatos` (candidate list); `buildCandidateDetailPath(id)` builds the detail path.

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

### 🪪 Visitor token

There are no user accounts. Everything that needs the API to recognize a returning browser uses a single **anonymous visitor token** — a JWT issued by `POST /api/v1/auth/token`. It is now centralized in [`src/utils/visitorToken.ts`](src/utils/visitorToken.ts) and shared by **three** features: the tests/match flow, the Emma chat, and analytics. (The test no longer keeps a separate `elegio_test_token`.)

- `createVisitorToken()` posts visitor/session metadata (language, timezone, screen size, pixel ratio, landing page, referer, viewport) to `POST /api/v1/auth/token` and returns the JWT.
- `getOrCreateVisitorToken()` returns the cached token, minting and persisting one only when missing.
- The token is stored in the `elegio_visitor_token` cookie (30-day max-age, `Path=/`, `SameSite=Lax`), so the same identity is reused across the test, chat and analytics and survives reloads.

Protected calls send it as `Authorization: Bearer <token>`; the API resolves the visitor (and, for answers, the current test attempt) server-side.

## 🗳 Tests & Match electoral

The `tests` feature ([`src/features/tests/`](src/features/tests/)) drives two question flows, both built on the [`useTestFlow`](src/features/tests/hooks/useTestFlow.ts) hook and the shared [visitor token](#-visitor-token):

- `/test` (`TestPage`) — the classic affinity questionnaire.
- `/match-electoral` (`MatchElectoralPage`) — the "match" flow, composed of [`MatchTestIntro`](src/features/tests/components/MatchTestIntro.tsx), [`MatchQuestionStep`](src/features/tests/components/MatchQuestionStep.tsx), and result charts under [`components/charts/`](src/features/tests/components/charts/).

### Match flow specifics

- **Intro chips.** `MatchTestIntro` shows derived stats — number of questions, number of distinct finalists (candidates referenced by the questions), and an estimated duration in minutes — computed from the active test's questions in `useTestFlow`.
- **Video questions.** [`QuestionVideo`](src/features/tests/components/QuestionVideo.tsx) renders a question's `video_url` as a TikTok embed, a YouTube embed, or a native `<video>` for direct files.
- **Emotion slider.** For `video_emotion_slider` questions, `MatchQuestionStep` shows an emotion slider — rechazo / neutral / empatía — mapped to a numeric `emotion_answer` in `[-1, 1]`.
- **Smooth scroll.** Advancing between questions gently scrolls the page to the top via [`smoothScrollToTop`](src/utils/smoothScroll.ts).

### API integration ([`testApi.ts`](src/features/tests/api/testApi.ts))

The answer/affinity endpoints are now scoped by the test attempt and the test id:

- `createAnswer({ testAttemptId, ... })` → `POST /api/v1/answers/{test_attempt_id}`, sending `question_id`, `response_option_id`, `emotion_answer` (for the slider) and `response_time`.
- `getAnswers(token, testId)` → `GET /api/v1/answers/{test_id}`.
- `getAffinity(token, testId)` → `GET /api/v1/answers/affinity/{test_id}`.
- `getCurrentTestAttempt(token, testId)` → `GET /api/v1/test-attempts?test_id=`; a `404` is treated as "no attempt yet" (the visitor may have a token from the chat or analytics without having started a test).

## 📈 Analytics

The `analytics` feature ([`src/features/analytics/`](src/features/analytics/)) records anonymous usage signals. [`AnalyticsTracker`](src/features/analytics/components/AnalyticsTracker.tsx) is mounted once in `RootLayout`, so it runs on every route, and emits three event types via [`trackEvent`](src/features/analytics/api/trackEvent.ts):

- `page_view` — on every route change (including first render).
- `click` — on interactive elements (`a`, `button`, `[role="button"]`, `input`, `[data-track]`), capturing the element's tag/id/class/text.
- `scroll` — once per `25/50/75/100%` depth milestone reached on a page.

`trackEvent` is fire-and-forget: it sends `POST /api/v1/events` with the shared [visitor token](#-visitor-token) and **swallows all errors** so analytics never block or disrupt the UI.

## 🤖 Emma chatbot

Emma is the in-app assistant that helps visitors verify candidate proposals. It lives in [`src/features/chat/`](src/features/chat/) and is surfaced everywhere through [`src/components/FloatingEmmaButton.tsx`](src/components/FloatingEmmaButton.tsx), which `RootLayout` mounts on every route.

### UI

- A floating button (bottom-right, blue `#2563eb`, Emma logo at `/logo-emma.webp`) toggles the chat window.
- While closed, the button shows a rotating bubble of invitation messages (`EMMA_MESSAGES`), swapping every 12s; the bubble can be dismissed.
- The chat window ([`ChatWindow.tsx`](src/features/chat/components/ChatWindow.tsx)) supports a **fullscreen** mode. Open/fullscreen state is reflected in the URL via a `chat` query param (`?chat=open` / `?chat=full`), so the panel state is bookmarkable and survives back/forward navigation.
- Assistant messages are rendered as Markdown via `react-markdown`.

### Conversation flow

The chat reuses the shared anonymous [**visitor token**](#-visitor-token), then streams replies over **Server-Sent Events (SSE)**. All of this is wrapped by the [`useEmmaChat`](src/features/chat/hooks/useEmmaChat.ts) hook, with the network layer in [`chatApi.ts`](src/features/chat/api/chatApi.ts):

1. **Visitor token** — `useEmmaChat` calls `getOrCreateVisitorToken()` from [`src/utils/visitorToken.ts`](src/utils/visitorToken.ts) (the same cookie the test and analytics use).
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
