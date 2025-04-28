import argparse

"""
author: openpineaplehub
copyright: 2025 all rights reversed
"""


def get_args():
    parser = argparse.ArgumentParser(prog="pinetodo")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Commands
    subparsers.add_parser("readocs", help="Show PineToDo documentation")
    
    # Add task
    parser_add = subparsers.add_parser("add", help="Add new task")
    parser_add.add_argument("-T", "--title", required=True, help="Title of the task")

    # List tasks
    subparsers.add_parser("list", help="Show all tasks")

    # Delete task
    parser_delete = subparsers.add_parser("delete", help="Delete task or subtask by ID")


    # Mark task as done
    parser_done = subparsers.add_parser("done", help="Mark a task as done by ID")
    parser_done.add_argument("task_id", help="ID of the task (use '#' prefix)")

    # Mark task back to todo
    parser_todo = subparsers.add_parser("todo", help="Mark a task back to todo by ID")
    parser_todo.add_argument("task_id", help="ID of the task (use '#' prefix)")

    # Add subtask
    parser_subtask = subparsers.add_parser("subtask", help="Add subtask to a task")
    parser_subtask.add_argument("-loc", required=True, help="Parent task ID (use '#' prefix)")
    parser_subtask.add_argument("-st", required=True, help="Title of the subtask")

    # Edit task
    parser_edit = subparsers.add_parser("edit", help="Edit a task by ID")
    parser_edit.add_argument("task_id", help="ID of the task (use '#' prefix)")
    parser_edit.add_argument("-T", "--title", help="New title for the task")
    parser_edit.add_argument("-s", "--status", choices=["todo", "done"], help="New status for the task")

    # Search tasks
    parser_search = subparsers.add_parser("search", help="Search for tasks by title and status")
    parser_search.add_argument("search_query", help="Keyword to search in task titles")
    parser_search.add_argument("-s", "--status", choices=["todo", "done"], help="Filter by status")

    # Sort tasks
    parser_short = subparsers.add_parser("short", help="Sort and display tasks")
    parser_short.add_argument("-by", choices=["title", "status", "id", "subtask_count"], default="title", help="Sort by field")
    parser_short.add_argument("-r", "--reverse", action="store_true", help="Sort in reverse order")

    # Task statistics
    subparsers.add_parser("stats", help="Show task statistics")

    # Import tasks
    parser_import = subparsers.add_parser("import", help="Import tasks database")
    group = parser_import.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--path", type=str, help="Path to local JSON file")
    group.add_argument("-r", "--raw", type=str, help="Raw GitHub URL to JSON file")

    # Export tasks
    subparsers.add_parser("export", help="Export tasks database")

    # Version
    parser.add_argument("-v", "--version", action="version", version="pinetodo 1.0.1")

    args = parser.parse_args()

    # Handle task ID formatting
    def preprocess_task_id(arg_name):
        value = getattr(args, arg_name, None)
        if value and not value.startswith("#"):
            setattr(args, arg_name, f"#{value}")

    if args.command in ["done", "todo", "edit"]:
        preprocess_task_id("task_id")
    elif args.command == "delete":
        preprocess_task_id("id")
    elif args.command == "subtask":
        preprocess_task_id("loc")

    return args


        #         MIT License

        # Copyright (c) 2025 openpineaplehub

        # Permission is hereby granted, free of charge, to any person obtaining a copy
        # of this software and associated documentation files (the "Software"), to deal
        # in the Software without restriction, including without limitation the rights
        # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        # copies of the Software, and to permit persons to whom the Software is
        # furnished to do so, subject to the following conditions:

        # The above copyright notice and this permission notice shall be included in all
        # copies or substantial portions of the Software.

        # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        # SOFTWARE.