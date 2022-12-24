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


def parse(data: list[str]) -> list[list[str]]:
    rows = [line[1:-1] for line in data[1:-1]]
    return rows


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


@dataclass
class Worker:
    map: list[list[str]]
    width: int
    height: int
    time: int = 0

    def blocked(self, pos: Point2D) -> bool:
        x, y = pos.x, pos.y
        map, time, width, height = self.map, self.time, self.width, self.height
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
        self,
        state: set[Point2D],
    ) -> set[Point2D]:
        self.time += 1
        return {q for p in state for q in p.next() if not self.blocked(q)}

    def char(
        self,
        pos: Point2D,
        state,
    ) -> bool:
        x, y = pos.x, pos.y
        if x < 0 or y < 0:
            snow = "" if (x == 0 and y == -1) else "#"
        elif x >= self.width or y >= self.height:
            snow = "" if (x == self.width - 1 and y == self.height) else "#"
        else:
            map, time, width, height = self.map, self.time, self.width, self.height
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

    def show(self, state) -> None:
        print("Initial state" if self.time == 0 else f"Minute {self.time}")
        for y in range(-1, self.height + 1):
            print(
                "".join(
                    self.char(
                        Point2D(x, y),
                        state,
                    )
                    for x in range(-1, self.width + 1)
                )
            )
        print()


def score_1(data: list[str], debug: bool = False) -> int:
    map = parse(data)
    width = len(map[0])
    height = len(map)

    start = Point2D(0, -1)
    end = Point2D(width - 1, height)

    state = {start}
    worker = Worker(map, width, height)
    if debug:
        worker.show(state)
    while end not in state:
        state = worker.options(state)
        if debug:
            worker.show(state)
    return worker.time


test_score = score_1(TEST, debug=True)
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
    worker = Worker(map, width, height)

    while end not in state:
        state = worker.options(state)
    state = {end}
    while start not in state:
        state = worker.options(state)
    state = {start}
    while end not in state:
        state = worker.options(state)
    return worker.time


if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    assert test_score == EXPECTED_2
    print("test", test_score)
    print("part 2", score_2(DATA))
