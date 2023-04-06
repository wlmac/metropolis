// @ts-check
const { test, expect } = require('@playwright/test');

test('sanity', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Metropolis/);
});

test('sanity 2', async ({ request }) => {
  const urls = [
    '/api/version',
    '/api/v3/staff',
    '/api/v3/feeds',
    '/api/v3/banners',
  ];
  urls.forEach((url) => {
    const resp = await request.get(url);
    expect(resp.ok()).toBeTruthy();
  })
});

test('token-based auth', async ({ request }) => {
  const auth = await request.post('/api/auth/token', {
    data: {
      username: 'sotokanda',
      password: 'verysecure',
    },
  });
  expect(auth.ok()).toBeTruthy();
  const tokens = await auth.json;
  const ctx = await request.newContext({
    extraHTTPHeaders: {
      "Authentication": `Bearer ${tokens.access}`,
    },
  });
  // TODO: refresh the token
  await ctx.get('/api/me');
});
