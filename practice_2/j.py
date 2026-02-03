a = int(input())
numbers = input().split()
for i in range(a):
    numbers[i] = int(numbers[i])
numbers.sort(reverse=True)
for x in numbers:
    print(x, end=' ')