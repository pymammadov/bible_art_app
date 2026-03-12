from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from backend.ingestion import map_external_record

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "bible_art.db"


def upsert_institution(conn: sqlite3.Connection, name: str | None, city: str | None, country: str | None, website: str | None) -> int | None:
    if not name:
        return None

    existing = conn.execute("SELECT id FROM institutions WHERE name = ?", (name,)).fetchone()
    if existing:
        return int(existing[0])

    cursor = conn.execute(
        """
        INSERT INTO institutions (name, city, country, website_url)
        VALUES (?, ?, ?, ?)
        """,
        (name, city, country, website),
    )
    return int(cursor.lastrowid)


def import_from_jsonl(path: Path) -> None:
    if not DB_PATH.exists():
        raise SystemExit("Database not found. Run `python scripts/reseed_db.py` first.")
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")

    imported = 0
    with sqlite3.connect(DB_PATH) as conn, path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            record = map_external_record(raw)

            institution_id = upsert_institution(
                conn,
                record.institution_name,
                record.institution_city,
                record.institution_country,
                record.institution_website_url,
            )

            conn.execute(
                """
                INSERT INTO artworks (title, artist, year, medium, description, institution_id, image_url, source_url, attribution)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.title,
                    record.artist,
                    record.year,
                    record.medium,
                    record.description,
                    institution_id,
                    record.image_url,
                    record.source_url,
                    record.attribution,
                ),
            )
            imported += 1

        conn.commit()

    print(f"Imported {imported} artwork record(s) from {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Artwork ingestion stub for future external museum feeds")
    parser.add_argument("jsonl_path", help="Path to JSONL file with normalized external artwork fields")
    args = parser.parse_args()
    import_from_jsonl(Path(args.jsonl_path))


if __name__ == "__main__":
    main()
