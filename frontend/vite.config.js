import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  envPrefix: ['VITE_', 'REACT_APP_'],
  server: {
    port: 5173,
    host: true,
    watch: {
      usePolling: true, // Crucial for hot-reloading to work inside Docker
    },
  },
})
