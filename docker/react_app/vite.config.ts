import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig, loadEnv } from "vite"

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    define: {
      'process.env.ACCOUNT_SERVICE_URL': JSON.stringify(env.ACCOUNT_SERVICE_URL),
      'process.env.PURCHASE_SERVICE_URL': JSON.stringify(env.PURCHASE_SERVICE_URL),
      'process.env.PRODUCT_CATALOG_URL': JSON.stringify(env.PRODUCT_CATALOG_URL),
      'process.env.SHOPPING_CART_URL': JSON.stringify(env.SHOPPING_CART_URL),
      'process.env.NUMBER_OF_BOOKS_TO_DISPLAY': JSON.stringify(env.NUMBER_OF_BOOKS_TO_DISPLAY),
      'process.env.PROXY_ALB_URL': JSON.stringify(env.PROXY_ALB_URL),
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
      // proxy: {
      //   '/api': {
      //     target: process.env.PROXY_ALB_URL,
      //     changeOrigin: true,
      //     secure: false,
      //     rewrite: (path) => path.replace(/^\/api/, '')
      //   }
      // }
      // https: true,
    },
  }
})