import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/generate": "http://localhost:8000",
      "/history": "http://localhost:8000",
      "/download": "http://localhost:8000",
    },
  },
});