import json
from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date, category):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.completed = False
        self.created_at = datetime.now().isoformat()

    def mark_complete(self):
        self.completed = True

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'category': self.category,
            'completed': self.completed,
            'created_at': self.created_at
        }

    @staticmethod
    def from_dict(data):
        task = Task(
            data['title'],
            data['description'],
            data['priority'],
            data['due_date'],
            data['category']
        )
        task.completed = data['completed']
        task.created_at = data['created_at']
        return task
class ToDoList:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
                return [Task.from_dict(task) for task in tasks]
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def update_task(self, old_title, new_task):
        for i, task in enumerate(self.tasks):
            if task.title == old_title:
                self.tasks[i] = new_task
                break
        self.save_tasks()

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def list_tasks(self, filter_by=None, show_completed=True):
        filtered_tasks = self.tasks
        if filter_by:
            if 'category' in filter_by:
                filtered_tasks = [task for task in filtered_tasks if task.category == filter_by['category']]
            if 'due_date' in filter_by:
                filtered_tasks = [task for task in filtered_tasks if task.due_date == filter_by['due_date']]
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task.completed]
        return filtered_tasks
def main():
    todo_list = ToDoList()

    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. View Tasks")
        print("5. Mark Task as Complete")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Title: ")
            description = input("Description: ")
            priority = input("Priority (low, medium, high): ")
            due_date = input("Due Date (YYYY-MM-DD): ")
            category = input("Category: ")
            task = Task(title, description, priority, due_date, category)
            todo_list.add_task(task)
            print("Task added successfully.")
        elif choice == '2':
            title = input("Enter the title of the task to delete: ")
            todo_list.delete_task(title)
            print("Task deleted successfully.")
        elif choice == '3':
            old_title = input("Enter the title of the task to update: ")
            task = todo_list.get_task(old_title)
            if task:
                title = input(f"Title ({task.title}): ") or task.title
                description = input(f"Description ({task.description}): ") or task.description
                priority = input(f"Priority ({task.priority}): ") or task.priority
                due_date = input(f"Due Date ({task.due_date}): ") or task.due_date
                category = input(f"Category ({task.category}): ") or task.category
                new_task = Task(title, description, priority, due_date, category)
                todo_list.update_task(old_title, new_task)
                print("Task updated successfully.")
            else:
                print("Task not found.")
        elif choice == '4':
            filter_by = {}
            show_completed = input("Show completed tasks? (yes/no): ").lower() == 'yes'
            filter_category = input("Filter by category (leave blank for no filter): ")
            if filter_category:
                filter_by['category'] = filter_category
            filter_due_date = input("Filter by due date (YYYY-MM-DD, leave blank for no filter): ")
            if filter_due_date:
                filter_by['due_date'] = filter_due_date
            tasks = todo_list.list_tasks(filter_by, show_completed)
            if tasks:
                for task in tasks:
                    print(f"Title: {task.title}, Description: {task.description}, Priority: {task.priority}, Due Date: {task.due_date}, Category: {task.category}, Completed: {task.completed}")
            else:
                print("No tasks found.")
        elif choice == '5':
            title = input("Enter the title of the task to mark as complete: ")
            task = todo_list.get_task(title)
            if task:
                task.mark_complete()
                todo_list.save_tasks()
                print("Task marked as complete.")
            else:
                print("Task not found.")
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
