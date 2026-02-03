a = int(input())
s = set()
for i in range(a):
    surname = input().strip()
    s.add(surname)
print(len(s))