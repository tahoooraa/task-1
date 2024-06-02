import json
from datetime import datetime

class Task:
    def __init__(self, title, priority="medium", due_date=None):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = False

    def mark_as_completed(self):
        self.completed = True

    def __str__(self):
        due_date_str = self.due_date.strftime('%Y-%m-%d') if self.due_date else "No due date"
        status = "Completed" if self.completed else "Pending"
        return f"{self.title} [{self.priority}] - {due_date_str} - {status}"

class TodoList:
    def __init__(self, storage_file='tasks.json'):
        self.tasks = []
        self.storage_file = storage_file
        self.load_tasks()

    def add_task(self, title, priority="medium", due_date=None):
        task = Task(title, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_as_completed()
            self.save_tasks()

    def save_tasks(self):
        with open(self.storage_file, 'w') as file:
            # Save tasks with dates formatted as 'YYYY-MM-DD'
            json.dump([{
                'title': task.title,
                'priority': task.priority,
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
                'completed': task.completed
            } for task in self.tasks], file, default=str)

    def load_tasks(self):
        try:
            with open(self.storage_file, 'r') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    # Strip time information from the due date if present
                    if task_data['due_date']:
                        due_date_str = task_data['due_date'].split()[0]
                        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                    else:
                        due_date = None
                    task = Task(task_data['title'], task_data['priority'], due_date)
                    task.completed = task_data['completed']
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def list_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i}. {task}")

def main():
    todo_list = TodoList()

    while True:
        print("\nTodo List Application")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Mark Task as Completed")
        print("4. List Tasks")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            title = input("Enter task title: ")
            priority = input("Enter task priority (high, medium, low): ")
            due_date_input = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            due_date = datetime.strptime(due_date_input, '%Y-%m-%d') if due_date_input else None
            todo_list.add_task(title, priority, due_date)
        elif choice == "2":
            index = int(input("Enter task index to remove: "))
            todo_list.remove_task(index)
        elif choice == "3":
            index = int(input("Enter task index to mark as completed: "))
            todo_list.mark_task_completed(index)
        elif choice == "4":
            todo_list.list_tasks()
        elif choice == "5":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
