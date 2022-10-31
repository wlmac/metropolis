#!/bin/env python3
import secrets

N = 80
RAFFLE_ID = 1
CODE_LEN = 8

tmpl = f'https://maclyonsden.com/raffle?r={RAFFLE_ID}&c={"{code}"}'

for i in range(N):
    url = tmpl.format(code=(code := secrets.token_urlsafe(CODE_LEN)))
    print(f'qrencode -l H -o \'qr-{code}.png\' \'{url}\'')
