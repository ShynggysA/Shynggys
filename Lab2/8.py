weight = int(input("Enter the boxer's weight (in kg): "))

if weight <= 60:
    category = "Lightweight"
elif weight <= 64:
    category = "First Welterweight"
elif weight <= 69:
    category = "Welterweight"
else:
    category = "Unknown"

print(category)
