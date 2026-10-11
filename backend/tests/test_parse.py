import pytest

from app.pipeline.parse import parse_line, parse_menu_text


@pytest.mark.parametrize(
    "line, name, price",
    [
        ("Classic Burger ........ $14.50", "Classic Burger", 14.50),
        ("Fish Tacos (3) - 12.95", "Fish Tacos (3)", 12.95),
        ("Margherita Pizza 18", "Margherita Pizza", 18.0),
        ("Oat Latte: $6.25", "Oat Latte", 6.25),
        ("12 inch Pepperoni Pizza 21", "12 inch Pepperoni Pizza", 21.0),
    ],
)
def test_parses_simple_lines(line, name, price):
    item = parse_line(line)
    assert item is not None
    assert item.name == name
    assert item.price == price


@pytest.mark.parametrize("line", ["", "   ", "BURGERS", "Open 11am - 10pm daily", "$14"])
def test_ignores_non_dish_lines(line):
    assert parse_line(line) is None


def test_parse_menu_text_skips_headers():
    text = "BURGERS\nClassic Burger 14\nDouble Burger 17.5\n"
    assert [i.name for i in parse_menu_text(text)] == ["Classic Burger", "Double Burger"]


# --- Your week 3 work: remove each skip, then make the test pass. ---


@pytest.mark.skip(reason="TODO week 3: add-on lines should not become dishes")
@pytest.mark.parametrize("line", ["+ Add chicken $3", "Add bacon +2", "Extra cheese +1.50"])
def test_ignores_add_on_lines(line):
    assert parse_line(line) is None


@pytest.mark.skip(reason="TODO week 3: attach description lines to the dish above")
def test_attaches_description_to_previous_dish():
    text = "Classic Burger 14\nBrioche bun, aged cheddar, pickles\n"
    items = parse_menu_text(text)
    assert len(items) == 1
    assert items[0].description == "Brioche bun, aged cheddar, pickles"
