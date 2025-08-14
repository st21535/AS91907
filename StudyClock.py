
from tkinter import * 
import time 
import json
from tkinter import ttk
class StudyClock:
    def __init__(self):
        self.root=Tk()
        self.root.title("StudyClock!")
        self.container=Frame(self.root)
        self.root.geometry("600x400")

        self.tasks=self.load_tasks()
        self.int_mins=25 #How many mins in a cycle
        self.tot_int=1
        self.current_seconds=self.int_mins * 60

        Label(self.root,text="Task Selector: ",font="arial 12").pack(pady=10,padx=10)
        self.task_var=StringVar()


        task_names=[task["Project Name"] for task in self.tasks] or ["here are no current tasks"]
        self.task_menu=ttk.Combobox(self.root,textvariable=self.task_var,values=task_names,state="readonly")
        self.task_menu.current(0)
        self.task_menu.pack(pady=5)                                    

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                tasks = json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []
        return tasks
        
    def run(self):
        self.root.mainloop()

app = StudyClock()
app.run()