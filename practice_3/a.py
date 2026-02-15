n = int(input())
def check_validity(n):
    for digit in str(n):
        if int(digit) % 2 != 0:
            return "Not valid"
    return "Valid"
print(check_validity(n))