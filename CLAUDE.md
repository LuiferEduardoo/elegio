# Elegio - Monorepo

## Project Structure

```
elegio/
├── api/           # FastAPI backend
├── elegio-front/  # Vite + React frontend
└── analysis/      # AI proposal analysis
```

## Tech Stack

### Backend ([api/](api/))
- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy 2.0 (async/sync)
- **Migrations**: Alembic
- **Validation**: Pydantic v2

### Frontend ([elegio-front/](elegio-front/))
- **Framework**: Vite + React 19
- **Styling**: CSS
- **State**: React Context / Zustand (as needed)

### AI ([analysis/](analysis/))
- Proposal analysis with language models

## Conventions

### Backend (FastAPI)
- Use **async/await** for database operations
- Domain structure: `api/app/domains/{domain}/`
- SQLAlchemy 2.0 models: `Mapped[]` and `mapped_column()`
- All models **must** include `created_at`, `updated_at`, and `deleted_at` (DateTime). Inherit from `TimestampMixin` in [api/app/core/database.py](api/app/core/database.py) instead of redefining them per model.
- Pydantic v2 for request/response models
- API routes: `/api/v1/{resource}`
- GET endpoints that return multiple items **must** be paginated via `limit` and `offset` query params. Default `limit` is `10` (max `100`); default `offset` is `0`.
- Every endpoint **must** declare a rate limit using slowapi:
  - **Public routes** (no JWT): `@limiter.limit(PUBLIC_RATE_LIMIT)`
  - **Private routes** (`Depends(get_token_payload)`): `@limiter.limit(PRIVATE_RATE_LIMIT)`
  - Constants live in [api/app/core/rate_limit.py](api/app/core/rate_limit.py). The decorated handler must accept `request: Request` as its first parameter so slowapi can read the client IP.

### Migrations (Alembic)
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migration: `alembic upgrade head`
- Rollback: `alembic downgrade -1`

### Frontend (Vite + React)
- Components in `components/`
- API calls should target the FastAPI backend at `http://localhost:8000` in local development

## Common Commands

### Backend
```bash
cd api
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env
# For the bundled local DB, set:
# DATABASE_URL=mysql+aiomysql://elegio_user:elegio_password@localhost:3306/elegio
# DATABASE_URL_SYNC=mysql+pymysql://elegio_user:elegio_password@localhost:3306/elegio
docker compose -f docker-compose.dev.yml up -d
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd elegio-front
npm install
npm run dev
```

### Testing
- Backend: `pytest`
- Frontend: `npm test`

## Environment Variables

Each service has its own `.env`:
- `api/.env` - Backend config (DB_URL, etc)
- `elegio-front/.env.local` - Frontend config (API_URL, etc)

## Code Conventions

- Python: Black formatter, Ruff linter
- TypeScript/React: Prettier, ESLint
- Commits: Conventional Commits (`feat:`, `fix:`, `chore:`)
- Commit authorship: only the repo owner. Do **not** add `Co-Authored-By:` trailers (no Claude, no AI agent) — every commit goes solo to the user.
