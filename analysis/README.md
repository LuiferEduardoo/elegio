# Elegio Analysis

Offline Python tool that uses **Google Gemini** to classify (rate) the political proposals stored by the [Elegio API](../api) on a `-1.0` / `+1.0` descriptive axis. For every proposal that does not yet have a `Posture`, the tool builds a category-specific prompt, asks Gemini for a JSON-structured rating, and writes the result back into the same MySQL database the API uses. It is a **batch script**, not a service: there is no HTTP server and no public API surface.

This service also owns the **chunking + embedding pipelines** that feed the API's hybrid search endpoint. Beyond proposals, it ingests three more candidate content sources — **news articles**, **documents** (PDFs), and **interviews** (video/speech transcripts) — each through its own `extract/load → chunk → embed` pipeline. Every content type is chunked, embedded with `gemini-embedding-001` (Gemini API), and upserted into its **own** Qdrant collection that the API can query at search time.

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
- **google-genai** — official Gemini SDK; used both for the JSON-schema classifier and for `gemini-embedding-001` embeddings
- **SQLAlchemy 2.0 Core (sync)** — Table definitions and connection management
- **PyMySQL** + **cryptography** — sync MySQL driver
- **Pydantic v2** — schemas for the LLM response and the in-memory proposal/category models
- **python-dotenv** — loads `.env` into process environment
- **pandas** — available for ad-hoc data exploration scripts (not used by `rate_batch` itself)
- **gemini-embedding-001** (via **google-genai**) — 1536-dim multilingual embeddings used by every chunking/embedding pipeline; no local model is loaded
- **qdrant-client** — pushes the embeddings into a local Qdrant instance (the same one the API queries). One collection per content type: `proposal_chunks`, `news_chunks`, `document_chunks`, `interview_chunks`
- **trafilatura** + **ftfy** — HTML article extraction and encoding repair for the news pipeline
- **docling** — parses PDFs into structure-preserving Markdown for the documents pipeline. It pulls `transformers`, which is pinned `<5` to stay compatible with the `torch 2.4.1` that pyannote requires; `torchvision` must be the matching `+cpu` build

> Unlike the [API](../api), this project uses **sync** SQLAlchemy. There is no async loop and no ORM session; data access goes through SQLAlchemy Core (`Table`, `select`, `insert`).

---

## 📁 Project structure

