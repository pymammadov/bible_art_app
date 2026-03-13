from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "database" / "bible_art.db"


def _parse_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_database_path() -> Path:
    raw_path = os.getenv("DATABASE_PATH")
    if not raw_path:
        return DEFAULT_DB_PATH
    return Path(raw_path).expanduser().resolve()


def get_auto_seed_db() -> bool:
    return _parse_bool(os.getenv("AUTO_SEED_DB"), default=True)


def get_allowed_origins() -> list[str]:
    raw_origins = os.getenv("ALLOWED_ORIGINS", "")
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins
