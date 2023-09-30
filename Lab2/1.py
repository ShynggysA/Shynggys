def check_ratio(number):
    num_str = str(number)

    if len(num_str) != 4:
        return "NO"

    first_digit = int(num_str[0])
    second_digit = int(num_str[1])
    third_digit = int(num_str[2])
    last_digit = int(num_str[3])

    if first_digit + last_digit == second_digit - third_digit:
        return "YES"
    else:
        return "NO"


num = int(input("Enter a four-digit number: "))

result = check_ratio(num)
print(result)
