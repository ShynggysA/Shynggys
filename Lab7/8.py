def func(f):
    with open('c:\\LAB_Python\\Shynggys\\Lab7\\11.txt', 'r', encoding='utf-8') as file:
        words = file.read().split()
        longest_word = max(words, key=len)
    return longest_word

result = func("c:\\LAB_Python\\Shynggys\\Lab7\\11.txt")
print(f"The longest word is: {result}")
