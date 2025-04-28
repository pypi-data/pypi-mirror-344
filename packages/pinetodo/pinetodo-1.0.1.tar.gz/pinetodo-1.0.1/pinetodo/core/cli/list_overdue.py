from datetime import datetime
from .functions import load_data

def list_overdue():
    data = load_data()
    tasks = data["tasks"]
    overdue_tasks = []

    for task in tasks:
        if "deadline" in task and task["status"] != "done":
            deadline = datetime.strptime(task["deadline"], "%Y-%m-%dT%H:%M:%S")
            if deadline < datetime.now():
                overdue_tasks.append(task)

    if not overdue_tasks:
        print(" No overdue tasks.")
        return

    for task in overdue_tasks:
        print(f"ID: {task['id']} | Title: {task['title']} | Deadline: {task['deadline']}")
