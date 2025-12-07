count = 0
currentNum = 50
line_number = 0

with open(r"C:\Users\retrac\Desktop\Coding Projects\AdventOfCode2025\12-01-2025\input.txt") as f:
    for line in f:
        line_number += 1
        line = line.strip()
        direction = line[0]
        step = int(line[1:])

        for i in range(step):
            if direction == 'R':
                currentNum = (currentNum + 1) % 100
            else:  # 'L'
                currentNum = (currentNum - 1) % 100

            if currentNum == 0:
                count += 1

        if line_number % 100 == 0:
            print(f"Line {line_number}: currentNum={currentNum}, total_count={count}")

print(f"Processed {line_number} lines in total.")
print("Password (total times dial points at 0):", count)
