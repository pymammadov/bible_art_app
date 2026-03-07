# Tasks for Codex

## Phase 1 — Database

- Inspect the current schema
- Refactor the database into a normalized production-ready schema
- Add missing entities:
  - institutions
  - books
  - chapters
  - verses
  - themes
  - licenses
  - source_links
  - image_assets
- Create migration SQL files
- Preserve current seed data where possible

## Phase 2 — Backend

Build a minimal backend using FastAPI with endpoints for:

- /stories
- /characters
- /locations
- /artworks

Include filtering by testament and story relationships.

## Phase 3 — Frontend

Build a minimal frontend with:

- homepage
- stories list
- story detail page
- artworks list
- search
- filtering
