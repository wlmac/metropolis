from datetime import datetime
from random import randint


def justinian_slam():
    letters = ["S", "K", "D", "J", "F", "L"]
    now = datetime.now().hour

    length = randint(4, 12)

    sub = min(6, length)
    out = letters[:sub]

    for i in range(length - sub):
        out.append(letters[i % 6])
    rand = 2
    if now < 8:
        rand = randint(0, now) + 5
    elif now > 21:
        rand = randint(0, now - 21) + 2
    for i in range(rand):
        a = randint(0, length - 1)
        b = randint(0, length - 1)
        out[a], out[b] = out[b], out[a]
    out = "".join(out)
    rand = randint(0, 98)
    if rand < 25:
        out += " XD"
    elif rand < 50:
        out += " LOL"
    return out
