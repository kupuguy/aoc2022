from pathlib import Path
from typing import Generator

TEST = [
    # SNAFU  Decimal
    ("1=-0-2", 1747),
    ("12111", 906),
    ("2=0=", 198),
    ("21", 11),
    ("2=01", 201),
    ("111", 31),
    ("20012", 1257),
    ("112", 32),
    ("1=-1=", 353),
    ("1-12", 107),
    ("12", 7),
    ("1=", 3),
    ("122", 37),
]
EXPECTED_1 = "2=-1=0"

DATA = Path("input/data25.txt").read_text().splitlines()

DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def snafu(s: str) -> int:
    v = 0
    for c in s:
        v = v * 5 + DIGITS[c]
    return v


def snafu_str(v: int) -> str:
    if v == 0:
        return "0"
    digits = []
    while v != 0:
        n = v % 5
        if n <= 2:
            digits.append(str(n))
        elif n == 3:
            digits.append("=")
            v += 5
        else:
            digits.append("-")
            v += 5
        v //= 5

    return "".join(digits[::-1])


def score_1(data: list[str]) -> str:
    total = sum(snafu(d) for d in data)

    return snafu_str(total)


for v, d in TEST:
    assert snafu(v) == d
    assert snafu_str(d) == v

test_score = score_1([v for v, d in TEST])
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))
