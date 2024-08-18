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
        self.tasks.append({'task': task})
        self.save_tasks()

    def view_tasks(self):
        for i, t in enumerate(self.tasks, 1):
            print(f"{i}. {t['task']}")

def main():
    app = TodoApp()
    while True:
        choice = input("\n1. Add Task\n2. View Tasks\n3. Exit\nChoice: ")
        if choice == '1':
            app.add_task(input("Task: "))
        elif choice == '2':
            app.view_tasks()
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
