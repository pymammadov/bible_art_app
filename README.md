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

This repository includes a minimal FastAPI backend and a reseedable SQLite dataset for stories, characters, locations, and artworks.


## Development startup script

From the repository root, run:

```bash
bash scripts/dev.sh
```

This installs backend/frontend dependencies, starts FastAPI on port `8000`, and starts Vite on port `5173`.

Vite now proxies frontend API calls from `/api/*` to `http://127.0.0.1:8000`, so local/Codespaces dev does not require setting `VITE_API_BASE_URL` or debugging CORS for normal development.



## Frontend API proxy (development)

During local development (`npm run dev`), the frontend calls relative endpoints such as `/api/stories`.
Vite forwards these to the backend on port `8000`.

For deployed environments, you can still set `VITE_API_BASE_URL` to a full backend URL if needed.

## Run backend locally

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Reseed the database

From the repository root:

```bash
python -m database.seed_data
```

This command recreates `database/bible_art.db` from schema + seed data.

### 3) Start the API

```bash
uvicorn backend.main:app --reload
```

The API will be available at:
- `http://127.0.0.1:8000`
- interactive docs at `http://127.0.0.1:8000/docs`

## API endpoints

All endpoints return JSON.

### Stories
- `GET /stories`
  - Optional filters: `testament`, `character_id`, `location_id`, `artwork_id`
- `GET /stories/{id}`

### Characters
- `GET /characters`
  - Optional filters: `story_id`, `name`
- `GET /characters/{id}`

### Locations
- `GET /locations`
  - Optional filters: `story_id`, `name`
- `GET /locations/{id}`

### Artworks
- `GET /artworks`
  - Optional filters: `story_id`, `artist`
- `GET /artworks/{id}`

Seeded artwork rows include `title`, `artist`, `year`, `museum`, and `related_story_id`.

Each resource includes a `relationships` object so clients can navigate connected entities.

## Frontend routes

The React app includes browse + detail pages for each main entity:

- `/` stories list
- `/stories/:storyId` story detail with linked characters, locations, and artworks
- `/characters` and `/characters/:characterId`
- `/locations` and `/locations/:locationId`
- `/artworks` and `/artworks/:artworkId`

All pages use the FastAPI endpoints above and render loading, error, and empty states.
