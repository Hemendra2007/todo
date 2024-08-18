import json
import os

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

    def add_task(self, task):
        self.tasks.append({'task': task, 'done': False})
        self.save_tasks()

    def view_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        for i, t in enumerate(self.tasks, 1):
            status = "✓" if t['done'] else "✗"
            print(f"{i}. {t['task']} [{status}]")

    def mark_task_done(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]['done'] = True
            self.save_tasks()

    def delete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.last_deleted_task = self.tasks.pop(task_number - 1)
            self.save_tasks()

    def edit_task(self, task_number, new_task):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]['task'] = new_task
            self.save_tasks()

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
                status = "✓" if t['done'] else "✗"
                print(f"{i}. {t['task']} [{status}]")
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

def main():
    app = TodoApp()
    while True:
        choice = input("\n1. Add Task\n2. View Tasks\n3. Mark Task as Done\n4. Delete Task\n5. Edit Task\n6. Clear All Tasks\n7. Search Task\n8. Undo Last Delete\n9. Exit\nChoice: ")
        
        if choice == '1':
            app.add_task(input("Task: "))
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
            app.clear_all_tasks()
        elif choice == '7':
            keyword = input("Search keyword: ")
            app.search_task(keyword)
        elif choice == '8':
            app.undo_last_delete()
        elif choice == '9':
            break

if __name__ == "__main__":
    main()
