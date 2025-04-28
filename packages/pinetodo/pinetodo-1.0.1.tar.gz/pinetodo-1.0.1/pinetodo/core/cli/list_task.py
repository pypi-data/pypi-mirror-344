from .functions import load_data
from rich.console import Console
from rich.tree import Tree

console = Console()

def list_tasks():
    data = load_data()
    tasks = data.get("tasks", [])

    if not tasks:
        console.print("No tasks available!")
        return

    tree = Tree("Task List")

    for task in tasks:
        status = f"[{task['status']}]".upper()
        node = tree.add(f"{task['id']} {task['title']} {status}")
        add_subtasks_to_tree(task.get("subtasks", []), node)

    console.print(tree)

def add_subtasks_to_tree(subtasks, parent_node):
    for subtask in subtasks:
        status = f"[{subtask['status']}]".upper()
        sub_node = parent_node.add(f"{subtask['id']} {subtask['title']} {status}")
        add_subtasks_to_tree(subtask.get("subtasks", []), sub_node)
