n = int(input())
numbers = map(int, input().split())
positive = all(x >= 0 for x in numbers)
if positive:
    print("Yes")
else:
    print("No")