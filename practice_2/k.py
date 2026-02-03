line1 = input().split()
n = int(line1[0])
a = int(line1[1])
b = int(line1[2])
arr = input().split()
for i in range(n):
    arr[i] = int(arr[i])
arr[a-1:b] = arr[a-1:b][::-1]
for x in arr:
    print(x, end=' ')