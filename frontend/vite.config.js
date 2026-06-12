import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Le proxy évite les soucis de CORS en développement :
// toute requête /api est transmise au backend FastAPI.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: { "/api": "http://localhost:8000" },
  },
});
