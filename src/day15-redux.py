from pathlib import Path
from typing import Generator
import re

TEST = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".splitlines()

EXPECTED_1 = 26
EXPECTED_2 = None

DATA = Path("input/data15.txt").read_text().splitlines()


def parse(data: list[str]) -> Generator[tuple[int, int, int, int], None, None]:
    rows = []
    for line in data:
        if not line:
            continue
        match = re.match(
            "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        # print(line, match.groups())
        sx, sy, bx, by = match.groups()
        yield int(sx), int(sy), int(bx), int(by)


def mdist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def show(p1, r1, p2, r2, maybe=()):
    print(p1, p2)
    p1x, p1y = p1
    p2x, p2y = p2
    lowy = min(0, min(p1y - r1, p2y - r2) - 1)
    hiy = max(p1y + r1, p2y + r2) + 1
    minx = min(0, min(p1x - r1, p2x - r2) - 1)
    hix = max(p1x + r1, p2x + r2) + 1
    for y in range(hiy + 2, lowy - 1, -1):
        print(
            "".join(
                "X"
                if (x, y) in maybe
                else "S"
                if (x, y) in {p1, p2}
                else "#"
                if mdist(p1, (x, y)) <= r1 or mdist(p2, (x, y)) <= r2
                else "."
                for x in range(minx, hix + 1)
            )
        )


def intersect_diagonals(m: int, b: int, n: int, c: int) -> tuple[int, int]:
    """Intersect two diagonals.
    {m,n} = {1,-1}
    switch if needed so m=1
        x+b = -x+c => 2x = c-b, 2y = 2x+2b
    Returns coordinates doubles to keep them int.
    """
    if m == -1:
        b, c = c, b
    two_x = c - b
    two_y = two_x + 2 * b
    return (two_x, two_y)


def candidates(
    px: int, py: int, pr: int, qx: int, qy: int, qr: int, limit: int = 4_000_000
):
    """Given two sensors that may overlap, find points exactly 1 step out of range
    of both.
    Each sensor has 4 edges:
    A: y = x + py - (px - pr - 1),
    B: y = -x + py + (px + pr + 1)
    C: y = x + py - (px + pr + 1)
    D: y = -x + py + (px - pr - 1)

    Find all the intersections. If not exact integers use the surrounding points
    """
    p_edges = [
        (1, py - (px - pr - 1)),
        (-1, py + (px + pr + 1)),
        (1, py - (px + pr + 1)),
        (-1, py + (px - pr - 1)),
    ]
    q_edges = [
        (1, qy - (qx - qr - 1)),
        (-1, qy + (qx + qr + 1)),
        (1, qy - (qx + qr + 1)),
        (-1, qy + (qx - qr - 1)),
    ]

    candidates = {
        intersect_diagonals(m, b, n, c)
        for m, b in p_edges
        for n, c in q_edges
        if m != n
    }

    # divide coords by 2. When not an int replace with surrounding points.
    c2 = []
    for two_x, two_y in candidates:
        c2.extend(
            [
                (x, y)
                for x in {two_x // 2, (two_x + 1) // 2}
                for y in {two_y // 2, (two_y + 1) // 2}
            ]
        )

    # Only keep candidates within the bounding boxes
    candidates = [
        (x, y)
        for x, y in c2
        if px - pr - 1 <= x <= px + pr + 1
        and py - pr - 1 <= y <= py + pr + 1
        and qx - qr - 1 <= x <= qx + qr + 1
        and qy - qr - 1 <= y <= qy + qr + 1
        and 0 <= x <= limit
        and 0 <= y <= limit
    ]

    # filter out points in range introduced by division
    candidates = [
        xy for xy in candidates if mdist(xy, (px, py)) > pr and mdist(xy, (qx, qy)) > qr
    ]

    return candidates


def debug(c1, r1, c2, r2):
    maybe = set(candidates(c1[0], c1[1], r1, c2[0], c2[1], r2))
    print(maybe)
    show(c1, r1, c2, r2, maybe)


if 0:
    debug((8, 7), 9, (13, 2), 3)
    debug((8, 7), 3, (13, 2), 9)
    debug((8, 2), 3, (13, 7), 9)
    debug((8, 2), 9, (13, 7), 3)
    debug((8, 6), 9, (13, 2), 3)
    debug((8, 6), 3, (13, 2), 9)
    debug((8, 2), 3, (13, 6), 9)
    debug((8, 2), 9, (13, 6), 3)


def score_2(data: list[str], maxy: int) -> int:
    beacons = set()
    sensors = {}
    maybe = set()
    for sx, sy, bx, by in parse(data):
        beacons.add((bx, by))
        dist = abs(sx - bx) + abs(sy - by)
        sensors[sx, sy] = dist

    maybe = []
    for c1, pr in sensors.items():
        px, py = c1
        for c2, qr in sensors.items():
            if c2 <= c1:
                continue
            qx, qy = c2
            maybe.extend(candidates(px, py, pr, qx, qy, qr, maxy))

    print(f"{len(sensors)} sensors, {len(maybe)} candidates")

    for p in maybe:
        if all(mdist(p, s) > r for s, r in sensors.items()):
            print("Found position", p)
            return p[0] * 4_000_000 + p[1]
    raise RuntimeError("blah!")


EXPECTED_2 = 56000011

if EXPECTED_2 is not None:
    test_score = score_2(TEST, maxy=20)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA, maxy=4_000_000))
