import { useState } from 'react'

const MODES = [
  { id: 'demo', label: 'Demo menu' },
  { id: 'text', label: 'Paste text' },
  { id: 'photo', label: 'Photo' },
]

// The form for getting a menu into the app. It keeps its own text/file state
// and hands everything to the parent through `onAnalyze` when submitted.
export default function MenuInput({ neighborhoods, neighborhood, onNeighborhoodChange, onAnalyze, loading }) {
  const [mode, setMode] = useState('demo')
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)

  // A chosen photo gets a temporary browser URL so we can show a preview.
  // Free the old URL whenever a new photo replaces it.
  function handleFileChange(event) {
    const next = event.target.files?.[0] ?? null
    if (previewUrl) URL.revokeObjectURL(previewUrl)
    setFile(next)
    setPreviewUrl(next ? URL.createObjectURL(next) : null)
  }

  const canSubmit =
    !loading && (mode === 'demo' || (mode === 'text' && text.trim()) || (mode === 'photo' && file))

  function handleSubmit(event) {
    event.preventDefault() // stop the browser from reloading the page
    if (canSubmit) onAnalyze({ mode, text, file })
  }

  return (
    <form className="panel" onSubmit={handleSubmit}>
      <label className="field">
        <span className="field-label">Neighborhood</span>
        <select value={neighborhood} onChange={(e) => onNeighborhoodChange(e.target.value)}>
          <option value="">All of Chicago</option>
          {neighborhoods.map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
      </label>

      <div className="tabs" role="tablist" aria-label="How to add the menu">
        {MODES.map((m) => (
          <button
            key={m.id}
            type="button"
            role="tab"
            aria-selected={mode === m.id}
            className={mode === m.id ? 'tab active' : 'tab'}
            onClick={() => setMode(m.id)}
          >
            {m.label}
          </button>
        ))}
      </div>

      {mode === 'demo' && (
        <p className="hint">
          Try a sample menu with burgers, tacos, ramen and more to see how the comparison works.
        </p>
      )}

      {mode === 'text' && (
        <label className="field">
          <span className="field-label">Menu text — one dish per line, price at the end</span>
          <textarea
            rows={8}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={'Classic Burger ........ $14.50\nAl Pastor Tacos (3) 11\nOat Latte 6.25'}
          />
        </label>
      )}

      {mode === 'photo' && (
        <div className="field">
          <span className="field-label">Photo of the menu</span>
          {/* On phones, capture="environment" opens the back camera directly. */}
          <input
            type="file"
            accept="image/*"
            capture="environment"
            onChange={handleFileChange}
          />
          {file && previewUrl && <img className="preview" src={previewUrl} alt="Selected menu" />}
          <p className="hint">Photo reading arrives in week 4 of the roadmap — the server will say so for now.</p>
        </div>
      )}

      <button className="primary" type="submit" disabled={!canSubmit}>
        {loading ? 'Checking prices…' : 'Check prices'}
      </button>
    </form>
  )
}
