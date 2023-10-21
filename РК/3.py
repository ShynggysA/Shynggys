def generate_fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    else:
        fibonacci_sequence = [1, 1]
        for i in range(2, n):
            next_term = fibonacci_sequence[-1] + fibonacci_sequence[-2]
            fibonacci_sequence.append(next_term)
        return fibonacci_sequence

while True:
    try:
        length = int(input("Please enter the length of the Fibonacci sequence: "))
        if length < 0:
            print("Please enter a positive number.")
        else:
            fibonacci_sequence = generate_fibonacci(length)
            print(f"The Fibonacci sequence for {length} is:")
            print(", ".join(map(str, fibonacci_sequence)))
            break
    except ValueError:
        print("Invalid input. Please enter a valid positive integer.")

