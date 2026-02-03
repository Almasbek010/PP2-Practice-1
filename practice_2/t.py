import sys
n_line = sys.stdin.readline()
if not n_line:
    exit()
n = int(n_line.strip())
document = {}
for _ in range(n):
    parts = sys.stdin.readline().split()
    if not parts:
        continue
    cmd, key = parts[0], parts[1]
    if cmd == "set":
        document[key] = parts[2]
    else:
        res = document.get(key)
        if res is not None:
            print(res)
        else:
            print(f"KE: no key {key} found in the document")