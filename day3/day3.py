import os

base = os.path.dirname(__file__)
path = os.path.join(base, "input.txt")
#part 1
total = 0
with open(path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        digits = [int(ch) for ch in line]
        max_joltage = 0
        for i in range(len(digits)):
            for j in range(i+1, len(digits)):
                value = digits[i]*10 + digits[j]
                if value > max_joltage:
                    max_joltage = value
        total += max_joltage

print("Total output joltage:", total)

#part 2
k = 12
total_part2 = 0

with open(path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        digits = [int(ch) for ch in line]
        stack = []

        for i, d in enumerate(digits):
            remaining = len(digits) - i

            while stack and d > stack[-1] and len(stack) + remaining > k:
                stack.pop()

            if len(stack) < k:
                stack.append(d)

        value = 0
        for digit in stack:
            value = value * 10 + digit

        total_part2 += value

print("Part 2 total output joltage:", total_part2)