import os

input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path) as f:
    data = f.read().strip()
#part 1
parts = data.split("\n\n")
range_lines = parts[0].strip().splitlines()
id_lines = parts[1].strip().splitlines()

ranges = []
for line in range_lines:
    start_str, end_str = line.split('-')
    start = int(start_str)
    end = int(end_str)
    ranges.append((start, end))

ids = []
for line in id_lines:
    strline = int(line)
    ids.append(strline)

fresh_count = 0

for ingredient in ids:
    for start, end in ranges:
        if start <= ingredient <= end:
            fresh_count += 1
            break

print(fresh_count)

#part 2
ranges.sort()

merged_ranges = []
if ranges:
    curr_start, curr_end = ranges[0]
    for i in range(1, len(ranges)):
        next_start, next_end = ranges[i]
        if next_start <= curr_end + 1:
            curr_end = max(curr_end, next_end)
        else:
            merged_ranges.append((curr_start, curr_end))
            curr_start, curr_end = next_start, next_end
    merged_ranges.append((curr_start, curr_end))

total_fresh_count = sum(end - start + 1 for start, end in merged_ranges)
print("Total fresh ingredient IDs:", total_fresh_count)