```
analysis/
├── app/
│   ├── __init__.py
│   ├── config.py                       # Settings loader (.env → pydantic model)
│   ├── core/
│   │   ├── database.py                 # Sync engine + Core Tables (categories, proposals, postures, *_chunks, news, documents, interviews, ...)
│   │   ├── gemini_client.py            # GeminiClassifier wrapper around google-genai
│   │   ├── embedder.py                 # Embedder wrapper around google-genai (gemini-embedding-001)
│   │   └── qdrant_client.py            # Qdrant client + collection names + ensure_collection() helper
│   └── domains/
│       ├── posture_proposal/
│       │   ├── prompt.py               # build_prompt(category, text) → Spanish prompt
│       │   ├── rubrics.py              # RUBRICS dict: per-category poles + numeric anchors
│       │   ├── schemas.py              # Pydantic models (QualificationLLM, ProposalRead, ...)
│       │   └── service.py              # PostureService.rate_proposal(proposal)
│       ├── proposal_chunk/
│       │   ├── chunker.py              # Paragraph-aware chunking (target/max/overlap in words)
│       │   ├── embedding.py            # MySQL → Qdrant glue (fetch_chunks, embed_and_upsert, ...)
│       │   ├── schemas.py
│       │   └── service.py              # chunk_and_insert + get_pending_proposals
│       ├── transcription/              # YouTube download → Whisper → pyannote → Gemini speaker map
│       ├── news/
│       │   ├── fetcher.py              # trafilatura.fetch_url + HTML cache
│       │   ├── extractor.py            # trafilatura.extract (content, title, date)
│       │   ├── preprocessor.py         # clean_content: encoding, URLs, boilerplate, tweets, refs
│       │   ├── loader.py               # news/<slug>.json → news table (resolve candidate by name)
│       │   └── service.py              # process_article(spec) orchestration
│       ├── news_chunk/
│       │   ├── chunker.py              # (reuses proposal_chunk.chunker)
│       │   ├── vitaminize.py           # [Candidato]/[Medio]/Titular prefix added to each chunk
│       │   ├── embedding.py            # MySQL → Qdrant (news_chunks collection)
│       │   └── service.py              # chunk_and_insert + get_pending_news
│       ├── document/
│       │   ├── converter.py            # Docling PDF → structure-preserving Markdown
│       │   ├── preprocessor.py         # Markdown cleanup
│       │   ├── loader.py               # documents/<slug>.json → documents table
│       │   └── service.py              # process_document(spec) orchestration
│       ├── document_chunk/
│       │   ├── chunker.py              # Structure-aware Markdown chunker (headings, tables, bullets)
│       │   ├── embedding.py            # MySQL → Qdrant (document_chunks collection)
│       │   └── service.py              # chunk_and_insert + get_pending_documents
│       ├── interview/
│       │   └── loader.py               # transcripts/<slug>.json → interviews + interview_segments
│       └── interview_chunk/
│           ├── chunker.py              # Conversation-aware chunker (groups turns, labels [speaker])
│           ├── embedding.py            # MySQL → Qdrant (interview_chunks collection)
│           └── service.py              # chunk_and_insert + get_pending_interview_ids
├── docker-compose.dev.yml              # Local Qdrant instance (ports 6333 REST, 6334 gRPC)
├── scripts/
│   ├── rate_batch.py                   # Classify every pending proposal
│   ├── chunk_proposals.py              # Split proposals into proposal_chunks rows
│   ├── embed_chunks.py                 # Embed proposal chunks and upsert them into Qdrant
│   ├── transcribe_videos.py            # videos.yaml → transcripts/<slug>.json
│   ├── extract_news.py                 # news.yaml → news/<slug>.json
│   ├── load_news.py                    # news/<slug>.json → news table
│   ├── chunk_news.py                   # Split news into news_chunks rows
│   ├── embed_news.py                   # Embed news chunks → news_chunks collection
│   ├── extract_documents.py            # documents.yaml → documents/<slug>.json (Docling)
│   ├── load_documents.py               # documents/<slug>.json → documents table
│   ├── chunk_documents.py              # Split documents into document_chunks rows
│   ├── embed_documents.py              # Embed document chunks → document_chunks collection
│   ├── load_interviews.py              # transcripts/<slug>.json → interviews + segments
│   ├── chunk_interviews.py             # Group interview turns into interview_chunks rows
│   ├── embed_interviews.py             # Embed interview chunks → interview_chunks collection
│   ├── documents.yaml / documents.example.yaml  # Documents pipeline config (yaml gitignored)
│   ├── news.yaml / news.example.yaml            # News pipeline config (yaml gitignored)
│   └── videos.yaml / videos.example.yaml        # Transcription/interview config (yaml gitignored)
├── reindex.py                          # Drop + rebuild the proposal_chunks Qdrant collection (re-embed all chunks)
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

### Chunking pipeline

```
┌──────────────────┐   ┌────────────────┐   ┌──────────────────┐
│ proposals (DB)   │──▶│  chunk_text()  │──▶│ proposal_chunks  │
│ no chunks yet    │   │ paragraph-     │   │ (DB)             │
└──────────────────┘   │ aware splitter │   └──────────────────┘
                       └────────────────┘
