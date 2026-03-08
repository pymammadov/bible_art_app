# Bible Art App

A database-first project for mapping:

- Old Testament stories
- New Testament stories
- biblical characters
- probable historical/traditional locations
- artworks inspired by biblical narratives

## Project goal

This project aims to become a searchable discovery app that connects:

- stories
- characters
- locations
- artworks
- institutions and galleries

## Current status

This repository includes a FastAPI backend backed by SQLite, plus a comprehensive starter seed dataset across stories, characters, locations, and artworks.

## Run backend locally

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Reseed local database (recommended)

```bash
python scripts/reseed_db.py
```

### 3) Start the API

From the repository root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:
- `http://127.0.0.1:8000`
- interactive docs at `http://127.0.0.1:8000/docs`

## Data model highlights

- `stories` now include `scripture_reference` and `summary`.
- `locations` include `region`.
- `artworks` include `medium`, `current_location`, and `related_story_id`.
- `related_story_id` provides a direct story pointer for artwork-centric API clients.

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
  - Optional filters: `story_id`, `artist`, `related_story_id`
- `GET /artworks/{id}`

Each resource includes a `relationships` object so clients can navigate connected entities.
For artworks, `relationships.related_story` is also returned when `related_story_id` is set.

## Basic validation

After reseeding, you can run a quick sanity check:

```bash
python - <<'PY'
from backend.db import get_connection

with get_connection() as conn:
    for table in ("stories", "characters", "locations", "artworks"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(table, count)
PY
```
