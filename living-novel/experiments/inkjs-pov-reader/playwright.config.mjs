import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.',
  testMatch: /browser\.spec\.mjs/,
  use: { baseURL: 'http://127.0.0.1:5173', browserName: 'chromium', headless: true },
  webServer: { command: 'npm run dev', url: 'http://127.0.0.1:5173', reuseExistingServer: false, timeout: 30000 },
  reporter: 'list',
});
