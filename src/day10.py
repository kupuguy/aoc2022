from pathlib import Path
from typing import Generator

TEST = Path("input/test10.txt").read_text().splitlines()

EXPECTED_1 = 13140

DATA = Path("input/data10.txt").read_text().splitlines()


def parse(data: list[str]) -> Generator[int, None, None]:
    x = 1
    yield x
    for line in data:
        if line == "noop":
            yield x
        elif line.startswith("addx"):
            yield x
            x += int(line.split()[1])
            yield x


def score_1(data: list[str]) -> int:
    total = sum(
        cycle * x
        for cycle, x in enumerate(parse(data), start=1)
        if cycle in {20, 60, 100, 140, 180, 220}
    )
    return total


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def score_2(data: list[str]) -> str:
    screen = [" "] * 240
    for cycle, x in enumerate(parse(data), start=0):
        if cycle >= len(screen):
            break
        if x - 1 <= cycle % 40 <= x + 1:
            screen[cycle] = "\u2588"

    return "\n".join("".join(screen[n : n + 40]) for n in (0, 40, 80, 120, 160, 200))


print(score_2(TEST))
print()
print(score_2(DATA))
