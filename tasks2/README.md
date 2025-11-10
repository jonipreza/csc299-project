# tasks2 - Iteration: Add due dates with specific times

This iteration builds on `tasks1` by allowing you to specify **due dates with times**.

## New Feature
- Add due dates when creating a task:
  ```bash
  python3 tasks2.py add "Finish English Essay" --due "Nov 20, 2025 3:00 pm"
  ```
- Tasks are saved with due date/time and displayed nicely when listed.

## Example Usage
```bash
# Add task with due date and time
python3 tasks2.py add "Finish English Essay" --due "2025-11-20 15:00"

# List tasks (sorted by due date)
python3 tasks2.py list

# Mark a task done
python3 tasks2.py done <id>
```

## Folder layout
```
csc299-project/
  tasks1/
  tasks2/
    tasks2.py
    README.md
```
