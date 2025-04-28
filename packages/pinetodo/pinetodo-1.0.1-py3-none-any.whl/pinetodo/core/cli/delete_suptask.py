from .functions import load_data, save_data

def delete_subtask(task_id: str, subtask_id: str):
    data = load_data()
    tasks = data["tasks"]

    task_to_modify = None
    subtask_to_delete = None

    for task in tasks:
        if task["id"] == task_id:
            task_to_modify = task
            subtask_to_delete = next((subtask for subtask in task.get("subtasks", []) if subtask["id"] == subtask_id), None)
            if subtask_to_delete:
                break

    if not task_to_modify:
        print(f"Task with ID {task_id} not found!")
        return

    if not subtask_to_delete:
        print(f"Subtask with ID {subtask_id} not found!")
        return

    task_to_modify["subtasks"].remove(subtask_to_delete)
    save_data(data)
    print(f"Subtask ID {subtask_id} has been deleted from Task ID {task_id}!")
