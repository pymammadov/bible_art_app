# Bible Art App

Bible Art App is a full-stack MVP for exploring links between biblical stories, characters, locations, and artworks.

## Stack

- Python 3.11+
- FastAPI
- SQLite
- React + Vite
- React Router
- Tailwind CSS

## Project Structure

- `backend/` FastAPI application and API routes
- `database/` SQLite file + seed SQL
- `frontend/` React client
- `scripts/` operational scripts (seed/reseed/validation/ingestion stub)
- `README.md`
- `requirements.txt`
- `.gitignore`

## One-command local run (recommended)

If setup is difficult, run everything with one script:

```bash
bash scripts/run_local.sh
```

This script will:
- create/activate `.venv`
- install backend dependencies
- reseed + validate the database
- start backend on `http://127.0.0.1:8000`
- install frontend dependencies
- start frontend on `http://127.0.0.1:5173` with `VITE_API_BASE_URL=http://127.0.0.1:8000`

## Backend Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start API:

```bash
uvicorn backend.main:app --reload
```

API base URL: `http://127.0.0.1:8000`

If you open the backend URL directly in a browser, you should now see a small JSON service message at `/` (instead of a 404). For API exploration use `/docs`; for the UI open the frontend URL (typically `http://127.0.0.1:5173`).

### CORS configuration

Backend CORS is configurable using environment variables:

- `CORS_ALLOW_ORIGINS` (comma-separated exact origins, default: `http://127.0.0.1:5173,http://localhost:5173`)
- `CORS_ALLOW_ORIGIN_REGEX` (regex for dynamic origins, default: disabled)
- `CORS_DEV_MODE` (`true/1/yes/on`) to allow all origins in development-friendly mode

Examples:

```bash
# Exact origins
CORS_ALLOW_ORIGINS=http://localhost:5173,http://my-frontend.example uvicorn backend.main:app --reload

# Dynamic origin matching (useful for port-forwarded/dev cloud URLs)
CORS_ALLOW_ORIGIN_REGEX='https://.*\.app\.github\.dev' uvicorn backend.main:app --reload

# Development-friendly mode (allow all origins; credentials disabled)
CORS_DEV_MODE=true uvicorn backend.main:app --reload
```

### Backend endpoints

- `GET /health`
- `GET /stories`
- `GET /stories/{id}`
- `GET /characters`
- `GET /characters/{id}`
- `GET /locations`
  - Optional filters: `story_id`, `name`, `has_coordinates`
- `GET /locations/{id}`
- `GET /artworks`
- `GET /artworks/{id}`
- `GET /institutions`
- `GET /institutions/{id}`
- `GET /search`

All endpoints return JSON and support filtering where appropriate.
Detailed endpoints include a `relationships` object.

## Database + Seeding

### Seed only if DB file does not exist

```bash
python scripts/seed_db.py
```

### Full reseed (recommended during development)

```bash
python scripts/reseed_db.py
```

### Validation checks

```bash
python scripts/validate_data.py
```

Validation verifies:

- 20 Old Testament stories
- 20 New Testament stories
- required characters present (Abraham, Moses, David, Solomon, Mary, Jesus, Peter, Paul)
- required locations present (Jerusalem, Bethlehem, Nazareth, Mount Sinai, Babylon, Galilee)
- artworks linked through `story_artworks`


## Artwork ingestion-ready layer

The schema now supports future external museum imports with incremental additions:

- `institutions` table (`name`, `city`, `country`, `website_url`)
- `artworks.institution_id` (nullable foreign key)
- `artworks.image_url`
- `artworks.source_url`
- `artworks.attribution`

Current API responses for artworks include these new fields, and `/institutions` endpoints are available for lookup.

### Ingestion stub (future external providers)

A provider-agnostic ingestion scaffold is included:

- `backend/ingestion.py` defines `ExternalArtworkRecord` and normalization mapping
- `scripts/import_artworks_stub.py` demonstrates JSONL-based import + institution upsert

Example usage:

```bash
python scripts/import_artworks_stub.py path/to/external_artworks.jsonl
```

Expected JSONL keys (normalized):
- `title` (required)
- optional: `artist`, `year`, `medium`, `description`
- optional institution fields: `institution_name`, `institution_city`, `institution_country`, `institution_website_url`
- optional attribution/media fields: `image_url`, `source_url`, `attribution`

This keeps the existing artworks model compatible while enabling phased ingestion work.


## Lightweight knowledge graph model

The app remains relational (SQLite) but now includes a graph-friendly edge table:

- `entity_links(source_type, source_id, target_type, target_id, relation_type, evidence)`

This table stores semantic links between entities such as:
- story -> character (`involves_character`)
- story -> location (`takes_place_in`)
- story -> artwork (`inspired_artwork`)
- artwork -> story (`depicts_primary_story`)
- artwork -> institution (`held_by_institution`)

