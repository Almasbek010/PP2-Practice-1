a = int(input())
arr = input().split()
for i in range(a):
    arr[i] = int(arr[i])
arr.sort()
max_freq = 0
result = arr[0]
current_freq = 0
for i in range(a):
    if i > 0 and arr[i] == arr[i-1]:
        current_freq += 1
    else:
        current_freq = 1
    if current_freq > max_freq:
        max_freq = current_freq
        result = arr[i]
print(result)