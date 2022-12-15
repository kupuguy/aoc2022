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


def excluded_at_y(y: int, sx: int, sy: int, dist: int) -> set[int]:
    # print(sx, sy, dist, y, abs(y-sy), dist - abs(y-sy))
    dist -= abs(y - sy)
    if dist > 0:
        return {x for x in range(sx - dist, sx + dist + 1)}
    return set()


def score_1(data: list[str], y: int) -> int:
    excludes: set[int] = set()
    beacons = set()
    for sx, sy, bx, by in parse(data):
        if by == y:
            beacons.add((bx, by))
        dist = abs(sx - bx) + abs(sy - by)
        excl = excluded_at_y(y, sx, sy, dist)
        excludes |= excl

    return len(excludes) - len(beacons)


test_score = score_1(TEST, y=10)
# print("test", test_score)
# assert test_score == EXPECTED_1
# print("part 1", score_1(DATA, y=2000000)) # 5367037


def mdist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def show(p1, r1, p2, r2, maybe=()):
    print(p1, p2)
    p1x, p1y = p1
    p2x, p2y = p2
    lowy = min(p1y - r1, p2y - r2) - 1
    hiy = max(p1y + r1, p2y + r2) + 1
    minx = min(p1x - r1, p2x - r2) - 1
    hix = max(p1x + r1, p2x + r2) + 1
    for y in range(lowy, hiy + 1):
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


def candidates(s1x, s1y, r1, s2x, s2y, r2):
    """Given two sensors that may overlap, find points exactly 1 step out of range
    of both."""
    d = abs(s1x - s2x) + abs(s1y - s2y)
    if s1x > s2x:
        # s1 is equal or left of s2
        s1x, s1y, r1, s2x, s2y, r2 = s2x, s2y, r2, s1x, s1y, r1

    if d > r1 + r2 or d < r1 or d < r2:
        # No useful overlap
        return

    # print(s1x, s1y, r1, s2x, s2y, r2)
    # s2x >= s1x
    rx = r2 - (s2x - s1x)
    w = r1 + rx - abs(s1y - s2y)
    if w > 0 and rx > 0:
        px = s1x - w
        py = s1y - r1 + w if s2y <= s1y else s1y + r1 - w + 1
        # print("A",px,py)
        yield (px, py)
        yield (px, py - 1)

    rx = r1 - (s2x - s1x)
    w = rx + r2 - abs(s1y - s2y)
    if w > 0 and rx > 0:
        px = s2x + w
        py = s2y + rx - w if s2y <= s1y else s2y - rx + w
        # print("B",px,py)
        yield (px, py)
        yield (px, py + 1)

    if s1y >= s2y:
        rx = r2 - (s1y - s2y)
        h = r1 + rx - abs(s1x - s2x)
        if h > 0 and rx > 0:
            py = s1y + h
            px = s1x + r1 - h
            # print("C",px,py)
            yield (px, py)
            yield (px + 1, py)

        rx = r1 - (s1y - s2y)
        h = rx + r2 - abs(s1x - s2x)
        if h > 0 and rx > 0:
            py = s2y - h
            px = s1x + rx - h
            # print("D",px,py)
            yield (px, py)
            yield (px + 1, py)

    if s2y >= s1y:
        rx = r2 - (s2y - s1y)
        h = r1 + rx - abs(s1x - s2x)
        if h > 0 and rx > 0:
            py = s1y - h
            px = s1x + r1 - h
            # print("E",px,py)
            yield (px, py)
            yield (px + 1, py)

        rx = r1 - (s2y - s1y)
        h = rx + r2 - abs(s1x - s2x)
        if h > 0 and rx > 0:
            py = s2y + h
            px = s1x + rx - h
            # print("F",px,py)
            yield (px, py)
            yield (px + 1, py)


def debug(c1, r1, c2, r2):
    maybe = set(candidates(c1[0], c1[1], r1, c2[0], c2[1], r2))
    print(maybe)
    show(c1, r1, c2, r2, maybe)


if 0:
    debug((8, 7), 9, (13, 2), 3)
    debug((8, 7), 3, (13, 2), 9)
    debug((8, 2), 3, (13, 7), 9)
    debug((8, 2), 9, (13, 7), 3)
    # exit()


def cand2(sensor: tuple[int, int], r: int):
    sx, sy = sensor
    r += 1
    for x in range(0, r + 1):
        y = r - x
        yield sx - x, sy - y
        yield sx - x, sy + y
        yield sx + x, sy - y
        yield sx + x, sy + y
    yield sx - r, sy - 1
    yield sx - r, sy + 1
    yield sx + r, sy - 1
    yield sx + r, sy + 1
    yield sx - 1, sy - r
    yield sx + 1, sy - r
    yield sx - 1, sy + r
    yield sx + 1, sy + r


show((0, 0), 2, (0, 0), 2, {})
show((0, 0), 2, (0, 0), 2, set(cand2((0, 0), 2)))
print(sorted(cand2((0, 0), 2)))


def score_2(data: list[str], maxy: int) -> int:
    beacons = set()
    sensors = {}
    maybe = set()
    for sx, sy, bx, by in parse(data):
        beacons.add((bx, by))
        dist = abs(sx - bx) + abs(sy - by)
        sensors[sx, sy] = dist

    for c1, r in sensors.items():
        for x in set(
            cx for cx in cand2(c1, r) if 0 <= cx[0] <= maxy and 0 <= cx[1] <= maxy
        ):
            if all(mdist(x, cx) > rx for cx, rx in sensors.items()):
                print(x)
                return x[0] * 4_000_000 + x[1]
    return "blah!"
    for c1 in sensors:
        r1 = sensors[c1]
        for c2 in sensors:
            r2 = sensors[c2]
            if c1 == c2:
                continue
            for poss in candidates(
                c1[0], c1[1], sensors[c1], c2[0], c2[1], sensors[c2]
            ):
                px, py = poss
                for x in (px - 1, px, px + 1):
                    for y in (py - 1, py, py + 1):
                        if (
                            mdist((x, y), c1) > sensors[c1]
                            and mdist((x, y), c2) > sensors[c2]
                        ):
                            maybe.add(poss)

    # print(sorted(maybe))

    for p in maybe:
        if 0 <= p[0] <= maxy and 0 <= p[1] <= maxy:
            if any(mdist(s, p) <= sensors[s] for s in sensors):
                continue
            print(p)
            return p[0] * 4_000_000 + p[1]

    print("nope")
    count = 0
    return count


EXPECTED_2 = 56000011

if EXPECTED_2 is not None:
    test_score = score_2(TEST, maxy=20)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA, maxy=4_000_000))
