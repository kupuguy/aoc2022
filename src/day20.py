from pathlib import Path
from typing import Generator

TEST = [
    int(n)
    for n in """1
2
-3
3
-2
0
4""".splitlines()
]

EXPECTED_1 = 3
EXPECTED_2 = None

DATA = [int(n) for n in Path("input/data20.txt").read_text().splitlines() if n]


def mix(data: list[int], positions: list[int]) -> list[int]:
    # positions = list(range(len(data)))

    for i in range(len(data)):
        pos = positions.index(i)
        n = data[pos]
        if n == 0:
            continue
        new_pos = (pos + n) % (len(data) - 1)

        if new_pos < pos:
            data = data[:new_pos] + [n] + data[new_pos:pos] + data[pos + 1 :]
            positions = (
                positions[:new_pos]
                + positions[pos : pos + 1]
                + positions[new_pos:pos]
                + positions[pos + 1 :]
            )
        else:
            data = data[:pos] + data[pos + 1 : new_pos + 1] + [n] + data[new_pos + 1 :]
            positions = (
                positions[:pos]
                + positions[pos + 1 : new_pos + 1]
                + positions[pos : pos + 1]
                + positions[new_pos + 1 :]
            )

    return data, positions


def score_1(data: list[int]) -> int:
    positions = list(range(len(data)))
    data, positions = mix(data, positions)
    zero = data.index(0)
    v = [data[(zero + n) % len(data)] for n in (1000, 2000, 3000)]
    print(v)
    return sum(v)


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def score_2(data: list[str]) -> int:
    positions = list(range(len(data)))
    for i in range(10):
        data, positions = mix(data, positions)

    zero = data.index(0)
    v = [data[(zero + n) % len(data)] for n in (1000, 2000, 3000)]
    print(v)
    return sum(v)


key = 811589153
EXPECTED_2 = 1623178306
if EXPECTED_2 is not None:
    TEST = [n * key for n in TEST]
    DATA = [n * key for n in DATA]
    test_score = score_2(TEST)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA))
