list = []
tasks = []

while True:
    print("Please choose the task you want to perform:")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Mark Task as Completed")
    print("4. View All Completed Tasks")
    print("5. Exit")
    
    choice = input("User Input: ")
    
    if choice == '1':
        task = input("Enter the task: ")
        todo_list.append(task)
        print(f'The task "{task}" was added to the to-do list')
    
    elif choice == '2':
        if list:
            print("All Tasks:")
            for i, task in enumerate(list, start=1):
                print(f"{i}. {task}")
        else:
            print("No tasks in the to-do list.")
    
    elif choice == '3':
        task = input("Enter the name of the task: ")
        if task in todo_list:
            list.remove(task)
            completed_tasks.append(task)
            print(f'The task "{task}" is marked as completed')
        else:
            print(f'Task "{task}" not found in the to-do list.')
    
    elif choice == '4':
        if tasks:
            print("All Completed Tasks:")
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task}")
        else:
            print("No completed tasks.")
    
    elif choice == '5':
        break
    
    else:
        print("Error. Choice (1, 2, 3, 4, or 5).")

