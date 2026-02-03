a = int(input())
arr = input().split()
seen = set()
for x in arr:
    if x not in seen:
        print("YES")
        seen.add(x)
    else:
        print("NO")