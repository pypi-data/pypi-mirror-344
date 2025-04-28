from .functions import load_data, save_data

def mark_subtasks_done(task):
    for subtask in task.get("subtasks", []):
        subtask["status"] = "done"
    if any(subtask['status'] == "done" for subtask in task['subtasks']):
        task["status"] = "done"

def mark_done(task_id: str):
    data = load_data()
    tasks = data["tasks"]

    task_to_mark = None

    if not task_id.startswith("#"):
        task_id = f"#{task_id}"
    for task in tasks:
        if task["id"] == task_id:
            task_to_mark = task
            break
        for subtask in task.get("subtasks", []):
            if subtask["id"] == task_id:
                task_to_mark = subtask
                break
        if task_to_mark:
            break

    if not task_to_mark:
        print(f"Task with ID {task_id} not found!")
        return

    if "subtasks" in task_to_mark:
        mark_subtasks_done(task_to_mark)

    task_to_mark["status"] = "done"
    save_data(data)
    print(f"Task ID {task_id} has been marked as done!")
