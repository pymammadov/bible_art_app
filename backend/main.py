from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import initialize_db
from .routes import router


def _get_cors_origins() -> list[str]:
    raw_value = os.getenv("CORS_ALLOW_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173")
    origins = [value.strip() for value in raw_value.split(",") if value.strip()]
    return origins or ["http://127.0.0.1:5173", "http://localhost:5173"]


app = FastAPI(title="Bible Art API")

cors_origins = _get_cors_origins()
allow_all_origins = "*" in cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=not allow_all_origins,
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