```

1. **Select proposals without chunks.** [`get_pending_proposals`](app/domains/proposal_chunk/service.py) returns proposals that do not yet have any `proposal_chunks` row. The batch is **idempotent** — rerunning it never re-chunks a proposal that already has chunks. To re-chunk, hard-delete its `proposal_chunks` rows first.
2. **Split the text.** [`chunk_text`](app/domains/proposal_chunk/chunker.py) packs paragraphs greedily until a chunk reaches the target word count, then seeds the next chunk with an overlap window so context is preserved across boundaries. The current defaults are:

   | Knob              | Value      | Notes                                                                             |
   | ----------------- | ---------: | --------------------------------------------------------------------------------- |
   | `TARGET_WORDS`    | `150`      | ~200 tokens of Spanish text (Gemini's rough 1.33 tokens/word ratio).              |
   | `MAX_WORDS`       | `300`      | Hard ceiling per chunk; a paragraph longer than this is window-split standalone.  |
   | `OVERLAP_WORDS`   | `20`       | Tail of the previous chunk reused as the head of the next.                        |
   | `MIN_SPLIT_WORDS` | `150`      | Inputs shorter than this are returned as a single chunk (no splitting at all).    |

3. **Persist.** `chunk_and_insert` writes one `proposal_chunks` row per chunk with `chunk_index` (0-based) and `total_chunks`. Soft-deleted proposals are skipped.

### Embedding pipeline

```
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ proposal_chunks  │──▶│ Embedder.embed_  │──▶│ Qdrant           │
│ JOIN proposals   │   │ passages (1536d) │   │ proposal_chunks  │
└──────────────────┘   └──────────────────┘   └──────────────────┘
```

1. **Diff against Qdrant.** [`scripts/embed_chunks.py`](scripts/embed_chunks.py) lists every non-deleted chunk id in MySQL, asks Qdrant which of those ids already exist as points, and processes only the difference. The Qdrant point id is the MySQL chunk id, so the operation is **naturally idempotent** — rerunning the script never re-embeds a chunk that is already stored.
2. **Fetch with context.** [`fetch_chunks`](app/domains/proposal_chunk/embedding.py) joins `proposal_chunks` with `proposals` so each Qdrant point's payload carries `proposal_id`, `chunk_index`, `total_chunks`, `content`, `category_id`, and `candidate_id`. The last two fields are what enables the API's filtered search (`?category_id=` / `?candidate_id=`).
3. **Embed in batches.** The [`Embedder`](app/core/embedder.py) calls `gemini-embedding-001` through the Gemini API (1536-dim, L2-normalized). It uses task-specific types — `RETRIEVAL_DOCUMENT` for chunks, `RETRIEVAL_QUERY` for searches. Documents and queries must use the **same** model, otherwise dot-product similarity is meaningless. Batch size is `100`.
4. **Upsert.** Points are upserted into the `proposal_chunks` Qdrant collection (`Distance.COSINE`, 1536-dim). The collection is created on demand by [`ensure_collection`](app/core/qdrant_client.py).

### End-to-end flow

```
docker compose -f docker-compose.dev.yml up -d        # 1. Start Qdrant
python -m scripts.chunk_proposals                     # 2. Split proposals into proposal_chunks rows
python -m scripts.embed_chunks                        # 3. Embed chunks and upsert into Qdrant
# 4. (Re)start the API — it picks up new chunks on its lifespan hook (see api/README.md)
```

Step 4 matters because the API's BM25 index has no auto-invalidation: the API must be restarted for newly embedded chunks to be searchable lexically. Qdrant is queried directly so dense results pick them up immediately.

### Content-source pipelines (news, documents, interviews)

Beyond proposals, three more candidate content sources are ingested through their own `extract/load → chunk → embed` pipelines. They all mirror the proposals flow: an idempotent chunker writes `*_chunks` rows in MySQL, then an idempotent embedder upserts them into a dedicated Qdrant collection where the Qdrant point id equals the MySQL chunk id. Collection names live in [`app/core/qdrant_client.py`](app/core/qdrant_client.py): `proposal_chunks`, `news_chunks`, `document_chunks`, `interview_chunks`. The Core `Table` definitions for every new table were added to [`app/core/database.py`](app/core/database.py) (the canonical schema is still owned by the API's Alembic migrations).

Run each pipeline's scripts in order:

#### 1. News

```
extract_news → load_news → chunk_news → embed_news
```

1. **`extract_news`** — for each article in [`scripts/news.yaml`](scripts/news.example.yaml), fetches the page HTML with `trafilatura` (cached under `news_cache/`) and extracts clean content + title + date. The [`preprocessor`](app/domains/news/preprocessor.py) repairs encoding (`ftfy`), strips stray URLs, and additionally removes recurring publisher boilerplate (subscribe prompts, fact-check intros/outros), inline reference markers like `(1, 2, 3)`, embedded tweet/X footers and `@handles`, then collapses whitespace. Writes `news/<slug>.json` per candidate (now including `publishing_house`).
2. **`load_news`** — joins `news.yaml` metadata with `news/<slug>.json` and inserts one row per article into the `news` table, resolving the candidate by name. Idempotent on `news.uuid`.
3. **`chunk_news`** — splits `content_raw` with the shared paragraph-aware chunker and stores each chunk **vitaminized** ([`vitaminize`](app/domains/news_chunk/vitaminize.py)) with a `[Candidato: …] [Medio: …]. Titular: …. Contenido: …` prefix, so the value embedded later is exactly what lives in `news_chunks.content_chunk`.
4. **`embed_news`** — embeds pending chunks and upserts them into the `news_chunks` Qdrant collection. Each point's payload carries `news_id`, `news_uuid`, `candidate_id`, `candidate_name`, `publishing_house`, `source_type`, and `content`.

#### 2. Documents

```
extract_documents → load_documents → chunk_documents → embed_documents
```

1. **`extract_documents`** — for each PDF in [`scripts/documents.yaml`](scripts/documents.example.yaml) (copy the example to `documents.yaml`; it is gitignored), [Docling](https://docling-project.github.io/docling/) parses the PDF into structure-preserving Markdown (headings, paragraphs, lists, tables) via the new [`app/domains/document/`](app/domains/document) converter + preprocessor. Per-document fields include `type` (e.g. `legal_document` / `campaign_document`) and `url`. Markdown is cached under `document_cache/`; writes `documents/<slug>.json` per candidate.
2. **`load_documents`** — inserts one row per PDF into the `documents` table (candidate resolved by name). Idempotent on `documents.uuid`.
3. **`chunk_documents`** — uses the **structure-aware Markdown chunker** in [`app/domains/document_chunk/chunker.py`](app/domains/document_chunk/chunker.py): it splits at heading/section boundaries (a chunk never spans two sections) and prefixes each chunk with its heading-path context, keeps tables (`| ... |` blocks) and bullet items whole, and groups continuous paragraphs up to a target size (windowing a single oversized paragraph with overlap). Defaults: `TARGET_WORDS=200`, `MAX_WORDS=400`, `OVERLAP_WORDS=30`.
4. **`embed_documents`** — embeds pending chunks into the `document_chunks` Qdrant collection. Payload carries `document_id`, `document_uuid`, `candidate_id`, `candidate_name`, `source_type`, `type`, `title`, `publishing_house`, `url`, and `content`.

#### 3. Interviews

```
(transcribe_videos →) load_interviews → chunk_interviews → embed_interviews
```

1. **`load_interviews`** — reads `transcripts/<slug>.json` (produced by the existing transcription pipeline, `scripts/transcribe_videos.py`) and inserts **one `interviews` row per video**, plus its `interview_segments` — consecutive same-speaker turns are merged into a single segment (keeping the first start_time, the last end_time, and concatenating text). Transcript `published_date` values are `YYYY-DD-MM` (day before month) and parsed accordingly. Idempotent on `interviews.uuid` (== `video_id`).
2. **`chunk_interviews`** — the conversation-aware chunker in [`app/domains/interview_chunk/chunker.py`](app/domains/interview_chunk/chunker.py) groups consecutive turns into chunks of ~target size (so a question and its answer stay together), labels each turn `[speaker]`, and tracks the chunk's `start_time` / `end_time`. A single oversized turn is windowed with overlap. Defaults: `TARGET_WORDS=200`, `MAX_WORDS=400`, `OVERLAP_WORDS=30`.
3. **`embed_interviews`** — embeds pending chunks into the `interview_chunks` Qdrant collection. Payload carries `interview_id`, `interview_uuid`, `candidate_id`, `candidate_name`, `source_type`, `format_type`, `title`, `media_outlet`, `url_video_audio`, `start_time`, `end_time`, and `content`.

> The schema for all these tables is **owned by the API**. Apply the migrations with `alembic upgrade head` from `api/` (against the shared MySQL DB) before running the load/chunk steps — `analysis/` never runs Alembic.

---

## 📦 Setup

### Prerequisites

- **Python 3.12**
- A running **MySQL 8** instance with the Elegio schema applied. The easiest path is to start the API's bundled docker-compose (see [api/README.md → Setup](../api/README.md#-setup)) and run `alembic upgrade head` from `api/`. `analysis/` will read and write the same database.
- A **Google AI Studio API key** for Gemini (`GEMINI_API_KEY`).
- **Docker** and **Docker Compose** to run the local **Qdrant** instance (needed for any `embed_*` script and for the API's search endpoint — not required by `rate_batch.py`).
- **ffmpeg** on `$PATH` — required only by the transcription pipeline (`transcribe_videos.py`).
- The **documents** pipeline pulls **Docling** (and `transformers`/`torchvision`); the requirements file pins `transformers<5` and a CPU `torchvision` to stay compatible with the `torch 2.4.1` pyannote requires. See [requirements.txt](requirements.txt) for the rationale.

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

### 3. Start Qdrant with Docker Compose (optional — required for embedding)

[docker-compose.dev.yml](docker-compose.dev.yml) ships a single-node Qdrant instance with a persistent volume (`qdrant_data`):

```bash
docker compose -f docker-compose.dev.yml up -d
```

It exposes:

- `6333` — REST API and dashboard ([http://localhost:6333/dashboard](http://localhost:6333/dashboard))
- `6334` — gRPC port

The `proposal_chunks` collection is created on demand by [`ensure_collection`](app/core/qdrant_client.py) the first time `embed_chunks.py` runs (`Distance.COSINE`, 1536-dim).

### 4. Smoke-test the Gemini client (optional)

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
| `QDRANT_URL`     |  **yes** | —       | URL of the Qdrant instance — defaults to `http://localhost:6333` in `.env.example`. Used by `embed_chunks.py`. |
| `QDRANT_API_KEY` |    no    | `""`    | Optional Qdrant API key. Leave empty for the local docker-compose instance. |

