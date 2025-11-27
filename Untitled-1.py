import json
import argparse
from pathlib import Path
from datetime import datetime

#!/usr/bin/env python3
"""
Simple CLI todo manager.
Save this file as Untitled-1.py and run: python Untitled-1.py add "Buy milk"
Commands:
    add "task text"
    list
    done INDEX
    remove INDEX
    clear
"""


DATA_FILE = Path(__file__).with_suffix('.todos.json')


def load_tasks():
        if not DATA_FILE.exists():
                return []
        try:
                return json.loads(DATA_FILE.read_text(encoding='utf-8'))
        except Exception:
                return []


def save_tasks(tasks):
        DATA_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding='utf-8')


def add_task(text):
        tasks = load_tasks()
        tasks.append({"text": text, "created": datetime.utcnow().isoformat(), "done": False})
        save_tasks(tasks)
        print(f'Added: "{text}"')


def list_tasks(show_all=False):
        tasks = load_tasks()
        if not tasks:
                print("No tasks.")
                return
        for i, t in enumerate(tasks, start=1):
                status = "✔" if t.get("done") else " "
                timestamp = t.get("created", "")[:19].replace("T", " ")
                print(f"{i:3}. [{status}] {t.get('text')} (created: {timestamp})")


def set_done(index, remove=False):
        tasks = load_tasks()
        if index < 1 or index > len(tasks):
                print("Invalid index.")
                return
        if remove:
                removed = tasks.pop(index - 1)
                save_tasks(tasks)
                print(f"Removed: {removed.get('text')}")
        else:
                tasks[index - 1]['done'] = True
                save_tasks(tasks)
                print(f"Marked done: {tasks[index - 1].get('text')}")


def clear_tasks():
        save_tasks([])
        print("All tasks cleared.")


def main():
        parser = argparse.ArgumentParser(prog="todo", description="Tiny todo CLI")
        sub = parser.add_subparsers(dest="cmd", required=True)

        p_add = sub.add_parser("add", help="Add a task")
        p_add.add_argument("text", nargs="+", help="Task text")

        p_list = sub.add_parser("list", help="List tasks")

        p_done = sub.add_parser("done", help="Mark task done by index")
        p_done.add_argument("index", type=int)

        p_remove = sub.add_parser("remove", help="Remove task by index")
        p_remove.add_argument("index", type=int)

        p_clear = sub.add_parser("clear", help="Clear all tasks")

        args = parser.parse_args()

        if args.cmd == "add":
                add_task(" ".join(args.text))
        elif args.cmd == "list":
                list_tasks()
        elif args.cmd == "done":
                set_done(args.index, remove=False)
        elif args.cmd == "remove":
                set_done(args.index, remove=True)
        elif args.cmd == "clear":
                clear_tasks()


if __name__ == "__main__":
        main()