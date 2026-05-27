# Elegio — Frontend

Web client for [Elegio](../README.md): a non-partisan platform to explore 2026 presidential candidates, their proposals, and an affinity test. Built with Vite + React 19 and styled with Tailwind CSS v4. It talks to the [FastAPI backend](../api) over HTTP.

## 🚀 Tech stack

- **Vite 8** — build tool and dev server
- **React 19** + **TypeScript** — UI, with the **React Compiler** enabled (`babel-plugin-react-compiler`)
- **React Router 7** — client-side routing (`createBrowserRouter`)
- **Tailwind CSS v4** — styling (via `@tailwindcss/vite`)
- **axios** — HTTP client, configured once in [`src/config/api.ts`](src/config/api.ts)
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
│   ├── components/           # Shared UI (RootLayout, Footer, SpectrumMarker)
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

## 🧹 Code style

- **Prettier** + **ESLint** for formatting and linting.
- **Conventional Commits** — `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`...
- Keep components in `components/`; colocate data fetching in the feature's `api/` and `hooks/`.
