def func(f):
    count_all = 0
    count_none = 0
    with open('c:\\LAB_Python\\Shynggys\\Lab7\\11.txt', 'r', encoding='utf-8') as file:
        words = file.read().split()
        count_all = words.count("all")
        count_none = words.count("none")
    return count_all, count_none

result_all, result_none = func("c:\\LAB_Python\\Shynggys\\Lab7\\11.txt")
print(f"Number of 'all' words: {result_all}")
print(f"Number of 'none' words: {result_none}")
