"""Map a dish name to a canonical category so we compare like with like.

WORKING BASELINE: keyword matching against data/categories.json. It is
fast, explainable, and wrong in predictable ways ("Burger-Style Pizza").

TODO (week 5): build a small labeled set (~200 dish names -> category) in
data/labeled_dishes.csv, measure this baseline's accuracy, then try
sentence-transformers embeddings (nearest category by cosine similarity).
Keep whichever wins - and keep the numbers. "Embeddings improved
categorization accuracy from 81% to 93%" is a resume line.
"""

import json
import re
from functools import lru_cache
from pathlib import Path

CATEGORIES_PATH = Path(__file__).resolve().parents[3] / "data" / "categories.json"


@lru_cache
def load_categories(path: Path = CATEGORIES_PATH) -> dict[str, list[str]]:
    return json.loads(path.read_text())


def categorize(name: str, description: str | None = None) -> str | None:
    """Return the best-matching category, or None if nothing matches.

    Scoring: the longest matching keyword wins, so "fried chicken sandwich"
    beats a shorter accidental match. Plurals ("tacos", "burgers") match too.
    """
    text = f"{name} {description or ''}".lower()
    best_category, best_score = None, 0

    for category, keywords in load_categories().items():
        for keyword in keywords:
            pattern = rf"\b{re.escape(keyword.lower())}s?\b"
            if re.search(pattern, text) and len(keyword) > best_score:
                best_category, best_score = category, len(keyword)

    return best_category
