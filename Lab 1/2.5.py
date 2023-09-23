num1 = float(input("Please enter the first number: "))
num2 = float(input("Please enter the second number: "))

cal = input("Please choose the operation (+, -, *, /): ")

if cal == '+':
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
elif cal == '-':
    result = num1 - num2
    print(f"{num1} - {num2} = {result}")
elif cal == '*':
    result = num1 * num2
    print(f"{num1} * {num2} = {result}")
elif cal == '/':
    if num2 == 0:
        print("Division by zero is not allowed.")
    else:
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
else:
    print("Invalid operation. Please choose from +, -, *, /.")


