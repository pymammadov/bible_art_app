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

This repository now includes a minimal FastAPI backend that serves Bible stories, characters, locations, and artworks from SQLite.

## Run backend locally

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]"
```

### 2) Start the API

From the repository root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:
- `http://127.0.0.1:8000`
- interactive docs at `http://127.0.0.1:8000/docs`

> On startup, the backend initializes `database/bible_art.db` from `database/bible_art_seed.sql` if the DB file does not exist.

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

Each resource includes a `relationships` object so clients can navigate connected entities.
