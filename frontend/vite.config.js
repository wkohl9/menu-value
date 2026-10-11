import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Any request to /api/... from the website is forwarded to the Python
    // backend, so the browser thinks both live on the same server (no CORS).
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
