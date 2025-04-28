from .functions import load_data, save_data

def edit_by_id(task_id: str, new_title: str = None, new_status: str = None):
    data = load_data()
    tasks = data["tasks"]

    if not task_id.startswith("#"):
        task_id = f"#{task_id}"

    task_to_edit = None
    subtask_to_edit = None
    parent_task = None

    for task in tasks:
        if task["id"] == task_id:
            task_to_edit = task
            break
        for subtask in task.get("subtasks", []):
            if subtask["id"] == task_id:
                subtask_to_edit = subtask
                parent_task = task
                break
        if subtask_to_edit:
            break

    if task_to_edit:
        if new_title:
            task_to_edit["title"] = new_title
        if new_status:
            task_to_edit["status"] = new_status
        save_data(data)
        print(f"Task ID {task_id} has been updated!")
        return

    if subtask_to_edit:
        if new_title:
            subtask_to_edit["title"] = new_title
        if new_status:
            subtask_to_edit["status"] = new_status
        save_data(data)
        print(f"Subtask ID {task_id} has been updated in Task ID {parent_task['id']}!")
        return

    print(f"Task or Subtask with ID {task_id} not found.")
