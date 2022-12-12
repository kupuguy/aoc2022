from collections import deque
from pathlib import Path

TEST = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".splitlines()

EXPECTED_1 = 31
EXPECTED_2 = 29

DATADIR = Path(__file__).parent / "../input"
DATA = (DATADIR / "data12.txt").read_text().splitlines()


def parse(data: list[str]) -> tuple[list[list[int]], complex, complex, int, int]:
    rows = [
        [0 if c == "S" else 25 if c == "E" else ord(c) - ord("a") for c in row]
        for row in data
    ]
    for y, row in enumerate(data):
        if "S" in row:
            start = row.find("S") + y * 1j
        if "E" in row:
            end = row.find("E") + y * 1j
    # print(f"start {start}, end {end}")

    return rows, start, end, len(row), len(data)


def neighbours(pos: complex, width: int, height: int):
    if pos.real >= 0:
        yield pos - 1
    if pos.real < width - 1:
        yield pos + 1
    if pos.imag >= 0:
        yield pos - 1j
    if pos.imag < height - 1:
        yield pos + 1j


def score_1(data: list[str]) -> int:
    grid, start, end, width, height = parse(data)
    steps = {start: 0}
    queue = deque([start])
    while end not in steps and queue:
        pos = queue.popleft()
        h = grid[int(pos.imag)][int(pos.real)]
        count = steps[pos] + 1
        for nxt in neighbours(pos, width, height):
            nh = grid[int(nxt.imag)][int(nxt.real)]
            if nxt not in steps and nh - h <= 1:
                steps[nxt] = count
                queue.append(nxt)

    return steps[end]


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def score_2(data: list[str]) -> int:
    grid, start, end, width, height = parse(data)
    steps = {end: 0}
    queue = deque([end])
    while queue:
        pos = queue.popleft()
        h = grid[int(pos.imag)][int(pos.real)]

        count = steps[pos] + 1
        for nxt in neighbours(pos, width, height):
            nh = grid[int(nxt.imag)][int(nxt.real)]

            if nxt not in steps and h - nh <= 1:
                if nh == 0:
                    return count
                steps[nxt] = count
                queue.append(nxt)

    return steps[start]


if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA))
