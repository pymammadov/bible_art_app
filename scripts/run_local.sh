#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d .venv ]]; then
  python -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install -r requirements.txt
python scripts/reseed_db.py
python scripts/validate_data.py

cleanup() {
  if [[ -n "${API_PID:-}" ]] && kill -0 "$API_PID" 2>/dev/null; then
    kill "$API_PID" || true
  fi
}
trap cleanup EXIT INT TERM

uvicorn backend.main:app --host 127.0.0.1 --port 8000 >/tmp/bible_art_api.log 2>&1 &
API_PID=$!

cd frontend
npm install

echo "Backend started at http://127.0.0.1:8000 (logs: /tmp/bible_art_api.log)"
echo "Frontend starting at http://127.0.0.1:5173"
VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev -- --host 127.0.0.1 --port 5173
