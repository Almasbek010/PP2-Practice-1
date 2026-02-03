n = int(input())
doramas = {}
for i in range(n):
    data = input().split()
    name = data[0]
    episodes = int(data[1])
    if name in doramas:
        doramas[name] += episodes
    else:
        doramas[name] = episodes
sorted_names = sorted(doramas.keys())
for name in sorted_names:
    print(name, doramas[name])