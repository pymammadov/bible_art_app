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
