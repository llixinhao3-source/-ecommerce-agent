import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue2'

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'dist'
  },
  server: {
    port: 8080,
    host: '0.0.0.0',
    allowedHosts: ['axlike-gaynell-fairily.ngrok-free.dev', 'localhost', '127.0.0.1'],
    proxy: {
      '/api/v1/chat/completions': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/cron': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/schedules': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/api/schedules': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/dashboard.html': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/chat': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/ws': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true,
        ws: true
      },
      '/static-openclaw': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/static-openclaw/, '/static')
      },
      '/static': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/star-office': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/star-office/, '')
      },
      '/agents': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/status': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/yesterday-memo': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/agent-push': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/agent-approve': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/agent-reject': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/join-agent': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/leave-agent': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/set_state': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/health': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      },
      '/api/workflow': {
        target: 'http://127.0.0.1:18789',
        changeOrigin: true
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
