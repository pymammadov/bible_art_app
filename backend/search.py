from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import Any

from .db import get_connection


@dataclass(slots=True)
class SearchHit:
    entity_type: str
    entity_id: int
    title: str
    snippet: str
    score: float


class SemanticSearchService:
    """Lightweight semantic-search scaffold.

    Current behavior:
    - keyword scoring over a normalized in-memory corpus
    Future behavior:
    - plug embeddings/vector retrieval into the same public methods
    """

    def __init__(self) -> None:
        self.embedding_provider = os.getenv("EMBEDDING_PROVIDER", "none")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "none")

    def _expand_terms(self, query: str) -> list[str]:
        base = [token for token in query.lower().split() if token.strip()]
        synonyms: dict[str, list[str]] = {
            "kings": ["king", "david", "solomon"],
            "moses": ["exodus", "sinai", "burning", "bush"],
            "jesus": ["christ", "messiah", "galilee", "jerusalem"],
            "places": ["location", "region", "city"],
            "artworks": ["art", "painting", "artist"],
        }
        expanded = list(base)
        for token in base:
            expanded.extend(synonyms.get(token, []))
        # deduplicate, preserve order
        seen: set[str] = set()
        ordered: list[str] = []
        for token in expanded:
            if token not in seen:
                seen.add(token)
                ordered.append(token)
        return ordered

    def build_corpus(self) -> list[dict[str, Any]]:
        with get_connection() as conn:
            stories = conn.execute(
                """
                SELECT id, title, summary, description, scripture_reference
                FROM stories
                """
            ).fetchall()
            characters = conn.execute(
                """
                SELECT id, name AS title, description
                FROM characters
                """
            ).fetchall()
            locations = conn.execute(
                """
                SELECT id, name AS title, region, description
                FROM locations
                """
            ).fetchall()
            artworks = conn.execute(
                """
                SELECT id, title, artist, description, medium
                FROM artworks
                """
            ).fetchall()

        corpus: list[dict[str, Any]] = []
        for row in stories:
            corpus.append(
                {
                    "entity_type": "story",
                    "entity_id": row["id"],
                    "title": row["title"],
                    "text": " ".join(
                        value or "" for value in (row["title"], row["summary"], row["description"], row["scripture_reference"])
                    ).lower(),
                    "snippet": row["summary"] or row["description"] or "",
                }
            )
        for row in characters:
            corpus.append(
                {
                    "entity_type": "character",
                    "entity_id": row["id"],
                    "title": row["title"],
                    "text": " ".join(value or "" for value in (row["title"], row["description"])).lower(),
                    "snippet": row["description"] or "",
                }
            )
        for row in locations:
            corpus.append(
                {
                    "entity_type": "location",
                    "entity_id": row["id"],
                    "title": row["title"],
                    "text": " ".join(value or "" for value in (row["title"], row["region"], row["description"])).lower(),
                    "snippet": row["description"] or row["region"] or "",
                }
            )
        for row in artworks:
            corpus.append(
                {
                    "entity_type": "artwork",
                    "entity_id": row["id"],
                    "title": row["title"],
                    "text": " ".join(value or "" for value in (row["title"], row["artist"], row["description"], row["medium"])).lower(),
                    "snippet": row["description"] or row["artist"] or "",
                }
            )
        return corpus

    def keyword_search(self, query: str, limit: int = 20) -> list[SearchHit]:
        terms = self._expand_terms(query)
        if not terms:
            return []

        scored: list[SearchHit] = []
        for item in self.build_corpus():
            score = 0.0
            for term in terms:
                if term in item["text"]:
                    score += 1.0
            if score > 0:
                scored.append(
                    SearchHit(
                        entity_type=item["entity_type"],
                        entity_id=int(item["entity_id"]),
                        title=item["title"],
                        snippet=item["snippet"],
                        score=score,
                    )
                )

        scored.sort(key=lambda hit: hit.score, reverse=True)
        return scored[:limit]

    def search(self, query: str, limit: int = 20, mode: str = "auto") -> dict[str, Any]:
        # Placeholder behavior until embeddings are integrated.
        items = [asdict(hit) for hit in self.keyword_search(query, limit=limit)]
        return {
            "query": query,
            "mode": mode,
            "engine": "keyword_fallback",
            "items": items,
            "count": len(items),
            "embedding_ready": {
                "provider": self.embedding_provider,
                "model": self.embedding_model,
                "index_backing": "sqlite_placeholder",
            },
        }


search_service = SemanticSearchService()
