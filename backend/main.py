from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import initialize_db
from .routes import router


def _is_truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _get_cors_origins() -> list[str]:
    raw_value = os.getenv("CORS_ALLOW_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173")
    origins = [value.strip() for value in raw_value.split(",") if value.strip()]
    return origins or ["http://127.0.0.1:5173", "http://localhost:5173"]


def _get_cors_origin_regex() -> str | None:
    raw_value = os.getenv("CORS_ALLOW_ORIGIN_REGEX", "").strip()
    return raw_value or None


app = FastAPI(title="Bible Art API")

cors_dev_mode = _is_truthy(os.getenv("CORS_DEV_MODE"))

if cors_dev_mode:
    # Development-friendly mode for environments where frontend/backend origins are dynamic.
    # Example: GitHub Codespaces forwarded ports.
    cors_origins = ["*"]
    cors_origin_regex = None
    allow_credentials = False
else:
    cors_origins = _get_cors_origins()
    cors_origin_regex = _get_cors_origin_regex()
    allow_credentials = "*" not in cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=cors_origin_regex,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    initialize_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(router)
