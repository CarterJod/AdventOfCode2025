import os
import sys

sys.set_int_max_str_digits(0)

# Construct the absolute path to input.txt so it works from any directory
input_path = os.path.join(os.path.dirname(__file__), "input.txt")

with open(input_path, "r") as f:
    lines = f.readlines()

# Clean up lines
lines = [line.rstrip('\n') for line in lines]
while lines and not lines[-1].strip():
    lines.pop()

if not lines:
    print("Input file is empty.")
    sys.exit(0)

# Pad lines to form a rectangle
width = max(len(line) for line in lines)
grid = [line.ljust(width, '.') for line in lines]
height = len(grid)

# Find Start 'S'
start_pos = None
for r, row in enumerate(grid):
    if 'S' in row:
        start_pos = (r, row.index('S'))
        break

if not start_pos:
    print("Start position 'S' not found.")
    sys.exit(0)

start_row, start_col = start_pos
current_beams = {start_col}
split_count = 0

# Simulate row by row
for r in range(start_row, height):
    next_beams = set()
    
    for c in current_beams:
        if 0 <= c < width:
            char = grid[r][c]
            if char == '^':
                split_count += 1
                if c - 1 >= 0: next_beams.add(c - 1)
                if c + 1 < width: next_beams.add(c + 1)
            else:
                next_beams.add(c)
    current_beams = next_beams

print(f"Total splits: {split_count}")

# Part 2
print("--- Part 2 ---")

# We track the number of timelines at each column.
# Start with 1 timeline at the start position.
timeline_counts = {start_col: 1}

for r in range(start_row, height):
    next_counts = {}
    
    for c, count in timeline_counts.items():
        if 0 <= c < width:
            char = grid[r][c]
            if char == '^':
                # Split creates two timelines
                if c - 1 >= 0:
                    next_counts[c - 1] = next_counts.get(c - 1, 0) + count
                if c + 1 < width:
                    next_counts[c + 1] = next_counts.get(c + 1, 0) + count
            else:
                # Continue straight
                next_counts[c] = next_counts.get(c, 0) + count
                
    timeline_counts = next_counts

total_timelines = sum(timeline_counts.values())
print(f"Total timelines: {total_timelines}")
