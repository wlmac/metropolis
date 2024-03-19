#!/usr/bin/env python3
import datetime as dt
from collections import defaultdict

import requests

METROPOLIS_STAFFS = {
    "Project Manager": {9},
    "Frontend Developer": {25, 265, 37, 338, 360, 139, 220, 222, 411},
    "Backend Developer": {1, 20, 165, 746, 156},
    "App Developer": {21, 56, 66, 799},
    "Graphic Designer": {5, 13, 267, 18, 347, 62, 35, 78},
    "Content Creator": {
        8,
        14,
        103,
        145,
        183,
        57,
        414,
        235,
        157,
        677,
        659,
        729,
        843,
    },
    "Game Developer": {475, 61},
    "Alumnus": {3, 4, 6, 16, 32, 33, 98, 297},
}

current_year = dt.datetime.now().year
if dt.datetime.now().month < 7:
    raise TypeError("鬱陶しいのは分かるけどちょっと待って！")  # LOL - json

r = requests.get("https://maclyonsden.com/api/v3/staff")
r.raise_for_status()
data = r.json()
print(len(data))
staffs = defaultdict(set)
for i, entry in enumerate(data):
    print(f"entry {i+1:02d}\t{entry['user']}")
    assert len(entry["roles"]) == 1
    role = entry["roles"][0]
    if role != "Alumnus":
        r2 = requests.get(f"https://maclyonsden.com/api/v3/obj/user/retrieve/{entry['user']}")
        r2.raise_for_status()
        data = r2.json()
        role = "Alumnus" if data["graduating_year"] == current_year else entry["roles"][0]
    staffs[role].add(entry["user"])

staffs = dict(staffs)
print(repr(staffs))