`GEMINI_API_KEY`, `DATABASE_URL`, and `QDRANT_URL` are validated as `min_length=1`, so an empty value at startup raises a Pydantic `ValidationError`.

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

### Chunking proposals — `scripts/chunk_proposals.py`

```bash
python -m scripts.chunk_proposals
```

The script:

1. Prints `Pending proposals: N` (proposals with no chunks yet).
2. For each proposal, prints `[i/N] · Proposal <id>: <n> chunk(s)` on success, or `[i/N] ∅ Proposal <id>: 0 chunk(s)` if the proposal had no embeddable text. Errors print `[i/N] x Proposal <id>: <error>`, the connection is rolled back, and the loop continues.
3. At the end, prints `Total chunks created: <N>` plus a summary of any failures.

Idempotent: only proposals that do not yet have any `proposal_chunks` row are processed. To re-chunk a proposal, hard-delete its existing rows first.

### Embedding chunks — `scripts/embed_chunks.py`

```bash
python -m scripts.embed_chunks
```

The script:

1. Calls `ensure_collection` to create the `proposal_chunks` Qdrant collection on first run.
2. Lists every non-deleted chunk id in MySQL, asks Qdrant which ids are already present, and prints the totals (`Total chunks in MySQL`, `Already in Qdrant`, `Pending`).
3. Embeds and upserts the pending chunks in batches, printing `[batch/total] · upserted <n> chunks` per batch. A failed batch is reported but does not stop the loop.
4. At the end, prints `Total upserted: <N>` plus a summary of any failed batches.

