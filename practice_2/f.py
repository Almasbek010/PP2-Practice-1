a = int(input())    
numbers = input().split()
max_val = int(numbers[0])
for s in numbers:
    num = int(s)
    if num > max_val:
        max_val = num
print(max_val)