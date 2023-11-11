from collections import Counter

def func(f):
    with open('c:\\LAB_Python\\Shynggys\\Lab7\\11.txt', 'r', encoding='utf-8') as file:
        words = file.read().split()
        word_freq = Counter(words)
    return word_freq

result = func("c:\\LAB_Python\\Shynggys\\Lab7\\11.txt")
print(result)
