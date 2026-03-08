Rajput Girl, [3/8/2026 11:52 AM]
# ============================================================
#   TO-DO LIST APPLICATION — Level 2, Task 1 (Intermediate)
#   Features: Add, View, Delete, Mark as Done
#   Storage : JSON file (tasks saved permanently)
# ============================================================

import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# ── Load tasks from file ──
def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# ── Save tasks to file ──
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# ── Add a new task ──
def add_task(tasks):
    title = input("\nEnter task title: ").strip()
    if not title:
        print("Task title cannot be empty!")
        return

    task = {
        "id":         len(tasks) + 1,
        "title":      title,
        "completed":  False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: '{title}'")

# ── View all tasks ──
def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks found! Add some tasks first.")
        return

    print("\n" + "=" * 55)
    print(f"  {'ID':<5} {'STATUS':<12} {'TITLE':<30} {'CREATED'}")
    print("=" * 55)

    pending   = 0
    completed = 0

    for task in tasks:
        status = "✅ Done" if task["completed"] else "⏳ Pending"
        print(f"  {task['id']:<5} {status:<12} {task['title']:<30} {task['created_at'][:10]}")
        if task["completed"]:
            completed += 1
        else:
            pending += 1

    print("=" * 55)
    print(f"  Total: {len(tasks)} | Pending: {pending} | Completed: {completed}")

# ── Mark task as done ──
def mark_done(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_id = int(input("\nEnter task ID to mark as done: ").strip())
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return

    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print(f"Task '{task['title']}' is already completed!")
            else:
                task["completed"] = True
                save_tasks(tasks)
                print(f"✅ Task '{task['title']}' marked as done!")
            return

    print(f"Task with ID {task_id} not found!")

# ── Delete a task ──
def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_id = int(input("\nEnter task ID to delete: ").strip())
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            confirm = input(f"Delete '{task['title']}'? (yes/no): ").strip().lower()
            if confirm in ["yes", "y"]:
                tasks.pop(i)
                # Re-number IDs
                for j, t in enumerate(tasks):
                    t["id"] = j + 1
                save_tasks(tasks)
                print(f"🗑️  Task deleted successfully!")
            else:
                print("Delete cancelled.")
            return

    print(f"Error: Task with ID {task_id} not found!")

# ── Delete all completed tasks ──
def clear_completed(tasks):
    completed = [t for t in tasks if t["completed"]]
    if not completed:
        print("No completed tasks to clear!")
        return

    confirm = input(f"Clear all {len(completed)} completed tasks? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        tasks[:] = [t for t in tasks if not t["completed"]]
        for i, t in enumerate(tasks):
            t["id"] = i + 1
        save_tasks(tasks)
        print(f"✅ Cleared {len(completed)} completed task(s)!")
    else:
        print("Cancelled.")

Rajput Girl, [3/8/2026 11:52 AM]
# ── MAIN ──
def main():
    print("=" * 50)
    print("       TO-DO LIST APPLICATION")
    print("    Level 2 Task 1 — Intermediate")
    print("=" * 50)
    print(f"  Tasks saved to: {TASKS_FILE}")

    tasks = load_tasks()
    print(f"  Loaded {len(tasks)} existing task(s).")

    while True:
        print("\n--- MENU ---")
        print("  1. Add new task")
        print("  2. View all tasks")
        print("  3. Mark task as done")
        print("  4. Delete a task")
        print("  5. Clear completed tasks")
        print("  6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            clear_completed(tasks)
        elif choice == "6":
            print("\nGoodbye! Your tasks are saved! 👋")
            break
        else:
            print("Invalid choice! Enter 1-6.")

if name == "main":
    main()
