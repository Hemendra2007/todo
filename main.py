import json
import os

class TodoApp:
    def __init__(self):
        self.filename = 'tasks.json'
        self.tasks = self.load_tasks()

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
        for i, t in enumerate(self.tasks, 1):
            status = "✓" if t['done'] else "✗"
            print(f"{i}. {t['task']} [{status}]")

    def mark_task_done(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]['done'] = True
            self.save_tasks()

    def delete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            del self.tasks[task_number - 1]
            self.save_tasks()

def main():
    app = TodoApp()
    while True:
        choice = input("\n1. Add Task\n2. View Tasks\n3. Mark Task as Done\n4. Delete Task\n5. Exit\nChoice: ")
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
            break

if __name__ == "__main__":
    main()
