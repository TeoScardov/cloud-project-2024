import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig, loadEnv } from "vite"

export default defineConfig(({ mode }) => {
  //const env = loadEnv(mode, process.cwd(), '');
  return {
    define: {
      'process.env': {}
    },
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      host: true,
      port: 8080,
      cors: true,
      //https: true,
    },
  }
})