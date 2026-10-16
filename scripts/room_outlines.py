"""
Traces room outlines from the floor plan images so the map can highlight whole rooms.

For every room point in customData (core/static/core/js/map/map.js), flood-fills the room's
colour on FloorOne.jpg / FloorTwo.jpg starting at that point, and writes the rectangle around the
filled area (in lng/lat) to core/static/core/js/map/room-outlines.js. Rectangles are aligned to
the building's grid angle so every outline has 90 degree corners and lines up with its neighbours.
Rooms that aren't rectangles get hand-placed corners in MANUAL_OUTLINES, snapped to the same grid.

Re-run after changing the floor plan images or room points. Needs numpy, scipy and pillow:
    python scripts/room_outlines.py
"""

import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import ConvexHull

ROOT = Path(__file__).resolve().parent.parent
MAP_JS = ROOT / "core/static/core/js/map/map.js"
OUTPUT = ROOT / "core/static/core/js/map/room-outlines.js"
IMAGES = {
    1: ROOT / "core/static/core/img/FloorOne.jpg",
    2: ROOT / "core/static/core/img/FloorTwo.jpg",
}
# corners of the floor plan image sources in map.js
WEST, EAST = -79.46270547634776, -79.46072668772469
NORTH, SOUTH = 43.75413886166868, 43.75274955916902

SKIP_PREFIXES = ("Exit", "Booth", "Stage")
COLOUR_TOLERANCE = 40  # JPEG noise
DOOR_GAP = 41  # px; wider than any doorway gap in the walls
CROP = 1400  # px
# rooms whose label text splits the fill once eroded; they have no doorway leaks
DOOR_GAP_OVERRIDES = {"dance studio (144)": 1}
# rooms open to a larger space, so there is no fill to trace: corners in image px
# Corners are approximate: edges must alternate along/across the building grid, and get snapped
# to it so every corner is 90 degrees.
MANUAL_OUTLINES = {
    # the washrooms in its north-east corner make a notch
    (1, "large gym (127)"): [
        (2467, 1789),
        (3357, 1653),
        (3435, 2153),
        (3463, 2149),
        (3536, 2757),
        (2637, 2900),
    ],
    # L-shaped: the main room plus the section running up beside the small gym
    (1, "fitness room (124c)"): [
        (1665, 2780),
        (1890, 2740),
        (1888, 2555),
        (2162, 2515),
        (2185, 2680),
        (2085, 2702),
        (2105, 2998),
        (1700, 3050),
    ],
}
# The library and Library A/B share walls, so they are built from one set of measured walls
# (two image px points along each) to make shared edges line up exactly.
LIBRARY_WALLS = {
    # across the grid (u = constant)
    "student_services": [(4813, 3083), (4725, 2433)],  # student services' east wall
    "staff_room": [
        (5008, 2417),
        (5033, 2575),
    ],  # staff room's west wall, beside the library's entrance
    "library_ab": [(4992, 2675), (5075, 3200)],  # Library A/B's west wall
    "east": [(5363, 2850), (5517, 3750)],  # outside wall
    "west": [(4592, 3300), (4683, 3983)],  # wall by rooms 108a/b
    # along the grid (v = constant)
    "hallway": [(4725, 2437), (4858, 2420)],  # top of the entrance from the hallway
    "staff_room_bottom": [(4980, 2603), (5317, 2553)],  # top of Library A
    "divider": [(5033, 2905), (5367, 2862)],  # between Library A and B
    "library_b_bottom": [(5080, 3197), (5413, 3150)],
    "bottom": [(4700, 3992), (5525, 3875)],
    "student_services_bottom": [(4583, 3292), (4700, 3262)],
}
LIBRARY_ROOMS = ("library (134)", "Library A", "Library B")
# student services' cut corner: a 45 degree wall between these two points
LIBRARY_CHAMFER = [(4700, 3262), (4805, 3108)]


