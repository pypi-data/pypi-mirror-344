from .functions import load_data

def short_task(by: str = "title", reverse: bool = False):
    data = load_data()
    tasks = data["tasks"]

    all_items = []

    for task in tasks:
        subtask_count = len(task.get("subtasks", []))
        all_items.append({
            "id": task["id"],
            "title": task["title"],
            "status": task["status"],
            "type": "task",
            "subtask_count": subtask_count
        })
        for subtask in task.get("subtasks", []):
            all_items.append({
                "id": subtask["id"],
                "title": subtask["title"],
                "status": subtask["status"],
                "type": "subtask",
                "subtask_count": 0
            })

    if not all_items:
        print("No tasks or subtasks available to sort.")
        return

    if by in ["title", "status", "id"]:
        all_items.sort(key=lambda x: str(x[by]).lower(), reverse=reverse)
    elif by == "subtask_count":
        all_items.sort(key=lambda x: x["subtask_count"], reverse=reverse)
    else:
        print(f"Invalid sort key '{by}'. Using 'title' instead.")
        all_items.sort(key=lambda x: str(x["title"]).lower(), reverse=reverse)

    print(f"Sorted task list by '{by}' {'(Z-A)' if reverse else '(A-Z)'}:")
    for item in all_items:
        icon = "📌" if item["type"] == "task" else "🔸"
        subtask_info = f" | Subtasks: {item['subtask_count']}" if item["type"] == "task" else ""
        print(f"{icon} {item['id']} | {item['title']} | {item['status']}{subtask_info}")
