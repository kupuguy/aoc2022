from pathlib import Path
from typing import Generator
import re

TEST = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".splitlines()

EXPECTED_1 = 6032
EXPECTED_2 = None

DATA = Path("input/data22.txt").read_text().splitlines()


def parse(data: list[str]) -> tuple[list[str], str]:
    rows = []
    for line in data[:-2]:
        if not line:
            continue
        rows.append(line)

    steps = [int(s) if s.isdigit() else s for s in re.split("(L|R)", data[-1])]
    return rows, steps


RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3


def score_1(data: list[str]) -> int:
    grid, steps = parse(data)
    height = len(grid)
    width = max(len(r) for r in grid)
    left = [len(r) - len(r.lstrip()) for r in grid]
    right = [len(r) for r in grid]
    top = [
        min(y for y in range(height) if left[y] <= x < right[y]) for x in range(width)
    ]
    bottom = [
        max(y for y in range(height) if left[y] <= x < right[y]) + 1
        for x in range(width)
    ]

    def next(x, y, face):
        if face == RIGHT:
            x += 1
            if x >= right[y]:
                return left[y], y
        elif face == DOWN:
            y += 1
            if y >= bottom[x]:
                return x, top[x]
        elif face == LEFT:
            x -= 1
            if x < left[y]:
                return right[y] - 1, y
        else:
            y -= 1
            if y < top[x]:
                return x, bottom[x] - 1
        return x, y

    face = RIGHT
    x = left[0]
    y = 0
    # print(x,y,face)

    for step in steps:
        if step == "R":
            face = (face + 1) % 4
        elif step == "L":
            face = (face - 1) % 4
        else:
            for i in range(step):
                nx, ny = next(x, y, face)
                # print(x,y,face,nx,ny)
                if grid[ny][nx] == "#":
                    break
                x, y = nx, ny
        # print(x,y,face)

    return 1000 * (y + 1) + 4 * (x + 1) + face


test_score = score_1(TEST)
print("test", test_score)
assert test_score == EXPECTED_1
print("part 1", score_1(DATA))

cube = """
        1111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666"""

cube2 = """
    22221111
    22221111
    22221111
    22221111
    3333  
    3333
    3333
    3333
44445555
44445555
44445555
44445555
6666
6666
6666
6666
"""


def cube_map2(face: int) -> dict[int, dict[tuple[int, int], tuple[int, int, int]]]:
    mapping = {LEFT: {}, RIGHT: {}, UP: {}, DOWN: {}}
    # bottom of 1 -> right of 3 moving left
    # right of 3 -> bottom of 1 moving up
    for x in range(face):
        mapping[DOWN][2 * face + x, face] = (2 * face - 1, face + x, LEFT)
        mapping[RIGHT][2 * face, face + x] = (2 * face + x, face - 1, UP)

    # right of 1 -> right of 5 moving left REVERSED
    # right of 5 -> right of 1 moving left REVERSED
    for y in range(face):
        mapping[RIGHT][3 * face, y] = (2 * face - 1, 3 * face - y - 1, LEFT)
        mapping[RIGHT][2 * face, 3 * face - y - 1] = (3 * face - 1, y, LEFT)

    # bottom of 5 -> right of 6 moving left
    # right of 6 -> bottom of 5 moving up
    for x in range(face):
        mapping[DOWN][face + x, 3 * face] = (face - 1, 3 * face + x, LEFT)
        mapping[RIGHT][face, 3 * face + x] = (face + x, 3 * face - 1, UP)

    # top of 1 moving up -> bottom of 6 moving up
    # bottom of 6 -> top of 1 moving down
    for x in range(face):
        mapping[UP][2 * face + x, -1] = (x, 4 * face - 1, UP)
        mapping[DOWN][x, 4 * face] = (2 * face + x, 0, DOWN)

    # top of 2 -> left of 6 moving right
    # left of 6 -> top of 2 moving down
    for x in range(face):
        mapping[UP][face + x, -1] = (0, 3 * face + x, RIGHT)
        mapping[LEFT][-1, 3 * face + x] = (face + x, 0, DOWN)

    # left of 2 -> left of 4 moving right
    # left of 4 -> left of 2 moving right
    for y in range(face):
        mapping[LEFT][face - 1, y] = (0, 3 * face - y - 1, RIGHT)
        mapping[LEFT][-1, 3 * face - y - 1] = (face, y, RIGHT)

    # left of 3 -> top of 4 moving down
    # top of 4 -> left of 3 moving right
    for y in range(face):
        mapping[LEFT][face - 1, face + y] = (y, 2 * face, DOWN)
        mapping[UP][y, 2 * face - 1] = (face, face + y, RIGHT)

    return mapping


