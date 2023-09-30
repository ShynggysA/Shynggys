age = int(input("Enter your age: "))

if age <= 13:
    age_group = "childhood"
elif age <= 24:
    age_group = "youth"
elif age <= 59:
    age_group = "maturity"
else:
    age_group = "old age"

print(age_group)
