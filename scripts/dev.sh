#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[dev] Repository root: $ROOT_DIR"
echo "[dev] Installing backend dependencies from requirements.txt..."
python -m pip install -r requirements.txt

if [[ ! -f "$ROOT_DIR/database/bible_art.db" ]]; then
  echo "[dev] Database not found. Seeding database..."
  python scripts/reseed_db.py
fi

CLEANED_UP=0
cleanup() {
  if [[ "$CLEANED_UP" -eq 1 ]]; then
    return
  fi
  CLEANED_UP=1

  if [[ -n "${BACKEND_PID:-}" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "[dev] Stopping backend (PID: $BACKEND_PID)..."
    kill "$BACKEND_PID" || true
  fi
}
trap cleanup EXIT INT TERM

echo "[dev] Starting FastAPI backend on http://0.0.0.0:8000 ..."
PYTHONPATH=/workspaces/bible_art_app python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "[dev] Installing frontend dependencies in frontend/..."
cd frontend
npm install

echo "[dev] Starting Vite frontend on http://0.0.0.0:5173 ..."
echo "[dev] Backend PID: $BACKEND_PID"
npm run dev -- --host 0.0.0.0 --port 5173
