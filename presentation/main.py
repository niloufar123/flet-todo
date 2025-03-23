import flet as ft
from application.task_service import TaskService
from infrastructure.task_repository import TaskRepository

def main(page: ft.Page):
    page.title = "TODO App - Flet & Clean Architecture"
    page.window_width = 400
    page.window_height = 600
    repository = TaskRepository()
    service = TaskService(repository)
    
    task_list = ft.Column()
    
    def refresh_task_list():
        task_list.controls.clear()
        for task in service.list_tasks():
            task_input = ft.TextField(value=task.title, expand=True, visible=False)
            
            def enable_edit(e, t=task.id):
                task_input.visible = True
                page.update()
                
            def save_edit(e, t=task.id, input_field=task_input):
                service.update_task(t, input_field.value)
                refresh_task_list()
            
            task_row = ft.Row([
                ft.Checkbox(value=task.completed, on_change=lambda e, t=task.id: toggle_task(t)),
                ft.Text(task.title, expand=True, weight=ft.FontWeight.BOLD if task.completed else ft.FontWeight.NORMAL),
                ft.IconButton(icon=ft.icons.EDIT, on_click=enable_edit),
                task_input,
                ft.IconButton(icon=ft.icons.SAVE, on_click=save_edit),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, t=task.id: delete_task(t)),
            ])
            task_list.controls.append(task_row)
        page.update()
    
    def add_task(e):
        if task_input.value:
            service.create_task(task_input.value)
            task_input.value = ""
            refresh_task_list()
    
    def toggle_task(task_id: int):
        service.toggle_task(task_id)
        refresh_task_list()
    
    def delete_task(task_id: int):
        service.delete_task(task_id)
        refresh_task_list()
    
    top_title = ft.Text("My to-do app with Flet", size=30, color="blue")
    
    content = ft.Row(
        controls=[top_title],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10  
    )
    task_input = ft.TextField(hint_text="Enter task", expand=True,)
    add_button = ft.ElevatedButton("Add", on_click=add_task)
    
    page.add(content,ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.CENTER,spacing=10), task_list)
    
    refresh_task_list()

ft.app(target=main)