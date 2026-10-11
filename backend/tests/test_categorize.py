import pytest

from app.pipeline.categorize import categorize


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Classic Smash Burger", "burger"),
        ("Double Cheeseburger", "burger"),
        ("Al Pastor Tacos (3)", "tacos"),
        ("Tonkotsu Ramen", "ramen"),
        ("Pad Thai with Shrimp", "pad_thai"),
        ("Nashville Hot Chicken Sandwich", "chicken_sandwich"),
        ("Oat Latte", "latte"),
        ("Chicago Deep Dish", "pizza"),
        ("House Salad", None),
    ],
)
def test_keyword_baseline(name, expected):
    assert categorize(name) == expected


def test_longest_keyword_wins():
    # "fried chicken sandwich" (22 chars) should beat any shorter match.
    assert categorize("Fried Chicken Sandwich") == "chicken_sandwich"


@pytest.mark.skip(reason="TODO week 5: the keyword baseline gets this wrong - can embeddings fix it?")
def test_tricky_name():
    assert categorize("Burger-Style Pizza") == "pizza"
