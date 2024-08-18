import json
import os
from datetime import datetime, timedelta

class TodoApp:
    def __init__(self):
        self.filename = 'tasks.json'
        self.tasks = self.load_tasks()
        self.last_deleted_task = None

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)
        print("Tasks saved automatically.")

    def add_task(self, task, due_date=None, priority="Medium", reminder_date=None):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tasks.append({
            'task': task,
            'done': False,
            'due_date': due_date,
            'priority': priority,
            'created_at': created_at,
            'reminder_date': reminder_date
        })
        self.save_tasks()

    def view_tasks(self):
        self.check_reminders()
        pending_tasks = [t for t in self.tasks if not t['done']]
        completed_tasks = [t for t in self.tasks if t['done']]

        print("\nPending Tasks:")
        if not pending_tasks:
            print("No pending tasks available.")
        for i, t in enumerate(pending_tasks, 1):
            self.print_task(t, i)

        print("\nCompleted Tasks:")
        if not completed_tasks:
            print("No completed tasks available.")
        for i, t in enumerate(completed_tasks, 1):
            self.print_task(t, i)

    def print_task(self, t, index):
        status = "✓" if t['done'] else "✗"
        due_date = f" (Due: {t['due_date']})" if t['due_date'] else ""
        overdue = self.check_overdue(t['due_date']) if t['due_date'] else False
        overdue_str = " (Overdue)" if overdue else ""
        priority = f" [Priority: {t['priority']}]" if 'priority' in t else ""
        created_at = f" [Created At: {t['created_at']}]"
        reminder_date = f" [Reminder: {t['reminder_date']}]" if t.get('reminder_date') else ""
        print(f"{index}. {t['task']} [{status}]{due_date}{overdue_str}{priority}{created_at}{reminder_date}")

    def set_due_date(self, task_number, new_due_date):
        try:
            if 0 < task_number <= len(self.tasks):
                self.tasks[task_number - 1]['due_date'] = new_due_date
                self.save_tasks()
                print(f"Due date of task {task_number} set to {new_due_date}.")
            else:
                print("Invalid task number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_overdue(self, due_date):
        if due_date:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            return datetime.now() > due_date_obj
        return False

    def set_priority(self, task_number, priority):
        try:
            if 0 < task_number <= len(self.tasks):
                self.tasks[task_number - 1]['priority'] = priority
                self.save_tasks()
                print(f"Priority of task {task_number} set to {priority}.")
            else:
                print("Invalid task number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def mark_task_done(self, task_number):
        try:
            if 0 < task_number <= len(self.tasks):
                self.tasks[task_number - 1]['done'] = True
                self.save_tasks()
                print(f"Task {task_number} marked as done.")
            else:
                print("Invalid task number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_task(self, task_number):
        try:
            if 0 < task_number <= len(self.tasks):
                self.last_deleted_task = self.tasks.pop(task_number - 1)
                self.save_tasks()
                print(f"Task {task_number} deleted.")
            else:
                print("Invalid task number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def edit_task(self, task_number, new_task):
        try:
            if 0 < task_number <= len(self.tasks):
                self.tasks[task_number - 1]['task'] = new_task
                self.save_tasks()
                print(f"Task {task_number} updated.")
            else:
                print("Invalid task number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def clear_all_tasks(self):
        confirm = input("Are you sure you want to clear all tasks? (y/n): ").lower()
        if confirm == 'y':
            self.tasks.clear()
            self.save_tasks()
            print("All tasks have been cleared.")

    def search_task(self, keyword):
        results = [t for t in self.tasks if keyword.lower() in t['task'].lower()]
        if results:
            for i, t in enumerate(results, 1):
                self.print_task(t, i)
        else:
            print("No tasks found.")

    def undo_last_delete(self):
        if self.last_deleted_task:
            self.tasks.append(self.last_deleted_task)
            self.last_deleted_task = None
            self.save_tasks()
            print("Last deleted task has been restored.")
        else:
            print("No task to undo.")

    def sort_tasks(self, by="name"):
        if by == "name":
            self.tasks.sort(key=lambda x: x['task'].lower())
        elif by == "status":
            self.tasks.sort(key=lambda x: x['done'])
        elif by == "priority":
            priority_order = {"High": 1, "Medium": 2, "Low": 3}
            self.tasks.sort(key=lambda x: priority_order.get(x['priority'], 4))
        elif by == "due_date":
            self.tasks.sort(key=lambda x: (x['due_date'] is None, x['due_date']))
        elif by == "created_at":
            self.tasks.sort(key=lambda x: datetime.strptime(x['created_at'], "%Y-%m-%d %H:%M:%S"))
        self.save_tasks()
        print(f"Tasks sorted by {by}.")

    def check_reminders(self):
        for task in self.tasks:
            if task['reminder_date']:
                reminder_date_obj = datetime.strptime(task['reminder_date'], "%Y-%m-%d")
                if datetime.now().date() == reminder_date_obj.date() and not task['done']:
                    print(f"Reminder: Task '{task['task']}' is due for today!")

    def set_reminder(self, task_number, reminder_date):
        try:
            if 0 < task_number <= len(self.tasks):
                self.tasks[task_number - 1]['reminder_date'] = reminder_date
                self.save_tasks()
                print(f"Reminder for task {task_number} set to {reminder_date}.")
            else:
                print("Invalid task number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def help_menu(self):
        print("""
        1. Add Task: Adds a new task with an optional due date, priority, and reminder.
        2. View Tasks: Views pending and completed tasks with status, due dates, priorities, and reminders.
        3. Mark Task as Done: Marks a specific task as done.
        4. Delete Task: Deletes a specific task.
        5. Edit Task: Edits the content of a specific task.
        6. Set Priority: Set a priority level (High, Medium, Low) for a task.
        7. Set Due Date: Update the due date of a task.
        8. Set Reminder: Set a reminder for a task.
        9. Clear All Tasks: Clears all tasks from the list.
        10. Search Task: Searches for tasks by keyword.
        11. Undo Last Delete: Restores the last deleted task.
        12. Sort Tasks: Sort tasks by name, status, priority, due date, or creation date.
        13. Help: Displays this help menu.
        14. Exit: Exits the application.
        """)

def main():
    app = TodoApp()
    while True:
        choice = input("\n1. Add Task\n2. View Tasks\n3. Mark Task as Done\n4. Delete Task\n5. Edit Task\n6. Set Priority\n7. Set Due Date\n8. Set Reminder\n9. Clear All Tasks\n10. Search Task\n11. Undo Last Delete\n12. Sort Tasks\n13. Help\n14. Exit\nChoice: ")
        
        if choice == '1':
            task = input("Task: ")
            due_date = input("Due date (YYYY-MM-DD, optional): ")
            priority = input("Priority (High/Medium/Low, default is Medium): ").capitalize() or "Medium"
            reminder_date = input("Reminder date (YYYY-MM-DD, optional): ")
            app.add_task(task, due_date if due_date else None, priority, reminder_date if reminder_date else None)
        elif choice == '2':
            app.view_tasks()
        elif choice == '3':
            task_num = int(input("Task number to mark as done: "))
            app.mark_task_done(task_num)
        elif choice == '4':
            task_num = int(input("Task number to delete: "))
            app.delete_task(task_num)
        elif choice == '5':
            task_num = int(input("Task number to edit: "))
            new_task = input("New task: ")
            app.edit_task(task_num, new_task)
        elif choice == '6':
            task_num = int(input("Task number to set priority: "))
            priority = input("New priority (High/Medium/Low): ").capitalize()
            app.set_priority(task_num, priority)
        elif choice == '7':
            task_num = int(input("Task number to set due date: "))
            new_due_date = input("New due date (YYYY-MM-DD): ")
            app.set_due_date(task_num, new_due_date)
        elif choice == '8':
            task_num = int(input("Task number to set reminder: "))
            reminder_date = input("Reminder date (YYYY-MM-DD): ")
            app.set_reminder(task_num, reminder_date)
        elif choice == '9':
            app.clear_all_tasks()
        elif choice == '10':
            keyword = input("Search keyword: ")
            app.search_task(keyword)
        elif choice == '11':
            app.undo_last_delete()
        elif choice == '12':
            sort_by = input("Sort by (name/status/priority/due_date/created_at): ").lower()
            app.sort_tasks(by=sort_by)
        elif choice == '13':
            app.help_menu()
        elif choice == '14':
            break

if __name__ == "__main__":
    main()