Idempotent: the Qdrant point id equals the MySQL chunk id, so re-running the script never re-embeds a chunk that is already stored.

> **Restart the API after embedding.** The API's BM25 index is built at startup from `proposal_chunks` and has no auto-invalidation. After a successful `embed_chunks` run, restart the API (or call `BM25Index.refresh(db)` programmatically) so the new chunks are searchable lexically too. See [api/README.md](../api/README.md) for details.

### Rebuilding the collection — `reindex.py`

```bash
GEMINI_API_KEY=... QDRANT_URL=... DATABASE_URL=... python reindex.py
```

Unlike `embed_chunks.py` (incremental, idempotent), [`reindex.py`](reindex.py) **drops** the `proposal_chunks` collection, recreates it at the current `EMBEDDING_DIM`, and re-embeds every non-deleted chunk. Run it after changing the embedding model or its output dimensionality — e.g. the migration from `multilingual-e5-large` (1024-dim) to `gemini-embedding-001` (1536-dim) — because the old vectors are incompatible with the new space. Restart the API afterwards (same BM25 caveat as above).

### Transcribing YouTube videos — `scripts/transcribe_videos.py`

```bash
OPENAI_API_KEY=... HF_TOKEN=... GEMINI_API_KEY=... python -m scripts.transcribe_videos
```

