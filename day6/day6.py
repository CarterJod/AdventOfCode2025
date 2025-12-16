import os
import sys

sys.set_int_max_str_digits(0)

# Construct the absolute path to input.txt so it works from any directory
input_path = os.path.join(os.path.dirname(__file__), "input.txt")

with open(input_path, "r") as f:
    lines = f.readlines()

#part 1
grid = []
for line in lines:
    parts = line.split()
    row = []
    for part in parts:
        try:
            row.append(int(part))
        except ValueError:
            row.append(part)
    if row:
        grid.append(row)

print(f"Processed {len(grid)} rows.")

if grid:
    operators = grid[-1]
    number_grid = grid[:-1]
    results = []

    for col_index, operator in enumerate(operators):
        current_val = number_grid[0][col_index]
        
        for row in number_grid[1:]:
            num = row[col_index]
            if operator == '+':
                current_val += num
            elif operator == '*':
                current_val *= num
        
        results.append(current_val)

    print("Sum of all column results:", sum(results))

#part 2
print("--- Part 2 ---")

# Clean up raw lines for processing
raw_lines = [line.rstrip('\n') for line in lines]
while raw_lines and not raw_lines[-1].strip():
    raw_lines.pop()

if raw_lines:
    width = max(len(line) for line in raw_lines)
    padded_lines = [line.ljust(width) for line in raw_lines]

    # Identify empty columns (all spaces)
    is_empty = [all(row[c] == ' ' for row in padded_lines) for c in range(width)]

    # Identify blocks of non-empty columns (Numbers)
    blocks = []
    current_block = []
    for c in range(width):
        if not is_empty[c]:
            current_block.append(c)
        else:
            if current_block:
                blocks.append(current_block)
                current_block = []
    if current_block:
        blocks.append(current_block)

    # Group blocks into Problems based on gap size
    # Gap of 1 space (1 empty column) -> Same problem
    # Gap of >1 space -> New problem
    problems = []
    if blocks:
        current_problem = [blocks[0]]
        for i in range(1, len(blocks)):
            prev_end = blocks[i-1][-1]
            curr_start = blocks[i][0]
            gap = curr_start - prev_end - 1
            
            if gap > 1:
                problems.append(current_problem)
                current_problem = []
            current_problem.append(blocks[i])
        problems.append(current_problem)

    total_sum_p2 = 0

    for prob in problems:
        # Parse numbers and ops for this problem
        parsed_cols = []
        for block in prob:
            # Construct number from all rows except last
            num_str = ""
            for r in range(len(padded_lines) - 1):
                # Extract the slice for this block
                row_slice = "".join(padded_lines[r][c] for c in block).strip()
                num_str += row_slice
            
            if not num_str:
                continue
                
            number = int(num_str)
            
            # Find operator from last row
            op_row = padded_lines[-1]
            op_char = "".join(op_row[c] for c in block).strip()
            
            parsed_cols.append((number, op_char))
        
        if not parsed_cols:
            continue

        # Evaluate Right-to-Left
        # Start with the rightmost number
        curr_val = parsed_cols[-1][0]
        
        # Iterate backwards from the second-to-last
        for i in range(len(parsed_cols) - 2, -1, -1):
            num, op = parsed_cols[i]
            
            if op == '+':
                curr_val += num
            elif op == '*':
                curr_val *= num
                
        total_sum_p2 += curr_val

    print("Total sum Part 2:")
    print(total_sum_p2)
