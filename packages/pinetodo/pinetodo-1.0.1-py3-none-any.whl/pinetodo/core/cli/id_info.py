import json
from .functions import load_data, save_data

def idInfo():
    data = load_data()
    id_count = data.get("id_count", 1)
    tasks = data.get("tasks", [])
    max_id = id_count
    for task in tasks:
        task_id = int(task["id"].strip("#"))
        max_id = max(max_id, task_id)
        for subtask in task.get("subtasks", []):
            subtask_id = int(subtask["id"].strip("#"))
            max_id = max(max_id, subtask_id)

    new_id = max_id + 1
    data["id_count"] = new_id
    save_data(data)
    return new_id
