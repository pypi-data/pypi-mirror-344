from .functions import load_data, save_data
from datetime import datetime
from .id_info import idInfo

def find_task_by_id(task_list, task_id):
    for task in task_list:
        if task["id"] == task_id:
            return task
        found = find_task_by_id(task.get("subtasks", []), task_id)
        if found:
            return found
    return None

def add_subtask(parent_id, title, loc=None):
    data = load_data()
    tasks = data.get("tasks", [])

    if not parent_id.startswith("#"):
        parent_id = f"#{parent_id}"
    parent_task = find_task_by_id(tasks, loc if loc else parent_id)

    if not parent_task:
        print(f"Parent task with ID {parent_id} or subtask ID {loc} not found.")
        return

    if "subtasks" not in parent_task:
        parent_task["subtasks"] = []

    new_subtask_id = f"#{idInfo()}"
    
    new_subtask = {
        "id": new_subtask_id,
        "title": title,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "subtasks": []
    }

    parent_task["subtasks"].append(new_subtask)
    save_data(data)

    print(f"Sub-task '{title}' added as {new_subtask_id} under task {parent_id}")
