# Elegio Analysis

Offline Python tool that uses **Google Gemini** to classify (rate) the political proposals stored by the [Elegio API](../api) on a `-1.0` / `+1.0` descriptive axis. For every proposal that does not yet have a `Posture`, the tool builds a category-specific prompt, asks Gemini for a JSON-structured rating, and writes the result back into the same MySQL database the API uses. It is a **batch script**, not a service: there is no HTTP server and no public API surface.

---

## Table of contents

- [Overview](#overview)
- [Tech stack](#-tech-stack)
- [Project structure](#-project-structure)
- [How it works](#-how-it-works)
- [Setup](#-setup)
- [Environment variables](#-environment-variables)
- [Usage](#-usage)
- [Data model](#-data-model)
- [Rubrics](#-rubrics)
- [Conventions](#-conventions)
- [Common commands](#-common-commands)
- [Code style](#-code-style)

---

## Overview

The Elegio platform compares each user's answers against a numeric coding of every candidate's proposals. That coding lives in the `postures` table: a `Posture` is a single rating of one `Proposal` on a `Category`'s descriptive axis (the `-1.0` / `+1.0` scale described in the [API README](../api/README.md#proposals)).

Manually coding every proposal is slow and prone to inconsistency. The `analysis/` service automates the first pass:

1. It selects proposals that don't have a posture yet.
2. It feeds each proposal — together with the rubric for its category — to Gemini.
3. It persists the model's answer (`score`, `confidence`, `reasoning`, `ambiguities`) as a `Posture` row tagged with `coder_type = "llm"` and `coder_name = "<gemini model>"`.

Human reviewers can later add their own postures (with `coder_type = "human"`) for the same proposals; the `coder_type` / `coder_name` fields are what makes that audit trail possible.

> The schema is **owned by the API**. All migrations live in [`api/alembic/`](../api/alembic). `analysis/` only reads and writes the existing tables.

---

## 🚀 Tech stack

- **Python** — sync runtime (no event loop, no FastAPI)
- **google-genai** — official Gemini SDK; configured to return JSON matching a Pydantic schema
- **SQLAlchemy 2.0 Core (sync)** — Table definitions and connection management
- **PyMySQL** + **cryptography** — sync MySQL driver
- **Pydantic v2** — schemas for the LLM response and the in-memory proposal/category models
- **python-dotenv** — loads `.env` into process environment
- **pandas** — available for ad-hoc data exploration scripts (not used by `rate_batch` itself)

> Unlike the [API](../api), this project uses **sync** SQLAlchemy. There is no async loop and no ORM session; data access goes through SQLAlchemy Core (`Table`, `select`, `insert`).

---

## 📁 Project structure

```
analysis/
├── app/
│   ├── __init__.py
│   ├── config.py                       # Settings loader (.env → pydantic model)
│   ├── core/
│   │   ├── database.py                 # Sync engine + Core Tables (categories, proposals, postures)
│   │   └── gemini_client.py            # GeminiClassifier wrapper around google-genai
│   └── domains/
│       └── posture_proposal/
│           ├── prompt.py               # build_prompt(category, text) → Spanish prompt
│           ├── rubrics.py              # RUBRICS dict: per-category poles + numeric anchors
│           ├── schemas.py              # Pydantic models (QualificationLLM, ProposalRead, ...)
│           └── service.py              # PostureService.rate_proposal(proposal)
├── scripts/
│   └── rate_batch.py                   # Entry point: classify every pending proposal
├── main.py                             # Smoke test for the Gemini client
├── requirements.txt
├── .env.example
└── .env                                # Local config (gitignored)
```

---

## ⚙️ How it works

### Pipeline

```
┌──────────────────┐   ┌────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ proposals (DB)   │──▶│ build_prompt() │──▶│ GeminiClassifier │──▶│ postures (DB)    │
│ joined w/ cats   │   │ + rubric       │   │ JSON-constrained │   │ coder_type = llm │
└──────────────────┘   └────────────────┘   └──────────────────┘   └──────────────────┘
       ▲                                                                    │
       └────────────────── only rows where no posture exists ◀──────────────┘
```

1. **Select pending proposals.** [`scripts/rate_batch.py`](scripts/rate_batch.py) runs a SQLAlchemy Core query that joins `proposals` and `categories`, left-joins `postures`, and keeps only rows where no posture exists (`postures.id IS NULL`). This makes the script **idempotent**: rerunning it never re-rates a proposal that already has a posture.
2. **Build the prompt.** [`build_prompt`](app/domains/posture_proposal/prompt.py) looks up the rubric for the proposal's category (negative pole, positive pole, and the five numeric anchors at `-1.0`, `-0.5`, `0.0`, `+0.5`, `+1.0`) and renders a Spanish prompt that frames the task as **descriptive, not evaluative** (the `-1`/`+1` axis is a position on a line, not a value judgement).
3. **Call Gemini.** [`GeminiClassifier.classify`](app/core/gemini_client.py) calls the model (default: `gemini-2.5-flash`) with `response_mime_type="application/json"`, `response_schema=QualificationLLM`, and `temperature=0.1`. The SDK returns an already-parsed `QualificationLLM` instance — no manual JSON parsing.
4. **Persist the posture.** [`PostureService.rate_proposal`](app/domains/posture_proposal/service.py) inserts a row into `postures` with the score, confidence, reasoning, ambiguities, `coder_type = "llm"`, and `coder_name = "<gemini model>"`. The connection is committed per proposal so a mid-batch failure does not lose previously rated proposals.
5. **Throttle.** The batch loop sleeps **1 second after a success** and **5 seconds after an error** — a small allowance for free-tier rate limits and transient API errors.

### LLM response contract

Gemini is forced to return JSON matching [`QualificationLLM`](app/domains/posture_proposal/schemas.py):

| Field         | Type                           | Notes                                                          |
| ------------- | ------------------------------ | -------------------------------------------------------------- |
| `ambiguities` | `str`                          | Aspects of the axis the proposal leaves vague or unaddressed   |
| `reasoning`   | `str`                          | 2–3 sentences explaining where the proposal was placed and why |
| `confidence`  | `"high" \| "medium" \| "low"`  | Maps directly to the DB enum                                   |
| `score`       | `float`, `-1.0 ≤ score ≤ 1.0`  | Recommended in increments of `0.25`                            |

The prompt asks the model to keep the score close to `0` with `low` confidence whenever the proposal is vague, mixed, or only tangential to the axis.

---

## 📦 Setup

### Prerequisites

- **Python 3.12**
- A running **MySQL 8** instance with the Elegio schema applied. The easiest path is to start the API's bundled docker-compose (see [api/README.md → Setup](../api/README.md#-setup)) and run `alembic upgrade head` from `api/`. `analysis/` will read and write the same database.
- A **Google AI Studio API key** for Gemini (`GEMINI_API_KEY`).

### 1. Install dependencies

```bash
cd analysis
python3.12 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```bash
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=mysql+pymysql://elegio_user:elegio_password@localhost:3306/elegio
```

> `DATABASE_URL` **must** point to the same database the API uses. `analysis/` does not run migrations — it expects the schema to already exist.

### 3. Smoke-test the Gemini client (optional)

```bash
python main.py
```

Expected output:

```
Analysis project ready. Gemini client initialized.
Available models: ['models/embedding-gecko-001', 'models/gemini-1.0-pro-vision-latest', 'models/gemini-pro-vision']
```

If the call fails, double-check that `GEMINI_API_KEY` is set and your network can reach `generativelanguage.googleapis.com`.

---

## 🔧 Environment variables

Loaded from `analysis/.env` via [`Settings`](app/config.py) (Pydantic v2). See [.env.example](.env.example).

| Key              | Required | Default | Description                                                                 |
| ---------------- | :------: | ------- | --------------------------------------------------------------------------- |
| `GEMINI_API_KEY` |  **yes** | —       | Google AI Studio API key. Used to authenticate the `google-genai` client.   |
| `DATABASE_URL`   |  **yes** | —       | Sync MySQL URL — `mysql+pymysql://user:pass@host:3306/elegio`               |

Both fields are validated as `min_length=1`, so an empty value at startup raises a Pydantic `ValidationError`.

---

## ▶️ Usage

Run the batch from the `analysis/` directory:

```bash
python -m scripts.rate_batch
```

The script:

1. Prints `Pending proposals: N`.
2. For each proposal, prints one line:
   ```
   [12/47] Proposal 134 (educacion): +0.50 (high)
   ```
3. On error, prints `[i/N] x Proposal <id>: <error message>`, rolls back the connection, and continues with the next proposal.
4. At the end, prints a summary of any failed proposals.

### Idempotency

Only proposals **without** a posture are picked up. To re-rate a proposal you must first soft-delete (or hard-delete) its existing `postures` rows. Soft-delete is set by stamping `deleted_at`; the current pending-proposal query in `rate_batch` does **not** filter on `deleted_at`, so a soft-deleted posture still hides its proposal from the next run. Hard-delete the row if you want it re-rated.

### Throttling

- `time.sleep(1)` after every success.
- `time.sleep(5)` after every failure.

These delays are hard-coded in [`scripts/rate_batch.py`](scripts/rate_batch.py). Adjust them in-place if you move to a paid Gemini tier with higher quotas.

### Choosing a different model

Pass a different model name when constructing the classifier:

```python
classifier = GeminiClassifier(model="gemini-2.5-pro")
```

The chosen model name is stored verbatim in `postures.coder_name`, so changing the model produces postures attributable to that specific model.

---

## 🗃 Data model

`analysis/` reads from `categories` + `proposals` and writes to `postures`. The columns are mirrored from the API's models in [`app/core/database.py`](app/core/database.py); the canonical definitions live in the API's SQLAlchemy models and Alembic migrations.

### Read

| Source       | Columns used                                                      |
| ------------ | ----------------------------------------------------------------- |
| `categories` | `id`, `name`, `weight`                                            |
| `proposals`  | `id`, `title`, `summary`, `full_text`, `category_id`              |

The query joins `proposals → categories` and left-joins `postures` to pick rows where no posture exists.

### Write

Every successful classification inserts a single row into `postures`:

| Column        | Value written                                          | Source                                     |
| ------------- | ------------------------------------------------------ | ------------------------------------------ |
| `proposal_id` | `proposal.id`                                          | from the pending-proposals query           |
| `axis_value`  | `result.score` (`-1.0 ≤ x ≤ 1.0`)                      | LLM output                                 |
| `confidence`  | `"high" \| "medium" \| "low"`                          | LLM output, mapped via `CONFIDENCE_MAP`    |
| `reasoning`   | `result.reasoning`                                     | LLM output                                 |
| `ambiguities` | `result.ambiguities`                                   | LLM output                                 |
| `coder_type`  | `"llm"`                                                | constant (`CoderType.LLM`)                 |
| `coder_name`  | the Gemini model id, e.g. `"gemini-2.5-flash"`         | `GeminiClassifier.model`                   |
| `created_at`  | `NOW()`                                                | DB default                                 |
| `updated_at`  | `NOW()` on insert / update                             | DB default                                 |
| `deleted_at`  | `NULL`                                                 | unset                                      |

The `coder_type` / `coder_name` pair is the audit trail the API surfaces for downstream consumers — it lets the UI distinguish LLM-generated postures from human-coded ones.

---

## 📐 Rubrics

Rubrics live in [`app/domains/posture_proposal/rubrics.py`](app/domains/posture_proposal/rubrics.py) as a `RUBRICS` dictionary keyed by category slug. Each entry has the same shape:

```python
"educacion": {
    "polo_negativo": {
        "nombre": "mercado-eleccion",
        "descripcion": "subsidios a la demanda, competencia y libertad de elección",
    },
    "polo_positivo": {
        "nombre": "publica-universal",
        "descripcion": "educación pública gratuita y universal como derecho",
    },
    "anclajes": {
        -1.0: "...",
        -0.5: "...",
         0.0: "...",
        +0.5: "...",
        +1.0: "...",
    },
}
```

`build_prompt` raises `ValueError` if it is asked for a category that is not in `RUBRICS`:

```
ValueError: No rubric defined for category 'foo'. Available: ['corrupcion', 'paz', ...]
```

To add a new axis:

1. Add a new key to `RUBRICS` with both poles and the five anchor descriptions.
2. Make sure the API has a `Category` row whose identifier matches that key (see the gap below).

### Known gap: category slug vs. category name

`RUBRICS` is keyed by **slug-like identifiers** (`"corrupcion"`, `"paz"`, `"transformacion_social"`, ...). The API's `Category` model, however, only exposes a `name` (no `slug`) — see [`api/app/domains/category/models.py`](../api/app/domains/category/models.py). [`PostureService.rate_proposal`](app/domains/posture_proposal/service.py) currently passes `category.name` as the `category_slug` argument:

```python
prompt = build_prompt(
    category_slug=proposal.category.name,
    category_name=proposal.category.name,
    proposal_text=proposal.full_text or proposal.summary or proposal.title,
)
```

This means the database's `categories.name` values must literally match the keys in `RUBRICS` (`"corrupcion"`, `"paz"`, …) for the batch to succeed. Any other display name will hit the `ValueError` above. Tracked as a gap to be resolved by adding a `slug` column to `Category` on the API side.

---

## 🧱 Conventions

### Schema ownership

- The Elegio database schema is **owned by the API**. Every migration belongs in [`api/alembic/`](../api/alembic).
- The `Table` definitions in [`app/core/database.py`](app/core/database.py) are read/write mirrors. **If the API's models change, the mirrors here must be updated by hand.**
- `analysis/` does **not** run Alembic and never creates tables.

### Sync I/O

- Use **sync** SQLAlchemy Core (`engine.connect()`, `conn.execute(...)`, `conn.commit()`).
- Do not introduce `asyncio` / `aiomysql` here — the rest of the project assumes the sync model.

### LLM responses

- Always pin the response shape with `response_schema=<PydanticModel>` so the SDK enforces JSON validity. Free-form text responses are not allowed.
- Set a low `temperature` (`0.1` today) to keep ratings reproducible.

### Code layout

- Domain code goes under `app/domains/<domain>/`, mirroring the API's structure.
- Reusable infrastructure (DB engine, LLM client, settings) goes under `app/core/`.
- Entry points (batch jobs, CLIs) go under `scripts/`. Run them with `python -m scripts.<name>` so package imports resolve correctly.

### Documentation

- Documentation is written in **English** to stay consistent with the rest of the monorepo.
- Prompts and rubric content stay in **Spanish** because they are aimed at the model's classification of Spanish-language Colombian political proposals.

---

## 🛠 Common commands

```bash
# Activate venv (Linux/Mac)
source venv/bin/activate

# Install / refresh deps
pip install -r requirements.txt

# Smoke-test the Gemini client
python main.py

# Run the batch classifier
python -m scripts.rate_batch
```

---

## 🧹 Code style

- **Black** — formatter
- **Ruff** — linter
- **Conventional Commits** — `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`...
