def func(f):
    count_A = 0
    count_B = 0
    with open('11.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        count_A = content.lower().count('a')
        count_B = content.lower().count('b')
    return count_A, count_B

result_A, result_B = func("11.txt")
print(f"A: {result_A}, B: {result_B}")
