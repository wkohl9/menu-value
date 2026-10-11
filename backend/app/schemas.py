"""Data shapes shared by the API, the pipeline and the tests.

Pydantic validates everything that crosses a boundary (HTTP requests,
OCR output, CSV rows), so bad data fails loudly instead of silently
producing a wrong price comparison.
"""

from typing import Literal

from pydantic import BaseModel, Field

Verdict = Literal["good value", "typical", "pricey", "not enough data"]


class MenuItem(BaseModel):
    """One dish as it appears on a menu."""

    name: str = Field(min_length=1)
    price: float = Field(gt=0, lt=1000)
    description: str | None = None


class DishAnalysis(BaseModel):
    """How one dish's price compares with similar dishes nearby."""

    item: MenuItem
    category: str | None = Field(
        description="Canonical dish category, e.g. 'burger'. None if unrecognized."
    )
    comparable_count: int = Field(description="How many similar dishes we compared against.")
    comparison_scope: str | None = Field(
        description="Where the comparables came from: a neighborhood name or 'Chicago'."
    )
    percentile: float | None = Field(
        default=None,
        description="0-100: share of comparable dishes that cost less than this one.",
    )
    typical_low: float | None = Field(default=None, description="25th percentile price.")
    typical_high: float | None = Field(default=None, description="75th percentile price.")
    verdict: Verdict


class MenuAnalysis(BaseModel):
    neighborhood: str | None
    dishes: list[DishAnalysis]
    using_sample_data: bool = Field(
        description="True while comparisons use the synthetic sample dataset, not real menus."
    )


class TextAnalysisRequest(BaseModel):
    text: str = Field(min_length=1, description="Raw menu text, one dish per line.")
    neighborhood: str | None = None
