from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ExternalArtworkRecord:
    """Normalized ingestion payload for future external museum providers."""

    title: str
    artist: str | None = None
    year: int | None = None
    medium: str | None = None
    description: str | None = None
    institution_name: str | None = None
    institution_city: str | None = None
    institution_country: str | None = None
    institution_website_url: str | None = None
    image_url: str | None = None
    source_url: str | None = None
    attribution: str | None = None


def map_external_record(raw: dict[str, Any]) -> ExternalArtworkRecord:
    """Map raw provider fields into a stable internal schema.

    This function is intentionally conservative and provider-agnostic.
    Provider-specific adapters can call this function after translating field names.
    """

    title = (raw.get("title") or "").strip()
    if not title:
        raise ValueError("Artwork title is required")

    year = raw.get("year")
    if year is not None:
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = None

    return ExternalArtworkRecord(
        title=title,
        artist=raw.get("artist"),
        year=year,
        medium=raw.get("medium"),
        description=raw.get("description"),
        institution_name=raw.get("institution_name"),
        institution_city=raw.get("institution_city"),
        institution_country=raw.get("institution_country"),
        institution_website_url=raw.get("institution_website_url"),
        image_url=raw.get("image_url"),
        source_url=raw.get("source_url"),
        attribution=raw.get("attribution"),
    )
