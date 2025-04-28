from .functions import load_data, save_data

def delete_by_id(task_id: str):
    data = load_data()
    tasks = data["tasks"]

    if not task_id.startswith("#"):
        task_id = f"#{task_id}"

    task_to_delete = None
    subtask_to_delete = None
    parent_task = None

    for task in tasks:
        if task["id"] == task_id:
            task_to_delete = task
            break
        for subtask in task.get("subtasks", []):
            if subtask["id"] == task_id:
                subtask_to_delete = subtask
                parent_task = task
                break
        if subtask_to_delete:
            break

    if task_to_delete:
        if "subtasks" in task_to_delete:
            task_to_delete["subtasks"].clear()
        tasks.remove(task_to_delete)
        save_data(data)
        print(f"Task ID {task_id} and all its subtasks have been deleted!")
        return

    if subtask_to_delete:
        parent_task["subtasks"].remove(subtask_to_delete)
        save_data(data)
        print(f"Subtask ID {task_id} has been deleted from Task ID {parent_task['id']}!")

    else:
        print(f"No task or subtask found with ID {task_id}.")
