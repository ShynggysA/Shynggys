population = int(input("Enter population of the unverse:"))

if population <= 0:
    print("Population must be a positive integer.")
else:
    if population % 2 == 0:
        survivors = population // 2
    else:
        survivors = (population + 1) // 2

        print(f"Survivors: {survivors}")