def library_outlines(angle: float) -> dict:
    rot = rotation(angle)

    def to_grid(p):
        return np.array(p, dtype=float) @ rot.T

    u = {k: np.mean([to_grid(p)[0] for p in pts]) for k, pts in LIBRARY_WALLS.items()}
    v = {k: np.mean([to_grid(p)[1] for p in pts]) for k, pts in LIBRARY_WALLS.items()}
    # the chamfer runs up and to the right at 45 degrees: u + v is constant along it
    c = np.mean([to_grid(p).sum() for p in LIBRARY_CHAMFER])
    lib_a = [
        (u["library_ab"], v["staff_room_bottom"]),
        (u["east"], v["staff_room_bottom"]),
        (u["east"], v["divider"]),
        (u["library_ab"], v["divider"]),
    ]
    lib_b = [
        (u["library_ab"], v["divider"]),
        (u["east"], v["divider"]),
        (u["east"], v["library_b_bottom"]),
        (u["library_ab"], v["library_b_bottom"]),
    ]
    library = [
        (u["student_services"], v["hallway"]),
        (u["staff_room"], v["hallway"]),
        (u["staff_room"], v["staff_room_bottom"]),
        (u["library_ab"], v["staff_room_bottom"]),
        (u["library_ab"], v["library_b_bottom"]),
        (u["east"], v["library_b_bottom"]),
        (u["east"], v["bottom"]),
        (u["west"], v["bottom"]),
        (u["west"], v["student_services_bottom"]),
        (c - v["student_services_bottom"], v["student_services_bottom"]),
        (u["student_services"], c - u["student_services"]),
    ]

    def back(ring):
        return [(float(x), float(y)) for x, y in np.array(ring) @ rot]

    return {
        "library (134)": back(library),
        "Library A": back(lib_a),
        "Library B": back(lib_b),
    }


# separate buildings, not on the main building's grid
OWN_ANGLE_PREFIXES = ("Portable",)
SEED_WINDOW = 60  # px around the point used to find the room's fill colour
MIN_ROOM_PX = 1000  # smallest fill counted as a room; letter holes are a few hundred px


def merc_y(lat: float) -> float:
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def inv_merc_y(y: float) -> float:
    return math.degrees(2 * math.atan(math.exp(y)) - math.pi / 2)


def load_rooms() -> list[dict]:
    """Reads the room points out of the customData object literal in map.js."""
    src = MAP_JS.read_text()
    block = src[
        src.index("const customData = ") : src.index("// map.dragRotate.disable();")
    ]
    rooms = []
    for feature in re.split(r'type: "Feature",', block)[1:]:
        title = re.search(r"title:\s*[\"']([^\"']+)[\"']", feature).group(1)
        floor = int(re.search(r"floor:\s*(\d)", feature).group(1))
        lng, lat = map(
            float,
            re.search(r"coordinates:\s*\[([-\d.]+),\s*([-\d.]+)\]", feature).groups(),
        )
        if not title.startswith(SKIP_PREFIXES):
            rooms.append({"title": title, "floor": floor, "lng": lng, "lat": lat})
    return rooms


def trace(img: np.ndarray, x: int, y: int, door_gap: int) -> np.ndarray | None:
    """Image px of the room's fill around (x, y)."""
    h, w, _ = img.shape
    win = img[
        max(0, y - SEED_WINDOW) : y + SEED_WINDOW,
        max(0, x - SEED_WINDOW) : x + SEED_WINDOW,
    ]
    pixels = win.reshape(-1, 3).astype(int)
    pixels = pixels[pixels.sum(axis=1) > 150]  # ignore walls and text
    quantized, counts = np.unique(pixels // 8, axis=0, return_counts=True)
    colour = quantized[np.argmax(counts)] * 8 + 4

    # work in a crop around the point; the biggest rooms (gyms) are ~1100px across
    x0, y0 = max(0, x - CROP), max(0, y - CROP)
    crop = img[y0 : y + CROP, x0 : x + CROP]
    x, y = x - x0, y - y0
    mask = np.abs(crop.astype(int) - colour).max(axis=2) < COLOUR_TOLERANCE
    # shrink the fill so doorways no longer connect neighbouring rooms, then grow it back
    eroded = ndimage.minimum_filter(mask.astype(np.uint8), size=door_gap).astype(bool)
    labels, _ = ndimage.label(eroded)
    # ignore specks such as the holes inside letters (the point may sit on a label's text)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    eroded = sizes[labels] >= MIN_ROOM_PX
    # component nearest to the point
    ys, xs = np.nonzero(eroded)
    if len(xs) == 0:
        return None
    nearest = np.argmin((xs - x) ** 2 + (ys - y) ** 2)
    if (xs[nearest] - x) ** 2 + (ys[nearest] - y) ** 2 > SEED_WINDOW**2 * 4:
        return None
    region = labels == labels[ys[nearest], xs[nearest]]
    region = (
        ndimage.maximum_filter(region.astype(np.uint8), size=door_gap).astype(bool)
        & mask
    )

    ry, rx = np.nonzero(region)
    points = np.column_stack([rx + x0, ry + y0]).astype(float)
    return points[ConvexHull(points).vertices]


def rotation(angle: float) -> np.ndarray:
    """Rotates image px by -angle, so edges at `angle` become axis-aligned."""
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, s], [-s, c]])


