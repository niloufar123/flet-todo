import flet as ft
from usecase.task_service import TaskService
from repository.task_repository import TaskRepository

def main(page: ft.Page):
    page.title = "TODO App - Flet & Clean Architecture"
    page.window_width = 400
    page.window_height = 600

    repository = TaskRepository()
    service = TaskService(repository)

    task_list = ft.Column()

    def refresh_task_list():
        """Refresh the task list UI."""
        task_list.controls.clear()
        
        for task in service.list_tasks():
            task_input = ft.TextField(value=task.title, expand=True, visible=False)
            
            def enable_edit(e, t_id=task.id, input_field=task_input):
                """Make input field visible for editing."""
                input_field.visible = True
                page.update()
            
            def save_edit(e, t_id=task.id, input_field=task_input):
                """Save edited task title."""
                if input_field.value.strip():
                    service.update_task(t_id, input_field.value)
                refresh_task_list()

            task_row = ft.Row(
                [
                    ft.Checkbox(
                        value=task.completed,
                        on_change=lambda e, t_id=task.id: toggle_task(t_id)
                    ),
                    ft.Text(
                        task.title, 
                        expand=True, 
                        weight=ft.FontWeight.BOLD if task.completed else ft.FontWeight.NORMAL,
                        visible=True
                    ),
                    task_input, 
                    ft.IconButton(ft.icons.EDIT, on_click=enable_edit),
                    ft.IconButton(ft.icons.SAVE, on_click=save_edit),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, t_id=task.id: delete_task(t_id)),
                ]
            )
            task_list.controls.append(task_row)
        
        page.update()

    def add_task(e):
        """Add a new task."""
        if task_input.value.strip():
            service.create_task(task_input.value.strip())
            task_input.value = ""
            task_input.update()
            refresh_task_list()

    def toggle_task(task_id: int):
        """Mark task as completed/uncompleted."""
        service.toggle_task(task_id)
        refresh_task_list()

    def delete_task(task_id: int):
        """Delete a task."""
        service.delete_task(task_id)
        refresh_task_list()

    top_title = ft.Text("My To-Do App", size=24, color="blue", weight=ft.FontWeight.BOLD)

    task_input = ft.TextField(hint_text="Enter task", expand=True)
    add_button = ft.ElevatedButton("Add", on_click=add_task)

    page.add(
        ft.Row([top_title], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.CENTER),
        task_list
    )

    refresh_task_list()

ft.app(target=main)
