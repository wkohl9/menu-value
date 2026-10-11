import { categoryLabel, describeComparison, formatPrice } from '../format.js'

// A horizontal bar showing the typical price range (shaded) and where this
// dish's price lands on it (the dot).
function RangeBar({ low, high, price }) {
  const min = Math.min(low, price) * 0.85
  const max = Math.max(high, price) * 1.15
  const toPercent = (value) => ((value - min) / (max - min)) * 100

  return (
    <div className="range" aria-hidden="true">
      <div
        className="range-typical"
        style={{ left: `${toPercent(low)}%`, width: `${toPercent(high) - toPercent(low)}%` }}
      />
      <div className="range-dot" style={{ left: `${toPercent(price)}%` }} />
      <span className="range-label" style={{ left: `${toPercent(low)}%` }}>
        {formatPrice(low)}
      </span>
      <span className="range-label right" style={{ left: `${toPercent(high)}%` }}>
        {formatPrice(high)}
      </span>
    </div>
  )
}

export default function DishCard({ dish }) {
  const { item, verdict } = dish
  const hasRange = dish.typical_low != null && dish.typical_high != null
  const verdictClass = verdict.replaceAll(' ', '-')

  return (
    <li className="dish">
      <div className="dish-top">
        <div>
          <h3 className="dish-name">{item.name}</h3>
          <span className="dish-category">{categoryLabel(dish.category)}</span>
        </div>
        <div className="dish-right">
          <span className="dish-price">{formatPrice(item.price)}</span>
          <span className={`verdict ${verdictClass}`}>{verdict}</span>
        </div>
      </div>
      {hasRange && <RangeBar low={dish.typical_low} high={dish.typical_high} price={item.price} />}
      <p className="dish-detail">
        {describeComparison(dish)}
        {hasRange && ` Typical: ${formatPrice(dish.typical_low)}–${formatPrice(dish.typical_high)}.`}
      </p>
    </li>
  )
}
