import os
import sys

sys.set_int_max_str_digits(0)

# Construct the absolute path to input.txt
input_path = os.path.join(os.path.dirname(__file__), "input.txt")

with open(input_path, "r") as f:
    lines = f.readlines()

#part 1

points = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    try:
        x, y, z = map(int, line.split(','))
        points.append((x, y, z))
    except ValueError:
        continue

N = len(points)
edges = []

# Calculate squared Euclidean distance for all pairs
for i in range(N):
    for j in range(i + 1, N):
        p1 = points[i]
        p2 = points[j]
        # Squared distance is sufficient for comparison and avoids sqrt
        dist_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
        edges.append((dist_sq, i, j))

# Sort pairs by distance (shortest first)
edges.sort(key=lambda x: x[0])

# Union-Find (Disjoint Set Union)
parent = list(range(N))
size = [1] * N

def find(i):
    if parent[i] == i:
        return i
    parent[i] = find(parent[i]) # Path compression
    return parent[i]

def union(i, j):
    root_i = find(i)
    root_j = find(j)
    
    if root_i != root_j:
        # Union by size
        if size[root_i] < size[root_j]:
            root_i, root_j = root_j, root_i
        parent[root_j] = root_i
        size[root_i] += size[root_j]
        return True
    return False

# Connect the 1000 closest pairs
limit = 1000
for k in range(min(len(edges), limit)):
    _, u, v = edges[k]
    union(u, v)

# Collect circuit sizes
circuit_sizes = []
seen_roots = set()

for i in range(N):
    root = find(i)
    if root not in seen_roots:
        circuit_sizes.append(size[root])
        seen_roots.add(root)

# Sort sizes descending
circuit_sizes.sort(reverse=True)

# Multiply the three largest
result = 1
count = 0
for s in circuit_sizes:
    result *= s
    count += 1
    if count == 3:
        break

print(f"Product of three largest circuits: {result}")

# Part 2
print("--- Part 2 ---")

# Re-initialize Union-Find
parent = list(range(N))
size = [1] * N
num_components = N

for dist_sq, u, v in edges:
    if union(u, v):
        num_components -= 1
        if num_components == 1:
            # Found the last connection
            x1 = points[u][0]
            x2 = points[v][0]
            print(f"Product of X coordinates of last connection: {x1 * x2}")
            break