// Every call to the Python backend lives in this file, so components never
// build URLs or parse errors themselves. When you build the Expo app in
// week 7, you can copy this file over almost unchanged.
//
// In development, Vite forwards /api/* to http://127.0.0.1:8000
// (see vite.config.js). In production, set VITE_API_URL to your API's URL.
const API_BASE = import.meta.env.VITE_API_URL ?? ''

async function request(path, options) {
  const res = await fetch(`${API_BASE}${path}`, options)
  if (!res.ok) {
    let message = `Something went wrong (error ${res.status}).`
    try {
      const body = await res.json()
      if (typeof body.detail === 'string') message = body.detail
    } catch {
      // The response wasn't JSON - keep the generic message.
    }
    throw new Error(message)
  }
  return res.json()
}

export function getNeighborhoods() {
  return request('/api/neighborhoods')
}

export function analyzeDemo(neighborhood) {
  const query = neighborhood ? `?neighborhood=${encodeURIComponent(neighborhood)}` : ''
  return request(`/api/analyze/demo${query}`)
}

export function analyzeText(text, neighborhood) {
  return request('/api/analyze/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, neighborhood: neighborhood || null }),
  })
}

export function analyzeImage(file, neighborhood) {
  const form = new FormData()
  form.append('image', file)
  if (neighborhood) form.append('neighborhood', neighborhood)
  return request('/api/analyze/image', { method: 'POST', body: form })
}
