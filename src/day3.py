from pathlib import Path

TEST_DATA = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def score(line: str) -> int:
    # print(line, len(line))
    a, b = line[: len(line) // 2], line[len(line) // 2 :]
    common = set(a) & set(b)
    assert len(common) == 1
    value = list(common)[0]
    if "A" <= value <= "Z":
        return ord(value) - ord("A") + 27
    return ord(value) - ord("a") + 1


def process_1(data: str) -> int:
    lines = data.strip().split()
    return sum(score(line) for line in lines)


assert process_1(TEST_DATA) == 157

print("Part 1", process_1(Path("input/data3.txt").read_text()))


def score2(group: tuple) -> int:
    a, b, c = group
    common = set(a) & set(b) & set(c)
    assert len(common) == 1

    value = list(common)[0]
    if "A" <= value <= "Z":
        return ord(value) - ord("A") + 27
    return ord(value) - ord("a") + 1


def process_2(data: str) -> int:
    lines = data.strip().split()
    groups = [
        (lines[r + 0], lines[r + 1], lines[r + 2]) for r in range(0, len(lines), 3)
    ]
    return sum(score2(group) for group in groups)


assert process_2(TEST_DATA) == 70
print("Part 2", process_2(Path("input/data3.txt").read_text()))
