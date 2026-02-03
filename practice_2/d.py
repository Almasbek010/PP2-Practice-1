a = input()
line = input().split()
count = 0
for s in line:
    num = int(s)
    if num > 0:
        count += 1
print(count)