from pathlib import Path
from typing import Generator

TEST = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".splitlines()

EXPECTED_1 = 13
EXPECTED_2 = 140

DATA = Path("input/data13.txt").read_text().splitlines()


def parse(data: list[str]) -> Generator[tuple[list, list], None, None]:
    rows = []
    for left, right in zip(data[::3], data[1::3]):
        yield eval(left), eval(right)


def in_right_order(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return right - left
    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            cmp = in_right_order(l, r)
            if cmp != 0:
                return cmp
        return len(right) - len(left)
    if isinstance(left, int):
        return in_right_order([left], right)
    if isinstance(right, int):
        return in_right_order(left, [right])


def score_1(data: list[str]) -> int:
    correct = sum(
        index
        for index, (left, right) in enumerate(parse(data), start=1)
        if in_right_order(left, right) >= 0
    )
    return correct


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))

from functools import cmp_to_key

keyfn = cmp_to_key(in_right_order)


def score_2(data: list[str]) -> int:
    packets = sorted(
        [eval(d) for d in data if d] + [[[2]], [[6]]], key=keyfn, reverse=True
    )
    start = packets.index([[2]]) + 1
    end = packets.index([[6]]) + 1
    return start * end


if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    assert test_score == EXPECTED_2
    print("test", test_score)
    print("part 2", score_2(DATA))
