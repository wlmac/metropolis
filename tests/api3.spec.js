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

test('token-based auth', async ({ request }) => {
  const auth = await request.post('/api/auth/token', {
    data: {
      username: 'sotokanda',
      password: 'verysecure',
    },
  });
  const tokens = await auth.json;
  const ctx = await request.newContext({
    extraHTTPHeaders: {
      "Authentication": `Bearer ${tokens.access}`,
    },
  });
  // TODO: refresh the token
  await ctx.get('/api/me');
});
