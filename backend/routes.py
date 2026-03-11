from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from .db import get_connection

router = APIRouter()


def _fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def _fetch_one(query: str, params: tuple[Any, ...]) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(query, params).fetchone()
    return dict(row) if row else None




def _graph_edges(entity_type: str, entity_id: int) -> list[dict[str, Any]]:
    with get_connection() as conn:
        edges = conn.execute(
            """
            SELECT relation_type, evidence,
                   target_type AS related_type,
                   target_id AS related_id,
                   'outgoing' AS direction
            FROM entity_links
            WHERE source_type = ? AND source_id = ?
            UNION ALL
            SELECT relation_type, evidence,
                   source_type AS related_type,
                   source_id AS related_id,
                   'incoming' AS direction
            FROM entity_links
            WHERE target_type = ? AND target_id = ?
            ORDER BY relation_type, related_type, related_id
            """,
            (entity_type, entity_id, entity_type, entity_id),
        ).fetchall()
    return [dict(row) for row in edges]


def _enrich_detail_relationships(base: dict[str, Any], entity_type: str, entity_id: int) -> dict[str, Any]:
    relationship_counts: dict[str, int] = {}
    for key, value in base.items():
        if isinstance(value, list):
            relationship_counts[key] = len(value)
        elif value is not None:
            relationship_counts[key] = 1
    base["relationship_counts"] = relationship_counts
    base["graph"] = {
        "entity": {"type": entity_type, "id": entity_id},
        "edges": _graph_edges(entity_type, entity_id),
    }
    return base


def _story_relationships(story_id: int) -> dict[str, list[dict[str, Any]]]:
    with get_connection() as conn:
        characters = conn.execute(
            """
            SELECT c.id, c.name, c.testament, c.description
            FROM characters c
            JOIN story_characters sc ON sc.character_id = c.id
            WHERE sc.story_id = ?
            ORDER BY c.name
            """,
            (story_id,),
        ).fetchall()
        locations = conn.execute(
            """
            SELECT l.id, l.name, l.region, l.description
            FROM locations l
            JOIN story_locations sl ON sl.location_id = l.id
            WHERE sl.story_id = ?
            ORDER BY l.name
            """,
            (story_id,),
        ).fetchall()
        artworks = conn.execute(
            """
            SELECT a.id, a.title, a.artist, a.year, a.medium, a.current_location,
                   a.description, a.related_story_id, a.institution_id, a.image_url,
                   a.source_url, a.attribution
            FROM artworks a
            JOIN story_artworks sa ON sa.artwork_id = a.id
            WHERE sa.story_id = ?
            ORDER BY a.title
            """,
            (story_id,),
        ).fetchall()
    return {
        "characters": [dict(row) for row in characters],
        "locations": [dict(row) for row in locations],
        "artworks": [dict(row) for row in artworks],
    }


def _character_relationships(character_id: int) -> dict[str, list[dict[str, Any]]]:
    with get_connection() as conn:
        stories = conn.execute(
            """
            SELECT s.id, s.title, s.testament, s.scripture_reference, s.summary, s.description
            FROM stories s
            JOIN story_characters sc ON sc.story_id = s.id
            WHERE sc.character_id = ?
            ORDER BY s.id
            """,
            (character_id,),
        ).fetchall()
    return {"stories": [dict(row) for row in stories]}


def _location_relationships(location_id: int) -> dict[str, list[dict[str, Any]]]:
    with get_connection() as conn:
        stories = conn.execute(
            """
            SELECT s.id, s.title, s.testament, s.scripture_reference, s.summary, s.description
            FROM stories s
            JOIN story_locations sl ON sl.story_id = s.id
            WHERE sl.location_id = ?
            ORDER BY s.id
            """,
            (location_id,),
        ).fetchall()
    return {"stories": [dict(row) for row in stories]}


