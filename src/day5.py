from pathlib import Path
from typing import Generator
import re

TEST = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".splitlines()

EXPECTED_1 = "CMZ"
EXPECTED_2 = "MCD"

DATADIR = Path(__file__).parent / "../input"
DATA = (DATADIR / "data5.txt").read_text().splitlines()


def parse(
    data: list[str], cols: int
) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    stacks: list[list[str]] = [[] for _ in range(cols)]
    moves = []
    data = iter(data)
    for line in data:
        if not line:
            break
        for stack, val in zip(stacks, line[1::4]):
            if val != " ":
                stack.insert(0, val)
    for stack in stacks:
        del stack[0]
    for line in data:
        groups = re.match("move (\d+) from (\d+) to (\d+)", line)
        if groups:
            moves.append((int(groups[1]), int(groups[2]), int(groups[3])))
    return stacks, moves


def score_1(data: list[str], cols: int) -> str:
    stacks, moves = parse(data, cols)
    for count, src, dest in moves:
        for i in range(count):
            stacks[dest - 1].append(stacks[src - 1].pop(-1))
    return "".join(stack[-1] for stack in stacks)


test_score = score_1(TEST, 3)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA, 9))


def score_2(data: list[str], cols: int) -> str:
    stacks, moves = parse(data, cols)
    for count, src, dest in moves:
        tmp = stacks[src - 1][-count:]
        stacks[src - 1][-count:] = []
        stacks[dest - 1].extend(tmp)
    return "".join(stack[-1] for stack in stacks)


if EXPECTED_2 is not None:
    test_score = score_2(TEST, 3)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA, 9))
