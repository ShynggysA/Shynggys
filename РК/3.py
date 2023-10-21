def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    else:
        sequence = [1, 1]
        for i in range(2, n):
            next = sequence[-1] + sequence[-2]
            sequence.append(next)
        return sequence

while True:
    try:
        length = int(input("Please enter the length of the Fibonacci sequence: "))
        if length < 0:
            print("Please enter a positive number.")
        else:
            sequence = generate(length)
            print(f"The Fibonacci sequence for {length} is:")
            print(", ".join(map(str, sequence)))
            break
    except ValueError:
        print("Invalid input. Please enter a valid positive integer.")
