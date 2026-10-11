"""Read the text off a photo of a menu.

TODO (week 4): implement `extract_text`. Suggested path:
  1. pip install paddleocr opencv-python  (or easyocr - try both, keep notes)
  2. Clean the image first with OpenCV: grayscale, deskew, boost contrast.
  3. OCR returns text boxes with coordinates. Group boxes into lines by their
     y-position, then sort each line left-to-right. Two-column menus are the
     hard case: split columns by x-position before grouping lines.
  4. Return one dish per line so parse.parse_menu_text() can take over.

Stretch: compare your pipeline with a vision-capable LLM that returns
structured JSON directly. Measure both on ~20 real menu photos you label by
hand (item/price accuracy). That comparison is a great interview story.
"""

# Used by the /analyze/demo endpoint so the whole app works before OCR exists.
DEMO_MENU_TEXT = """\
SANDWICHES & BURGERS
Classic Smash Burger ........ $13.50
Wagyu Cheeseburger ........ $24
Nashville Hot Chicken Sandwich - 15.95
TACOS
Al Pastor Tacos (3) 11
Birria Tacos (3) ........ 16.50
NOODLES
Tonkotsu Ramen 18
Pad Thai with Shrimp 17.25
COFFEE
Oat Latte 6.25
House Salad 9
"""


class OCRNotImplemented(NotImplementedError):
    pass


def extract_text(image_bytes: bytes) -> str:
    raise OCRNotImplemented(
        "Photo scanning isn't built yet (week 4 of the roadmap). "
        "Paste the menu text or try the demo menu for now."
    )
