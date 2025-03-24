from entities.task import Task
from typing import List
import json
import os

TASKS_FILE = "tasks.json"

class TaskRepository:
    def __init__(self):
        self.tasks = []
        self.current_id = 1
        self.load_tasks()

    def save_tasks(self):
        with open(TASKS_FILE, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as file:
                try:
                    data = json.load(file)
                    self.tasks = [Task.from_dict(task) for task in data]
                    if self.tasks:
                        self.current_id = max(task.id for task in self.tasks) + 1
                except json.JSONDecodeError:
                    self.tasks = []

    def add_task(self, title: str) -> Task:
        task = Task(self.current_id, title)
        self.tasks.append(task)
        self.current_id += 1
        self.save_tasks()
        return task

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def toggle_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                break
        self.save_tasks()

    def update_task(self, task_id: int, new_title: str):
        for task in self.tasks:
            if task.id == task_id:
                task.title = new_title
                break
        self.save_tasks()

    def remove_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()