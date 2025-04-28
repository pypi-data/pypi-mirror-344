"""
author: openpineaplehub
copyright: 2025 all rights reversed
"""

from .parse import get_args
from .core.cli.add_task import add_task
from .core.cli.list_task import list_tasks
from .core.cli.delete_by_id import delete_by_id
from .core.cli.mark_done import mark_done
from .core.cli.mark_todo import mark_todo
from .core.cli.add_subtask import add_subtask
from .core.cli.edit_by_id import edit_by_id
from .core.cli.search_task import search_task
from .core.cli.statistics import show_statistics
from .core.cli.sort_tasks import short_task
from .core.cli.imports_tasks import import_data
from .core.cli.export import export_database

def handle_command():
    args = get_args()
    
    command_map = {
        "add": lambda: add_task(args.title),
        "list": lambda: list_tasks(),
        "delete": lambda: delete_by_id(args.id),
        "done": lambda: mark_done(args.task_id),
        "todo": lambda: mark_todo(args.task_id),
        "subtask": lambda: add_subtask(args.loc, args.st),
        "edit": lambda: edit_by_id(args.task_id, args.title, args.status),
        "search": lambda: search_task(args.search_query, args.status),
        "stats": lambda: show_statistics(),
        "import": lambda: import_data(path=args.path, raw_url=args.raw),
        "export": lambda: export_database(),
        "short": lambda: short_task(args.by, args.reverse),
    }

    command_action = command_map.get(args.command)
    
    if command_action:
        command_action()
    else:
        print("Use -h or --help to see help.")
