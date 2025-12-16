import os
import sys

sys.set_int_max_str_digits(0)
sys.setrecursionlimit(2000)

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

if not os.path.exists(input_path):
    print(f"Error: input.txt not found at {input_path}")
    sys.exit(1)

with open(input_path, "r") as f:
    raw_content = f.read()

#part 1

lines = raw_content.splitlines()

shapes = {}
regions = []

current_shape_id = None
current_shape_rows = []

def parse_shape(rows):
    coords = set()
    for r, row in enumerate(rows):
        for c, char in enumerate(row):
            if char == '#':
                coords.add((r, c))
    return coords

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if ':' in line:
        header = line.split(':')[0]
        if 'x' in header:
            # It's a region
            # Finish previous shape if needed
            if current_shape_id is not None:
                shapes[current_shape_id] = parse_shape(current_shape_rows)
                current_shape_id = None
                current_shape_rows = []
            
            # Parse region: "12x5: 1 0 1 0 2 2"
            dims, counts_str = line.split(':')
            w_str, h_str = dims.split('x')
            w, h = int(w_str), int(h_str)
            counts = list(map(int, counts_str.strip().split()))
            regions.append({'w': w, 'h': h, 'counts': counts})
        else:
            # It's a shape header: "0:"
            if current_shape_id is not None:
                shapes[current_shape_id] = parse_shape(current_shape_rows)
            
            try:
                current_shape_id = int(header)
            except ValueError:
                current_shape_id = header
            current_shape_rows = []
    else:
        if current_shape_id is not None:
            current_shape_rows.append(line)

if current_shape_id is not None:
    shapes[current_shape_id] = parse_shape(current_shape_rows)

def normalize(coords):
    if not coords:
        return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)

def get_variations(base_coords):
    variations = set()
    current = list(base_coords)
    
    # 4 rotations
    for _ in range(4):
        # Rotate 90 deg: (r, c) -> (c, -r)
        current = [(c, -r) for r, c in current]
        variations.add(normalize(current))
        
    # Flip
    current = [(r, -c) for r, c in base_coords]
    for _ in range(4):
        current = [(c, -r) for r, c in current]
        variations.add(normalize(current))
        
    return list(variations)

# Precompute variations for all shapes
shape_variations = {sid: get_variations(coords) for sid, coords in shapes.items()}

def solve_region(region):
    W = region['w']
    H = region['h']
    counts = region['counts']
    
    pieces = []
    for sid, count in enumerate(counts):
        if sid in shapes:
            for _ in range(count):
                pieces.append(sid)
    
    # Quick check: Total area
    total_area = 0
    for sid in pieces:
        total_area += len(shapes[sid])
    
    if total_area > W * H:
        return False
        
    # Sort pieces: Size Descending, then ID
    # Sorting by size helps fail fast.
    # Sorting by ID groups identical pieces together for symmetry breaking.
    pieces_info = []
    for sid in pieces:
        pieces_info.append((len(shapes[sid]), sid))
    
    pieces_info.sort(key=lambda x: (x[0], x[1]), reverse=True)
    sorted_pieces = [p[1] for p in pieces_info]
    
    # Precompute valid masks for the required shapes on this specific grid size
    unique_sids = set(sorted_pieces)
    masks_cache = {}
    
    for sid in unique_sids:
        valid_masks = []
        vars = shape_variations[sid]
        for var in vars:
            max_r = max(r for r, c in var)
            max_c = max(c for r, c in var)
            
            if max_r >= H or max_c >= W:
                continue
                
            for r in range(H - max_r):
                for c in range(W - max_c):
                    mask = 0
                    for vr, vc in var:
                        bit = (r + vr) * W + (c + vc)
                        mask |= (1 << bit)
                    valid_masks.append(mask)
        
        # Sort masks to ensure deterministic order for symmetry breaking
        valid_masks = sorted(list(set(valid_masks)))
        masks_cache[sid] = valid_masks
        
        if not valid_masks:
            return False

    n_pieces = len(sorted_pieces)
    
    # DFS Solver
    # idx: index of piece in sorted_pieces to place
    # grid_mask: bitmask of currently occupied cells
    # last_mask_idx: index of the mask used by the previous piece (if identical)
    def dfs(idx, grid_mask, last_mask_idx):
        if idx == n_pieces:
            return True
            
        sid = sorted_pieces[idx]
        
        # Symmetry breaking:
        # If this piece is the same as the previous one, we must choose a mask
        # that appears strictly after the previous one in the list.
        # This prevents checking permutations of identical pieces.
        start_mask_idx = 0
        if idx > 0 and sorted_pieces[idx] == sorted_pieces[idx-1]:
            start_mask_idx = last_mask_idx + 1
            
        possible_masks = masks_cache[sid]
        
        for i in range(start_mask_idx, len(possible_masks)):
            m = possible_masks[i]
            if (grid_mask & m) == 0:
                if dfs(idx + 1, grid_mask | m, i):
                    return True
        return False

    return dfs(0, 0, -1)

success_count = sum(1 for r in regions if solve_region(r))
print(f"Regions fitting all presents: {success_count}")