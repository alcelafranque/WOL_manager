import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import ViteYaml from '@modyfi/vite-plugin-yaml'

export default defineConfig({
  plugins: [react(), ViteYaml()],
  server: {
      host: "0.0.0.0",
      port: 3000,
  },
  build: {
      outDir: 'build',
  }
})
