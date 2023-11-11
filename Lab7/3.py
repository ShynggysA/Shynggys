def func(f):
    count = 0
    with open('11.txt', 'r', encoding='utf-8') as file:
        for line in file:
            count += sum(1 for char in line if char.isupper())
    return count

result = func("text1.txt")
print(f"Uppercase characters count: {result}")