def _artwork_relationships(artwork_id: int) -> dict[str, Any]:
    with get_connection() as conn:
        stories = conn.execute(
            """
            SELECT s.id, s.title, s.testament, s.scripture_reference, s.summary, s.description
            FROM stories s
            JOIN story_artworks sa ON sa.story_id = s.id
            WHERE sa.artwork_id = ?
            ORDER BY s.id
            """,
            (artwork_id,),
        ).fetchall()
        related_story = conn.execute(
            """
            SELECT s.id, s.title, s.testament, s.scripture_reference
            FROM stories s
            JOIN artworks a ON a.related_story_id = s.id
            WHERE a.id = ?
            """,
            (artwork_id,),
        ).fetchone()
        institution = conn.execute(
            """
            SELECT i.id, i.name, i.city, i.country, i.website_url
            FROM institutions i
            JOIN artworks a ON a.institution_id = i.id
            WHERE a.id = ?
            """,
            (artwork_id,),
        ).fetchone()

    return {
        "stories": [dict(row) for row in stories],
        "related_story": dict(related_story) if related_story else None,
        "institution": dict(institution) if institution else None,
    }


@router.get("/stories")
def list_stories(
    testament: str | None = Query(default=None),
    character_id: int | None = Query(default=None),
    location_id: int | None = Query(default=None),
    artwork_id: int | None = Query(default=None),
) -> dict[str, Any]:
    conditions: list[str] = []
    params: list[Any] = []

    if testament:
        conditions.append("s.testament = ?")
        params.append(testament)
    if character_id is not None:
        conditions.append("EXISTS (SELECT 1 FROM story_characters sc WHERE sc.story_id = s.id AND sc.character_id = ?)")
        params.append(character_id)
    if location_id is not None:
        conditions.append("EXISTS (SELECT 1 FROM story_locations sl WHERE sl.story_id = s.id AND sl.location_id = ?)")
        params.append(location_id)
    if artwork_id is not None:
        conditions.append("EXISTS (SELECT 1 FROM story_artworks sa WHERE sa.story_id = s.id AND sa.artwork_id = ?)")
        params.append(artwork_id)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    stories = _fetch_all(
        f"""
        SELECT s.id, s.title, s.testament, s.scripture_reference, s.summary, s.description
        FROM stories s
        {where_clause}
        ORDER BY s.id
        """,
        tuple(params),
    )

    for story in stories:
        story["relationships"] = _story_relationships(story["id"])

    return {"items": stories, "count": len(stories)}


@router.get("/stories/{story_id}")
def get_story(story_id: int) -> dict[str, Any]:
    story = _fetch_one(
        """
        SELECT id, title, testament, scripture_reference, summary, description
        FROM stories
        WHERE id = ?
        """,
        (story_id,),
    )
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    story["relationships"] = _enrich_detail_relationships(_story_relationships(story_id), "story", story_id)
    return story


@router.get("/characters")
def list_characters(story_id: int | None = Query(default=None), name: str | None = Query(default=None)) -> dict[str, Any]:
    conditions: list[str] = []
    params: list[Any] = []

    if story_id is not None:
        conditions.append("EXISTS (SELECT 1 FROM story_characters sc WHERE sc.character_id = c.id AND sc.story_id = ?)")
        params.append(story_id)
    if name:
        conditions.append("c.name LIKE ?")
        params.append(f"%{name}%")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    characters = _fetch_all(
        f"""
        SELECT c.id, c.name, c.testament, c.description
        FROM characters c
        {where_clause}
        ORDER BY c.name
        """,
        tuple(params),
    )

    for character in characters:
        character["relationships"] = _character_relationships(character["id"])

    return {"items": characters, "count": len(characters)}


@router.get("/characters/{character_id}")
def get_character(character_id: int) -> dict[str, Any]:
    character = _fetch_one(
        """
        SELECT id, name, testament, description
        FROM characters
        WHERE id = ?
        """,
        (character_id,),
    )
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    character["relationships"] = _enrich_detail_relationships(_character_relationships(character_id), "character", character_id)
    return character


