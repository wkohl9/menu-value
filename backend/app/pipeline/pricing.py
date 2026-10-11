"""Compare a dish's price with similar dishes nearby.

WORKING BASELINE: percentiles against comparable dishes (same category),
using the neighborhood when it has enough data and falling back to all of
Chicago otherwise. No ML yet - and that's on purpose. This baseline is what
your model has to beat.

TODO (week 6): train a model that predicts a fair price from more than the
category - restaurant rating, price tier, cuisine, and ingredients pulled
from the description (wagyu, truffle, "for two"). LightGBM's quantile
objective gives you a low/high range directly. Evaluate on held-out dishes
and report median absolute error against THIS baseline.
"""

import csv
import statistics
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.schemas import Verdict

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
REAL_DATA_PATH = DATA_DIR / "menus.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample_menus.csv"

# Below this many comparable dishes, a percentile is mostly noise.
MIN_COMPARABLES = 5


@dataclass(frozen=True)
class Comparison:
    comparable_count: int
    scope: str | None
    percentile: float | None
    typical_low: float | None
    typical_high: float | None
    verdict: Verdict


@dataclass(frozen=True)
class PriceRow:
    neighborhood: str
    category: str
    price: float


class PriceReference:
    """All known dish prices, indexed for comparison."""

    def __init__(self, rows: list[PriceRow], is_sample: bool):
        self.rows = rows
        self.is_sample = is_sample

    @classmethod
    def from_csv(cls, path: Path, is_sample: bool) -> "PriceReference":
        with path.open(newline="") as f:
            rows = [
                PriceRow(
                    neighborhood=r["neighborhood"],
                    category=r["category"],
                    price=float(r["price"]),
                )
                for r in csv.DictReader(f)
                if r["category"] and r["price"]
            ]
        return cls(rows, is_sample)

    def prices_for(self, category: str, neighborhood: str | None = None) -> list[float]:
        return [
            r.price
            for r in self.rows
            if r.category == category
            and (neighborhood is None or r.neighborhood.lower() == neighborhood.lower())
        ]

    def compare(self, category: str | None, price: float, neighborhood: str | None) -> Comparison:
        if category is None:
            return Comparison(0, None, None, None, None, "not enough data")

        # Prefer the neighborhood; fall back to the whole city.
        comps, scope = [], None
        if neighborhood:
            comps, scope = self.prices_for(category, neighborhood), neighborhood
        if len(comps) < MIN_COMPARABLES:
            comps, scope = self.prices_for(category), "Chicago"
        if len(comps) < MIN_COMPARABLES:
            return Comparison(len(comps), scope, None, None, None, "not enough data")

        cheaper = sum(p < price for p in comps)
        ties = sum(p == price for p in comps)
        percentile = round(100 * (cheaper + 0.5 * ties) / len(comps), 1)

        q1, _, q3 = statistics.quantiles(comps, n=4, method="inclusive")

        if percentile <= 25:
            verdict: Verdict = "good value"
        elif percentile >= 75:
            verdict = "pricey"
        else:
            verdict = "typical"

        return Comparison(len(comps), scope, percentile, round(q1, 2), round(q3, 2), verdict)


@lru_cache
def get_reference() -> PriceReference:
    """Use your real collected data once it exists; otherwise the sample set."""
    if REAL_DATA_PATH.exists() and REAL_DATA_PATH.stat().st_size > 0:
        ref = PriceReference.from_csv(REAL_DATA_PATH, is_sample=False)
        if ref.rows:
            return ref
    return PriceReference.from_csv(SAMPLE_DATA_PATH, is_sample=True)
