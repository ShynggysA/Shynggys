def is_arithmetic_progression(a, b, c):
    if b - a == c - b:
        return "YES"
    else:
        return "NO"

a = int(input())
b = int(input())
c = int(input())

result = is_arithmetic_progression(a, b, c)
print(result)
