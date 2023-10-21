# Create an empty set to store unique items and an empty dictionary to count non-unique items
unique_items = set()
non_unique_items = {}

while True:
    print("Please choose the task you want to perform:")
    print("1. Enter items")
    print("2. Exit")

    choice = input("User Input: ")

    if choice == '1':
        item_input = input("Please enter items separated by comma: ")
        items = item_input.split(', ')
        
        for item in items:
            if item in unique_items:
                if item in non_unique_items:
                    non_unique_items[item] += 1
                else:
                    non_unique_items[item] = 2
            else:
                unique_items.add(item)

        print("Items are saved")
        
    elif choice == '2':
        break

    else:
        print("Invalid choice. Please choose a valid option (1 or 2).")

print("Unique items:", unique_items)
print("Not unique items:", tuple((item, count) for item, count in non_unique_items.items()))
