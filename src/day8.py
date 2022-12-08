from pathlib import Path
from typing import Generator

TEST = """30373
25512
65332
33549
35390""".splitlines()

EXPECTED_1 = 21
EXPECTED_2 = 8

DATADIR = Path(__file__).parent / "../input"
DATA = (DATADIR / "data8.txt").read_text().splitlines()


def can_see(row: str) -> Generator[int, None, None]:
    nearest = 9999999
    count = 0
    for height in "9876543210":
        pos = row.find(height)
        if pos >= 0 and pos < nearest:
            yield pos
            nearest = pos


def score_1(data: list[str]) -> int:
    rows = len(data)
    cols = len(data[0])
    visible = [[0] * cols for i in range(rows)]

    for index, row in enumerate(data):
        for seen in can_see(row):
            visible[index][seen] = 1
        for seen in can_see(row[::-1]):
            visible[index][len(row) - seen - 1] = 1

    grid = "".join(data)
    columns = [grid[col::cols] for col in range(cols)]
    for index, row in enumerate(columns):
        for seen in can_see(row):
            visible[seen][index] = 1
        for seen in can_see(row[::-1]):
            visible[len(row) - seen - 1][index] = 1

    return sum(sum(v) for v in visible)


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def scenic_score(tree: str, view: str) -> int:
    nearest = len(view)
    blockers = "9876543210"[: 10 - int(tree)]
    for height in blockers:
        pos = view.find(height)
        if pos >= 0 and pos < nearest:
            nearest = pos + 1
    return nearest


def score_2(data: list[str]) -> int:
    rows = len(data)
    cols = len(data[0])
    grid = "".join(data)
    columns = [grid[col::cols] for col in range(cols)]

    best = 0
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            views = (
                data[row][:col][::-1],
                data[row][col + 1 :],
                columns[col][:row][::-1],
                columns[col][row + 1 :],
            )
            scores = [scenic_score(data[row][col], view) for view in views]
            score = scores[0] * scores[1] * scores[2] * scores[3]
            if score > best:
                best = score
    return best


if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    assert test_score == EXPECTED_2
    print("test", test_score)
    print("part 2", score_2(DATA))
