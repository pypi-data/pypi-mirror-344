from .functions import load_data

def search_task(keyword: str, status: str = None):
    data = load_data()
    tasks = data["tasks"]
    found_tasks = []

    for task in tasks:
        if keyword.lower() in task["title"].lower() and (not status or task["status"].lower() == status.lower()):
            found_tasks.append(task)
        
        for subtask in task.get("subtasks", []):
            if keyword.lower() in subtask["title"].lower() and (not status or subtask["status"].lower() == status.lower()):
                found_tasks.append(subtask)

    if not found_tasks:
        print(f"No tasks or subtasks found with the keyword '{keyword}' and status '{status if status else 'any'}'")
        return

    print(f"Search results for '{keyword}' (status: {status if status else 'any'}):")
    for task in found_tasks:
        if "subtasks" in task:
            print(f"{task['id']} | Title: {task['title']} | Status: {task['status']}")
            for subtask in task.get("subtasks", []):
                print(f"  {subtask['id']} | Title: {subtask['title']} | Status: {subtask['status']}")
        else:
            print(f"{task['id']} | Title: {task['title']} | Status: {task['status']}")
