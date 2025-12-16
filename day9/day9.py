import os
import sys

sys.set_int_max_str_digits(0)

# Construct the absolute path to input.txt
input_path = os.path.join(os.path.dirname(__file__), "input.txt")

if not os.path.exists(input_path):
    print(f"Error: input.txt not found at {input_path}")
    sys.exit(1)

with open(input_path, "r") as f:
    lines = f.readlines()

points = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    try:
        # Input format is "X,Y"
        parts = line.split(',')
        if len(parts) >= 2:
            x = int(parts[0])
            y = int(parts[1])
            points.append((x, y))
    except ValueError:
        continue

max_area = 0
n = len(points)

# Iterate through all unique pairs of points
for i in range(n):
    for j in range(i, n):
        p1 = points[i]
        p2 = points[j]
        
        width = abs(p1[0] - p2[0]) + 1
        height = abs(p1[1] - p2[1]) + 1
        area = width * height
        
        if area > max_area:
            max_area = area

print(f"Largest rectangle area: {max_area}")

# Part 2

# Build polygon edges from the ordered points
edges = []
for k in range(n):
    p1 = points[k]
    p2 = points[(k + 1) % n]
    edges.append((p1, p2))

max_area_p2 = 0

for i in range(n):
    for j in range(i, n):
        p1 = points[i]
        p2 = points[j]
        
        # Rectangle bounds
        rx1, rx2 = sorted((p1[0], p2[0]))
        ry1, ry2 = sorted((p1[1], p2[1]))
        
        width = rx2 - rx1 + 1
        height = ry2 - ry1 + 1
        area = width * height
        
        if area <= max_area_p2:
            continue
            
        # Check 1: No polygon edge intersects the interior of the rectangle
        is_valid = True
        for u, v in edges:
            # Vertical edge
            if u[0] == v[0]:
                ex = u[0]
                ey1, ey2 = sorted((u[1], v[1]))
                # Check if x is strictly between rect x-bounds and y-intervals overlap
                if rx1 < ex < rx2 and max(ry1, ey1) < min(ry2, ey2):
                    is_valid = False
                    break
            # Horizontal edge
            else:
                ey = u[1]
                ex1, ex2 = sorted((u[0], v[0]))
                if ry1 < ey < ry2 and max(rx1, ex1) < min(rx2, ex2):
                    is_valid = False
                    break
        
        if is_valid:
            # Check 2: Center of rectangle is inside polygon (Ray Casting)
            cx, cy = rx1 + 0.5, ry1 + 0.5
            intersections = 0
            for u, v in edges:
                # Check vertical edges for ray crossing (ray to +infinity on x-axis)
                if u[0] == v[0]:
                    ex = u[0]
                    ey1, ey2 = sorted((u[1], v[1]))
                    if ex > cx and ey1 < cy < ey2:
                        intersections += 1
            
            if intersections % 2 == 1:
                max_area_p2 = area

print(f"Largest valid rectangle area (Part 2): {max_area_p2}")