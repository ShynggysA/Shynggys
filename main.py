num = int(input("Enter a four-digit number: "))

if 1000 <= num <= 9999:
    thousand = num // 1000
    hundred = (num % 1000) // 100
    tens = (num % 100) // 10
    ones = num % 10

    print(f"Thousand: {thousand}")
    print(f"Hundred: {hundred}")
    print(f"Tens: {tens}")
    print(f"Ones: {ones}")
else:
    print("The number must be a four-digit number.")
