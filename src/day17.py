from pathlib import Path
from typing import Generator

TEST = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

EXPECTED_1 = 3068
EXPECTED_2 = 1_514_285_714_288

DATA = Path("input/data17.txt").read_text().strip()

rock = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""
rocks = [
    (0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j),
    (1 + 0j, 0 + 1j, 1 + 1j, 2 + 1j, 1 + 2j),
    (0 + 0j, 1 + 0j, 2 + 0j, 2 + 1j, 2 + 2j),
    (0 + 0j, 0 + 1j, 0 + 2j, 0 + 3j),
    (0 + 0j, 1 + 0j, 0 + 1j, 1 + 1j),
]

from itertools import cycle
from typing import Sequence


def drop(
    rock: tuple[complex], height: int, cave: set[complex], moves: Sequence[str]
) -> tuple[set[complex], int, int]:
    """Drop a rock starting at the given height."""
    start_pos = 3 + height * 1j
    rock = {r + start_pos for r in rock}
    # show(cave, height+1, rock)
    for step, lr in enumerate(moves, start=1):
        move = -1 if lr == "<" else 1
        moved_rock = {r + move for r in rock}
        if not (moved_rock & cave):
            rock = moved_rock
        move = -1j  # drop
        moved_rock = {r + move for r in rock}
        if moved_rock & cave:
            # Can't drop so stop there
            cave |= rock
            return cave, int(max(r.imag for r in rock)) + 1, step

        rock = moved_rock
        # show(cave, height, rock)


def show(cave, height, rock=()):
    for h in range(height + 1, -1, -1):
        print(
            "".join(
                "@" if c + h * 1j in rock else "#" if c + h * 1j in cave else "."
                for c in range(0, 9)
            )
        )
    print()


def score_1(data: list[str], limit: int) -> int:
    height = 1
    cave = {n + 0j for n in range(0, 9)}
    # add walls
    cave |= {n * 1j for n in range(height + 8)} | {
        8 + n * 1j for n in range(height + 8)
    }
    nrocks = 0
    move_cycle = cycle(data)
    delta = 0
    delta_rocks = 0
    total_steps = 0

    for nrocks, rock in enumerate(cycle(rocks), start=1):
        cave, new_height, steps = drop(rock, height + 3, cave, move_cycle)
        total_steps += steps

        cave |= {n * 1j for n in range(height + 8, new_height + 8)} | {
            8 + n * 1j for n in range(height + 8, new_height + 8)
        }
        height = max(height, new_height)
        if nrocks == limit:
            return height - 1
        if (nrocks - 1090) % 1710 == 0:  # % 5 == 0 and total_steps % len(data) == 23:
            print(nrocks, nrocks - delta_rocks, height - delta, height)
            delta = height
            delta_rocks = nrocks


test_score = score_1(TEST, 2022)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA, 2022))

print("part 2x", score_1(DATA, 6220))

# Debug prints shows the pattern repeats every 1710 blocks after the first 1090
repeat = 1710
first = 1_000_000_000_000 % repeat
height_after_first = score_1(DATA, first)
height_after_repeat = score_1(DATA, first + repeat)
result = height_after_first + (height_after_repeat - height_after_first) * (
    1_000_000_000_000 // repeat
)
print("part 2", result)
