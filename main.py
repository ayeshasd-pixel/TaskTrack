import json
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            print("Could not read saved tasks.")
    return []


def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=4))


def add_task(tasks):
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
    if due_date:
        try:
            date.fromisoformat(due_date)
        except ValueError:
            print("Invalid date format.")
            return

    priority = input("Priority (low/medium/high): ").strip().lower()
    if priority not in ("low", "medium", "high"):
        print("Choose low, medium, or high.")
        return

    tasks.append({
        "title": title,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    })
    save_tasks(tasks)
    print("Task added successfully!")


def list_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return

    for index, task in enumerate(tasks, start=1):
        status = "Done" if task["completed"] else "Pending"
        due = task["due_date"] or "No deadline"
        print(
            f'{index}. [{status}] {task["title"]} | '
            f'Priority: {task["priority"]} | Due: {due}'
        )


def complete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return

    try:
        number = int(input("Task number to complete: "))
        if not 1 <= number <= len(tasks):
            raise ValueError
    except ValueError:
        print("Enter a valid task number.")
        return

    tasks[number - 1]["completed"] = True
    save_tasks(tasks)
    print("Task marked as completed!")


def delete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return

    try:
        number = int(input("Task number to delete: "))
        if not 1 <= number <= len(tasks):
            raise ValueError
    except ValueError:
        print("Enter a valid task number.")
        return

    removed = tasks.pop(number - 1)
    save_tasks(tasks)
    print(f'Task "{removed["title"]}" deleted.')


def main():
    tasks = load_tasks()

    while True:
        print("\n=== TaskTrack ===")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Thanks for using TaskTrack!")
            break
        else:
            print("Invalid option. Choose 1 to 5.")


if __name__ == "__main__":
    main()
