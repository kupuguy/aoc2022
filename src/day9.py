from pathlib import Path
from typing import Generator

TEST = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".splitlines()

EXPECTED_1 = 13
EXPECTED_2 = 1

DATADIR = Path(__file__).parent / "../input"
DATA = (DATADIR / "data9.txt").read_text().splitlines()

DIRECTIONS = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}


def parse(data: list[str]) -> Generator[tuple[int, int], None, None]:
    rows = []
    for line in data:
        if not line:
            continue
        direction, number = line.split()

        for i in range(int(number)):
            yield DIRECTIONS[direction] + (direction,)


# def show(h, t, width=5, height=5):
#    for r in range(height, -1, -1):
#        for c in range(0, width):
#            print(
#                ("H"
#                if h[0] == c and h[1] == r
#                else "T"
#                if t[0] == c and t[1] == r
#                else "."),
#                sep="",
#                end="",
#            )
#        print()
#    print()


def score_1(data: list[str]) -> int:
    visited = {(0, 0)}
    hx, hy, tx, ty = 0, 0, 0, 0
    for xd, yd, instr in parse(data):
        hx += xd
        hy += yd
        if abs(hx - tx) > 1 or abs(hy - ty) > 1:
            if hx > tx:
                tx += 1
            elif hx < tx:
                tx -= 1
            if hy > ty:
                ty += 1
            elif hy < ty:
                ty -= 1
        visited.add((tx, ty))
    return len(visited)


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def move(head, tail):
    hx, hy = head
    tx, ty = tail
    if abs(hx - tx) > 1 or abs(hy - ty) > 1:
        if hx > tx:
            tx += 1
        elif hx < tx:
            tx -= 1
        if hy > ty:
            ty += 1
        elif hy < ty:
            ty -= 1
    return (tx, ty)


def show(h, t):
    rlow = min(0, min(pos[1] for pos in [h] + t))
    rhigh = max(0, max(pos[1] for pos in [h] + t))
    clow = min(0, min(pos[0] for pos in [h] + t))
    chigh = max(0, max(pos[0] for pos in [h] + t))

    for r in range(rhigh + 2, rlow - 3, -1):
        for c in range(clow - 2, chigh + 3):
            if h[0] == c and h[1] == r:
                print("H", sep="", end="")
            elif (c, r) in t:
                print(t.index((c, r)) + 1, sep="", end="")
            elif c == 0 and r == 0:
                print("s", sep="", end="")
            else:
                print(".", sep="", end="")
        print()
    print()


def score_2(data: list[str], debug=False) -> int:
    visited = {(0, 0)}
    hx, hy = 0, 0
    tails = [(0, 0)] * 9
    last = ""
    for xd, yd, instr in parse(data):
        if instr != last:
            if debug:
                show((hx, hy), tails)
            last = instr
        hx += xd
        hy += yd
        new_tails = []
        head = (hx, hy)
        for t in tails:
            head = move(head, t)
            new_tails.append(head)
        tails = new_tails
        visited.add(tails[-1])
    show((hx, hy), tails)
    return len(visited)


TEST2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".splitlines()

if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    print("test", test_score)
    assert test_score == EXPECTED_2
    test_score = score_2(TEST2, debug=True)
    print("test2", test_score)
    assert test_score == 36
    print("part 2", score_2(DATA))
