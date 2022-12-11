from pathlib import Path
from typing import Generator

TEST = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".splitlines()

EXPECTED_1 = 0
EXPECTED_2 = None

DATADIR = Path(__file__).parent / "../input"
DATA = (DATADIR / "data4.txt").read_text().splitlines()


class Item:
    def __init__(self, worry):
        self.worry = worry

    def __repr__(self):
        return f"item {self.worry}"


class Monkey:
    def __init__(self, id, items, operation, test) -> None:
        self.id = id
        self.items = [Item(worry) for worry in items]
        self.operation = operation
        self.test = test
        self.inspect = 0

    def process(self):
        items = self.items
        self.items = []
        for item in items:
            self.inspect += 1
            item.worry = self.operation(item) // 3
            throw = self.test(item)
            MONKEYS[throw].items.append(item)

    def __repr__(self):
        return f"{self.id} {[item for item in self.items]}"


MONKEYS = [
    Monkey(
        0,
        [79, 98],
        lambda item: item.worry * 19,
        lambda item: 2 if item.worry % 23 == 0 else 3,
    ),
    Monkey(
        1,
        [54, 65, 75, 74],
        lambda item: item.worry + 6,
        lambda item: 2 if item.worry % 19 == 0 else 0,
    ),
    Monkey(
        2,
        [79, 60, 97],
        lambda item: item.worry * item.worry,
        lambda item: 1 if item.worry % 13 == 0 else 3,
    ),
    Monkey(
        3,
        [74],
        lambda item: item.worry + 3,
        lambda item: 0 if item.worry % 17 == 0 else 1,
    ),
]


def round():
    for monkey in MONKEYS:
        monkey.process()

    # for monkey in MONKEYS:
    #     print(monkey)


def run():
    for i in range(20):
        round()

    monkeys = sorted(MONKEYS, key=lambda monkey: monkey.inspect, reverse=True)[:2]
    return monkeys[0].inspect * monkeys[1].inspect


assert run() == 10605

MONKEYS = [
    Monkey(
        0,
        [54, 89, 94],
        lambda item: item.worry * 7,
        lambda item: 5 if item.worry % 17 == 0 else 3,
    ),
    Monkey(
        1,
        [66, 71],
        lambda item: item.worry + 4,
        lambda item: 0 if item.worry % 3 == 0 else 3,
    ),
    Monkey(
        2,
        [76, 55, 80, 55, 55, 96, 78],
        lambda item: item.worry + 2,
        lambda item: 7 if item.worry % 5 == 0 else 4,
    ),
    Monkey(
        3,
        [93, 69, 76, 66, 89, 54, 59, 94],
        lambda item: item.worry + 7,
        lambda item: 5 if item.worry % 7 == 0 else 2,
    ),
    Monkey(
        4,
        [80, 54, 58, 75, 99],
        lambda item: item.worry * 17,
        lambda item: 1 if item.worry % 11 == 0 else 6,
    ),
    Monkey(
        5,
        [69, 70, 85, 83],
        lambda item: item.worry + 8,
        lambda item: 2 if item.worry % 19 == 0 else 7,
    ),
    Monkey(
        6,
        [89],
        lambda item: item.worry + 6,
        lambda item: 0 if item.worry % 2 == 0 else 1,
    ),
    Monkey(
        7,
        [62, 80, 58, 57, 93, 56],
        lambda item: item.worry * item.worry,
        lambda item: 6 if item.worry % 13 == 0 else 4,
    ),
]

print(run())
