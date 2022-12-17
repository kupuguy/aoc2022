from pathlib import Path
from typing import Generator

TEST = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()

EXPECTED_1 = 1651
EXPECTED_2 = None

DATADIR = Path(__file__).parent / "../input"
DATA = (DATADIR / "data16.txt").read_text().splitlines()


def parse(data: list[str]) -> Generator[tuple[str, int, list[str]], None, None]:
    rows = []
    for line in data:
        if not line:
            continue
        a, b = line.split(";")
        name = a.split()[1]
        flow_rate = int(a.split("=", 1)[1])
        valves = [
            v.strip() for v in b.split("valve", 1)[1].removeprefix("s ").split(",")
        ]
        yield name, flow_rate, valves


def best_move(
    current: str,
    open: set[str],
    time: int,
    flow: dict[str, int],
    dists: dict[str, dict[str, int]],
) -> tuple[int, list[str]]:
    if time <= 1:
        return 0, []

    value_open = flow[current] * time
    options = [
        best_move(n, open | {n}, time - d - 1, flow, dists)
        for n, d in dists[current].items()
        if n not in open
    ]
    if options:
        value_move = max(options, default=0, key=lambda r: r[0])
        # print(current, open, time, value_open, value_move)
        return value_open + value_move[0], value_move[1] + [current]
    return value_open, [current]


def distances(
    neighbours: dict[str, list[str]], flows: dict[str, int]
) -> dict[str, dict[str, int]]:
    distances = {}
    for valve, nlist in neighbours.items():
        distances[valve] = {n: 1 for n in nlist}

    def dist(a, b, visited: set):
        if a == b:
            return 0
        if b in distances[a]:
            return distances[a][b]

        v = (
            min(
                [dist(n, b, visited | {n}) for n in neighbours[a] if n not in visited],
                default=999,
            )
            + 1
        )
        return v

    for a in distances:
        for b in distances:
            if a != b:
                distances[a][b] = dist(a, b, set())

    for a in list(distances):
        distances[a] = {b: n for b, n in distances[a].items() if flows[b] != 0}

    return distances


def score_1(data: list[str]) -> int:
    flows: dict[str, int] = {}
    neighbours: dict[str, list[str]] = {}

    for name, flow, n in parse(data):
        flows[name] = flow
        neighbours[name] = n

    d = distances(neighbours, flows)

    best = max(
        best_move(n, {n}, 29 - d["AA"][n], flows, d) for n in d["AA"] if flows[n] > 0
    )
    print("Best path", best[0], best[1])
    return best[0]


# test_score = score_1(TEST)
# print("test", test_score)
# assert test_score == EXPECTED_1
# print("part 1", score_1(DATA))


def best_combined(
    human: str,
    open: set[str],
    human_time: int,
    elephant: str,
    elephant_time: int,
    flow: dict[str, int],
    dists: dict[str, dict[str, int]],
) -> tuple[int, list[str], list[str]]:
    if human_time < 1 and elephant_time < 1:
        return 0, [], []

    value_open = 0

    if human_time >= elephant_time:
        value_open = flow[human] * (human_time - 1)
        options = [
            best_combined(
                n, open | {n}, human_time - d - 1, elephant, elephant_time, flow, dists
            )
            for n, d in dists[human].items()
            if n not in open and human_time - d - 1 > 0
        ]
        if options:
            value_move, h_open, e_open = max(options, default=0, key=lambda r: r[0])
            return (
                value_open + value_move,
                h_open + [(human, human_time, value_open)],
                e_open,
            )

        v, h, e = best_combined("AA", open, 0, elephant, elephant_time, flow, dists)
        return v + value_open, h + [(human, human_time, value_open)], e
    else:
        value_open = flow[elephant] * (elephant_time - 1)
        options = [
            best_combined(
                human, open | {n}, human_time, n, elephant_time - d - 1, flow, dists
            )
            for n, d in dists[elephant].items()
            if n not in open and elephant_time - d - 1 > 0
        ]
        if options:
            value_move, h_open, e_open = max(options, default=0, key=lambda r: r[0])
            return (
                value_open + value_move,
                h_open,
                e_open + [(elephant, elephant_time, value_open)],
            )

        v, h, e = best_combined(human, open, human_time, "AA", 0, flow, dists)
        return v + value_open, h, e + [(elephant, elephant_time, value_open)]


def score_2(data: list[str]) -> int:
    flows: dict[str, int] = {}
    neighbours: dict[str, list[str]] = {}

    for name, flow, n in parse(data):
        flows[name] = flow
        neighbours[name] = n

    d = distances(neighbours, flows)

    best = 0
    best_human = []
    best_elephant = []
    for human in d["AA"]:
        for elephant in d["AA"].keys() - {human}:
            if elephant < human:
                continue
            score, path_human, path_elephant = best_combined(
                human,
                {human, elephant},
                26 - d["AA"][human],
                elephant,
                26 - d["AA"][elephant],
                flows,
                d,
            )
            print(
                f"{human}, {elephant}, {score}, {path_human[::-1]}, {path_elephant[::-1]}"
            )
            if score > best:
                best, best_human, best_elephant = score, path_human, path_elephant

    for v in sorted(
        best_human + best_elephant, key=lambda p: (p[1], p[0]), reverse=True
    ):
        print(f"Minute {27-v[1]} open {v[0]} for {v[1]}*{flows[v[0]]}={v[2]}")
    print("total=", sum(v[2] for v in best_human + best_elephant))
    print("Best path", best, best_human, best_elephant)
    return best


EXPECTED_2 = 1707

if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA))
