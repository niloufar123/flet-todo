import flet as ft
import time 

def main(page:ft.Page):
    def addTask(e):
            check=ft.Checkbox(label=taskName.value,label_style=ft.TextStyle(weight=ft.FontWeight.BOLD))
            page.add(check)
            taskName.value=""
            taskName.focus()
            page.update()
  
    taskName=ft.TextField(label="Enter your task")
    addBtn=ft.ElevatedButton(text="add task",on_click=addTask)
    appText=ft.Text("To Do: ",size=30,color="blue")
    page.add(appText,ft.Text(
            style=ft.TextStyle(weight=ft.FontWeight.BOLD)
        ))

    page.add(ft.Row(controls=[taskName,addBtn],alignment="center"))
    pass

ft.app(target=main)