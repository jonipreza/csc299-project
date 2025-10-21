def format_task_output(task):
    return f"Title: {task['title']}\nDescription: {task['description']}\nStatus: {task['status']}\n"

def validate_task_input(title, description):
    if not title or not description:
        raise ValueError("Title and description cannot be empty.")
    return True