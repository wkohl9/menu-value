import { useEffect, useState } from 'react'
import { analyzeDemo, analyzeImage, analyzeText, getNeighborhoods } from './api.js'
import MenuInput from './components/MenuInput.jsx'
import Results from './components/Results.jsx'

export default function App() {
  const [neighborhoods, setNeighborhoods] = useState([])
  const [neighborhood, setNeighborhood] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Load the neighborhood list once, when the page first appears.
  useEffect(() => {
    getNeighborhoods()
      .then(setNeighborhoods)
      .catch(() => setError("Can't reach the server. Is the backend running on port 8000?"))
  }, [])

  async function handleAnalyze({ mode, text, file }) {
    setLoading(true)
    setError(null)
    try {
      let result
      if (mode === 'demo') result = await analyzeDemo(neighborhood)
      else if (mode === 'text') result = await analyzeText(text, neighborhood)
      else result = await analyzeImage(file, neighborhood)
      setAnalysis(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <header className="masthead">
        <h1>Menu Value</h1>
        <p className="tagline">How does each dish's price compare with similar dishes nearby?</p>
      </header>

      <MenuInput
        neighborhoods={neighborhoods}
        neighborhood={neighborhood}
        onNeighborhoodChange={setNeighborhood}
        onAnalyze={handleAnalyze}
        loading={loading}
      />

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      {analysis && <Results analysis={analysis} />}

      <footer className="footer">Chicago only, for now · Prices are estimates, not judgments</footer>
    </main>
  )
}
