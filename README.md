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
- `scripts/` operational scripts (seed/reseed/validation)
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
- `GET /locations/{id}`
- `GET /artworks`
- `GET /artworks/{id}`

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
