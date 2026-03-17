n = int(input())
numbers = map(int, input().split())
even_numbers = filter(lambda x: x % 2 == 0, numbers)
print(len(list(even_numbers)))