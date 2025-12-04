import os

base = os.path.dirname(__file__)
path = os.path.join(base, "input.txt")

# Part 1
grid = []
with open(path) as f:
    for line in f:
        line = line.strip()
        if line:
            grid.append(line)

rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0

total_accessible = 0

neighbors = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1),          (0, 1),
             (1, -1),  (1, 0), (1, 1)]

for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '@':
            count = 0
            #chat for logic
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == '@':
                        count += 1

            if count < 4:
                total_accessible += 1

print("Total accessible rolls:", total_accessible)

# Part 2

grid = []

with open(path) as f:
    for line in f:
        line = line.strip()
        if line:
            grid.append(list(line)) 

rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0

total_removed = 0

neighbors = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1),          (0, 1),
             (1, -1),  (1, 0), (1, 1)]

while True:
    removed_this_round = []
    #chat for logic
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                count = 0
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '@':
                            count += 1
                if count < 4:
                    removed_this_round.append((r, c))

    if not removed_this_round:
        break
    
    for r, c in removed_this_round:
        grid[r][c] = '.'
        total_removed += 1

print("Total rolls removed:", total_removed)