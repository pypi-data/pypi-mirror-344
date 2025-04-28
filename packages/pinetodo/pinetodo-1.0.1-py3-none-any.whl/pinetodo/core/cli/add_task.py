from .functions import load_data, save_data
from datetime import datetime
from .id_info import idInfo

def add_task(title, priority="medium"):
    data = load_data()
    tasks = data.get("tasks", [])

    new_id = f"#{idInfo()}"
    
    new_task = {
        "id": new_id,
        "title": title,
        "status": "todo",
        "priority": priority,
        "created_at": str(datetime.now()),
        "subtasks": [],
    }

    tasks.append(new_task)
    data["tasks"] = tasks
    save_data(data)

    print(f"Task added: {title} ({new_id}) with priority {priority}")
