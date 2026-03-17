data = input().split()
a = data[0]
b = data[1]
primes = []
for a in data:
    if a < 1:
        continue 
    is_prime = True
    for i in range(2, int(b**0.5) + 1):
        if b % i == 0:
            is_prime = False
            break 
    if is_prime:
        primes.append(str(b))
if primes:
    print(" ".join(primes))
else:
    print("No primes")