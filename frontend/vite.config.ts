import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import { resolve } from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": resolve("src"),
      "@/utils": resolve("src/utils"),
      "@/components": resolve("src/components"),
      "@/views": resolve("src/views"),
      "@/layouts": resolve("src/layouts"),
      "@/assets": resolve("src/assets"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
    watch: {
      usePolling: true,
    },
    hmr: {
      port: 3000,
    },
  },
});
