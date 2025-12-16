import os
import sys
import re
import math
import itertools
from fractions import Fraction

sys.set_int_max_str_digits(0)

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

if not os.path.exists(input_path):
    print(f"Error: input.txt not found at {input_path}")
    sys.exit(1)

with open(input_path, "r") as f:
    lines = f.readlines()

#part 1

def get_reachable(btns):
    """
    Generates all reachable states from a list of buttons.
    Returns a dict mapping state_value -> min_presses.
    """
    dist = {0: 0}
    for b in btns:
        # Iterate over a snapshot of items to avoid runtime modification issues
        # and to combine current results with the new button
        current_items = list(dist.items())
        for v, p in current_items:
            nv = v ^ b
            np = p + 1
            if nv not in dist or np < dist[nv]:
                dist[nv] = np
    return dist

def solve_machine(line):
    line = line.strip()
    if not line:
        return 0
        
    # Parse target: [.##.]
    m_target = re.search(r'\[([.#]+)\]', line)
    if not m_target:
        return 0
    target_str = m_target.group(1)
    target_val = 0
    for i, ch in enumerate(target_str):
        if ch == '#':
            target_val |= (1 << i)
            
    # Parse buttons: (0,1) (2) ...
    button_strs = re.findall(r'\(([\d,]+)\)', line)
    buttons = []
    for b_str in button_strs:
        val = 0
        parts = b_str.split(',')
        for p in parts:
            if p:
                idx = int(p)
                val |= (1 << idx)
        buttons.append(val)
        
    # Meet-in-the-middle
    n = len(buttons)
    mid = n // 2
    left_buttons = buttons[:mid]
    right_buttons = buttons[mid:]
    
    left_dist = get_reachable(left_buttons)
    right_dist = get_reachable(right_buttons)
    
    min_total = float('inf')
    
    for r_val, r_presses in right_dist.items():
        needed = target_val ^ r_val
        if needed in left_dist:
            total = left_dist[needed] + r_presses
            if total < min_total:
                min_total = total
                
    return min_total if min_total != float('inf') else 0

total_presses = 0
for line in lines:
    total_presses += solve_machine(line)

print(f"Total fewest button presses: {total_presses}")

# Part 2
print("--- Part 2 ---")

def solve_linear_system(A, b):
    n = len(A)
    if n == 0: return []
    M = [row[:] + [val] for row, val in zip(A, b)]
    
    for i in range(n):
        pivot = i
        while pivot < n and M[pivot][i] == 0:
            pivot += 1
        if pivot == n: return None 
        
        M[i], M[pivot] = M[pivot], M[i]
        
        div = M[i][i]
        for j in range(i, n+1):
            M[i][j] /= div
            
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n+1):
                    M[k][j] -= factor * M[i][j]
                    
    return [row[n] for row in M]

def solve_ilp(A, b):
    m = len(A)
    n = len(A[0])
    
    # Gaussian elimination
    M = [[Fraction(x) for x in row] + [Fraction(val)] for row, val in zip(A, b)]
    
    # Pre-calculate safe upper bounds for all variables based on A*x = b and A >= 0
    # This is used to bound the search for free variables.
    # x_j <= b_i / A_ij for all i where A_ij > 0
    var_upper_bounds = []
    for j in range(n):
        bnd = float('inf')
        for i in range(m):
            if A[i][j] > 0:
                bnd = min(bnd, b[i] // A[i][j])
        var_upper_bounds.append(bnd if bnd != float('inf') else 0)

    pivots = []
    pivot_cols = set()
    
    curr_row = 0
    for col in range(n):
        if curr_row >= m: break
        
        pivot_row = -1
        for r in range(curr_row, m):
            if M[r][col] != 0:
                pivot_row = r
                break
        
        if pivot_row == -1: continue
            
        M[curr_row], M[pivot_row] = M[pivot_row], M[curr_row]
        
        pivot_val = M[curr_row][col]
        for c in range(col, n + 1):
            M[curr_row][c] /= pivot_val
            
        for r in range(m):
            if r != curr_row and M[r][col] != 0:
                factor = M[r][col]
                for c in range(col, n + 1):
                    M[r][c] -= factor * M[curr_row][c]
        
        pivots.append((curr_row, col))
        pivot_cols.add(col)
        curr_row += 1
        
    for r in range(curr_row, m):
        if M[r][n] != 0:
            return None 
            
    free_cols = [c for c in range(n) if c not in pivot_cols]
    col_to_row = {c: r for r, c in pivots}
    
    def get_solution(free_vals):
        x = [Fraction(0)] * n
        for c, v in free_vals.items():
            x[c] = v
        for c in range(n):
            if c in col_to_row:
                r = col_to_row[c]
                val = M[r][n]
                for fc in free_cols:
                    val -= M[r][fc] * x[fc]
                x[c] = val
        return x

    # If no free variables, check the unique solution
    if not free_cols:
        sol = get_solution({})
        if all(v.denominator == 1 and v >= 0 for v in sol):
            return sum(int(v) for v in sol)
        return float('inf')

    best_sum = float('inf')
    
    # Iterate over integer values for free variables within their safe bounds
    # Since num_free is small (usually 0-2), this is feasible.
    ranges = []
    for fc in free_cols:
        # The variable must be non-negative and <= its structural upper bound
        ranges.append(range(int(var_upper_bounds[fc]) + 1))
    
    # Use product to iterate all combinations
    for t_vals in itertools.product(*ranges):
        free_vals_dict = {fc: Fraction(tv) for fc, tv in zip(free_cols, t_vals)}
        
        # Compute full solution
        full_sol = get_solution(free_vals_dict)
        
        # Check validity
        if all(v.denominator == 1 and v >= 0 for v in full_sol):
            s = sum(int(v) for v in full_sol)
            if s < best_sum:
                best_sum = s

    return best_sum

total_presses_p2 = 0
for line in lines:
    line = line.strip()
    if not line: continue
    
    m_target = re.search(r'\{([\d,]+)\}', line)
    if not m_target: continue
    b = [int(x) for x in m_target.group(1).split(',')]
    num_eq = len(b)
    
    button_strs = re.findall(r'\(([\d,]+)\)', line)
    A_cols = []
    for b_str in button_strs:
        col = [0] * num_eq
        if b_str:
            parts = b_str.split(',')
            for p in parts:
                if p:
                    idx = int(p)
                    if idx < num_eq:
                        col[idx] = 1
        A_cols.append(col)
        
    num_vars = len(A_cols)
    if num_vars == 0: continue
    A_mat = [[A_cols[c][r] for c in range(num_vars)] for r in range(num_eq)]
    
    res = solve_ilp(A_mat, b)
    if res != float('inf'):
        total_presses_p2 += res

print(f"Total fewest button presses Part 2: {total_presses_p2}")