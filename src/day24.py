from pathlib import Path
from typing import Generator
from dataclasses import dataclass

TEST = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".splitlines()

EXPECTED_1 = 18
EXPECTED_2 = None

DATA = Path("input/data24.txt").read_text().splitlines()


@dataclass(frozen=True, slots=True, eq=True)
class Point2D:
    x: int
    y: int

    def next(self) -> set["Point2D"]:
        return {
            self,
            Point2D(self.x - 1, self.y),
            Point2D(self.x + 1, self.y),
            Point2D(self.x, self.y - 1),
            Point2D(self.x, self.y + 1),
        }


def parse(data: list[str]) -> list[list[str]]:
    rows = [line[1:-1] for line in data[1:-1]]
    return rows


def blocked(
    pos: Point2D, time: int, map: list[list[str]], width: int, height: int
) -> bool:
    x, y = pos.x, pos.y
    if x < 0 or y < 0:
        return not (x == 0 and y == -1)
    if x >= width or y >= height:
        return not (x == width - 1 and y == height)

    return (
        map[y][(x + time) % width] == "<"
        or map[y][(x - time) % width] == ">"
        or map[(y + time) % height][x] == "^"
        or map[(y - time) % height][x] == "v"
    )


def options(
    state: set[Point2D], time: int, map: list[list[str]], width: int, height: int
) -> set[Point2D]:
    new_state = set()
    xmax, ymax = width - 1, height - 1
    for p in state:
        new_state |= {q for q in p.next() if not blocked(q, time, map, width, height)}
    return new_state


def char(
    pos: Point2D, state, time: int, map: list[list[str]], width: int, height: int
) -> bool:
    x, y = pos.x, pos.y
    if x < 0 or y < 0:
        snow = "" if (x == 0 and y == -1) else "#"
    elif x >= width or y >= height:
        snow = "" if (x == width - 1 and y == height) else "#"
    else:
        snow = "".join(
            [
                "<" if map[y][(x + time) % width] == "<" else "",
                ">" if map[y][(x - time) % width] == ">" else "",
                "^" if map[(y + time) % height][x] == "^" else "",
                "v" if map[(y - time) % height][x] == "v" else "",
            ]
        )
    if pos in state:
        return "E" if len(snow) == 0 else "!"

    return "." if len(snow) == 0 else snow[0] if len(snow) == 1 else str(len(snow))


def show(state, time, map, width, height) -> None:
    print("Initial state" if time == 0 else f"Minute {time}")
    for y in range(-1, height + 1):
        print(
            "".join(
                char(Point2D(x, y), state, time, map, width, height)
                for x in range(-1, width + 1)
            )
        )
    print()


def score_1(data: list[str]) -> int:
    map = parse(data)
    width = len(map[0])
    height = len(map)

    start = Point2D(0, -1)
    end = Point2D(width - 1, height)

    state = {start}
    time = 0
    # show(state, time, map, width, height)
    while end not in state:
        time += 1
        state = options(state, time, map, width, height)
        # show(state, time, map, width, height)
    return time


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))

EXPECTED_2 = 54


def score_2(data: list[str]) -> int:
    map = parse(data)
    width = len(map[0])
    height = len(map)

    start = Point2D(0, -1)
    end = Point2D(width - 1, height)

    state = {start}
    time = 0

    while end not in state:
        time += 1
        state = options(state, time, map, width, height)
    state = {end}
    while start not in state:
        time += 1
        state = options(state, time, map, width, height)
    state = {start}
    while end not in state:
        time += 1
        state = options(state, time, map, width, height)
    return time


if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    assert test_score == EXPECTED_2
    print("test", test_score)
    print("part 2", score_2(DATA))
