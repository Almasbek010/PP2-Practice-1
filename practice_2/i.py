a = int(input())
data = input().split()
arr = []
for s in data:
    arr.append(int(s))
min = arr[0]
max = arr[0]
for x in arr:
    if x < min:
        min = x
    if x > max:
        max = x
for i in range(a):
    if arr[i] == max:
        arr[i] = min
for val in arr:
    print(val, end=' ')