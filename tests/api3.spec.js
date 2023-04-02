// @ts-check
const { test, expect } = require('@playwright/test');

test('sanity', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Metropolis/);
});

test('sanity 2', async ({ request }) => {
  await request.get('/api/version');
  await request.get('/api/v3/staff');
  await request.get('/api/v3/feeds');
  await request.get('/api/v3/banners');
});
