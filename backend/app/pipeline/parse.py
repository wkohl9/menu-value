"""Turn raw menu text (from OCR or a website) into structured MenuItems.

WORKING EXAMPLE: `parse_menu_text` handles the simple, common case of
one dish per line with the price at the end. Real menus are messier;
the TODOs below are your Week 3 work. Each one has a skipped test in
tests/test_parse.py - remove the skip, make it pass.
"""

import re

from app.schemas import MenuItem

# A line that ends in a price, e.g.
#   "Classic Burger ........ $14.50"
#   "Fish Tacos (3) - 12.95"
#   "Margherita Pizza 18"
# Group "name" is everything before the separator; group "price" is the number.
_ITEM_LINE = re.compile(
    r"""^
    (?P<name>.*?[A-Za-z].*?)        # name: must contain at least one letter
    [\s.\-–—:|]*                    # leader dots, dashes, colons, spaces
    \$?\s*
    (?P<price>\d{1,3}(?:\.\d{1,2})?)  # 1-3 digits, optional cents
    \s*$""",
    re.VERBOSE,
)


def parse_line(line: str) -> MenuItem | None:
    """Parse one line. Returns None if the line is not a dish with a price."""
    line = line.strip()
    if not line:
        return None

    # TODO (week 3): add-on lines like "+ Add chicken $3" or "Add bacon +2"
    # should NOT become dishes. Detect them and return None (or attach them
    # to the previous dish as an option - your call, document why).

    match = _ITEM_LINE.match(line)
    if not match:
        return None

    name = match.group("name").strip(" .-–—:|")
    price = float(match.group("price"))
    if not name:
        return None
    return MenuItem(name=name, price=price)


def parse_menu_text(text: str) -> list[MenuItem]:
    """Parse a whole menu, one dish per line."""
    items: list[MenuItem] = []
    for line in text.splitlines():
        item = parse_line(line)
        if item is not None:
            items.append(item)

    # TODO (week 3): a line with no price directly under a dish is usually its
    # description ("Brioche bun, aged cheddar, pickles"). Attach it to the
    # previous item's `description` - the ingredients matter for pricing later.

    # TODO (week 3): multi-size prices like "Latte  S 4.50 / L 5.75". Decide on
    # a rule (keep the smallest? one item per size?) and write it down in
    # docs/decisions.md - interviewers love asking about these choices.

    return items
