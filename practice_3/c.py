words = ["ZER", "ONE", "TWO", "THR", "FOU", "FIV", "SIX", "SEV", "EIG", "NIN"]
s = input()
if "+" in s:
    op = "+"
elif "-" in s:
    op = "-"
else:
    op = "*"
left_part, right_part = s.split(op)
def decode(text):
    res = ""
    for i in range(0, len(text), 3):
        triplet = text[i:i+3]
        res += str(words.index(triplet))
    return int(res)
num1 = decode(left_part)
num2 = decode(right_part)
if op == "+":
    result = num1 + num2
elif op == "-":
    result = num1 - num2
else:
    result = num1 * num2
final_str = ""
for digit in str(result):
    if digit == "-":
        continue
    index = int(digit)
    final_str += words[index]
print(final_str)