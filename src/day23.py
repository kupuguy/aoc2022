from pathlib import Path
from typing import Generator
from collections import defaultdict

TEST = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..""".splitlines()

EXPECTED_1 = 110
EXPECTED_2 = None

DATA = Path("input/data23.txt").read_text().splitlines()


def parse(data: list[str]) -> set[complex]:
    elves = set()
    for y, line in enumerate(data):
        for x, e in enumerate(line):
            if e == "#":
                elves.add(x + y * 1j)
    return elves


def move(
    elves: set[complex], directions: list[tuple[complex, complex, complex]]
) -> set[complex]:
    consider: dict[complex, int] = defaultdict(int)

    for e in elves:
        neighbours = {e + z for d in directions for z in d}
        if not (neighbours & elves):
            continue
        for a, b, c in directions:
            if not ({e + a, e + b, e + c} & elves):
                consider[e + b] += 1
                break

    new_elves = set()
    for e in elves:
        new_pos = e
        neighbours = {e + z for d in directions for z in d}
        if neighbours & elves:
            # must move
            for a, b, c in directions:
                if not ({e + a, e + b, e + c} & elves):
                    if consider[e + b] == 1:
                        new_pos = e + b
                    break
        new_elves.add(new_pos)
    return new_elves


def show(elves):
    xmin, xmax = int(min(x.real for x in elves)), int(max(x.real for x in elves))
    ymin, ymax = int(min(x.imag for x in elves)), int(max(x.imag for x in elves))
    for y in range(ymin - 1, ymax + 2):
        print(
            "".join(
                "#" if x + y * 1j in elves else "." for x in range(xmin - 1, xmax + 2)
            )
        )
    print()


DIRECTIONS = [
    (-1 - 1j, 0 - 1j, 1 - 1j),
    (-1 + 1j, 0 + 1j, 1 + 1j),
    (-1 - 1j, -1 + 0j, -1 + 1j),
    (1 - 1j, 1 + 0j, 1 + 1j),
]


def score_1(data: list[str]) -> int:
    dir = DIRECTIONS
    elves = parse(data)
    # show(elves)
    n_elves = len(elves)
    for round in range(10):
        new_elves = move(elves, dir)
        if elves == new_elves:
            break
        elves = new_elves
        # show(elves)
        dir = dir[1:] + dir[:1]
        assert len(elves) == n_elves

    xmin, xmax = int(min(x.real for x in elves)), int(max(x.real for x in elves))
    ymin, ymax = int(min(x.imag for x in elves)), int(max(x.imag for x in elves))
    area = (xmax + 1 - xmin) * (ymax + 1 - ymin)
    return area - n_elves


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def score_2(data: list[str]) -> int:
    dir = DIRECTIONS
    elves = parse(data)
    n_elves = len(elves)
    round = 1
    while True:
        new_elves = move(elves, dir)
        if elves == new_elves:
            return round

        elves = new_elves
        round += 1
        dir = dir[1:] + dir[:1]
        assert len(elves) == n_elves


EXPECTED_2 = 20
if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    assert test_score == EXPECTED_2
    print("test", test_score)
    print("part 2", score_2(DATA))
