import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig, loadEnv } from "vite"

export default defineConfig(({ mode }) => {
  //const env = loadEnv(mode, process.cwd(), '');
  return {
    // define: {
    //   'process.env.ACCOUNT_SERVICE_URL': JSON.stringify(env.ACCOUNT_SERVICE_URL || 'http://localhost:4001'),
    //   'process.env.PURCHASE_SERVICE_URL': JSON.stringify(env.PURCHASE_SERVICE_URL || 'http://localhost:4004'),
    //   'process.env.PRODUCT_CATALOG_URL': JSON.stringify(env.PRODUCT_CATALOG_URL || 'http://localhost:4003'),
    //   'process.env.SHOPPING_CART_URL': JSON.stringify(env.SHOPPING_CART_URL || 'http://localhost:4005'),
    //   'process.env.NUMBER_OF_BOOKS_TO_DISPLAY': JSON.stringify(env.NUMBER_OF_BOOKS_TO_DISPLAY || 10),
    //   //'process.env.PROXY_ALB_URL': JSON.stringify(env.PROXY_ALB_URL),
    // },
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
      cors: false,
      //https: true,
    },
  }
})