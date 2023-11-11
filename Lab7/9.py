def func(f):
    with open('c:\\LAB_Python\\Shynggys\\Lab7\\11.txt', 'r', encoding='utf-8') as file:
        content = file.read().replace('B', 'J').replace('b', 'j')

    print(content)

result = func("c:\\LAB_Python\\Shynggys\\Lab7\\11.txt")
print(result)
