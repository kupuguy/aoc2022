SCORES = {
    "AX": 1 + 3,
    "BY": 2 + 3,
    "CZ": 3 + 3,
    "AY": 2 + 6,
    "BZ": 3 + 6,
    "CX": 1 + 6,
    "AZ": 3 + 0,
    "BX": 1 + 0,
    "CY": 2 + 0,
}

test = """A Y
B X
C Z"""


def score(input: list[str], scores: dict[str, int]) -> int:
    score = 0
    for round in input:
        score += scores[round.strip().replace(" ", "")]
    return score


print("test", score(test.split("\n"), SCORES))

from pathlib import Path

print("part 1", score(Path("input/data2.txt").read_text().strip().split("\n"), SCORES))

SCORES2 = {
    "AX": 3 + 0,
    "BY": 2 + 3,
    "CZ": 1 + 6,
    "AY": 1 + 3,
    "BZ": 3 + 6,
    "CX": 2 + 0,
    "AZ": 2 + 6,
    "BX": 1 + 0,
    "CY": 3 + 3,
}
print("test", score(test.split("\n"), SCORES2))

print("part 2", score(Path("input/data2.txt").read_text().strip().split("\n"), SCORES2))
