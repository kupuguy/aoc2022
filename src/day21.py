from pathlib import Path
from typing import Generator

TEST = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".splitlines()

EXPECTED_1 = 152
EXPECTED_2 = None

DATA = Path("input/data21.txt").read_text().splitlines()

import operator
from typing import Callable

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def parse(data: list[str]) -> dict[str, int | tuple[Callable, str, str]]:
    monkeys = {}
    for line in data:
        if not line:
            continue
        monkey, _, value = line.partition(": ")
        if value.isdigit():
            monkeys[monkey] = int(value)
        else:
            ma, op, mb = tuple(value.split())
            monkeys[monkey] = (OPERATORS[op], ma, mb)
    return monkeys


def score_1(data: list[str]) -> int:
    monkeys = parse(data)
    done = {m: v for m, v in monkeys.items() if isinstance(v, int)}
    queue = {m: v for m, v in monkeys.items() if not isinstance(v, int)}

    while "root" not in done and queue:
        for q in list(queue):
            op, a, b = queue[q]
            if a in done and b in done:
                done[q] = op(done[a], done[b])
                del queue[q]

    return done["root"]


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))

# q = a + b => a = q - b, b = q -a
# q = a - b => a = q - b, b = a - q
# q = a * b => a = q / b, b = q / a
# q = a /b => a = q * b, b = a / q
REVOPS = {
    operator.add: operator.sub,
    operator.sub: operator.add,
    operator.mul: operator.floordiv,
    operator.floordiv: operator.mul,
}
REVOPS2 = {
    operator.add: operator.sub,
    operator.sub: (lambda q, a: a - q),
    operator.mul: operator.floordiv,
    operator.floordiv: (lambda q, a: a // q),
}


def score_2(data: list[str]) -> int:
    monkeys = parse(data)
    del monkeys["humn"]
    done = {m: v for m, v in monkeys.items() if isinstance(v, int)}
    queue = {m: v for m, v in monkeys.items() if not isinstance(v, int)}
    computed = done.keys()  # Live view of dict keys
    rootop, roota, rootb = queue.pop("root")

    while roota not in done and rootb not in done:
        for q in list(queue):
            op, a, b = queue[q]
            if {a, b} < computed:
                done[q] = op(done[a], done[b])
                del queue[q]

    if roota in done:
        done["root"] = done[rootb] = done[roota]
    else:
        done["root"] = done[roota] = done[rootb]

    while "humn" not in done:
        for q in list(queue):
            op, a, b = queue[q]
            if {a, b} <= computed:
                done[q] = op(done[a], done[b])
                del queue[q]
            elif {q, b} <= computed:
                done[a] = REVOPS[op](done[q], done[b])
                del queue[q]
            elif {q, a} <= computed:
                done[b] = REVOPS2[op](done[q], done[a])
                del queue[q]

    return done["humn"]


EXPECTED_2 = 301

if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    assert test_score == EXPECTED_2
    print("test", test_score)
    print("part 2", score_2(DATA))
