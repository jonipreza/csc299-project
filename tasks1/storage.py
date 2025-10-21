def load_tasks(file_path='data/tasks.json'):
    import json
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_tasks(tasks, file_path='data/tasks.json'):
    import json
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)