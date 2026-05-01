# Elegio - Monorepo

## Project Structure

```
elegio/
├── api/           # FastAPI backend
├── frontend/      # Next.js frontend
└── analysis/      # AI proposal analysis
```

## Tech Stack

### Backend ([api/](api/))
- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy 2.0 (async/sync)
- **Migrations**: Alembic
- **Validation**: Pydantic v2

### Frontend ([frontend/](frontend/))
- **Framework**: Next.js
- **Styling**: Tailwind CSS
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

### Migrations (Alembic)
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migration: `alembic upgrade head`
- Rollback: `alembic downgrade -1`

### Frontend (Next.js)
- App Router (Next.js 13+)
- Components in `components/`
- Server Actions for mutations
- Route Handlers for backend calls

## Common Commands

### Backend
```bash
cd api
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Testing
- Backend: `pytest`
- Frontend: `npm test`

## Environment Variables

Each service has its own `.env`:
- `api/.env` - Backend config (DB_URL, etc)
- `frontend/.env.local` - Frontend config (API_URL, etc)

## Code Conventions

- Python: Black formatter, Ruff linter
- TypeScript/React: Prettier, ESLint
- Commits: Conventional Commits (`feat:`, `fix:`, `chore:`)
