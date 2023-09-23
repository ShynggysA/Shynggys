num1 = int(input("Введите число:"))
num2 = int(input("Введите число:"))

total = num2 // num1
remains = num2 - total * num1

print(f"{total}")
print(f"{remains}")