def rect_at_angle(hull: np.ndarray, angle: float) -> tuple[list, float]:
    """Rectangle around the points with its sides at `angle` (radians)."""
    rot = rotation(angle)
    r = hull @ rot.T
    (minx, miny), (maxx, maxy) = r.min(axis=0), r.max(axis=0)
    box = np.array([[minx, miny], [maxx, miny], [maxx, maxy], [minx, maxy]]) @ rot
    return [(float(x), float(y)) for x, y in box], (maxx - minx) * (maxy - miny)


def min_area_angle(hull: np.ndarray) -> float:
    """Angle (radians, within +-45 degrees) of the smallest rectangle around the points."""
    best = None
    for i in range(len(hull)):
        edge = hull[(i + 1) % len(hull)] - hull[i]
        angle = math.atan2(edge[1], edge[0])
        angle = (angle + math.pi / 4) % (math.pi / 2) - math.pi / 4
        _, area = rect_at_angle(hull, angle)
        if best is None or area < best[0]:
            best = (area, angle)
    return best[1]


def snap_to_grid(corners: list, angle: float) -> list:
    """Makes a hand-placed outline rectilinear on the grid at `angle`: every corner 90 degrees.
    Each edge becomes exactly along or across the grid, at the average of its two ends."""
    rot = rotation(angle)
    r = np.array(corners, dtype=float) @ rot.T
    n = len(r)
    horizontal = [
        abs(r[(i + 1) % n][0] - r[i][0]) > abs(r[(i + 1) % n][1] - r[i][1])
        for i in range(n)
    ]
    for i in range(n):
        if horizontal[i] == horizontal[i - 1]:
            raise ValueError(
                f"edges {i - 1} and {i} both run the same way; add or remove a corner"
            )
    snapped = []
    for i in range(n):
        # corner i joins edge i-1 and edge i: one gives its x, the other its y
        x_edge, y_edge = (i, i - 1) if horizontal[i - 1] else (i - 1, i)
        x = (r[x_edge][0] + r[(x_edge + 1) % n][0]) / 2
        y = (r[y_edge][1] + r[(y_edge + 1) % n][1]) / 2
        snapped.append((x, y))
    return [(float(x), float(y)) for x, y in np.array(snapped) @ rot]


def main() -> None:
    top, bottom = merc_y(NORTH), merc_y(SOUTH)
    outlines = {}
    for floor, path in IMAGES.items():
        Image.MAX_IMAGE_PIXELS = None
        img = np.asarray(Image.open(path).convert("RGB"))
        h, w, _ = img.shape

        hulls = {}
        for room in (r for r in load_rooms() if r["floor"] == floor):
            if (floor, room["title"]) in MANUAL_OUTLINES or (
                floor == 1 and room["title"] in LIBRARY_ROOMS
            ):
                continue
            x = round((room["lng"] - WEST) / (EAST - WEST) * w)
            y = round((top - merc_y(room["lat"])) / (top - bottom) * h)
            door_gap = DOOR_GAP_OVERRIDES.get(room["title"], DOOR_GAP)
            if room["title"].startswith(OWN_ANGLE_PREFIXES):
                door_gap = 1  # free-standing, so no doorways to close; eroding would split the label
            hull = trace(img, x, y, door_gap)
            if hull is None:
                print(f"skipped {room['title']}: no fill found")
            else:
                hulls[room["title"]] = hull

        # every room shares the building's grid angle, measured from the classrooms
        grid = float(
            np.median(
                [min_area_angle(hulls[t]) for t in hulls if t.startswith("Room ")]
            )
        )
        print(f"floor {floor}: building grid at {math.degrees(grid):.2f} degrees")

        rings = {}
        for title, hull in hulls.items():
            angle = (
                min_area_angle(hull) if title.startswith(OWN_ANGLE_PREFIXES) else grid
            )
            rings[title], _ = rect_at_angle(hull, angle)
        for (manual_floor, title), corners in MANUAL_OUTLINES.items():
            if manual_floor == floor:
                rings[title] = snap_to_grid(corners, grid)
        if floor == 1:
            rings.update(library_outlines(grid))

        for title, ring in rings.items():
            outlines[title] = [
                [
                    round(WEST + px / w * (EAST - WEST), 8),
                    round(inv_merc_y(top - py / h * (top - bottom)), 8),
                ]
                for px, py in ring + [ring[0]]
            ]

    OUTPUT.write_text(
        "// Generated by scripts/room_outlines.py: room title -> outline polygon ring [lng, lat].\n"
        f"const ROOM_OUTLINES = {json.dumps(outlines, indent=1)};\n"
    )


if __name__ == "__main__":
    main()
