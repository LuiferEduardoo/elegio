# Elegio API

Backend FastAPI for **Elegio**, an open-source platform that helps voters choose a presidential candidate. The API powers the test-based recommender, the comparison of candidate proposals, and the analytics events captured during a test attempt. It is consumed by the [frontend](../frontend) and the [analysis](../analysis) services.

---

## Table of contents

- [Overview](#overview)
- [End-to-end flow](#-end-to-end-flow)
- [Tech stack](#-tech-stack)
- [Project structure](#-project-structure)
- [Setup](#-setup)
- [Environment variables](#-environment-variables)
- [Authentication](#-authentication)
- [Rate limits](#-rate-limits)
- [Pagination convention](#-pagination-convention)
- [Endpoint reference](#-endpoint-reference)
  - [Tests](#tests)
  - [Test Attempts](#test-attempts)
  - [Candidates](#candidates)
  - [Proposals](#proposals)
  - [Government Plans](#government-plans)
  - [Questions](#questions)
  - [Response Options](#response-options)
  - [Events](#events)
  - [Answers](#answers)
  - [Search](#search)
- [Conventions](#-conventions)
- [Common commands](#-common-commands)
- [Code style](#-code-style)

---

## Overview

Elegio is an open-source platform that helps voters identify the presidential candidate that best matches their views. It does this by:

1. Running a **test** of categorized questions (economic axis, social axis, etc.).
2. Recording the user's **answers** during a single **test attempt**.
3. Comparing the user's positions against each candidate's **proposals**, **postures**, and full **government plan**.
4. Capturing anonymized **visitor**, **session**, and **event** signals to improve the experience.

This API exposes the REST endpoints behind that flow:

- Public, read-only endpoints for the catalogue (tests, questions, candidates, proposals, government plans).
- A bootstrap endpoint that creates a `Visitor` + `Session` + `TestAttempt` and returns a JWT scoped to the attempt.
- Authenticated endpoints for writing answers, tracking events, and computing candidate affinity for that attempt.

---

## 🔁 End-to-end flow

A typical client integration looks like this:

```
┌──────────┐                                              ┌──────────┐
│  Client  │                                              │   API    │
└────┬─────┘                                              └────┬─────┘
     │  1. GET /api/v1/tests                                   │
     │ ──────────────────────────────────────────────────────► │
     │ ◄────────────────────────────────────────────────────── │  list of tests
     │                                                         │
     │  2. POST /api/v1/test-attempts/initialize { test_id }   │
     │ ──────────────────────────────────────────────────────► │  creates Visitor + Session + TestAttempt
     │ ◄────────────────────────────────────────────────────── │  returns { test_attempt, visitor_id, token }
     │                                                         │
     │  3. GET /api/v1/questions/by-test/{test_id}             │
     │ ──────────────────────────────────────────────────────► │
     │ ◄────────────────────────────────────────────────────── │  ordered questions + categories
     │                                                         │
     │  4. GET /api/v1/response-options/question/{id}          │
     │ ──────────────────────────────────────────────────────► │
     │ ◄────────────────────────────────────────────────────── │  options for the current question
     │                                                         │
     │  5. POST /api/v1/answers          (Bearer <token>)      │
     │ ──────────────────────────────────────────────────────► │  loops over the questions
     │ ◄────────────────────────────────────────────────────── │  { answer, test_completed, status }
     │                                                         │
     │  6. GET /api/v1/answers/affinity  (Bearer <token>)      │
     │ ──────────────────────────────────────────────────────► │  computes weighted Manhattan affinity
     │ ◄────────────────────────────────────────────────────── │  ranked candidates with affinity score
     │                                                         │
```

Steps 1, 3, and 4 are public. Steps 2, 5, and 6 require the JWT issued in step 2 to be sent as `Authorization: Bearer <token>`. The test attempt auto-completes on step 5 once every active question of the test has been answered (see [Answers](#answers)).

---

## 🚀 Tech stack

- **FastAPI** `0.115` — async web framework
- **SQLAlchemy 2.0** `[asyncio]` — async ORM (`Mapped[]` / `mapped_column()`)
- **Alembic** `1.14` — database migrations
- **Pydantic v2** + **pydantic-settings** — request/response validation and config
- **MySQL 8** via `aiomysql` (async) and `pymysql` (sync, used by Alembic)
- **PyJWT** `2.10` — JWT issuance and validation (HS256)
- **slowapi** `0.1.9` — IP-based rate limiting
- **sentence-transformers** `3.3.1` — multilingual E5 embeddings (`intfloat/multilingual-e5-large`, 1024-dim) for the hybrid search endpoint
- **qdrant-client** `1.13.2` — Qdrant client used to query the `proposal_chunks` vector collection
- **rank-bm25** `0.2.2` — in-memory BM25 lexical index fused with the dense results via Reciprocal Rank Fusion

---

## 📁 Project structure

```
api/
├── alembic/                  # Migration environment and versions
├── alembic.ini               # Alembic config (sqlalchemy.url injected from env)
├── docker-compose.dev.yml    # Local MySQL + phpMyAdmin
├── app/
│   ├── main.py               # FastAPI entrypoint (mounts router, limiter, middleware)
│   ├── api/v1/router.py      # /api/v1 root router (includes every domain router)
│   ├── core/
│   │   ├── config.py         # Settings (loads .env via pydantic-settings)
│   │   ├── database.py       # Async engine, Base, TimestampMixin, get_db()
│   │   ├── security.py       # JWT helpers + get_token_payload dependency
│   │   ├── rate_limit.py     # slowapi Limiter + PUBLIC/PRIVATE constants
│   │   ├── embedder.py       # multilingual-e5-large SentenceTransformer singleton
│   │   ├── qdrant_client.py  # Qdrant client + collection metadata
│   │   └── bm25_index.py     # In-memory BM25 index over proposal_chunks
│   └── domains/              # One folder per domain
│       ├── answer/
│       ├── candidate/
│       ├── category/
│       ├── event/
│       ├── government_plan/
│       ├── posture/
│       ├── proposal/
│       ├── proposal_chunk/
│       ├── question/
│       ├── response_option/
│       ├── search/
│       ├── session/
│       ├── source/
│       ├── tagging/
│       ├── test/
│       ├── test_attempt/
│       └── visitor/
├── requirements.txt
├── .env.example
└── .env                      # Local config (gitignored)
```

Each domain folder follows the same shape:

```
app/domains/{domain}/
├── __init__.py
├── models.py       # SQLAlchemy 2.0 models (Mapped[], mapped_column())
├── schemas.py      # Pydantic v2 request/response models
├── routes.py       # APIRouter with /api/v1/{resource}
└── service.py      # Business logic (async)
```

Domain routers are wired into the v1 router in [app/api/v1/router.py](app/api/v1/router.py).

---

## 📦 Setup

### Prerequisites

- **Python 3.12**
- **MySQL 8+** (or use the bundled docker-compose)
- **Docker** and **Docker Compose** (recommended for local DB)

### 1. Install dependencies

```bash
cd api
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 2. Start MySQL with Docker Compose

[docker-compose.dev.yml](docker-compose.dev.yml) ships a MySQL 8 instance and a phpMyAdmin UI:

```bash
docker compose -f docker-compose.dev.yml up -d
```

It exposes:

- MySQL on `localhost:3306`
  - Database: `elegio`
  - User: `elegio_user`
  - Password: `elegio_password`
  - Root password: `password`
- phpMyAdmin on [http://localhost:8080](http://localhost:8080)

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` so the URLs match the docker-compose credentials, for example:

```bash
DATABASE_URL=mysql+aiomysql://elegio_user:elegio_password@localhost:3306/elegio
DATABASE_URL_SYNC=mysql+pymysql://elegio_user:elegio_password@localhost:3306/elegio
```

### 4. Run migrations

```bash
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

Useful URLs once the server is up:

- `GET /` — app info (`{"app": "...", "env": "..."}`)
- `GET /docs` — interactive Swagger UI
- `GET /redoc` — ReDoc UI

> **Search warm-up.** By default, local development skips the expensive search pre-load so the API starts quickly. Set `EAGER_LOAD_SEARCH_ON_STARTUP=true` to make the FastAPI [`lifespan`](app/main.py) hook eagerly load the multilingual-e5-large SentenceTransformer (~1.5 GB RAM per worker; the first start downloads the weights) and build the BM25 index from `proposal_chunks`. If either pre-load fails, the API still starts and falls back to lazy loading on the first search request.
>
> Operational notes:
> - With `uvicorn --reload` both pre-loads run on every reload — expect a slow loop during development.
> - With multiple workers each worker holds its own copy of the model and BM25 index.
> - BM25 has no auto-invalidation. After new chunks are embedded (see [analysis/README.md](../analysis/README.md)), restart the API — or call `BM25Index.refresh(db)` programmatically — for them to be searchable lexically. Qdrant is queried directly so dense results pick up new chunks immediately.

---

## 🔧 Environment variables

Loaded from `api/.env` via [`Settings`](app/core/config.py) (pydantic-settings). See [.env.example](.env.example).

| Key                   | Required | Default                  | Description                                                   |
| --------------------- | :------: | ------------------------ | ------------------------------------------------------------- |
| `APP_NAME`            |    no    | `elegio-api`             | App name shown in OpenAPI metadata                            |
| `APP_ENV`             |    no    | `development`            | `development` / `staging` / `production`                      |
| `DEBUG`               |    no    | `True`                   | Enables SQL echo and FastAPI debug                            |
| `DATABASE_URL`        |  **yes** | —                        | Async URL — `mysql+aiomysql://user:pass@host:3306/db`         |
| `DATABASE_URL_SYNC`   |  **yes** | —                        | Sync URL used by Alembic — `mysql+pymysql://user:pass@host/db`|
| `JWT_SECRET_KEY`      |    no    | `change-me-in-production`| HMAC secret used to sign access tokens. **Override in prod.** |
| `JWT_ALGORITHM`       |    no    | `HS256`                  | JWT signing algorithm                                         |
| `JWT_EXPIRES_MINUTES` |    no    | `1440` (24 h)            | Token lifetime in minutes                                     |
| `QDRANT_URL`          |    no    | `http://localhost:6333`  | URL of the Qdrant instance backing the `/search/proposals` endpoint |
| `QDRANT_API_KEY`      |    no    | `""` (unset)             | Optional Qdrant API key. Leave empty for the local docker-compose instance |
| `EAGER_LOAD_SEARCH_ON_STARTUP` | no | `False` | Pre-loads the embedding model and BM25 index during FastAPI startup when enabled |

---

## 🔐 Authentication

Authentication is **session-scoped**, not user-scoped: there are no user accounts. Instead, a single token represents one anonymous test attempt.

### Issuing a token

A token is issued by `POST /api/v1/test-attempts/initialize` ([routes](app/domains/test_attempt/routes.py), [service](app/domains/test_attempt/service.py)). The handler:

1. Validates that the requested `test_id` exists.
2. Creates a new `Visitor` with a fresh `visitor_uid` (UUID hex).
3. Creates the first `Session` for that visitor.
4. Creates a `TestAttempt` (`uuid` = UUIDv4, `status = IN_PROGRESS`).
5. Signs a JWT (HS256) with the following payload:

```json
{
  "test_attempt_uuid": "<uuid>",
  "visitor_id": 123,
  "test_id": 1,
  "exp": 1735689600
}
```

The token is returned in the response body as `token`.

### Using a token

Pass the token in the `Authorization` header on every protected endpoint:

```
Authorization: Bearer <token>
```

Token validation is centralized in [`get_token_payload`](app/core/security.py). Failures raise `401 Unauthorized`:

| Scenario             | Response                                          |
| -------------------- | ------------------------------------------------- |
| Header missing       | `401 Unauthorized` — `Not authenticated`          |
| Token expired        | `401 Unauthorized` — `Token expired`              |
| Token signature bad  | `401 Unauthorized` — `Invalid token`              |

Any route that depends on `get_token_payload` is **private** (see [Rate limits](#-rate-limits)).

---

## ⏱ Rate limits

All endpoints — **public and private alike** — are rate-limited per **client IP** (`get_remote_address`) using [slowapi](https://github.com/laurentS/slowapi). Authentication does not exempt a route from throttling; private endpoints simply use a higher ceiling. Limits live in [app/core/rate_limit.py](app/core/rate_limit.py):

| Class    | Constant              | Value         | Applies to                                  |
| -------- | --------------------- | ------------- | ------------------------------------------- |
| Public   | `PUBLIC_RATE_LIMIT`   | `100/minute`  | Routes without `Depends(get_token_payload)` |
| Private  | `PRIVATE_RATE_LIMIT`  | `500/minute`  | Routes with `Depends(get_token_payload)`    |

When the limit is exceeded the API returns:

```
HTTP/1.1 429 Too Many Requests
{
  "error": "Rate limit exceeded: 100 per 1 minute"
}
```

> Every endpoint **must** declare a limit using `@limiter.limit(...)` and accept `request: Request` as the first parameter (slowapi reads the client IP from it).

---

## 📑 Pagination convention

Every endpoint that returns a collection is paginated. The contract is identical across domains:

**Query params**

| Param    | Type | Default | Min | Max | Description              |
| -------- | ---- | ------: | --: | --: | ------------------------ |
| `limit`  | int  |    `10` |  1  | 100 | Max items per page       |
| `offset` | int  |     `0` |  0  |  —  | Number of items to skip  |

**Response body**

```json
{
  "items": [ /* list of resources */ ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

Soft-deleted rows (`deleted_at IS NOT NULL`) are filtered out of every list and read endpoint.

---

## 📚 Endpoint reference

All endpoints are mounted under `/api/v1`. For interactive exploration, run the server and open `/docs`.

Liveness probe.

- **Auth**: none
- **Rate limit**: not limited (handler is registered directly on the v1 router)

Response `200 OK`:

```json
{ "status": "ok" }
```

---

### Tests

[routes.py](app/domains/test/routes.py) · [service.py](app/domains/test/service.py) · [models.py](app/domains/test/models.py)

A `Test` is a questionnaire definition (set of categorized questions). Tests are listed publicly so the frontend can let the user pick one.

#### `GET /api/v1/tests`

List tests, ordered by `id ASC`.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Query**: `limit` (1–100, default 10), `offset` (≥0, default 0)

Response `200 OK`:

```json
{
  "items": [
    {
      "id": 1,
      "nombre": "Test presidencial 2026",
      "descripcion": "20 preguntas para encontrar tu candidato",
      "created_at": "2026-04-01T12:00:00"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

> ⚠ The `Test` resource is the only one that exposes Spanish field names (`nombre`, `descripcion`) — the rest of the API uses English. These names mirror the underlying column names and are kept stable for backward compatibility with the existing seed data.

Errors: `429 Too Many Requests`.

---

### Test Attempts

[routes.py](app/domains/test_attempt/routes.py) · [service.py](app/domains/test_attempt/service.py) · [models.py](app/domains/test_attempt/models.py)

A `TestAttempt` is a single user's run through a test. It owns a `uuid`, a `status` (`in_progress`, `completed`, `abandoned`, `timed_out`), and timestamps. The `uuid` is what the JWT carries.

#### `POST /api/v1/test-attempts/initialize`

Bootstrap endpoint. Creates `Visitor` + `Session` + `TestAttempt` and returns a JWT bound to that attempt. **This is the entry point for any client that needs to call protected endpoints.**

- **Auth**: none
- **Rate limit**: `100/minute`
- **Status**: `201 Created`

Request body — [`TestAttemptInitialize`](app/domains/test_attempt/schemas.py):

```json
{
  "test_id": 1,
  "visitor": {
    "browser_name": "Chrome",
    "browser_version": "120.0.0",
    "os_name": "Windows",
    "os_version": "11",
    "device_type": "desktop",
    "is_mobile": false,
    "is_bot": false,
    "screen_width": 1920,
    "screen_height": 1080,
    "primary_language": "es-PE",
    "timezone": "America/Lima",
    "consent_given": true,
    "consent_at": "2026-05-02T12:00:00",
    "consent_version": "1.0"
  },
  "session": {
    "ip_address": "200.10.20.30",
    "country_code": "PE",
    "city": "Lima",
    "viewport_width": 1440,
    "viewport_height": 900,
    "referer": "https://google.com",
    "utm_source": "twitter",
    "utm_campaign": "launch"
  }
}
```

The `visitor` and `session` schemas accept many more optional fields (device hardware, geo, UTM tags, consent metadata). See [visitor/schemas.py](app/domains/visitor/schemas.py) for the full list. Both `visitor.is_bot` and `session.is_vpn` / `is_proxy` / `is_datacenter` default to `false`. `session` is itself optional and defaults to an empty object.

Response `201 Created`:

```json
{
  "test_attempt": {
    "id": 42,
    "uuid": "9f1c4b0e-2d48-4e85-9a1a-72ae8b1a55b3",
    "visitor_id": 17,
    "test_id": 1,
    "status": "in_progress",
    "started_at": "2026-05-02T12:00:00",
    "finished_at": null,
    "created_at": "2026-05-02T12:00:00"
  },
  "visitor_id": 17,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Errors:

| Status | When                                |
| ------ | ----------------------------------- |
| `400`  | Validation failed (Pydantic)        |
| `404`  | `test_id` does not exist or is soft-deleted |
| `429`  | Rate limit exceeded                 |

#### `GET /api/v1/test-attempts`

Returns the test attempt embedded in the bearer token. Useful to check current status / `finished_at`.

- **Auth**: required
- **Rate limit**: `500/minute`

Response `200 OK` — same shape as `test_attempt` above.

Errors:

| Status | When                                                  |
| ------ | ----------------------------------------------------- |
| `401`  | Missing / expired / invalid token, or token has no `test_attempt_uuid` |
| `404`  | The attempt referenced by the token no longer exists  |
| `429`  | Rate limit exceeded                                   |

---

### Candidates

[routes.py](app/domains/candidate/routes.py) · [service.py](app/domains/candidate/service.py) · [models.py](app/domains/candidate/models.py)

A `Candidate` represents a presidential ticket (presidential + vice-presidential candidate, political group, photos, political spectrum).

#### `GET /api/v1/candidates`

List candidates, ordered by `id ASC`.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Query**: `limit`, `offset`

Response `200 OK`:

```json
{
  "items": [
    {
      "id": 1,
      "presidential_candidate": "Jane Doe",
      "vice_presidential_candidate": "John Roe",
      "political_group": "Partido Ejemplo",
      "photo_of_political_group": "https://cdn.elegio.app/groups/1.png",
      "photo_president": "https://cdn.elegio.app/p/1.jpg",
      "photo_vice_president": "https://cdn.elegio.app/vp/1.jpg",
      "troubles_questions": null,
      "political_spectrum": "center-left",
      "created_at": "2026-04-01T12:00:00",
      "category_averages": [
        {
          "category_id": 3,
          "category_name": "Educación",
          "weight": 1.5,
          "negative_pole_name": "Mercado",
          "negative_pole_description": "Educación gestionada por el sector privado y la competencia.",
          "positive_pole_name": "Estado",
          "positive_pole_description": "Educación pública, gratuita y gestionada por el Estado.",
          "average": 0.65,
          "proposals_count": 4
        }
      ]
    }
  ],
  "total": 12,
  "limit": 10,
  "offset": 0
}
```

Each candidate carries a `category_averages` array — a per-category roll-up of every `Posture` attached to that candidate's proposals. Each entry exposes the category's axis metadata (`weight`, `negative_pole_*`, `positive_pole_*`) plus:

| Field             | Type    | Description                                                                                  |
| ----------------- | ------- | -------------------------------------------------------------------------------------------- |
| `average`         | `float` | Mean of `posture.axis_value` over the candidate's proposals in this category (`[-1, +1]`).   |
| `proposals_count` | `int`   | Number of distinct proposals contributing to `average`.                                       |

Notes:

- The aggregation runs in a single `GROUP BY candidate_id, category_id` query over the candidates on the current page — no N+1.
- Candidates with no rated proposals get `category_averages: []`.
- Soft-deleted proposals, postures, and categories are excluded.

#### `GET /api/v1/candidates/{candidate_id}`

Fetch one candidate.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Path**: `candidate_id` (int, `> 0`)

Response `200 OK`: same shape as one item above, including the `category_averages` array.

Errors:

| Status | When                                                |
| ------ | --------------------------------------------------- |
| `404`  | Candidate not found or soft-deleted                 |
| `422`  | `candidate_id` is not a positive integer            |
| `429`  | Rate limit exceeded                                 |

---

### Proposals

[routes.py](app/domains/proposal/routes.py) · [service.py](app/domains/proposal/service.py) · [models.py](app/domains/proposal/models.py)

A `Proposal` is a single policy item from a candidate. It is always returned with its **category**, **candidate**, **postures** (axis values), **taggings**, and **sources** eagerly loaded.

> **About postures.** A `Posture` ([app/domains/posture/models.py](app/domains/posture/models.py)) records a candidate's coded position for a proposal on a given axis. Each row persists more than what the API exposes today: the numeric `axis_value`, plus a `confidence` enum (`high` / `medium` / `low`), free-text `reasoning` and `ambiguities`, and authorship metadata via `coder_type` (`llm` / `human`) and `coder_name`. The Proposal endpoints only surface `id` and `axis_value` — the remaining fields are kept for downstream auditing and analysis (see the [analysis](../analysis) service).
>
> **About categories.** A `Category` ([app/domains/category/models.py](app/domains/category/models.py)) is the descriptive axis a `Posture.axis_value` is placed on (the same `-1.0` / `+1.0` scale). In addition to `id`, `name`, and `weight`, every category persists the labels and descriptions of its two poles:
>
> | Field                        | Type          | Nullable | Description                                       |
> | ---------------------------- | ------------- | :------: | ------------------------------------------------- |
> | `negative_pole_name`         | `String(64)`  |    no    | Short label for the `-1.0` end of the axis        |
> | `negative_pole_description`  | `Text`        |    no    | Longer description of the negative pole           |
> | `positive_pole_name`         | `String(64)`  |    no    | Short label for the `+1.0` end of the axis        |
> | `positive_pole_description`  | `Text`        |    no    | Longer description of the positive pole           |
>
> These pole fields are stored on the model (migration `51c9fb4e4f9d_add_fields_negative_pole_name_negative_*`) and are intended to be used by the [analysis](../analysis) service when reasoning about each axis. The nested `category` object returned by the Proposals and Questions endpoints currently exposes only `id`, `name`, and `weight`.
>
> **About chunks.** A `ProposalChunk` ([app/domains/proposal_chunk/models.py](app/domains/proposal_chunk/models.py)) stores a paragraph-aware slice of a proposal used by the [Search](#search) endpoint. Each row carries `proposal_id` (FK), `chunk_index`, `total_chunks`, `content`, and the usual `TimestampMixin` columns. `Proposal.chunks` exposes the relationship. Chunks are produced and embedded by the [analysis](../analysis) service, not by the API itself — the API only consumes them at search time.

#### `GET /api/v1/proposals`

List proposals.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Query**:
  - `candidate_id` (int, `> 0`, optional) — filter by candidate
  - `category_id` (int, `> 0`, optional) — filter by category
  - `limit` (1–100, default 10)
  - `offset` (≥0, default 0)

Response `200 OK`:

```json
{
  "items": [
    {
      "id": 101,
      "title": "Reforma educativa universal",
      "summary": "Educación pública gratuita hasta nivel superior.",
      "full_text": "Texto completo de la propuesta...",
      "category": {
        "id": 3,
        "name": "Educación",
        "weight": 1.5
      },
      "candidate": {
        "id": 1,
        "presidential_candidate": "Jane Doe",
        "vice_presidential_candidate": "John Roe",
        "political_group": "Partido Ejemplo",
        "political_spectrum": "center-left",
        "photo_president": "https://cdn.elegio.app/p/1.jpg",
        "photo_vice_president": "https://cdn.elegio.app/vp/1.jpg",
        "photo_of_political_group": "https://cdn.elegio.app/groups/1.png"
      },
      "postures": [
        { "id": 5001, "axis_value": 0.7 }
      ],
      "taggings": [
        { "id": 9001, "name": "educación" },
        { "id": 9002, "name": "presupuesto público" }
      ],
      "sources": [
        { "id": 7001, "url": "https://example.org/plan-de-gobierno.pdf" }
      ],
      "created_at": "2026-04-10T08:00:00"
    }
  ],
  "total": 47,
  "limit": 10,
  "offset": 0
}
```

#### `GET /api/v1/proposals/{proposal_id}`

Fetch one proposal with the same eager-loaded relations.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Path**: `proposal_id` (int, `> 0`)

Errors:

| Status | When                                                |
| ------ | --------------------------------------------------- |
| `404`  | Proposal not found or soft-deleted                  |
| `422`  | `proposal_id` is not a positive integer             |
| `429`  | Rate limit exceeded                                 |

---

### Government Plans

[routes.py](app/domains/government_plan/routes.py) · [service.py](app/domains/government_plan/service.py) · [models.py](app/domains/government_plan/models.py)

A `GovernmentPlan` groups a candidate's proposals into a single document. The candidate is eagerly loaded.

#### `GET /api/v1/government-plans`

List all government plans.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Query**: `limit`, `offset`

Response `200 OK`:

```json
{
  "items": [
    {
      "id": 1,
      "candidate": {
        "id": 1,
        "presidential_candidate": "Jane Doe",
        "vice_presidential_candidate": "John Roe",
        "political_group": "Partido Ejemplo",
        "political_spectrum": "center-left",
        "photo_president": "https://cdn.elegio.app/p/1.jpg",
        "photo_vice_president": "https://cdn.elegio.app/vp/1.jpg",
        "photo_of_political_group": "https://cdn.elegio.app/groups/1.png"
      },
      "created_at": "2026-04-01T12:00:00"
    }
  ],
  "total": 12,
  "limit": 10,
  "offset": 0
}
```

#### `GET /api/v1/government-plans/{candidate_id}`

List the government plans of a single candidate. Returns the same paginated shape as the previous endpoint.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Path**: `candidate_id` (int, `> 0`)
- **Query**: `limit`, `offset`

Errors:

| Status | When                                                 |
| ------ | ---------------------------------------------------- |
| `404`  | Candidate not found or soft-deleted                  |
| `422`  | `candidate_id` is not a positive integer             |
| `429`  | Rate limit exceeded                                  |

---

### Questions

[routes.py](app/domains/question/routes.py) · [service.py](app/domains/question/service.py) · [models.py](app/domains/question/models.py)

Questions are returned **ordered by `question_order ASC, id ASC`**, with their `category` eagerly loaded. `type_question` is one of: `multiple_choice`, `boolean`, `only_option`, `open_question`.

#### `GET /api/v1/questions/by-test/{test_id}`

List the questions that belong to a test.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Path**: `test_id` (int, `> 0`)
- **Query**: `limit`, `offset`

Response `200 OK`:

```json
{
  "items": [
    {
      "id": 11,
      "test_id": 1,
      "title": "¿Estás de acuerdo con la educación pública universal?",
      "type_question": "only_option",
      "question_order": 1,
      "is_active": true,
      "category": {
        "id": 3,
        "name": "Educación",
        "weight": 1.5
      },
      "created_at": "2026-04-01T12:00:00"
    }
  ],
  "total": 20,
  "limit": 10,
  "offset": 0
}
```

Errors: `404` if the test does not exist or is soft-deleted; `422` for an invalid path; `429` rate limit.

#### `GET /api/v1/questions/by-category/{category_id}`

Same shape as above, but filtered by category instead of by test.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Path**: `category_id` (int, `> 0`)
- **Query**: `limit`, `offset`

Errors: `404` if the category does not exist or is soft-deleted; `422` invalid path; `429` rate limit.

---

### Response Options

[routes.py](app/domains/response_option/routes.py) · [service.py](app/domains/response_option/service.py) · [models.py](app/domains/response_option/models.py)

Response options are the choices attached to a question. Each option carries a numeric `value` used by the recommender.

#### `GET /api/v1/response-options/question/{question_id}`

List the response options for one question, ordered by `id ASC`.

- **Auth**: none
- **Rate limit**: `100/minute`
- **Path**: `question_id` (int, `> 0`)
- **Query**: `limit`, `offset`

Response `200 OK`:

```json
{
  "items": [
    {
      "id": 501,
      "question_id": 11,
      "title": "Totalmente de acuerdo",
      "value": 1.0,
      "created_at": "2026-04-01T12:00:00"
    },
    {
      "id": 502,
      "question_id": 11,
      "title": "En desacuerdo",
      "value": -1.0,
      "created_at": "2026-04-01T12:00:00"
    }
  ],
  "total": 5,
  "limit": 10,
  "offset": 0
}
```

Errors: `404` if the question does not exist or is soft-deleted; `422` invalid path; `429` rate limit.

---

### Events

[routes.py](app/domains/event/routes.py) · [service.py](app/domains/event/service.py) · [models.py](app/domains/event/models.py)

Analytics events tied to the test attempt's visitor + session. The `visitor_id` and `session_id` are derived server-side from the JWT's `test_attempt_uuid` — clients never send them. The session resolved is the **most recent** session of the visitor (ordered by `started_at DESC`).

#### `POST /api/v1/events`

Record a single event.

- **Auth**: required
- **Rate limit**: `500/minute`
- **Status**: `201 Created`

Request body — [`EventCreate`](app/domains/event/schemas.py):

```json
{
  "event_type": "click",
  "event_name": "answer_submitted",
  "page_url": "https://elegio.app/test/1/q/3",
  "page_path": "/test/1/q/3",
  "page_title": "Pregunta 3",
  "element_tag": "button",
  "element_id": "answer-btn-1",
  "element_class": "btn primary",
  "element_text": "Totalmente de acuerdo",
  "scroll_depth": 80,
  "duration_ms": 4200,
  "properties": {
    "question_id": 11,
    "selected_value": 1.0
  }
}
```

Validation:

- `event_type` is required, 1–50 chars.
- `event_name` ≤ 100 chars (optional).
- `scroll_depth` is `0..100` (optional).
- `duration_ms` ≥ 0 (optional).
- `properties` is an arbitrary JSON object (optional).

Response `201 Created`:

```json
{
  "id": 9001,
  "session_id": 51,
  "visitor_id": 17,
  "event_type": "click",
  "event_name": "answer_submitted",
  "page_url": "https://elegio.app/test/1/q/3",
  "page_path": "/test/1/q/3",
  "page_title": "Pregunta 3",
  "element_tag": "button",
  "element_id": "answer-btn-1",
  "element_class": "btn primary",
  "element_text": "Totalmente de acuerdo",
  "scroll_depth": 80,
  "duration_ms": 4200,
  "properties": { "question_id": 11, "selected_value": 1.0 },
  "occurred_at": "2026-05-02T12:01:00",
  "created_at": "2026-05-02T12:01:00"
}
```

Errors:

| Status | When                                                                       |
| ------ | -------------------------------------------------------------------------- |
| `401`  | Missing / invalid token, or token has no `test_attempt_uuid`               |
| `404`  | Test attempt not found, or visitor has no session                          |
| `422`  | Body fails validation                                                       |
| `429`  | Rate limit exceeded                                                         |

---

### Answers

[routes.py](app/domains/answer/routes.py) · [service.py](app/domains/answer/service.py) · [models.py](app/domains/answer/models.py)

Answers belong to the `TestAttempt` referenced by the JWT. Creating an answer also runs the **auto-completion** logic: when the count of distinct answered questions for the attempt reaches the count of active questions in the test, the attempt is transitioned to `status = COMPLETED` and `finished_at` is stamped.

#### `POST /api/v1/answers`

Create an answer for the current test attempt.

- **Auth**: required
- **Rate limit**: `500/minute`
- **Status**: `201 Created`

Request body — [`AnswerCreate`](app/domains/answer/schemas.py):

```json
{
  "question_id": 11,
  "response_option_id": 501,
  "boolean_answer": null,
  "open_text_answer": null,
  "response_time": 4200
}
```

Field rules:

- `question_id` is required and `> 0`.
- `response_option_id` is `> 0` if provided. Use it for `multiple_choice` / `only_option` questions.
- `boolean_answer` for `boolean` questions.
- `open_text_answer` for `open_question`.
- `response_time` (ms) is `≥ 0` if provided.

Service-side validations:

- Test attempt must exist and have `status = IN_PROGRESS`.
- Question must exist and belong to the test in the token.
- If `response_option_id` is set, it must exist and belong to `question_id`.

Response `201 Created`:

```json
{
  "answer": {
    "id": 7001,
    "test_attempt_id": 42,
    "question_id": 11,
    "response_option_id": 501,
    "boolean_answer": null,
    "open_text_answer": null,
    "response_time": 4200,
    "created_at": "2026-05-02T12:01:30"
  },
  "test_completed": false,
  "test_attempt_status": "in_progress"
}
```

When the answer happens to be the last one needed to complete the test:

```json
{
  "answer": { "...": "..." },
  "test_completed": true,
  "test_attempt_status": "completed"
}
```

Errors:

| Status | Cause                                                                                       |
| ------ | ------------------------------------------------------------------------------------------- |
| `400`  | `TestAttemptNotInProgressError` — attempt is `completed`/`abandoned`/`timed_out`            |
| `400`  | `QuestionDoesNotBelongToTestError` — question's `test_id` ≠ attempt's `test_id`             |
| `400`  | `ResponseOptionDoesNotBelongToQuestionError` — option's `question_id` ≠ payload `question_id`|
| `401`  | Missing / invalid token                                                                     |
| `404`  | `TestAttemptNotFoundError` / `QuestionNotFoundError` / `ResponseOptionNotFoundError`        |
| `422`  | Body fails Pydantic validation                                                               |
| `429`  | Rate limit exceeded                                                                          |

#### `PATCH /api/v1/answers/{answer_id}`

Partially update an answer that belongs to the current test attempt. Only fields present in the body are modified (`exclude_unset=True`).

- **Auth**: required
- **Rate limit**: `500/minute`
- **Path**: `answer_id` (int, `> 0`)

Request body — [`AnswerUpdate`](app/domains/answer/schemas.py):

```json
{
  "response_option_id": 502,
  "response_time": 5500
}
```

Validations: same as `POST` for the fields provided. The attempt must still be `IN_PROGRESS`, and the answer must belong to the attempt referenced by the token.

Response `200 OK`: the updated `AnswerRead` shape.

Errors:

| Status | Cause                                                                                |
| ------ | ------------------------------------------------------------------------------------ |
| `400`  | Attempt not in progress, or response option does not belong to the answer's question |
| `401`  | Missing / invalid token                                                              |
| `404`  | Answer / test attempt / response option not found                                    |
| `422`  | Body fails Pydantic validation                                                        |
| `429`  | Rate limit exceeded                                                                   |

#### `GET /api/v1/answers`

List answers belonging to the current test attempt (derived from the JWT's `test_attempt_uuid` + `test_id`). Ordered by `created_at DESC, id DESC`.

- **Auth**: required
- **Rate limit**: `500/minute`
- **Query**: `limit`, `offset`

Response `200 OK`:

```json
{
  "items": [
    {
      "id": 7001,
      "test_attempt_id": 42,
      "question_id": 11,
      "response_option_id": 501,
      "boolean_answer": null,
      "open_text_answer": null,
      "response_time": 4200,
      "created_at": "2026-05-02T12:01:30"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

Errors: `401` for missing/invalid tokens; `429` rate limit.

#### `GET /api/v1/answers/affinity`

Compute the affinity between the current test attempt and every candidate that has at least one posture in a category the user actually answered.

The algorithm — implemented in [`service.get_affinity`](app/domains/answer/service.py) — works as follows:

1. **User vector** — for every category in which the user answered at least one question, compute `user_avg[c] = mean(response_option.value)`.
2. **Candidate vector** — for every candidate, compute `candidate_avg[c] = mean(posture.axis_value)` over their proposals in the same categories.
3. **Weighted Manhattan distance** — `distance = Σ |user_avg[c] − candidate_avg[c]| × weight[c]`.
4. **Normalized affinity** — axis values are in `[-1, +1]`, so the max possible per-category gap is `2`. The score is normalized to `[0, 1]`:
   `affinity = 1 − distance / Σ (2 × weight[c])`.

Only categories present in **both** vectors are compared (`categories_compared`). Candidates with zero shared categories are dropped. Results are sorted by `affinity DESC`.

Filtering rules applied throughout the aggregation:

- Answers without a `response_option_id` (i.e. boolean / open-text answers) are ignored.
- Questions without a `category_id` are ignored.
- Soft-deleted rows are excluded on `Answer`, `Question`, `Proposal`, `Posture`, and `Candidate`.

The response shape — defined by [`AffinityResponse`](app/domains/answer/schemas.py) (`CategoryAverage`, `CandidateAffinity`) — degrades gracefully:

| State                                                                  | `user_averages` | `candidates` |
| ---------------------------------------------------------------------- | --------------- | ------------ |
| User has not answered any categorized closed question yet              | `[]`            | `[]`         |
| User has answered, but no candidate has postures in those categories   | populated       | `[]`         |
| Both vectors overlap on ≥ 1 category                                   | populated       | populated    |

- **Auth**: required (uses `test_attempt_uuid` from the JWT, like the other answer endpoints)
- **Rate limit**: `500/minute`

Response `200 OK`:

```json
{
  "test_attempt_uuid": "9f1c4b0e-2d48-4e85-9a1a-72ae8b1a55b3",
  "user_averages": [
    {
      "category_id": 3,
      "category_name": "Educación",
      "weight": 1.5,
      "average": 0.6
    },
    {
      "category_id": 5,
      "category_name": "Economía",
      "weight": 1.0,
      "average": -0.2
    }
  ],
  "candidates": [
    {
      "candidate_id": 1,
      "presidential_candidate": "Jane Doe",
      "vice_presidential_candidate": "John Roe",
      "political_group": "Partido Ejemplo",
      "political_spectrum": "center-left",
      "photo_president": "https://cdn.elegio.app/p/1.jpg",
      "photo_vice_president": "https://cdn.elegio.app/vp/1.jpg",
      "photo_of_political_group": "https://cdn.elegio.app/groups/1.png",
      "affinity": 0.82,
      "distance": 0.9,
      "categories_compared": 2
    }
  ]
}
```

All graceful-degradation states above still return `200 OK` — only a missing test attempt yields an error.

Errors:

| Status | When                                                  |
| ------ | ----------------------------------------------------- |
| `401`  | Missing / invalid token                               |
| `404`  | Test attempt referenced by the token does not exist   |
| `429`  | Rate limit exceeded                                   |

---

### Search

[routes.py](app/domains/search/routes.py) · [service.py](app/domains/search/service.py) · [schemas.py](app/domains/search/schemas.py)

Hybrid full-text search across all proposal chunks. The endpoint runs a dense search against Qdrant (cosine similarity over multilingual-e5-large embeddings) and a BM25 lexical search against the in-memory index in parallel, then fuses the two ranked lists with Reciprocal Rank Fusion (`k = 60`). Results are collapsed to one entry per proposal (best-ranked chunk wins) and hydrated from MySQL with the full `candidate` and `category` relations. Soft-deleted proposals are filtered out during hydration.

> **Prerequisite.** The Qdrant collection (`proposal_chunks`) and the `proposal_chunks` MySQL rows must already be populated by the [analysis](../analysis) service. With an empty collection and an empty BM25 index the endpoint returns `{ "total": 0, "items": [] }`.

#### `GET /api/v1/search/proposals`

- **Auth**: none
- **Rate limit**: `100/minute`
- **Query**:
  - `q` (string, required, `min_length=1`) — search query
  - `category_id` (int, `> 0`, optional) — restrict to one category. Applied as a payload filter in Qdrant and as a metadata filter in BM25.
  - `candidate_id` (int, `> 0`, optional) — restrict to one candidate
  - `limit` (int, `1..100`, default `10`) — number of fused proposals to return

Response shape — defined by [`SearchResponse`](app/domains/search/schemas.py) / [`SearchHit`](app/domains/search/schemas.py). See `/docs` for the full schema. Each hit carries:

| Field            | Description                                                                                  |
| ---------------- | -------------------------------------------------------------------------------------------- |
| `score`          | RRF fusion score (higher is better; not normalized).                                          |
| `semantic_rank`  | 1-based position in the dense list, or `null` if the proposal was not retrieved semantically. |
| `semantic_score` | Cosine similarity from Qdrant for the best chunk.                                             |
| `lexical_rank`   | 1-based position in the BM25 list, or `null` if the proposal was not retrieved lexically.    |
| `lexical_score`  | Raw BM25 score for the best chunk.                                                            |
| `excerpt`        | Content of the best-matching chunk — semantic chunk preferred, otherwise lexical.            |

Errors: `422` if `q` is empty; `429` rate limit.

---

## 🧱 Conventions

### Domain layout

Each business area lives under `app/domains/{domain}/` with the four files documented in [Project structure](#-project-structure). Register the domain router in [app/api/v1/router.py](app/api/v1/router.py):

```python
from app.domains.candidate.routes import router as candidate_router
api_router.include_router(candidate_router)
```

### Models

- Use SQLAlchemy 2.0 syntax: `Mapped[]` and `mapped_column()`.
- Inherit from `Base` and `TimestampMixin` ([app/core/database.py](app/core/database.py)) so every table gets `created_at`, `updated_at`, and `deleted_at` for free. **Do not redefine these columns per model.**
- Soft-delete with `deleted_at` rather than hard deletes. All read queries filter `deleted_at IS NOT NULL` rows out.
- For constrained string sets, declare a `str, enum.Enum` and persist it with `SAEnum(MyEnum, name="my_enum")` so a native database enum is created. See `ConfidenceLevel` and `CoderType` in [app/domains/posture/models.py](app/domains/posture/models.py) for an example.

```python
from app.core.database import Base, TimestampMixin

class Candidate(Base, TimestampMixin):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    presidential_candidate: Mapped[str] = mapped_column(String(255), nullable=False)
    # ...
```

### Schemas

- Use **Pydantic v2** with `BaseModel`.
- For ORM-derived response models, set `model_config = ConfigDict(from_attributes=True)`.
- Validate inputs with `Field(...)` (`gt`, `ge`, `le`, `min_length`, `max_length`).

### Routes

- Every endpoint must declare a rate limit:
  - Public routes (no JWT): `@limiter.limit(PUBLIC_RATE_LIMIT)`.
  - Private routes (`Depends(get_token_payload)`): `@limiter.limit(PRIVATE_RATE_LIMIT)`.
- The handler must accept `request: Request` as its first parameter (slowapi requirement).
- List endpoints must accept `limit` and `offset` and return `{ items, total, limit, offset }`.
- Use `Path(gt=0)` and `Query(...)` to push validations to FastAPI.
- Translate domain exceptions from `service.py` to `HTTPException` with the right status code.

### Database access

Use the async session via dependency injection:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

@router.get("/items")
async def list_items(request: Request, db: AsyncSession = Depends(get_db)):
    ...
```

### Migrations (Alembic)

```bash
# Generate a migration after editing models
alembic revision --autogenerate -m "add candidate table"

# Apply
alembic upgrade head

# Rollback last
alembic downgrade -1
```

> When adding a new domain, import its models in [alembic/env.py](alembic/env.py) so autogenerate detects them.

---

## 🛠 Common commands

```bash
# Activate venv (Linux/Mac)
source venv/bin/activate

# Install / refresh deps
pip install -r requirements.txt

# Local DB
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml down

# Migrations
alembic upgrade head
alembic revision --autogenerate -m "..."
alembic downgrade -1

# Dev server
uvicorn app.main:app --reload

# Tests
pytest
```

---

## 🧹 Code style

- **Black** — formatter
- **Ruff** — linter
- **Conventional Commits** — `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`...
