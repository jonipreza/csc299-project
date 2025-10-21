class Task:
    def __init__(self, title, description="", status="pending"):
        self.title = title
        self.description = description
        self.status = status

    def mark_completed(self):
        self.status = "completed"

    def __repr__(self):
        return f"Task(title={self.title}, description={self.description}, status={self.status})"