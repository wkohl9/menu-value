# Design decisions

One entry per real decision. Interviewers ask "why did you do it that way?"
- this file is your answer key.

Template:

## YYYY-MM-DD - Short title
**Decision:** what you chose.
**Alternatives:** what else you considered.
**Why:** the reason, ideally with a number or an example.

---

## 2026-10-11 - Show "price context", not "overcharging"
**Decision:** label dishes good value / typical / pricey by percentile among
comparable dishes, and show the typical range.
**Alternatives:** a binary "overcharging" flag.
**Why:** we can't see portion size or ingredient quality, so an accusation
isn't supportable; a percentile is honest about what we actually know.

## 2026-10-11 - Neighborhood first, citywide fallback, minimum 5 comparables
**Decision:** compare within the neighborhood when it has 5+ similar
dishes, otherwise all of Chicago; below 5 citywide, say "not enough data".
**Alternatives:** always citywide; any number of comparables.
**Why:** prices differ by neighborhood, but a percentile over 2-3 dishes is
noise. 5 is a starting guess - revisit once real data exists.
