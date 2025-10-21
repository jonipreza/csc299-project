# csc299-project
# Task Manager CLI

This project is a simple command-line interface (CLI) task manager that allows users to store, list, and search tasks. The tasks are stored in a JSON file, making it easy to manage and retrieve them.

## Project Structure

```
task-manager
├── tasks1
│   ├── __init__.py
│   ├── cli.py
│   ├── storage.py
│   ├── models.py
│   └── utils.py
├── tests
│   ├── test_cli.py
│   └── test_storage.py
├── data
│   └── tasks.json
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd task-manager
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Running the Task Manager

To run the task manager, execute the following command in your terminal:

```
python -m tasks1.cli
```

## Features

- **Add a Task:** You can add a new task by providing a title and description.
- **List Tasks:** View all tasks stored in the JSON file.
- **Search Tasks:** Search for tasks by title or description.

## Running Tests

To ensure everything is working correctly, you can run the tests using:

```
pytest
```

## License

This project is licensed under the MIT License.
