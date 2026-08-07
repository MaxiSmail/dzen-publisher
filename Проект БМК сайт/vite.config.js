import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // Ensures relative assets paths so that the compiled index.html can be opened directly from disk (file:///...)
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false
  }
})
