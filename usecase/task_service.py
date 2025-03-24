from repository.task_repository import TaskRepository
from entities.task import Task
from typing import List

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, title: str) -> Task:
        return self.repository.add_task(title)

    def list_tasks(self) -> List[Task]:
        return self.repository.get_tasks()

    def toggle_task(self, task_id: int):
        self.repository.toggle_task(task_id)

    def update_task(self, task_id: int, new_title: str):
        self.repository.update_task(task_id, new_title)

    def delete_task(self, task_id: int):
        self.repository.remove_task(task_id)