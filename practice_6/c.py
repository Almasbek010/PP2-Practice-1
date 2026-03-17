n = int(input())
words = input().split()
pairs = []
for index, word in enumerate(words):
    pairs.append(f"{index}:{word}")
print(" ".join(pairs))