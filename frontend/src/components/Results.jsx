import { countVerdicts } from '../format.js'
import DishCard from './DishCard.jsx'

export default function Results({ analysis }) {
  const { dishes } = analysis

  if (dishes.length === 0) {
    return (
      <section className="panel">
        <p className="hint">
          No dishes found. Make sure each line has a dish name followed by a price.
        </p>
      </section>
    )
  }

  const counts = countVerdicts(dishes)

  return (
    <section aria-label="Price check results">
      {analysis.using_sample_data && (
        <p className="notice">
          Comparisons use synthetic sample prices, not real Chicago menus yet. Add real data to
          <code> data/menus.csv</code> and this note disappears.
        </p>
      )}
      <p className="summary">
        <strong>{dishes.length} dishes</strong> · {counts['good value']} good value · {counts.typical}{' '}
        typical · {counts.pricey} pricey
      </p>
      <ul className="dishes">
        {dishes.map((dish, i) => (
          <DishCard key={`${dish.item.name}-${i}`} dish={dish} />
        ))}
      </ul>
    </section>
  )
}
