from app.pipeline.pricing import PriceReference, PriceRow


def make_reference() -> PriceReference:
    rows = [PriceRow("Pilsen", "burger", p) for p in [10, 11, 12, 13, 14]]
    rows += [PriceRow("West Loop", "burger", p) for p in [16, 18, 20]]  # only 3: too few
    return PriceReference(rows, is_sample=False)


def test_cheap_dish_is_good_value():
    c = make_reference().compare("burger", 10.5, "Pilsen")
    assert c.scope == "Pilsen"
    assert c.verdict == "good value"
    assert c.percentile == 20.0  # cheaper than 1 of 5


def test_expensive_dish_is_pricey():
    c = make_reference().compare("burger", 15, "Pilsen")
    assert c.verdict == "pricey"
    assert c.percentile == 100.0


def test_falls_back_to_citywide_when_neighborhood_is_thin():
    c = make_reference().compare("burger", 15, "West Loop")
    assert c.scope == "Chicago"
    assert c.comparable_count == 8


def test_unknown_category_has_no_verdict():
    c = make_reference().compare(None, 15, "Pilsen")
    assert c.verdict == "not enough data"
    assert c.percentile is None


def test_typical_range_is_interquartile():
    c = make_reference().compare("burger", 12, "Pilsen")
    assert (c.typical_low, c.typical_high) == (11.0, 13.0)
