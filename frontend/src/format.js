// Small pure functions for turning API data into words.
// "Pure" = same input, same output, no side effects - easy to test and reuse.

const CATEGORY_LABELS = {
  burger: 'Burger',
  tacos: 'Tacos',
  pizza: 'Pizza',
  ramen: 'Ramen',
  pad_thai: 'Pad Thai',
  chicken_sandwich: 'Chicken sandwich',
  latte: 'Latte',
}

export function formatPrice(amount) {
  return amount == null ? '—' : `$${amount.toFixed(2)}`
}

export function categoryLabel(category) {
  return CATEGORY_LABELS[category] ?? category ?? 'Uncategorized'
}

export function describeComparison(dish) {
  if (dish.verdict === 'not enough data') {
    if (!dish.category) return "We don't track this kind of dish yet."
    return `Only ${dish.comparable_count} similar dishes on file — not enough to compare yet.`
  }
  const pct = Math.round(dish.percentile)
  return `Costs more than ${pct}% of ${dish.comparable_count} similar dishes in ${dish.comparison_scope}.`
}

export function countVerdicts(dishes) {
  const counts = { 'good value': 0, typical: 0, pricey: 0, 'not enough data': 0 }
  for (const dish of dishes) counts[dish.verdict] += 1
  return counts
}
