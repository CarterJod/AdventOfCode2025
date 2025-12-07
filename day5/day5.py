# Read input
with open("input.txt") as f:
    data = f.read().strip()

# --- Split into the two sections ---
parts = data.split("\n\n")
range_lines = parts[0].strip().splitlines()
id_lines = parts[1].strip().splitlines()

# --- Parse ranges ---
ranges = []
for line in range_lines:
    # TODO: parse "x-y" into integers
    pass

# --- Parse ingredient IDs ---
ids = []
for line in id_lines:
    # TODO: convert each line to an int
    pass

# --- Check which IDs are fresh ---
fresh_count = 0

for ingredient in ids:
    # TODO: determine if ingredient falls in ANY range
    # if yes: increment fresh_count
    pass

print(fresh_count)
