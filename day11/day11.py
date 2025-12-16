import os
import sys

sys.set_int_max_str_digits(0)
sys.setrecursionlimit(10000)

# Construct the absolute path to input.txt
input_path = os.path.join(os.path.dirname(__file__), "input.txt")

if not os.path.exists(input_path):
    print(f"Error: input.txt not found at {input_path}")
    sys.exit(1)

with open(input_path, "r") as f:
    lines = f.readlines()

#part 1

# Parse the graph
adj = {}
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if ':' in line:
        src, dests_str = line.split(':', 1)
        src = src.strip()
        # Split by whitespace to get destination nodes
        dests = dests_str.split()
        adj[src] = dests

# Memoization dictionary to store path counts
memo = {}

def count_paths(node):
    # Base case: reached the target
    if node == 'out':
        return 1
    
    if node in memo:
        return memo[node]
    
    total = 0
    if node in adj:
        for neighbor in adj[node]:
            total += count_paths(neighbor)
            
    memo[node] = total
    return total

print(f"Total paths from 'you' to 'out': {count_paths('you')}")

# Part 2
print("--- Part 2 ---")

def count_paths_between(start_node, end_node, graph):
    # Local memoization for this specific target
    memo_target = {}
    
    def dfs(node):
        if node == end_node:
            return 1
        if node in memo_target:
            return memo_target[node]
        
        total = 0
        if node in graph:
            for neighbor in graph[node]:
                total += dfs(neighbor)
        
        memo_target[node] = total
        return total

    return dfs(start_node)

# Calculate paths for sequence: svr -> dac -> fft -> out
path1 = count_paths_between('svr', 'dac', adj) * \
        count_paths_between('dac', 'fft', adj) * \
        count_paths_between('fft', 'out', adj)

# Calculate paths for sequence: svr -> fft -> dac -> out
path2 = count_paths_between('svr', 'fft', adj) * \
        count_paths_between('fft', 'dac', adj) * \
        count_paths_between('dac', 'out', adj)

print(f"Total paths visiting both 'dac' and 'fft': {path1 + path2}")