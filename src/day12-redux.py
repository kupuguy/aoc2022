from pathlib import Path

data = Path("input/data12.txt").read_text()
start, width = data.index("S"), data.index("\n") + 1

grid = {
    i: ord(c) - ord("a")
    for i, c in enumerate(data.replace("S", "a").replace("E", "z"))
    if c != "\n"
}
for part in (1, 2):
    steps = {start: 0} if part == 1 else {p: 0 for p in grid if grid[p] == 0}
    queue = list(steps)
    for pos in queue:
        neighbours = [
            n
            for n in ({pos + 1, pos - 1, pos + width, pos - width} & grid.keys())
            - steps.keys()
            if grid[n] <= grid[pos] + 1
        ]
        steps |= {n: steps[pos] + 1 for n in neighbours}
        queue.extend(neighbours)
    print("Part", part, steps[data.index("E")])
