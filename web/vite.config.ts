import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    cors: true,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:9000/",
        // target: "https://memos.justsven.top/",
        changeOrigin: true,
      },
    },
  },
});
