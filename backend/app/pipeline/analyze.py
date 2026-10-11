"""The full pipeline: menu text -> dishes -> categories -> price comparisons."""

from app.pipeline.categorize import categorize
from app.pipeline.parse import parse_menu_text
from app.pipeline.pricing import PriceReference, get_reference
from app.schemas import DishAnalysis, MenuAnalysis


def analyze_menu_text(
    text: str,
    neighborhood: str | None = None,
    reference: PriceReference | None = None,
) -> MenuAnalysis:
    reference = reference or get_reference()
    dishes: list[DishAnalysis] = []

    for item in parse_menu_text(text):
        category = categorize(item.name, item.description)
        c = reference.compare(category, item.price, neighborhood)
        dishes.append(
            DishAnalysis(
                item=item,
                category=category,
                comparable_count=c.comparable_count,
                comparison_scope=c.scope,
                percentile=c.percentile,
                typical_low=c.typical_low,
                typical_high=c.typical_high,
                verdict=c.verdict,
            )
        )

    return MenuAnalysis(
        neighborhood=neighborhood,
        dishes=dishes,
        using_sample_data=reference.is_sample,
    )