End-to-end pipeline per video listed in [`scripts/videos.yaml`](scripts/videos.example.yaml) (copy the example to `scripts/videos.yaml` — it is gitignored):

1. **Download** the audio with `yt-dlp` and re-encode to 64 kbps mono mp3 (fits the OpenAI Whisper 25 MB limit for ~50 min) plus a 16 kHz mono PCM wav for diarization. Cached under `audio_cache/`.
2. **Transcribe** with the **OpenAI Whisper API** (`whisper-1`, verbose_json segments). `gpt-4o-transcribe` / `gpt-4o-mini-transcribe` are cheaper but don't return segment timestamps yet, which the diarization aligner needs. Long audios are split with ffmpeg and their timestamps re-aligned to the original timeline. Known Whisper hallucinations (e.g. the "Subtítulos … Amara.org" loop on music) are filtered out by [`hallucinations.py`](app/domains/transcription/hallucinations.py) before alignment.
3. **Diarize** with **pyannote.audio** (`pyannote/speaker-diarization-3.1`) to get anonymous `SPEAKER_00`, `SPEAKER_01`, … turns. Requires `HF_TOKEN` from a HuggingFace account that has accepted the model license; first run downloads ~250 MB of weights.
4. **Align** Whisper segments with diarization turns by maximum time overlap.
5. **Map** anonymous labels → real participant names. The aligner samples a handful of utterances per speaker and asks **Gemini** to assign one of the `participants` from the YAML, using conversational context (questions vs answers, mentions).
6. **Write** one JSON per candidate at `transcripts/<slug>.json` (a list of video objects with the schema documented in [scripts/videos.example.yaml](scripts/videos.example.yaml)). Per-video output is also cached at `transcripts/_videos/<video_id>.json`, so re-runs skip work that already succeeded — delete a cache file to redo just that video.

System prerequisites: **ffmpeg** on `$PATH`. A CUDA GPU dramatically speeds up pyannote (CPU runs at roughly 10× realtime).

### Extracting news articles — `scripts/extract_news.py`

```bash
python -m scripts.extract_news
```

End-to-end pipeline per article listed in [`scripts/news.yaml`](scripts/news.example.yaml) (copy the example to `scripts/news.yaml` — it is gitignored):

