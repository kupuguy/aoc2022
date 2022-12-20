from pathlib import Path
from typing import Generator

TEST = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".splitlines()

EXPECTED_1 = 64
EXPECTED_2 = None

DATA = Path("input/data18.txt").read_text().splitlines()


def parse(data: list[str]) -> list[tuple[int, int, int]]:
    rows = [
        tuple(int(n) for n in line.strip().split(",")) for line in data if line.strip()
    ]
    return rows


def score_1(data: list[str]) -> int:
    cubes = set(p for p in parse(data))

    common = 0
    for a, b, c in cubes:
        if (a + 1, b, c) in cubes:
            common += 1
        if (a, b + 1, c) in cubes:
            common += 1
        if (a, b, c + 1) in cubes:
            common += 1

    return 6 * len(cubes) - 2 * common


assert score_1("1,1,1\n2,1,1".splitlines()) == 10

test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))

EXPECTED_2 = 58

from collections import deque


def score_2(data: list[str]) -> int:
    cubes = set(p for p in parse(data))
    min_a, max_a, min_b, max_b, min_c, max_c = (
        min(a for a, b, c in cubes) - 1,
        max(a for a, b, c in cubes) + 1,
        min(b for a, b, c in cubes) - 1,
        max(b for a, b, c in cubes) + 1,
        min(c for a, b, c in cubes) - 1,
        max(c for a, b, c in cubes) + 1,
    )
    # print(min_a, max_a, min_b, max_b, min_c, max_c)
    queue = deque([(max_a, max_b, max_c)])
    outside = {(max_a, max_b, max_c)}
    while queue:
        a, b, c = queue.popleft()
        for q in [
            (a + 1, b, c),
            (a - 1, b, c),
            (a, b + 1, c),
            (a, b - 1, c),
            (a, b, c + 1),
            (a, b, c - 1),
        ]:
            d, e, f = q
            if (
                q not in outside
                and q not in cubes
                and min_a <= d <= max_a
                and min_b <= e <= max_b
                and min_c <= f <= max_c
            ):
                outside.add(q)
                queue.append(q)

    faces = 0
    for a, b, c in cubes:
        if (a + 1, b, c) in outside:
            faces += 1
        if (a, b + 1, c) in outside:
            faces += 1
        if (a, b, c + 1) in outside:
            faces += 1
        if (a - 1, b, c) in outside:
            faces += 1
        if (a, b - 1, c) in outside:
            faces += 1
        if (a, b, c - 1) in outside:
            faces += 1

    return faces


if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA))
