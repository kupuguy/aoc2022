from pathlib import Path
from typing import Generator
from dataclasses import dataclass, replace
import functools
from heapq import nlargest

TEST = """Blueprint 1:\
  Each ore robot costs 4 ore.\
  Each clay robot costs 2 ore.\
  Each obsidian robot costs 3 ore and 14 clay.\
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:\
  Each ore robot costs 2 ore.\
  Each clay robot costs 3 ore.\
  Each obsidian robot costs 3 ore and 8 clay.\
  Each geode robot costs 3 ore and 12 obsidian.""".splitlines()

EXPECTED_1 = 33
EXPECTED_2 = None

DATA = Path("input/data19.txt").read_text().splitlines()


@dataclass(eq=True, frozen=True)
class Blueprint:
    id: int
    ore: int
    clay_ore: int
    obsidian_ore: int
    obsidian_clay: int
    geode_ore: int
    geode_obsidian: int


@dataclass(eq=True, frozen=True, order=True)
class State:
    geode: int = 0
    geode_robot: int = 0
    obsidian_robot: int = 0
    clay_robot: int = 0
    ore_robot: int = 1
    obsidian: int = 0
    clay: int = 0
    ore: int = 0


def parse(data: list[str]) -> Generator[Blueprint, None, None]:
    rows = []
    for line in data:
        if not line:
            continue
        numbers = [int(s.strip(":")) for s in line.split() if s.strip(":").isdigit()]
        yield Blueprint(*numbers)


def options(
    blueprint: Blueprint,
    state: State,
    max_ore: int,
    max_clay: int,
    max_obsidian: int,
) -> set[State]:
    """Find all possible options for the next step"""
    states = set()

    if state.ore >= blueprint.geode_ore and state.obsidian >= blueprint.geode_obsidian:
        states.add(
            replace(
                state,
                geode_robot=state.geode_robot + 1,
                ore=state.ore + state.ore_robot - blueprint.geode_ore,
                clay=state.clay + state.clay_robot,
                obsidian=(
                    state.obsidian + state.obsidian_robot - blueprint.geode_obsidian
                ),
                geode=state.geode + state.geode_robot,
            )
        )

    if (
        state.obsidian_robot < max_obsidian
        and state.ore >= blueprint.obsidian_ore
        and state.clay >= blueprint.obsidian_clay
    ):
        states.add(
            replace(
                state,
                obsidian_robot=state.obsidian_robot + 1,
                ore=state.ore + state.ore_robot - blueprint.obsidian_ore,
                clay=state.clay + state.clay_robot - blueprint.obsidian_clay,
                obsidian=state.obsidian + state.obsidian_robot,
                geode=state.geode + state.geode_robot,
            )
        )

    if state.clay_robot < max_clay and state.ore >= blueprint.clay_ore:
        states.add(
            replace(
                state,
                clay_robot=state.clay_robot + 1,
                ore=state.ore + state.ore_robot - blueprint.clay_ore,
                clay=state.clay + state.clay_robot,
                obsidian=state.obsidian + state.obsidian_robot,
                geode=state.geode + state.geode_robot,
            )
        )

    if state.ore_robot < max_ore and state.ore >= blueprint.ore:
        states.add(
            replace(
                state,
                ore_robot=state.ore_robot + 1,
                ore=state.ore + state.ore_robot - blueprint.ore,
                clay=state.clay + state.clay_robot,
                obsidian=state.obsidian + state.obsidian_robot,
                geode=state.geode + state.geode_robot,
            )
        )

    states.add(
        replace(
            state,
            ore=state.ore + state.ore_robot,
            clay=state.clay + state.clay_robot,
            obsidian=state.obsidian + state.obsidian_robot,
            geode=state.geode + state.geode_robot,
        )
    )
    return states


def all_options(
    blueprint: Blueprint,
    current: set[State],
    minutes: int,
    max_ore: int,
    max_clay: int,
    max_obsidian: int,
    geode_robots: int,
    limit: int = 2000,
) -> set[State]:
    new_states = set()
    filter_geode_robots = False

    for st in current:
        opts = options(blueprint, st, max_ore, max_clay, max_obsidian)
        new_states |= opts

    if len(new_states) > limit:
        new_states = set(st for st in nlargest(limit, new_states))

    # print(
    #    f"{minutes=} {len(new_states)=}, {max(st.geode_robot for st in new_states)} {max(geodes)}"
    # )
    return new_states, geode_robots + (1 if filter_geode_robots else 0)


def best(blueprint: Blueprint, state: State, max_minutes: int = 24) -> int:
    options = {state}
    geode_robots = 0
    max_ore = max(
        blueprint.ore - 1,
        blueprint.clay_ore,
        blueprint.obsidian_ore,
        blueprint.geode_ore,
    )
    max_clay = blueprint.obsidian_clay
    max_obsidian = blueprint.geode_obsidian

    for minutes in range(1, max_minutes + 1):
        options, geode_robots = all_options(
            blueprint, options, minutes, max_ore, max_clay, max_obsidian, geode_robots
        )

    value = max(st.geode for st in options)
    print(f"Blueprint {blueprint.id} best {value}")
    return value


def score_1(data: list[str]) -> int:
    return sum(bp.id * best(bp, State()) for bp in parse(data))


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def score_2(data: list[str]) -> int:
    v = 1
    for bp in list(parse(data))[:3]:
        v *= best(bp, State(), 32)

    return v


EXPECTED_2 = 3472

if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    assert test_score == EXPECTED_2
    print("test", test_score)
    print("part 2", score_2(DATA))
