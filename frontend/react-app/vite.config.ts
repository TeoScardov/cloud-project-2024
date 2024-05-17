import path from "path"
import react from "@vitejs/plugin-react"
import mkcert from 'vite-plugin-mkcert'
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
  // plugins: [react(),mkcert()],
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
