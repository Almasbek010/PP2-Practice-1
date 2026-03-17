s = input()
vowels = "aeiou"
has_vowel = any(c.lower() in vowels for c in s)
if has_vowel:
    print("Yes")
else:
    print("No")