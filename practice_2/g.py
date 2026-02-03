a = int(input())
numbers = input().split()
max_val = int(numbers[0])
max_pos = 1
for i in range(len(numbers)):
    current_num = int(numbers[i])
    if current_num > max_val:
        max_val = current_num
        max_pos = i + 1
print(max_pos)