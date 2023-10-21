addition = lambda x, y: x + y
multiplication = lambda x, y: x * y
division = lambda x, y: x / y
exponentiation = lambda x, y: x ** y

operations = int(input("Please chose the task you want to perform: \n1.Addition \n2.Multiplication \n3.Division \n4.Exponentiation: ))

if operations in [1, 2, 3, 4]:
    numbers = input("Please enter two numbers, comma separated: ").split(',')
    
    if len(numbers) != 2:
        print("Invalid input. Please enter two numbers separated by a comma.")
    else:
        x, y = map(float, numbers)
        
        if operations == 1:
            result = addition(x, y)
        elif operations == 2:
            result = multiplication(x, y)
        elif operations == 3:
            if y == 0:
                result = "Error."
            else:
                result = division(x, y)
        else:
            result = exponentiation(x, y)
        
        print("Result:", result)
else:
    print("Error. Choice (1, 2, 3, or 4).")