@router.get("/locations")
def list_locations(story_id: int | None = Query(default=None), name: str | None = Query(default=None)) -> dict[str, Any]:
    conditions: list[str] = []
    params: list[Any] = []

    if story_id is not None:
        conditions.append("EXISTS (SELECT 1 FROM story_locations sl WHERE sl.location_id = l.id AND sl.story_id = ?)")
        params.append(story_id)
    if name:
        conditions.append("l.name LIKE ?")
        params.append(f"%{name}%")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    locations = _fetch_all(
        f"""
        SELECT l.id, l.name, l.region, l.description
        FROM locations l
        {where_clause}
        ORDER BY l.name
        """,
        tuple(params),
    )

    for location in locations:
        location["relationships"] = _location_relationships(location["id"])

    return {"items": locations, "count": len(locations)}


@router.get("/locations/{location_id}")
def get_location(location_id: int) -> dict[str, Any]:
    location = _fetch_one(
        """
        SELECT id, name, region, description
        FROM locations
        WHERE id = ?
        """,
        (location_id,),
    )
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    location["relationships"] = _enrich_detail_relationships(_location_relationships(location_id), "location", location_id)
    return location


@router.get("/artworks")
def list_artworks(
    story_id: int | None = Query(default=None),
    artist: str | None = Query(default=None),
    related_story_id: int | None = Query(default=None),
) -> dict[str, Any]:
    conditions: list[str] = []
    params: list[Any] = []

    if story_id is not None:
        conditions.append("EXISTS (SELECT 1 FROM story_artworks sa WHERE sa.artwork_id = a.id AND sa.story_id = ?)")
        params.append(story_id)
    if artist:
        conditions.append("a.artist LIKE ?")
        params.append(f"%{artist}%")
    if related_story_id is not None:
        conditions.append("a.related_story_id = ?")
        params.append(related_story_id)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    artworks = _fetch_all(
        f"""
        SELECT a.id, a.title, a.artist, a.year, a.medium, a.current_location,
               a.description, a.related_story_id, a.institution_id, a.image_url,
               a.source_url, a.attribution
        FROM artworks a
        {where_clause}
        ORDER BY a.title
        """,
        tuple(params),
    )

    for artwork in artworks:
        artwork["relationships"] = _artwork_relationships(artwork["id"])

    return {"items": artworks, "count": len(artworks)}


@router.get("/artworks/{artwork_id}")
def get_artwork(artwork_id: int) -> dict[str, Any]:
    artwork = _fetch_one(
        """
        SELECT id, title, artist, year, medium, current_location, description, related_story_id,
               institution_id, image_url, source_url, attribution
        FROM artworks
        WHERE id = ?
        """,
        (artwork_id,),
    )
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")

    artwork["relationships"] = _enrich_detail_relationships(_artwork_relationships(artwork_id), "artwork", artwork_id)
    return artwork


@router.get("/institutions")
def list_institutions(name: str | None = Query(default=None)) -> dict[str, Any]:
    conditions: list[str] = []
    params: list[Any] = []

    if name:
        conditions.append("i.name LIKE ?")
        params.append(f"%{name}%")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    institutions = _fetch_all(
        f"""
        SELECT i.id, i.name, i.city, i.country, i.website_url
        FROM institutions i
        {where_clause}
        ORDER BY i.name
        """,
        tuple(params),
    )
    return {"items": institutions, "count": len(institutions)}


@router.get("/institutions/{institution_id}")
def get_institution(institution_id: int) -> dict[str, Any]:
    institution = _fetch_one(
        """
        SELECT id, name, city, country, website_url
        FROM institutions
        WHERE id = ?
        """,
        (institution_id,),
    )
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    artworks = _fetch_all(
        """
        SELECT id, title, artist, year, medium, current_location, description, related_story_id,
               institution_id, image_url, source_url, attribution
        FROM artworks
        WHERE institution_id = ?
        ORDER BY title
        """,
        (institution_id,),
    )
    institution["relationships"] = _enrich_detail_relationships({"artworks": artworks}, "institution", institution_id)
    return institution
