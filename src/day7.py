from pathlib import Path
from typing import Generator

TEST = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".splitlines()

EXPECTED_1 = 95437
EXPECTED_2 = 24933642

DATADIR = Path(__file__).parent / "../input"
DATA = (DATADIR / "data7.txt").read_text().splitlines()

from collections import defaultdict


def parse(data: list[str]) -> dict:
    path = Path("/")
    files = {}
    cwd = files
    for row in data:
        if row == "$ cd /":
            path = Path("/")
        if row.startswith("$ cd"):
            path = (path / row.split()[-1]).resolve(strict=False)
            cwd = files
            for dir in str(path).split("/"):
                if dir:
                    cwd = cwd.setdefault(dir, {})
        elif row.startswith("$ ls"):
            continue
        elif row.startswith("dir "):
            cwd[row.split()[-1]] = {}
        else:
            size, name = row.split()
            cwd[name] = int(size)
    return files


def sizes(files: dict):
    total = 0
    all_sub = []
    for name, v in files.items():
        if isinstance(v, dict):
            sub = sizes(v)
            all_sub += sub
            if sub:
                total += sub[-1]
        else:
            total += v
    return all_sub + [total]


def score_1(data: list[str]) -> int:
    files = parse(data)
    return sum(f for f in sizes(files) if f < 100000)


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))


def score_2(data: list[str]) -> int:
    disk_size = 70000000
    needed = 30000000
    files = parse(data)

    sz = sizes(files)
    used = sz[-1]
    unused = disk_size - used
    needed -= unused
    return min(size for size in sz if size >= needed)


if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    print("test", test_score)
    assert test_score == EXPECTED_2
    print("part 2", score_2(DATA))
