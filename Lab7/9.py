def func(f):
    with open('11.txt', 'r', encoding='utf-8') as file:
        content = file.read().replace('B', 'J').replace('b', 'j')

    print(content)

result = func("11.txt")
print(result)
