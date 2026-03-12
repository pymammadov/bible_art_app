from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.search import search_service

OUT_PATH = BASE_DIR / "database" / "search_corpus_preview.json"


def main() -> None:
    corpus = search_service.build_corpus()
    OUT_PATH.write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(corpus)} records to {OUT_PATH}")


if __name__ == "__main__":
    main()
