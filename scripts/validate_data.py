from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "bible_art.db"

REQUIRED_CHARACTERS = {"Abraham", "Moses", "David", "Solomon", "Mary", "Jesus", "Peter", "Paul"}
REQUIRED_LOCATIONS = {"Jerusalem", "Bethlehem", "Nazareth", "Mount Sinai", "Babylon", "Galilee"}


def scalar(conn: sqlite3.Connection, query: str, params: tuple = ()) -> int:
    return int(conn.execute(query, params).fetchone()[0])


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit("Database file not found. Run `python scripts/reseed_db.py` first.")

    with sqlite3.connect(DB_PATH) as conn:
        old_count = scalar(conn, "SELECT COUNT(*) FROM stories WHERE testament = 'Old Testament'")
        new_count = scalar(conn, "SELECT COUNT(*) FROM stories WHERE testament = 'New Testament'")
        if old_count != 20 or new_count != 20:
            raise SystemExit(f"Expected 20 OT + 20 NT stories, got OT={old_count}, NT={new_count}")

        names = {row[0] for row in conn.execute("SELECT name FROM characters")}
        missing_characters = sorted(REQUIRED_CHARACTERS - names)
        if missing_characters:
            raise SystemExit(f"Missing required characters: {', '.join(missing_characters)}")

        locations = {row[0] for row in conn.execute("SELECT name FROM locations")}
        missing_locations = sorted(REQUIRED_LOCATIONS - locations)
        if missing_locations:
            raise SystemExit(f"Missing required locations: {', '.join(missing_locations)}")

        missing_links = scalar(
            conn,
            """
            SELECT COUNT(*)
            FROM artworks a
            LEFT JOIN story_artworks sa ON sa.artwork_id = a.id
            WHERE sa.artwork_id IS NULL
            """,
        )
        if missing_links > 0:
            raise SystemExit(f"Found {missing_links} artworks without story_artworks link")

        institutions_count = scalar(conn, "SELECT COUNT(*) FROM institutions")
        if institutions_count < 1:
            raise SystemExit("Expected at least one institution record")

        nullable_metadata_count = scalar(
            conn,
            """
            SELECT COUNT(*)
            FROM artworks
            WHERE image_url IS NOT NULL OR source_url IS NOT NULL OR attribution IS NOT NULL
            """,
        )
        if nullable_metadata_count < 1:
            raise SystemExit("Expected at least one artwork with ingestion metadata (image/source/attribution)")

    print("Validation checks passed.")


if __name__ == "__main__":
    main()