1. **Fetch** the page HTML with [`trafilatura.fetch_url`](https://trafilatura.readthedocs.io). Raw HTML is cached at `news_cache/<new_id>.html` so the extractor can be improved and re-run without re-hitting the source.
2. **Extract** clean article content with `trafilatura.extract` (precision-favored, no comments/tables/links) plus title and publication date from `extract_metadata`. This is the library that handles ads, cookie banners, sidebars, and paywall stubs.
3. **Preprocess** ([`preprocessor.clean_content`](app/domains/news/preprocessor.py)): repair encoding with `ftfy`, strip stray URLs, and remove recurring publisher boilerplate (subscribe prompts, fact-check bot intros/outros), inline reference markers like `(1, 2, 3)`, embedded tweet/X footers and standalone `@handles`, then collapse whitespace.
4. **Write** one JSON per candidate at `news/<slug>.json` (a list of article objects with the schema documented in [scripts/news.example.yaml](scripts/news.example.yaml)), now including `publishing_house`. Per-article output is also cached at `news/_articles/<new_id>.json`, so re-runs skip URLs that already succeeded — delete a cache file to redo just that article. (Older cached articles missing `publishing_house` are backfilled in place on the next run.)

### Loading, chunking & embedding news

```bash
python -m scripts.load_news        # news/<slug>.json → news table (idempotent on news.uuid)
python -m scripts.chunk_news       # news → news_chunks (vitaminized chunks)
python -m scripts.embed_news       # news_chunks → Qdrant news_chunks collection
```

`load_news` joins `news.yaml` metadata with the extracted JSON and resolves each candidate by name (its `presidential_candidate` value). `chunk_news` reuses the proposal paragraph chunker and stores each chunk **vitaminized** with a `[Candidato]/[Medio]/Titular` prefix. `embed_news` is incremental and idempotent (Qdrant point id == MySQL chunk id), like `embed_chunks`.

### Documents pipeline — `scripts/extract_documents.py`

```bash
python -m scripts.extract_documents
python -m scripts.load_documents
python -m scripts.chunk_documents
python -m scripts.embed_documents
```

For each PDF in [`scripts/documents.yaml`](scripts/documents.example.yaml) (copy the example to `documents.yaml`; gitignored), **Docling** parses the PDF into structure-preserving Markdown (headings, paragraphs, lists, tables). Each per-document spec carries `type` (e.g. `legal_document` / `campaign_document`) and `url`; most metadata is optional. Raw Markdown is cached at `document_cache/<doc_id>.md` and per-document JSON at `documents/_files/<doc_id>.json`, so re-runs skip PDFs that already succeeded.

`chunk_documents` uses a **structure-aware Markdown chunker** ([`document_chunk/chunker.py`](app/domains/document_chunk/chunker.py)) that splits at heading/section boundaries (prefixing each chunk with its heading-path context), keeps tables and bullet items whole, and groups paragraphs up to a target size. `load_documents` / `embed_documents` follow the same idempotency rules as the news pipeline.

### Interviews pipeline — `scripts/load_interviews.py`

```bash
python -m scripts.load_interviews
python -m scripts.chunk_interviews
python -m scripts.embed_interviews
```

Reads `transcripts/<slug>.json` (produced by [`scripts.transcribe_videos`](#transcribing-youtube-videos--scriptstranscribe_videospy)) and inserts **one `interviews` row per video**. Consecutive same-speaker segments are merged into single `interview_segments` (first start_time, last end_time, concatenated text). Transcript dates are `YYYY-DD-MM` (day before month) and parsed accordingly. Idempotent on `interviews.uuid` (== `video_id`).

`chunk_interviews` groups consecutive turns into conversation-aware chunks (labelling each turn `[speaker]` and tracking the chunk's time span), so a question and its answer stay together. `embed_interviews` upserts into the `interview_chunks` Qdrant collection, idempotent on the shared chunk id.

> **Apply migrations first.** The `news`, `documents`, `interviews` tables (and their `*_chunks` / `interview_segments` tables) are owned by the API. Run `alembic upgrade head` from `api/` against the shared DB before the load/chunk steps — `analysis/` never runs Alembic.

---

## 🗃 Data model

`analysis/` reads from `categories` + `proposals` and writes to `postures`. It also writes the candidate content sources — `news`, `documents`, `interviews` — and their chunk/segment tables. The columns are mirrored from the API's models in [`app/core/database.py`](app/core/database.py); the canonical definitions live in the API's SQLAlchemy models and Alembic migrations.

### Read

| Source             | Columns used                                                                              |
| ------------------ | ----------------------------------------------------------------------------------------- |
| `categories`       | `id`, `name`, `weight`                                                                    |
| `proposals`        | `id`, `title`, `summary`, `full_text`, `category_id`, `candidate_id`                      |
| `proposal_chunks`  | `id`, `proposal_id`, `chunk_index`, `total_chunks`, `content`, `deleted_at`               |
| `candidates`       | `id`, `presidential_candidate`, `deleted_at` — to resolve a candidate by name             |

The rating query joins `proposals → categories` and left-joins `postures` to pick rows where no posture exists. The chunking query left-joins `proposal_chunks` to pick proposals with no chunks yet. The embedding query joins `proposal_chunks → proposals` so each Qdrant point's payload can carry the `category_id` and `candidate_id` used by the API's filtered search.

### Content-source tables

The news/documents/interviews pipelines write to the tables below. Each parent table carries a `uuid` (the idempotency key and Qdrant-side reference), a `candidate_id`, and a `source_type`; each `*_chunks` table carries `chunk_index`, `total_chunks`, and `content_chunk`. The chunk and segment tables use `BigInteger` ids and a parent FK with `ON DELETE CASCADE`. See [api/README.md → Content-source tables](../api/README.md#-content-source-tables) for the full column reference.

| Table                | Written by                          | Notes                                                              |
| -------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| `news`               | `load_news`                         | one row per article; `content_raw` holds the cleaned full text     |
| `news_chunks`        | `chunk_news`                        | `content_chunk` is the **vitaminized** chunk text                  |
| `documents`          | `load_documents`                    | one row per PDF; `content` holds the extracted Markdown            |
| `document_chunks`    | `chunk_documents`                   | structure-aware Markdown chunks                                    |
| `interviews`         | `load_interviews`                   | one row per video                                                  |
| `interview_segments` | `load_interviews`                   | merged per-speaker turns (`start_time`/`end_time`/`speaker`/`text_segment`) |
| `interview_chunks`   | `chunk_interviews`                  | conversation-aware chunks with a time span                        |

The `embed_*` scripts do **not** write to MySQL — they only upsert into the matching Qdrant collection, with the point id equal to the MySQL chunk id.

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

`chunk_proposals.py` inserts into `proposal_chunks`:

| Column          | Value written                          | Source              |
| --------------- | -------------------------------------- | ------------------- |
| `proposal_id`   | the parent proposal's id               | pending-proposals query |
| `chunk_index`   | 0-based position of the chunk          | `chunk_text` output |
| `total_chunks`  | number of chunks generated for that proposal | `chunk_text` output |
| `content`       | the chunk text                         | `chunk_text` output |
| `created_at` / `updated_at` / `deleted_at` | DB defaults / unset | TimestampMixin     |

`embed_chunks.py` does not touch MySQL — it only writes to Qdrant. Each Qdrant point's id is the MySQL chunk id, and its payload mirrors `proposal_id`, `chunk_index`, `total_chunks`, `content`, `category_id`, and `candidate_id` so the API can filter and hydrate results without round-tripping through MySQL for every hit.

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

# Local Qdrant
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml down

# Proposals: chunking + embedding pipeline
python -m scripts.chunk_proposals
python -m scripts.embed_chunks
python reindex.py            # drop + rebuild the proposal_chunks collection (after a model/dim change)

# News pipeline
python -m scripts.extract_news
python -m scripts.load_news
python -m scripts.chunk_news
python -m scripts.embed_news

# Documents pipeline (Docling)
python -m scripts.extract_documents
python -m scripts.load_documents
python -m scripts.chunk_documents
python -m scripts.embed_documents

# Interviews pipeline (after scripts.transcribe_videos)
python -m scripts.load_interviews
python -m scripts.chunk_interviews
python -m scripts.embed_interviews
```

---

## 🧹 Code style

- **Black** — formatter
- **Ruff** — linter
- **Conventional Commits** — `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`...
