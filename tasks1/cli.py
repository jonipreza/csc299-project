def main():
    import argparse
    from tasks1 import storage, models, utils

    parser = argparse.ArgumentParser(description="Simple Task Manager")
    parser.add_argument('command', choices=['add', 'list', 'search'], help='Command to execute')
    parser.add_argument('--title', type=str, help='Title of the task')
    parser.add_argument('--description', type=str, help='Description of the task')
    
    args = parser.parse_args()

    if args.command == 'add':
        if not args.title or not args.description:
            print("Title and description are required to add a task.")
            return
        task = models.Task(title=args.title, description=args.description)
        tasks = storage.load_tasks()
        tasks.append(task)
        storage.save_tasks(tasks)
        print(f"Task '{task.title}' added successfully.")

    elif args.command == 'list':
        tasks = storage.load_tasks()
        if not tasks:
            print("No tasks available.")
        else:
            for task in tasks:
                print(utils.format_task(task))

    elif args.command == 'search':
        if not args.title:
            print("Title is required to search for a task.")
            return
        tasks = storage.load_tasks()
        found_tasks = [task for task in tasks if args.title.lower() in task.title.lower()]
        if not found_tasks:
            print("No tasks found with that title.")
        else:
            for task in found_tasks:
                print(utils.format_task(task))

if __name__ == "__main__":
    main()