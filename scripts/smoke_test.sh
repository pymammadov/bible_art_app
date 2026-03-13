#!/usr/bin/env bash
set -euo pipefail

FRONTEND_URL="${1:-}"
BACKEND_URL="${2:-}"

if [[ -z "$FRONTEND_URL" || -z "$BACKEND_URL" ]]; then
  echo "Usage: $0 <frontend_url> <backend_url>"
  exit 1
fi

FRONTEND_URL="${FRONTEND_URL%/}"
BACKEND_URL="${BACKEND_URL%/}"

echo "[1/6] Health check"
curl -fsS "$BACKEND_URL/health" | python3 -c 'import json,sys; data=json.load(sys.stdin); assert data=={"status":"ok"}, data; print(data)'

echo "[2/6] Stories list"
FIRST_STORY_ID=$(curl -fsS "$BACKEND_URL/stories" | python3 -c 'import json,sys; data=json.load(sys.stdin); assert data.get("count",0)>0, data; print(data["items"][0]["id"])')

echo "[3/6] Story detail for ID ${FIRST_STORY_ID}"
curl -fsS "$BACKEND_URL/stories/${FIRST_STORY_ID}" | python3 -c 'import json,sys; data=json.load(sys.stdin); assert data.get("id"), data; print({"id":data["id"],"title":data["title"]})'

echo "[4/6] Frontend home HTML"
curl -fsS "$FRONTEND_URL/" >/dev/null

echo "[5/6] CORS preflight"
CORS_HEADERS=$(curl -isS -X OPTIONS "$BACKEND_URL/stories" -H "Origin: $FRONTEND_URL" -H 'Access-Control-Request-Method: GET')
echo "$CORS_HEADERS" | rg -qi "access-control-allow-origin: $FRONTEND_URL"

echo "[6/6] Frontend wired API base URL sanity"
if [[ -n "${VITE_API_BASE_URL:-}" ]]; then
  echo "VITE_API_BASE_URL env present in shell: $VITE_API_BASE_URL"
else
  echo "VITE_API_BASE_URL not set locally; ensure it is configured in Vercel dashboard."
fi

echo "Smoke tests passed."
