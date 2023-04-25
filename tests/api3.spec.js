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
  for (let url of urls) {
    const res = await request.get(url);
    expect(res.ok()).toBeTruthy();
    expect(res.status()).toBe(200);
  }
});

async function authenticate({ request }) {
  const auth = await request.post('/api/auth/token', {
    data: {
      username: 'sotokanda',
      password: 'verysecure',
    },
  });
  console.log("authenticate: auth:", auth);
  expect(auth.ok()).toBeTruthy();
  const tokens = await auth.json();
  const ctx = await await req.newContext({
    extraHTTPHeaders: {
      "Authorization": `Bearer ${tokens.access}`,
    },
  });
  // NOTE: not checking refresh token for now (token should work aniway)
  // check access token works
  const res1 = await ctx.get('/api/me');
  console.log("authenticate: res1:", res1);
  expect(res1.ok()).toBeTruthy();
  expect(res1.status()).toBe(200);
  return ctx;
};

test('expo notif token', async ({ request }) => {
  const ctx = await authenticate({ request });
  const fakeTokens = [ "fakeExpoToken1", "ExponentPushToken[fakeExpoToken2]" ];
  for (let fakeToken of fakeTokens) {
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
  }

  // deleting nonexistent token should return 200
  const nonexistentToken = "nonexistentToken";
  const res = await ctx.delete('/api/v3/notif/token', {
    data: { expo_push_token: nonexistentToken },
  });
  expect(res.ok()).toBeTruthy();
  expect(res.status()).toBe(200);
});

test('all: list', async ({ request }) => {
  const ctx = await authenticate({ request });
  const cases = [
    { type: "announcement" },
    { type: "blog-post" },
    { type: "exhibit" },
    { type: "event" },
    { type: "organization" },
    { type: "tag" },
  ];
  for (let case_ of cases) {
    const res = await ctx.get(`/api/v3/obj/${case_.type}`)
    expect(res.ok()).toBeTruthy();
    expect(res.status()).toBe(200);
  }
});
