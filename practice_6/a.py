n = int(input())
numbers = map(int, input().split())
result = sum(map(lambda x: x**2, numbers))
print(result)