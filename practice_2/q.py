n = int(input())
counts = {}
for i in range(n):
    phone = input().strip()
    if phone in counts:
        counts[phone] += 1
    else:
        counts[phone] = 1
result_count = 0
for phone in counts:
    if counts[phone] == 3:
        result_count += 1
print(result_count)