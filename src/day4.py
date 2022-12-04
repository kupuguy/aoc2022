from pathlib import Path

TEST = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".split(
    "\n"
)

DATA = Path("input/data4.txt").read_text().split("\n")


def parse(data: list[str]) -> list[tuple[set, set]]:
    rows = []
    for line in data:
        if not line:
            continue
        a, b = line.split(",")
        a1, a2 = a.split("-")
        b1, b2 = b.split("-")
        rows.append(
            (set(range(int(a1), int(a2) + 1)), set(range(int(b1), int(b2) + 1)))
        )
    return rows


def score_1(data: list[str]) -> int:
    count = 0
    for a, b in parse(data):
        if (a & b) == a or (a & b) == b:
            count += 1
    return count


print("test", score_1(TEST))
print("part 1", score_1(DATA))


def score_2(data: list[str]) -> int:
    count = 0
    for a, b in parse(data):
        if (a & b) != set():
            count += 1
    return count


print("test", score_2(TEST))
print("part 2", score_2(DATA))
