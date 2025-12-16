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

    # Identify columns
    cols = []
    for x in range(width):
        col_chars = [line[x] for line in padded_lines]
        cols.append(col_chars)

    # Group into blocks (problems)
    # Problems are separated by a column consisting only of spaces
    blocks = []
    current_block = []
    for col in cols:
        if all(c == ' ' for c in col):
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            current_block.append(col)
    if current_block:
        blocks.append(current_block)

    total_sum_p2 = 0

    for block in blocks:
        # Find operator
        operator = None
        for col in block:
            for char in col:
                if char in ('+', '*'):
                    operator = char
                    break
            if operator:
                break
        
        if not operator:
            continue

        numbers = []
        # Process columns Right-to-Left
        for col in reversed(block):
            # Extract digits
            digit_str = "".join(c for c in col if c.isdigit())
            if digit_str:
                numbers.append(int(digit_str))
        
        if not numbers:
            continue

        # Calculate
        res = numbers[0]
        for num in numbers[1:]:
            if operator == '+':
                res += num
            elif operator == '*':
                res *= num
        
        total_sum_p2 += res

    print("Total sum Part 2:")
    print(total_sum_p2)
