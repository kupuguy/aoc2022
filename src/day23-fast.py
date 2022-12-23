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


def show(elves: set[complex], sad_elves: set[complex]):
    xmin, xmax = int(min(x.real for x in elves)), int(max(x.real for x in elves))
    ymin, ymax = int(min(x.imag for x in elves)), int(max(x.imag for x in elves))
    for y in range(ymin - 1, ymax + 2):
        print(
            "".join( "*" if x + y * 1j in elves and x + y * 1j  in sad_elves else
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

NEIGHBOURS = {1 - 1j, 1 + 0j, 1 + 1j, -1j, 1j, (-1) - 1j, (-1) + 0j, (-1) + 1j}


def neighbours(elf: complex, elves: set[complex]) -> set[complex]:
    return {elf + n for n in NEIGHBOURS if elf + n in elves}


def move_sad_elves(
    elves: set[complex],
    sad_elves: set[complex],
    directions: list[tuple[complex, complex, complex]],
) -> set[complex]:
    """Move all the sad elves and return a new set of sad elves."""
    consider: dict[complex, int] = defaultdict(int)
    potential: dict[complex, complex] = {}

    for e in sad_elves:
        for a, b, c in directions:
            possible = e + b
            if e+a in elves or possible in elves or e+c in elves:
                continue
            consider[possible] += 1
            potential[e] = possible
            break

    # Move the elves
    minus = []
    plus = []
    for e, possible in potential.items():
        if consider[possible] == 1:
            minus.append(e)
            plus.append(possible)
    m = set(minus)
    p = set(plus)
    elves -= m
    elves |= p
    sad_elves -= m
    sad_elves |= p

    # Now find all the still sad elves: moved ones still with a neighbour and their neighbours
    sad = set()
    for e in sad_elves:
        near = {e + n for n in NEIGHBOURS if e + n in elves}
        if near:
            sad |= near | {e}
    return sad


def score_2(data: list[str]) -> int:
    dir = DIRECTIONS
    elves = parse(data)
    sad_elves = {e for e in elves if neighbours(e, elves)}

    round = 1
    while sad_elves:
        sad_elves = move_sad_elves(elves, sad_elves, dir)
        round += 1
        dir = dir[1:] + dir[:1]
    return round


EXPECTED_2 = 20
if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA))