def cube_map(face: int) -> dict[int, dict[tuple[int, int], tuple[int, int, int]]]:
    mapping = {LEFT: {}, RIGHT: {}, UP: {}, DOWN: {}}
    # right of 1 maps to right of 6 (moving left)
    # right of 6 maps to right of 1 moving left
    for y in range(face):
        mapping[RIGHT][3 * face, y] = (4 * face - 1, 3 * face - y - 1, LEFT)
        mapping[RIGHT][4 * face, 3 * face - y - 1] = (3 * face - 1, y, LEFT)

    # top of 1 maps to top of 2 (moving down)
    # top of 2 maps to top of 1 (moving down)
    for x in range(face):
        mapping[UP][x + 2 * face, -1] = (face - x - 1, face, DOWN)
        mapping[UP][face - x - 1, face - 1] = (x + 2 * face, 0, DOWN)

    # left of 1 maps to top of 3 (moving down)
    # top of 3 maps to left of 1 moving right
    for y in range(face):
        mapping[LEFT][2 * face - 1, y] = (face + y, face, DOWN)
        mapping[UP][face + y, face - 1] = (2 * face, y, RIGHT)

    # left of 2 maps to bottom of 6 (moving up)
    # bottom of 6 maps to left of 2 moving right
    for y in range(face):
        mapping[LEFT][-1, face + y] = (4 * face - y - 1, 3 * face - 1, UP)
        mapping[DOWN][4 * face - y - 1, 3 * face] = (0, face + y, RIGHT)

    # bottom of 2 maps to bottom of 5 (moving up)
    # bottom of 5 maps to bottom of 2 moving up
    for x in range(face):
        mapping[DOWN][x, 2 * face] = (3 * face - x - 1, 3 * face - 1, UP)
        mapping[DOWN][3 * face - x - 1, 3 * face] = (x, 2 * face - 1, UP)

    # bottom of 3 maps to left of 5 (moving right)
    # left of 5 maps to bottom of 3 moving up
    for x in range(face):
        mapping[DOWN][face + x, 2 * face] = (2 * face, 3 * face - x - 1, RIGHT)
        mapping[LEFT][2 * face - 1, 3 * face - x - 1] = (face + x, 2 * face - 1, UP)

    # top of 6 maps to right of 4 moving left
    # right of 4 maps to top of 6 moving down
    for x in range(face):
        mapping[UP][3 * face + x, 2 * face - 1] = (3 * face - 1, 2 * face - x - 1, LEFT)
        mapping[RIGHT][3 * face, 2 * face - x - 1] = (3 * face + x, 2 * face, DOWN)
    return mapping


MARKERS = {UP: "^", RIGHT: ">", LEFT: "<", DOWN: "v"}


def score_2(data: list[str]) -> int:
    grid, steps = parse(data)
    height = len(grid)
    width = max(len(r) for r in grid)
    left = [len(r) - len(r.lstrip()) for r in grid]
    right = [len(r) for r in grid]
    top = [
        min(y for y in range(height) if left[y] <= x < right[y]) for x in range(width)
    ]
    bottom = [
        max(y for y in range(height) if left[y] <= x < right[y]) + 1
        for x in range(width)
    ]

    path = [list(r) for r in grid]

    if width > height:
        face_size = width // 4
        mapping = cube_map(face_size)
        x = 2 * face_size
    else:
        face_size = height // 4
        mapping = cube_map2(face_size)
        x = face_size

    # Validate mapping
    for _x in range(width):
        assert (_x, top[_x] - 1) in mapping[UP], f"up {_x}, {top[_x]-1}"
        assert (_x, bottom[_x]) in mapping[DOWN], f"down {_x}, {bottom[_x]}"
    for _y in range(height):
        assert (left[_y] - 1, _y) in mapping[LEFT], f"left {left[_y]-1}, {_y}"
        assert (right[_y], _y) in mapping[RIGHT], f"right {right[_y]} {_y}"

    f = face_size

    def next(x: int, y: int, face: int) -> tuple[int, int, int]:
        if face == RIGHT:
            return mapping[face].get((x + 1, y), (x + 1, y, face))
        elif face == DOWN:
            return mapping[face].get((x, y + 1), (x, y + 1, face))
        elif face == LEFT:
            return mapping[face].get((x - 1, y), (x - 1, y, face))

        return mapping[face].get((x, y - 1), (x, y - 1, face))

    face = RIGHT
    y = 0
    path = [list(r) for r in grid]
    path[y][x] = MARKERS[face]

    for step in steps:
        if step == "R":
            face = (face + 1) % 4
            path[y][x] = MARKERS[face]
        elif step == "L":
            face = (face - 1) % 4
            path[y][x] = MARKERS[face]
        else:
            for i in range(step):
                nx, ny, nface = next(x, y, face)

                if grid[ny][nx] == "#":
                    break

                x, y, face = nx, ny, nface
                path[y][x] = MARKERS[face]

    if face_size == 4:
        for r in path:
            print("".join(r))

    return 1000 * (y + 1) + 4 * (x + 1) + face


EXPECTED_2 = 5031

if EXPECTED_2 is not None:
    test_score = score_2(TEST)
    assert test_score == EXPECTED_2
    print("test", test_score)
    print("part 2", score_2(DATA))
