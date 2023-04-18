// @ts-check
const { test, expect } = require('@playwright/test');
import {request as req} from '@playwright/test';

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
  urls.forEach((url) => async () => {
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
  const ctx = await req.newContext({
    extraHTTPHeaders: {
      "Authentication": `Bearer ${tokens.access}`,
    },
  });
  // TODO: refresh the token
  await ctx.get('/api/me');
  const fakeTokens = [ "fakeExpoToken1", "ExponentPushToken[fakeExpoToken2]" ];
  fakeTokens.forEach((fakeToken) => {
    const res1 = await ctx.put('/api/v3/notif/token', {
      data: { expo_push_token: fakeToken },
    });
    expect(res1.ok()).toBeTruthy();
    expect(res1.status()).toBe(200);
    const res2 = await ctx.delete('/api/v3/notif/token', {
      data: { expo_push_token: fakeToken },
    });
    expect(res2.ok()).toBeTruthy();
    expect(res2.status()).toBe(200);
  });

  // deleting nonexistent token should work
  const nonexistentToken = "nonexistentToken";
  const res = await ctx.delete('/api/v3/notif/token', {
    data: { expo_push_token: fakeToken },
  });
  expect(res.ok()).toBeTruthy();
  expect(res.status()).toBe(200);
});
