from pathlib import Path
from typing import Generator
import re

TEST = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

EXPECTED_1 = 7
EXPECTED_2 = 19

DATA = (Path("input") / "data6.txt").read_text()


def score_1(data: str) -> int:
    for i in range(len(data)):
        if len(set(data[i - 4 : i])) == 4:
            return i
    return 0


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def score_2(data: str) -> int:
    for i in range(len(data)):
        if len(set(data[i - 14 : i])) == 14:
            return i
    return 0


if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA))
