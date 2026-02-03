n = int(input())
occur = {}
for i in range(1, n + 1):
    s = input().strip()
    if s not in occur:
        occur[s] = i
keys = list(occur.keys())
keys.sort()
for s in keys:
    print(s, occur[s])