// Vite config that enables React and proxies API requests to the backend container.

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    // Allow external tunnels (ngrok) to reach the dev server.
    allowedHosts: "all",
    proxy: {
      "/api": {
        target: process.env.VITE_PROXY_TARGET || "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
});
