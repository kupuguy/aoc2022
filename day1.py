import heapq
from pathlib import Path

data = Path("data1.txt").read_text()
data = [int(row) if row.strip() else None for row in Path("data1.txt").open()]
elves = []
elves = [0]
for row in data:
    if row is None:
        elves.append(0)
    else:
        elves[-1] += row

print("Part 1", max(elves))
print("Part 2", sum(heapq.nlargest(3, elves)))
