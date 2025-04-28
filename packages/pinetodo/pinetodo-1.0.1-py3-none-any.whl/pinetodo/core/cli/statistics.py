from .functions import load_data

def show_statistics():
    data = load_data()
    tasks = data["tasks"]
    todo_count = sum(1 for task in tasks if task["status"] == "todo")
    done_count = sum(1 for task in tasks if task["status"] == "done")

    print(f"📊 Task Statistics:")
    print(f"Total Tasks: {len(tasks)}")
    print(f"Pending Tasks (Todo): {todo_count}")
    print(f"Completed Tasks (Done): {done_count}")