Detail endpoints now include richer relationship metadata:
- `relationships.relationship_counts`
- `relationships.graph.entity`
- `relationships.graph.edges` (incoming + outgoing typed edges)

### Schema recommendations (next incremental steps)

To evolve further without moving to a graph database:

1. Add `created_at` / `updated_at` timestamps to `entity_links`.
2. Add optional `confidence` and `source_dataset` columns for provenance quality scoring.
3. Add unique index on `(source_type, source_id, target_type, target_id, relation_type)` to prevent duplicates.
4. Add API filters for edge traversal (e.g. by `relation_type`, `direction`).
5. Add dedicated `/graph/neighbors` endpoint for lightweight traversal use-cases.


## Map-ready location data

Locations now include optional geospatial fields:

- `latitude` (nullable)
- `longitude` (nullable)
- `certainty_level` (`high`, `probable`, `traditional`)

This avoids false precision: uncertain/traditional locations can keep coordinates as `NULL` while still carrying a certainty label.

For API consumers:

- use `GET /locations?has_coordinates=true` for map pins
- use `GET /locations?has_coordinates=false` for locations that should remain list-only
- detail responses include coordinates and certainty fields

Future map component guidance:

1. Fetch coordinate-ready points via `/locations?has_coordinates=true`.
2. Render each point with a tooltip containing `name`, `region`, and `certainty_level`.
3. Keep a side list for `/locations?has_coordinates=false` so uncertain places are still discoverable.
4. Use `certainty_level` to vary marker style (e.g. solid/high vs dashed/traditional).


## AI-assisted search scaffold

A lightweight natural-language search layer is now scaffolded without external vector infrastructure.

### Current architecture

- `backend/search.py` contains `SemanticSearchService`
- `GET /search` accepts natural language query (`q`)
- current engine uses keyword fallback with small query expansion (e.g. `kings` -> `king`, `david`, `solomon`)
- search runs across stories, characters, locations, and artworks
- response already includes `embedding_ready` metadata for future vector search wiring

### Integration points for future embeddings

1. **Corpus generation**: use `SemanticSearchService.build_corpus()` as canonical document stream.
2. **Embedding generation**: embed corpus text with provider chosen by env (`EMBEDDING_PROVIDER`, `EMBEDDING_MODEL`).
3. **Index storage**: start with SQLite-backed table (or sidecar files) before moving to external vector DB.
4. **Hybrid retrieval**: combine vector similarity + existing keyword score.
5. **Reranking**: optional reranker stage before returning final hits.

### Staged implementation plan

- **Stage 1 (now)**: keyword fallback + NL query endpoint (`/search`) and corpus preview tooling.
- **Stage 2**: persist embeddings locally and add vector similarity retrieval in SQLite-compatible form.
- **Stage 3**: hybrid ranking + relation-aware boosting using `entity_links`.
- **Stage 4**: optional external vector backend behind same search service interface.

### Developer utilities

Generate a local corpus preview for inspection:

```bash
python scripts/build_search_corpus_stub.py
```

Run a natural-language search query:

```bash
curl 'http://127.0.0.1:8000/search?q=artworks%20related%20to%20Moses'
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`

### API configuration

Frontend reads API base URL from `VITE_API_BASE_URL`.
If not set, it defaults to `http://127.0.0.1:8000`.

Quick run example:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Optional `.env.local` in `frontend/`:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The frontend now includes request timeout handling, more descriptive API error messages,
and a global error boundary to reduce blank-screen failures.


### Frontend routes

- `/` stories list
- `/stories/:storyId` story detail
- `/characters` characters list
- `/characters/:characterId` character detail
- `/locations` locations list
- `/locations/:locationId` location detail
- `/locations-map` map-ready locations view
- `/artworks` artworks list
- `/artworks/:artworkId` artwork detail

## Notes

- CORS is enabled for local development.
- SQLite schema includes relationship tables:
  - `story_characters`
  - `story_locations`
  - `story_artworks`
- `artworks.related_story_id` is included for direct relation lookups.


## GitHub Codespaces usage

When frontend and backend are exposed on different forwarded URLs, configure both API base URL and CORS:

1. Start backend in one terminal:

```bash
CORS_ALLOW_ORIGIN_REGEX='https://.*\.app\.github\.dev' uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Alternative (most permissive for development only):

```bash
CORS_DEV_MODE=true uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

2. Start frontend in another terminal:

```bash
cd frontend
npm install
VITE_API_BASE_URL=<YOUR_BACKEND_CODESPACES_URL> npm run dev -- --host 0.0.0.0 --port 5173
```

Example backend URL shape:

```text
https://<codespace-name>-8000.app.github.dev
```

This setup avoids browser CORS-related `Failed to fetch` errors when ports use different origins.
