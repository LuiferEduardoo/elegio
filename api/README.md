# Elegio API

Backend FastAPI for the Elegio platform — exposes the REST endpoints consumed by the frontend and the analysis service.

## 🚀 Tech Stack

- **FastAPI** — async web framework
- **SQLAlchemy 2.0** — async ORM (`Mapped[]` / `mapped_column()`)
- **Alembic** — database migrations (async template)
- **Pydantic v2** + **pydantic-settings** — validation and config
- **MySQL** via `aiomysql` (async) and `pymysql` (sync fallback)

## 📁 Structure

```
api/
├── alembic/              # Migration environment and versions
├── alembic.ini           # Alembic config (sqlalchemy.url injected from env)
├── app/
│   ├── main.py           # FastAPI entrypoint
│   ├── api/v1/router.py  # /api/v1 root router
│   ├── core/
│   │   ├── config.py     # Settings (loads .env)
│   │   └── database.py   # Async engine, Base, get_db()
│   └── domains/          # One folder per domain (models, schemas, routes, services)
├── requirements.txt
├── .env.example
└── .env                  # Local config (gitignored)
```

## 📦 Setup

### Prerequisites
- Python 3.12
- MySQL 8+

### Install

```bash
cd api
python3.12 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### Configure

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Variables:

| Key                  | Description                                       |
| -------------------- | ------------------------------------------------- |
| `APP_NAME`           | App name shown in OpenAPI                         |
| `APP_ENV`            | `development` / `staging` / `production`          |
| `DEBUG`              | Enables SQL echo and FastAPI debug                |
| `DATABASE_URL`       | Async URL — `mysql+aiomysql://user:pass@host/db`  |
| `DATABASE_URL_SYNC`  | Sync URL — `mysql+pymysql://user:pass@host/db`    |

### Run migrations

```bash
alembic upgrade head
```

### Start the server

```bash
uvicorn app.main:app --reload
```

Endpoints:
- `GET /` — app info
- `GET /api/v1/health` — health check
- `GET /docs` — interactive Swagger UI
- `GET /redoc` — ReDoc UI

## 🧱 Conventions

### Domains

Each business area lives under `app/domains/{domain}/`. Suggested layout:

```
app/domains/candidate/
├── __init__.py
├── models.py       # SQLAlchemy 2.0 models (Mapped[], mapped_column())
├── schemas.py      # Pydantic v2 request/response models
├── routes.py       # APIRouter with /api/v1/{resource}
└── service.py      # Business logic (async)
```

Then register the domain router in [app/api/v1/router.py](app/api/v1/router.py):

```python
from app.domains.candidate.routes import router as candidate_router
api_router.include_router(candidate_router)
```

### Database access

Use async sessions via dependency injection:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

@router.get("/items")
async def list_items(db: AsyncSession = Depends(get_db)):
    ...
```

### Migrations

```bash
# Generate a migration after editing models
alembic revision --autogenerate -m "add candidate table"

# Apply
alembic upgrade head

# Rollback last
alembic downgrade -1
```

> When adding a new domain, import its models in [alembic/env.py](alembic/env.py) so autogenerate detects them.

## 🧪 Testing

```bash
pytest
```

## 🧹 Code style

- **Black** — formatter
- **Ruff** — linter
- Conventional Commits (`feat:`, `fix:`, `chore:`, ...)
