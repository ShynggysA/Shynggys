def func(f):
    count = 0
    with open('c:\\LAB_Python\\Shynggys\\Lab7\\11.txt', 'r', encoding='utf-8') as file:
        words = file.read().split()
        count += sum(1 for word in words if word.endswith(('F', 'f')))
    return count

result = func("c:\\LAB_Python\\Shynggys\\Lab7\\11.txt")
print(f"Number of words ending with 'F': {result}")
