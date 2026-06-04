import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 清除系统代理，直连本地后端
delete process.env.HTTP_PROXY
delete process.env.http_proxy
delete process.env.HTTPS_PROXY
delete process.env.https_proxy
process.env.NO_PROXY = '*'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
