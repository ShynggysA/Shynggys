def permission(age):
    if age >= 18:
        return "Access allowed"
    else:
        return "Access denied"

age = int(input("Enter your age: "))

result = permission(age)
print(result)
