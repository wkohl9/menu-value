"""Generate data/sample_menus.csv: SYNTHETIC prices so the app works on day one.

These are made-up restaurants with plausible-looking random prices. They are
NOT real Chicago data - every analysis made with them is flagged
`using_sample_data: true`. Replace them with real menus in weeks 1-2 by
filling in data/menus.csv (same columns); the app switches over automatically.

Run from the project root:  python scripts/make_sample_data.py
"""

import csv
import random
from datetime import date
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "sample_menus.csv"

NEIGHBORHOODS = ["Hyde Park", "Lincoln Park", "Logan Square", "Pilsen", "West Loop", "Wicker Park"]

# category: (dish name, typical low, typical high)
DISHES = {
    "burger": ("Cheeseburger", 12.0, 20.0),
    "tacos": ("Tacos (3)", 9.0, 16.0),
    "pizza": ("Margherita Pizza", 14.0, 26.0),
    "ramen": ("Tonkotsu Ramen", 14.0, 20.0),
    "pad_thai": ("Pad Thai", 13.0, 18.0),
    "chicken_sandwich": ("Fried Chicken Sandwich", 11.0, 17.0),
    "latte": ("Latte", 4.5, 6.75),
}

# Some neighborhoods run pricier than others, so local comparisons differ.
NEIGHBORHOOD_FACTOR = {
    "Hyde Park": 0.95, "Lincoln Park": 1.08, "Logan Square": 1.02,
    "Pilsen": 0.88, "West Loop": 1.18, "Wicker Park": 1.05,
}

COLUMNS = ["restaurant", "neighborhood", "cuisine", "rating", "price_tier",
           "dish_name", "category", "price", "source", "collected_on"]


def main() -> None:
    rng = random.Random(42)  # fixed seed -> same file every run
    rows = []
    n = 0
    for hood in NEIGHBORHOODS:
        for category, (dish, low, high) in DISHES.items():
            for _ in range(6):
                n += 1
                price = rng.uniform(low, high) * NEIGHBORHOOD_FACTOR[hood]
                price = round(price * 4) / 4 - 0.01 if price > 10 else round(price * 4) / 4
                rows.append({
                    "restaurant": f"Sample Spot {n:03d}",
                    "neighborhood": hood,
                    "cuisine": "sample",
                    "rating": round(rng.uniform(3.6, 4.8), 1),
                    "price_tier": rng.choice([1, 2, 2, 3]),
                    "dish_name": dish,
                    "category": category,
                    "price": f"{price:.2f}",
                    "source": "synthetic",
                    "collected_on": date(2026, 10, 1).isoformat(),
                })
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic rows to {OUT}")


if __name__ == "__main__":
    main()
